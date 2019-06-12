#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2018, 2019 Kevin Breit (@kbreit) <kevin.breit@kevinbreit.net>
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
module: jctanner.network_meraki.meraki_network
short_description: Manage networks in the Meraki cloud
version_added: "2.6"
description:
- Allows for creation, management, and visibility into networks within Meraki.

options:
    auth_key:
        description:
        - Authentication key provided by the dashboard. Required if environmental variable MERAKI_KEY is not set.
    state:
        description:
        - Create or modify an organization.
        choices: [ absent, present, query ]
        default: present
    net_name:
        description:
        - Name of a network.
        aliases: [ name, network ]
    net_id:
        description:
        - ID number of a network.
    org_name:
        description:
        - Name of organization associated to a network.
    org_id:
        description:
        - ID of organization associated to a network.
    type:
        description:
        - Type of network device network manages.
        - Required when creating a network.
        - As of Ansible 2.8, C(combined) type is no longer accepted.
        - As of Ansible 2.8, changes to this parameter are no longer idempotent.
        choices: [ appliance, switch, wireless ]
        aliases: [ net_type ]
        type: list
    tags:
        type: list
        description:
        - List of tags to assign to network.
        - C(tags) name conflicts with the tags parameter in Ansible. Indentation problems may cause unexpected behaviors.
        - Ansible 2.8 converts this to a list from a comma separated list.
    timezone:
        description:
        - Timezone associated to network.
        - See U(https://en.wikipedia.org/wiki/List_of_tz_database_time_zones) for a list of valid timezones.
    enable_vlans:
        description:
        - Boolean value specifying whether VLANs should be supported on a network.
        - Requires C(net_name) or C(net_id) to be specified.
        type: bool
        version_added: '2.9'
    disable_my_jctanner.network_meraki.meraki:
        description: >
            - Disables the local device status pages (U[my.jctanner.network_meraki.meraki.com](my.jctanner.network_meraki.meraki.com), U[ap.jctanner.network_meraki.meraki.com](ap.jctanner.network_meraki.meraki.com), U[switch.jctanner.network_meraki.meraki.com](switch.jctanner.network_meraki.meraki.com),
            U[wired.jctanner.network_meraki.meraki.com](wired.jctanner.network_meraki.meraki.com)).
            - Mutually exclusive of C(enable_my_jctanner.network_meraki.meraki).
            - Will be deprecated in Ansible 2.13 in favor of C(enable_my_jctanner.network_meraki.meraki).
        type: bool
        version_added: '2.7'
    enable_my_jctanner.network_meraki.meraki:
        description: >
            - Enables the local device status pages (U[my.jctanner.network_meraki.meraki.com](my.jctanner.network_meraki.meraki.com), U[ap.jctanner.network_meraki.meraki.com](ap.jctanner.network_meraki.meraki.com), U[switch.jctanner.network_meraki.meraki.com](switch.jctanner.network_meraki.meraki.com),
            U[wired.jctanner.network_meraki.meraki.com](wired.jctanner.network_meraki.meraki.com)).
            - Ansible 2.7 had this parameter as C(disable_my_jctanner.network_meraki.meraki).
        type: bool
        version_added: '2.9'
    enable_remote_status_page:
        description:
            - Enables access to the device status page (U(http://device LAN IP)).
            - Can only be set if C(enable_my_jctanner.network_meraki.meraki:) is set to C(yes).
        type: bool
        version_added: '2.9'

author:
    - Kevin Breit (@kbreit)
extends_documentation_fragment: jctanner.network_meraki.meraki
'''

EXAMPLES = r'''
- delegate_to: localhost
  block:
    - name: List all networks associated to the YourOrg organization
      jctanner.network_meraki.meraki_network:
        auth_key: abc12345
        state: query
        org_name: YourOrg
    - name: Query network named MyNet in the YourOrg organization
      jctanner.network_meraki.meraki_network:
        auth_key: abc12345
        state: query
        org_name: YourOrg
        net_name: MyNet
    - name: Create network named MyNet in the YourOrg organization
      jctanner.network_meraki.meraki_network:
        auth_key: abc12345
        state: present
        org_name: YourOrg
        net_name: MyNet
        type: switch
        timezone: America/Chicago
        tags: production, chicago
    - name: Create combined network named MyNet in the YourOrg organization
      jctanner.network_meraki.meraki_network:
        auth_key: abc12345
        state: present
        org_name: YourOrg
        net_name: MyNet
        type:
          - switch
          - appliance
        timezone: America/Chicago
        tags: production, chicago
    - name: Enable VLANs on a network
      jctanner.network_meraki.meraki_network:
        auth_key: abc12345
        state: query
        org_name: YourOrg
        net_name: MyNet
        enable_vlans: yes
'''

RETURN = r'''
data:
    description: Information about the created or manipulated object.
    returned: info
    type: complex
    contains:
      id:
        description: Identification string of network.
        returned: success
        type: str
        sample: N_12345
      name:
        description: Written name of network.
        returned: success
        type: str
        sample: YourNet
      organizationId:
        description: Organization ID which owns the network.
        returned: success
        type: str
        sample: 0987654321
      tags:
        description: Space delimited tags assigned to network.
        returned: success
        type: str
        sample: " production wireless "
      timeZone:
        description: Timezone where network resides.
        returned: success
        type: str
        sample: America/Chicago
      type:
        description: Functional type of network.
        returned: success
        type: str
        sample: switch
      disableMyMerakiCom:
        description: States whether U(my.jctanner.network_meraki.meraki.com) and other device portals should be disabled.
        returned: success
        type: bool
        sample: true
      disableRemoteStatusPage:
        description: Disables access to the device status page.
        returned: success
        type: bool
        sample: true
'''

import os
from ansible.module_utils.basic import AnsibleModule, json, env_fallback
from ansible.module_utils.urls import fetch_url
from ansible.module_utils._text import to_native
from ansible_collections.jctanner.network_jctanner.network_meraki.meraki.plugins.module_utils.network.jctanner.network_meraki.meraki.jctanner.network_meraki.meraki import MerakiModule, jctanner.network_meraki.meraki_argument_spec


def is_net_valid(data, net_name=None, net_id=None):
    if net_name is None and net_id is None:
        return False
    for n in data:
        if net_name:
            if n['name'] == net_name:
                return True
        elif net_id:
            if n['id'] == net_id:
                return True
    return False


def construct_tags(tags):
    formatted_tags = ' '.join(tags)
    return ' {0} '.format(formatted_tags)  # Meraki needs space padding


def list_to_string(data):
    new_string = str()
    for i, item in enumerate(data):
        if i == len(new_string) - 1:
            new_string += i
        else:
            new_string = "{0}{1} ".format(new_string, item)
    return new_string.strip()


def main():

    # define the available arguments/parameters that a user can pass to
    # the module

    argument_spec = jctanner.network_meraki.meraki_argument_spec()
    argument_spec.update(
        net_id=dict(type='str'),
        type=dict(type='list', choices=['wireless', 'switch', 'appliance'], aliases=['net_type']),
        tags=dict(type='list'),
        timezone=dict(type='str'),
        net_name=dict(type='str', aliases=['name', 'network']),
        state=dict(type='str', choices=['present', 'query', 'absent'], default='present'),
        enable_vlans=dict(type='bool'),
        disable_my_jctanner.network_meraki.meraki=dict(type='bool', removed_in_version=2.13),
        enable_my_jctanner.network_meraki.meraki=dict(type='bool'),
        enable_remote_status_page=dict(type='bool'),
    )

    # the AnsibleModule object will be our abstraction working with Ansible
    # this includes instantiation, a couple of common attr would be the
    # args/params passed to the execution, as well as if the module
    # supports check mode
    module = AnsibleModule(argument_spec=argument_spec,
                           supports_check_mode=False,
                           mutually_exclusive=[('disable_my_jctanner.network_meraki.meraki', 'enable_my_jctanner.network_meraki.meraki'),
                                               ]
                           )

    jctanner.network_meraki.meraki = MerakiModule(module, function='network')
    module.params['follow_redirects'] = 'all'
    payload = None

    create_urls = {'network': '/organizations/{org_id}/networks'}
    update_urls = {'network': '/networks/{net_id}'}
    delete_urls = {'network': '/networks/{net_id}'}
    enable_vlans_urls = {'network': '/networks/{net_id}/vlansEnabledState'}
    get_vlan_status_urls = {'network': '/networks/{net_id}/vlansEnabledState'}
    jctanner.network_meraki.meraki.url_catalog['create'] = create_urls
    jctanner.network_meraki.meraki.url_catalog['update'] = update_urls
    jctanner.network_meraki.meraki.url_catalog['delete'] = delete_urls
    jctanner.network_meraki.meraki.url_catalog['enable_vlans'] = enable_vlans_urls
    jctanner.network_meraki.meraki.url_catalog['status_vlans'] = get_vlan_status_urls

    if not jctanner.network_meraki.meraki.params['org_name'] and not jctanner.network_meraki.meraki.params['org_id']:
        jctanner.network_meraki.meraki.fail_json(msg='org_name or org_id parameters are required')
    if jctanner.network_meraki.meraki.params['state'] != 'query':
        if not jctanner.network_meraki.meraki.params['net_name'] and not jctanner.network_meraki.meraki.params['net_id']:
            jctanner.network_meraki.meraki.fail_json(msg='net_name or net_id is required for present or absent states')
    if jctanner.network_meraki.meraki.params['net_name'] and jctanner.network_meraki.meraki.params['net_id']:
        jctanner.network_meraki.meraki.fail_json(msg='net_name and net_id are mutually exclusive')
    if not jctanner.network_meraki.meraki.params['net_name'] and not jctanner.network_meraki.meraki.params['net_id']:
        if jctanner.network_meraki.meraki.params['enable_vlans']:
            jctanner.network_meraki.meraki.fail_json(msg="The parameter 'enable_vlans' requires 'net_name' or 'net_id' to be specified")
    if jctanner.network_meraki.meraki.params['enable_my_jctanner.network_meraki.meraki'] is True and jctanner.network_meraki.meraki.params['enable_remote_status_page'] is False:
        jctanner.network_meraki.meraki.fail_json(msg='enable_my_jctanner.network_meraki.meraki must be true when setting enable_remote_status_page')

    # if the user is working with this module in only check mode we do not
    # want to make any changes to the environment, just return the current
    # state with no modifications
    if module.check_mode:
        return jctanner.network_meraki.meraki.result

    # Construct payload
    if jctanner.network_meraki.meraki.params['state'] == 'present':
        payload = dict()
        if jctanner.network_meraki.meraki.params['net_name']:
            payload['name'] = jctanner.network_meraki.meraki.params['net_name']
        if jctanner.network_meraki.meraki.params['type']:
            payload['type'] = list_to_string(jctanner.network_meraki.meraki.params['type'])
        if jctanner.network_meraki.meraki.params['tags']:
            payload['tags'] = construct_tags(jctanner.network_meraki.meraki.params['tags'])
        if jctanner.network_meraki.meraki.params['timezone']:
            payload['timeZone'] = jctanner.network_meraki.meraki.params['timezone']
        if jctanner.network_meraki.meraki.params['enable_my_jctanner.network_meraki.meraki'] is not None:
            if jctanner.network_meraki.meraki.params['enable_my_jctanner.network_meraki.meraki'] is True:
                payload['disableMyMerakiCom'] = False
            else:
                payload['disableMyMerakiCom'] = True
        elif jctanner.network_meraki.meraki.params['disable_my_jctanner.network_meraki.meraki'] is not None:
            payload['disableMyMerakiCom'] = jctanner.network_meraki.meraki.params['disable_my_jctanner.network_meraki.meraki']
        if jctanner.network_meraki.meraki.params['enable_remote_status_page'] is not None:
            if jctanner.network_meraki.meraki.params['enable_remote_status_page'] is True:
                payload['disableRemoteStatusPage'] = False
                # jctanner.network_meraki.meraki.fail_json(msg="Debug", payload=payload)
            else:
                payload['disableRemoteStatusPage'] = True

    # manipulate or modify the state as needed (this is going to be the
    # part where your module will do what it needs to do)

    org_id = jctanner.network_meraki.meraki.params['org_id']
    if not org_id:
        org_id = jctanner.network_meraki.meraki.get_org_id(jctanner.network_meraki.meraki.params['org_name'])
    nets = jctanner.network_meraki.meraki.get_nets(org_id=org_id)

    # check if network is created
    net_id = jctanner.network_meraki.meraki.params['net_id']
    net_exists = False
    if net_id is not None:
        if is_net_valid(nets, net_id=net_id) is False:
            jctanner.network_meraki.meraki.fail_json(msg="Network specified by net_id does not exist.")
        net_exists = True
    elif jctanner.network_meraki.meraki.params['net_name']:
        if is_net_valid(nets, net_name=jctanner.network_meraki.meraki.params['net_name']) is True:
            net_id = jctanner.network_meraki.meraki.get_net_id(net_name=jctanner.network_meraki.meraki.params['net_name'], data=nets)
            net_exists = True

    if jctanner.network_meraki.meraki.params['state'] == 'query':
        if not jctanner.network_meraki.meraki.params['net_name'] and not jctanner.network_meraki.meraki.params['net_id']:
            jctanner.network_meraki.meraki.result['data'] = nets
        elif jctanner.network_meraki.meraki.params['net_name'] or jctanner.network_meraki.meraki.params['net_id'] is not None:
            jctanner.network_meraki.meraki.result['data'] = jctanner.network_meraki.meraki.get_net(jctanner.network_meraki.meraki.params['org_name'],
                                                   jctanner.network_meraki.meraki.params['net_name'],
                                                   data=nets
                                                   )
    elif jctanner.network_meraki.meraki.params['state'] == 'present':
        if net_exists is False:  # Network needs to be created
            if 'type' not in jctanner.network_meraki.meraki.params or jctanner.network_meraki.meraki.params['type'] is None:
                jctanner.network_meraki.meraki.fail_json(msg="type parameter is required when creating a network.")
            path = jctanner.network_meraki.meraki.construct_path('create',
                                         org_id=org_id
                                         )
            r = jctanner.network_meraki.meraki.request(path,
                               method='POST',
                               payload=json.dumps(payload)
                               )
            if jctanner.network_meraki.meraki.status == 201:
                jctanner.network_meraki.meraki.result['data'] = r
                jctanner.network_meraki.meraki.result['changed'] = True
        else:  # Network exists, make changes
            # jctanner.network_meraki.meraki.fail_json(msg="nets", nets=nets, net_id=net_id)
            # jctanner.network_meraki.meraki.fail_json(msg="compare", original=net, payload=payload)
            if jctanner.network_meraki.meraki.params['enable_vlans'] is not None:  # Modify VLANs configuration
                status_path = jctanner.network_meraki.meraki.construct_path('status_vlans', net_id=net_id)
                status = jctanner.network_meraki.meraki.request(status_path, method='GET')
                payload = {'enabled': jctanner.network_meraki.meraki.params['enable_vlans']}
                # jctanner.network_meraki.meraki.fail_json(msg="here", payload=payload)
                if jctanner.network_meraki.meraki.is_update_required(status, payload):
                    path = jctanner.network_meraki.meraki.construct_path('enable_vlans', net_id=net_id)
                    r = jctanner.network_meraki.meraki.request(path,
                                       method='PUT',
                                       payload=json.dumps(payload))
                    if jctanner.network_meraki.meraki.status == 200:
                        jctanner.network_meraki.meraki.result['data'] = r
                        jctanner.network_meraki.meraki.result['changed'] = True
                        jctanner.network_meraki.meraki.exit_json(**jctanner.network_meraki.meraki.result)
                else:
                    jctanner.network_meraki.meraki.result['data'] = status
                    jctanner.network_meraki.meraki.exit_json(**jctanner.network_meraki.meraki.result)
            net = jctanner.network_meraki.meraki.get_net(jctanner.network_meraki.meraki.params['org_name'], net_id=net_id, data=nets)
            if jctanner.network_meraki.meraki.is_update_required(net, payload):
                path = jctanner.network_meraki.meraki.construct_path('update', net_id=net_id)
                # jctanner.network_meraki.meraki.fail_json(msg="Payload", path=path, payload=payload)
                r = jctanner.network_meraki.meraki.request(path,
                                   method='PUT',
                                   payload=json.dumps(payload))
                if jctanner.network_meraki.meraki.status == 200:
                    jctanner.network_meraki.meraki.result['data'] = r
                    jctanner.network_meraki.meraki.result['changed'] = True
            else:
                jctanner.network_meraki.meraki.result['data'] = net
    elif jctanner.network_meraki.meraki.params['state'] == 'absent':
        if is_net_valid(nets, net_id=net_id) is True:
            path = jctanner.network_meraki.meraki.construct_path('delete', net_id=net_id)
            r = jctanner.network_meraki.meraki.request(path, method='DELETE')
            if jctanner.network_meraki.meraki.status == 204:
                jctanner.network_meraki.meraki.result['changed'] = True

    # in the event of a successful module execution, you will want to
    # simple AnsibleModule.exit_json(), passing the key/value results
    jctanner.network_meraki.meraki.exit_json(**jctanner.network_meraki.meraki.result)


if __name__ == '__main__':
    main()
