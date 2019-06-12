#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2018, Kevin Breit (@kbreit) <kevin.breit@kevinbreit.net>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = r'''
---
module: jctanner.network_meraki.meraki_mr_l3_firewall
short_description: Manage MR access point layer 3 firewalls in the Meraki cloud
version_added: "2.7"
description:
- Allows for creation, management, and visibility into layer 3 firewalls implemented on Meraki MR access points.
- Module is not idempotent as of current release.
options:
    state:
        description:
        - Create or modify an organization.
        type: str
        choices: [ present, query ]
        default: present
    org_name:
        description:
        - Name of organization.
        type: str
    org_id:
        description:
        - ID of organization.
        type: int
    net_name:
        description:
        - Name of network containing access points.
        type: str
    net_id:
        description:
        - ID of network containing access points.
        type: str
    number:
        description:
        - Number of SSID to apply firewall rule to.
        type: int
        aliases: [ ssid_number ]
    ssid_name:
        description:
        - Name of SSID to apply firewall rule to.
        type: str
        aliases: [ ssid ]
    allow_lan_access:
        description:
        - Sets whether devices can talk to other devices on the same LAN.
        type: bool
        default: yes
    rules:
        description:
        - List of firewall rules.
        type: list
        suboptions:
            policy:
                description:
                - Specifies the action that should be taken when rule is hit.
                type: str
                choices: [ allow, deny ]
            protocol:
                description:
                - Specifies protocol to match against.
                type: str
                choices: [ any, icmp, tcp, udp ]
            dest_port:
                description:
                - Comma-seperated list of destination ports to match.
                type: str
            dest_cidr:
                description:
                - Comma-separated list of CIDR notation networks to match.
                type: str
            comment:
                description:
                - Optional comment describing the firewall rule.
                type: str
author:
- Kevin Breit (@kbreit)
extends_documentation_fragment: jctanner.network_meraki.meraki
'''

EXAMPLES = r'''
- name: Create single firewall rule
  jctanner.network_meraki.meraki_mr_l3_firewall:
    auth_key: abc123
    state: present
    org_name: YourOrg
    net_id: 12345
    number: 1
    rules:
      - comment: Integration test rule
        policy: allow
        protocol: tcp
        dest_port: 80
        dest_cidr: 192.0.2.0/24
    allow_lan_access: no
  delegate_to: localhost

- name: Enable local LAN access
  jctanner.network_meraki.meraki_mr_l3_firewall:
    auth_key: abc123
    state: present
    org_name: YourOrg
    net_id: 123
    number: 1
    rules:
    allow_lan_access: yes
  delegate_to: localhost

- name: Query firewall rules
  jctanner.network_meraki.meraki_mr_l3_firewall:
    auth_key: abc123
    state: query
    org_name: YourOrg
    net_name: YourNet
    number: 1
  delegate_to: localhost
'''

RETURN = r'''

'''

import os
from ansible.module_utils.basic import AnsibleModule, json, env_fallback
from ansible.module_utils.urls import fetch_url
from ansible.module_utils._text import to_native
from ansible_collections.jctanner.network_jctanner.network_meraki.meraki.plugins.module_utils.network.jctanner.network_meraki.meraki.jctanner.network_meraki.meraki import MerakiModule, jctanner.network_meraki.meraki_argument_spec


def assemble_payload(jctanner.network_meraki.meraki):
    params_map = {'policy': 'policy',
                  'protocol': 'protocol',
                  'dest_port': 'destPort',
                  'dest_cidr': 'destCidr',
                  'comment': 'comment',
                  }
    rules = []
    for rule in jctanner.network_meraki.meraki.params['rules']:
        proposed_rule = dict()
        for k, v in rule.items():
            proposed_rule[params_map[k]] = v
        rules.append(proposed_rule)
    payload = {'rules': rules}
    return payload


def get_rules(jctanner.network_meraki.meraki, net_id, number):
    path = jctanner.network_meraki.meraki.construct_path('get_all', net_id=net_id, custom={'number': number})
    response = jctanner.network_meraki.meraki.request(path, method='GET')
    if jctanner.network_meraki.meraki.status == 200:
        return response


def get_ssid_number(name, data):
    for ssid in data:
        if name == ssid['name']:
            return ssid['number']
    return False


def get_ssids(jctanner.network_meraki.meraki, net_id):
    path = jctanner.network_meraki.meraki.construct_path('get_all', net_id=net_id)
    return jctanner.network_meraki.meraki.request(path, method='GET')


def main():
    # define the available arguments/parameters that a user can pass to
    # the module

    fw_rules = dict(policy=dict(type='str', choices=['allow', 'deny']),
                    protocol=dict(type='str', choices=['tcp', 'udp', 'icmp', 'any']),
                    dest_port=dict(type='str'),
                    dest_cidr=dict(type='str'),
                    comment=dict(type='str'),
                    )

    argument_spec = jctanner.network_meraki.meraki_argument_spec()
    argument_spec.update(state=dict(type='str', choices=['present', 'query'], default='present'),
                         net_name=dict(type='str'),
                         net_id=dict(type='str'),
                         number=dict(type='str', aliases=['ssid_number']),
                         ssid_name=dict(type='str', aliases=['ssid']),
                         rules=dict(type='list', default=None, elements='dict', options=fw_rules),
                         allow_lan_access=dict(type='bool', default=True),
                         )

    # seed the result dict in the object
    # we primarily care about changed and state
    # change is if this module effectively modified the target
    # state will include any data that you want your module to pass back
    # for consumption, for example, in a subsequent task
    result = dict(
        changed=False,
    )
    # the AnsibleModule object will be our abstraction working with Ansible
    # this includes instantiation, a couple of common attr would be the
    # args/params passed to the execution, as well as if the module
    # supports check mode
    module = AnsibleModule(argument_spec=argument_spec,
                           supports_check_mode=True,
                           )
    jctanner.network_meraki.meraki = MerakiModule(module, function='mr_l3_firewall')

    jctanner.network_meraki.meraki.params['follow_redirects'] = 'all'

    query_urls = {'mr_l3_firewall': '/networks/{net_id}/ssids/{number}/l3FirewallRules'}
    update_urls = {'mr_l3_firewall': '/networks/{net_id}/ssids/{number}/l3FirewallRules'}

    jctanner.network_meraki.meraki.url_catalog['get_all'].update(query_urls)
    jctanner.network_meraki.meraki.url_catalog['update'] = update_urls

    payload = None

    # if the user is working with this module in only check mode we do not
    # want to make any changes to the environment, just return the current
    # state with no modifications
    # FIXME: Work with Meraki so they can implement a check mode
    if module.check_mode:
        jctanner.network_meraki.meraki.exit_json(**jctanner.network_meraki.meraki.result)

    # execute checks for argument completeness

    # manipulate or modify the state as needed (this is going to be the
    # part where your module will do what it needs to do)
    org_id = jctanner.network_meraki.meraki.params['org_id']
    orgs = None
    if org_id is None:
        orgs = jctanner.network_meraki.meraki.get_orgs()
        for org in orgs:
            if org['name'] == jctanner.network_meraki.meraki.params['org_name']:
                org_id = org['id']
    net_id = jctanner.network_meraki.meraki.params['net_id']
    if net_id is None:
        if orgs is None:
            orgs = jctanner.network_meraki.meraki.get_orgs()
        net_id = jctanner.network_meraki.meraki.get_net_id(net_name=jctanner.network_meraki.meraki.params['net_name'],
                                   data=jctanner.network_meraki.meraki.get_nets(org_id=org_id))
    number = jctanner.network_meraki.meraki.params['number']
    if jctanner.network_meraki.meraki.params['ssid_name']:
        number = get_ssid_number(jctanner.network_meraki.meraki.params['ssid_name'], get_ssids(jctanner.network_meraki.meraki, net_id))

    if jctanner.network_meraki.meraki.params['state'] == 'query':
        jctanner.network_meraki.meraki.result['data'] = get_rules(jctanner.network_meraki.meraki, net_id, number)
    elif jctanner.network_meraki.meraki.params['state'] == 'present':
        rules = get_rules(jctanner.network_meraki.meraki, net_id, number)
        path = jctanner.network_meraki.meraki.construct_path('get_all', net_id=net_id, custom={'number': number})
        if jctanner.network_meraki.meraki.params['rules']:
            payload = assemble_payload(jctanner.network_meraki.meraki)
        else:
            payload = dict()
        update = False
        try:
            if len(rules) != len(payload['rules']):  # Quick and simple check to avoid more processing
                update = True
            if update is False:
                for r in range(len(rules) - 2):
                    if jctanner.network_meraki.meraki.is_update_required(rules[r], payload[r]) is True:
                        update = True
        except KeyError:
            pass
        if rules[len(rules) - 2] != jctanner.network_meraki.meraki.params['allow_lan_access']:
            update = True
        if update is True:
            payload['allowLanAccess'] = jctanner.network_meraki.meraki.params['allow_lan_access']
            response = jctanner.network_meraki.meraki.request(path, method='PUT', payload=json.dumps(payload))
            if jctanner.network_meraki.meraki.status == 200:
                jctanner.network_meraki.meraki.result['data'] = response
                jctanner.network_meraki.meraki.result['changed'] = True
        else:
            jctanner.network_meraki.meraki.result['data'] = rules

    # in the event of a successful module execution, you will want to
    # simple AnsibleModule.exit_json(), passing the key/value results
    jctanner.network_meraki.meraki.exit_json(**jctanner.network_meraki.meraki.result)


if __name__ == '__main__':
    main()
