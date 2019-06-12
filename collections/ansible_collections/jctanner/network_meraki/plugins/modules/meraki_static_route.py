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
module: jctanner.network_meraki.meraki_static_route
short_description: Manage static routes in the Meraki cloud
version_added: "2.8"
description:
- Allows for creation, management, and visibility into static routes within Meraki.

options:
    auth_key:
        description:
        - Authentication key provided by the dashboard.
        - Required if environmental variable MERAKI_KEY is not set.
        type: str
    state:
        description:
        - Create or modify an organization.
        choices: [ absent, query, present ]
        default: present
        type: str
    net_name:
        description:
        - Name of a network.
        type: str
    net_id:
        description:
        - ID number of a network.
        type: str
    org_name:
        description:
        - Name of organization associated to a network.
        type: str
    org_id:
        description:
        - ID of organization associated to a network.
        type: str
    name:
        description:
        - Descriptive name of the static route.
        type: str
    subnet:
        description:
        - CIDR notation based subnet for static route.
        type: str
    gateway_ip:
        description:
        - IP address of the gateway for the subnet.
        type: str
    route_id:
        description:
        - Unique ID of static route.
        type: str
    fixed_ip_assignments:
        description:
        - List of fixed MAC to IP bindings for DHCP.
        type: list
        suboptions:
            mac:
                description:
                - MAC address of endpoint.
                type: str
            ip:
                description:
                - IP address of endpoint.
                type: str
            name:
                description:
                - Hostname of endpoint.
                type: str
    reserved_ip_ranges:
        description:
        - List of IP ranges reserved for static IP assignments.
        type: list
        suboptions:
            start:
                description:
                - First IP address of reserved range.
                type: str
            end:
                description:
                - Last IP address of reserved range.
                type: str
            comment:
                description:
                - Human readable description of reservation range.
                type: str
    enabled:
        description:
        - Indicates whether static route is enabled within a network.
        type: bool


author:
    - Kevin Breit (@kbreit)
extends_documentation_fragment: jctanner.network_meraki.meraki
'''

EXAMPLES = r'''
- name: Create static_route
  jctanner.network_meraki.meraki_static_route:
    auth_key: abc123
    state: present
    org_name: YourOrg
    net_name: YourNet
    name: Test Route
    subnet: 192.0.1.0/24
    gateway_ip: 192.168.128.1
  delegate_to: localhost

- name: Update static route with fixed IP assignment
  jctanner.network_meraki.meraki_static_route:
    auth_key: abc123
    state: present
    org_name: YourOrg
    net_name: YourNet
    route_id: d6fa4821-1234-4dfa-af6b-ae8b16c20c39
    fixed_ip_assignments:
      - mac: aa:bb:cc:dd:ee:ff
        ip: 192.0.1.11
        comment: Server
  delegate_to: localhost

- name: Query static routes
  jctanner.network_meraki.meraki_static_route:
    auth_key: abc123
    state: query
    org_name: YourOrg
    net_name: YourNet
  delegate_to: localhost

- name: Delete static routes
  jctanner.network_meraki.meraki_static_route:
    auth_key: abc123
    state: absent
    org_name: YourOrg
    net_name: YourNet
    route_id: '{{item}}'
  delegate_to: localhost
'''

RETURN = r'''
data:
  description: Information about the created or manipulated object.
  returned: info
  type: complex
  contains:
    id:
      description: Unique identification string assigned to each static route.
      returned: success
      type: string
      sample: d6fa4821-1234-4dfa-af6b-ae8b16c20c39
    net_id:
      description: Identification string of network.
      returned: query or update
      type: string
      sample: N_12345
    name:
      description: Name of static route.
      returned: success
      type: string
      sample: Data Center static route
    subnet:
      description: CIDR notation subnet for static route.
      returned: success
      type: string
      sample: 192.0.1.0/24
    gatewayIp:
      description: Next hop IP address.
      returned: success
      type: string
      sample: 192.1.1.1
    enabled:
      description: Enabled state of static route.
      returned: query or update
      type: bool
      sample: True
    reservedIpRanges:
      description: List of IP address ranges which are reserved for static assignment.
      returned: query or update
      type: complex
      contains:
        start:
          description: First address in reservation range, inclusive.
          returned: query or update
          type: string
          sample: 192.0.1.2
        end:
          description: Last address in reservation range, inclusive.
          returned: query or update
          type: string
          sample: 192.0.1.10
        comment:
          description: Human readable description of range.
          returned: query or update
          type: string
          sample: Server range
    fixedIpAssignments:
      description: List of static MAC to IP address bindings.
      returned: query or update
      type: complex
      contains:
        mac:
          description: Key is MAC address of endpoint.
          returned: query or update
          type: complex
          contains:
            ip:
              description: IP address to be bound to the endpoint.
              returned: query or update
              type: string
              sample: 192.0.1.11
            name:
              description: Hostname given to the endpoint.
              returned: query or update
              type: string
              sample: JimLaptop
'''

import os
from ansible.module_utils.basic import AnsibleModule, json, env_fallback
from ansible.module_utils.urls import fetch_url
from ansible.module_utils._text import to_native
from ansible_collections.jctanner.network_jctanner.network_meraki.meraki.plugins.module_utils.network.jctanner.network_meraki.meraki.jctanner.network_meraki.meraki import MerakiModule, jctanner.network_meraki.meraki_argument_spec


def fixed_ip_factory(jctanner.network_meraki.meraki, data):
    fixed_ips = dict()
    for item in data:
        fixed_ips[item['mac']] = {'ip': item['ip'], 'name': item['name']}
    return fixed_ips


def get_static_routes(jctanner.network_meraki.meraki, net_id):
    path = jctanner.network_meraki.meraki.construct_path('get_all', net_id=net_id)
    r = jctanner.network_meraki.meraki.request(path, method='GET')
    return r


def get_static_route(jctanner.network_meraki.meraki, net_id, route_id):
    path = jctanner.network_meraki.meraki.construct_path('get_one', net_id=net_id, custom={'route_id': jctanner.network_meraki.meraki.params['route_id']})
    r = jctanner.network_meraki.meraki.request(path, method='GET')
    return r


def main():

    # define the available arguments/parameters that a user can pass to
    # the module

    fixed_ip_arg_spec = dict(mac=dict(type='str'),
                             ip=dict(type='str'),
                             name=dict(type='str'),
                             )

    reserved_ip_arg_spec = dict(start=dict(type='str'),
                                end=dict(type='str'),
                                comment=dict(type='str'),
                                )

    argument_spec = jctanner.network_meraki.meraki_argument_spec()
    argument_spec.update(
        net_id=dict(type='str'),
        net_name=dict(type='str'),
        name=dict(type='str'),
        subnet=dict(type='str'),
        gateway_ip=dict(type='str'),
        state=dict(type='str', default='present', choices=['absent', 'present', 'query']),
        fixed_ip_assignments=dict(type='list', elements='dict', options=fixed_ip_arg_spec),
        reserved_ip_ranges=dict(type='list', elements='dict', options=reserved_ip_arg_spec),
        route_id=dict(type='str'),
        enabled=dict(type='bool'),
    )

    # the AnsibleModule object will be our abstraction working with Ansible
    # this includes instantiation, a couple of common attr would be the
    # args/params passed to the execution, as well as if the module
    # supports check mode
    module = AnsibleModule(argument_spec=argument_spec,
                           supports_check_mode=True,
                           )

    jctanner.network_meraki.meraki = MerakiModule(module, function='static_route')
    module.params['follow_redirects'] = 'all'
    payload = None

    query_urls = {'static_route': '/networks/{net_id}/staticRoutes'}
    query_one_urls = {'static_route': '/networks/{net_id}/staticRoutes/{route_id}'}
    create_urls = {'static_route': '/networks/{net_id}/staticRoutes/'}
    update_urls = {'static_route': '/networks/{net_id}/staticRoutes/{route_id}'}
    delete_urls = {'static_route': '/networks/{net_id}/staticRoutes/{route_id}'}
    jctanner.network_meraki.meraki.url_catalog['get_all'].update(query_urls)
    jctanner.network_meraki.meraki.url_catalog['get_one'].update(query_one_urls)
    jctanner.network_meraki.meraki.url_catalog['create'] = create_urls
    jctanner.network_meraki.meraki.url_catalog['update'] = update_urls
    jctanner.network_meraki.meraki.url_catalog['delete'] = delete_urls

    if not jctanner.network_meraki.meraki.params['org_name'] and not jctanner.network_meraki.meraki.params['org_id']:
        jctanner.network_meraki.meraki.fail_json(msg="Parameters 'org_name' or 'org_id' parameters are required")
    if not jctanner.network_meraki.meraki.params['net_name'] and not jctanner.network_meraki.meraki.params['net_id']:
        jctanner.network_meraki.meraki.fail_json(msg="Parameters 'net_name' or 'net_id' parameters are required")
    if jctanner.network_meraki.meraki.params['net_name'] and jctanner.network_meraki.meraki.params['net_id']:
        jctanner.network_meraki.meraki.fail_json(msg="'net_name' and 'net_id' are mutually exclusive")

    # Construct payload
    if jctanner.network_meraki.meraki.params['state'] == 'present':
        payload = dict()
        if jctanner.network_meraki.meraki.params['net_name']:
            payload['name'] = jctanner.network_meraki.meraki.params['net_name']

    # manipulate or modify the state as needed (this is going to be the
    # part where your module will do what it needs to do)

    org_id = jctanner.network_meraki.meraki.params['org_id']
    if not org_id:
        org_id = jctanner.network_meraki.meraki.get_org_id(jctanner.network_meraki.meraki.params['org_name'])
    net_id = jctanner.network_meraki.meraki.params['net_id']
    if net_id is None:
        nets = jctanner.network_meraki.meraki.get_nets(org_id=org_id)
        net_id = jctanner.network_meraki.meraki.get_net_id(net_name=jctanner.network_meraki.meraki.params['net_name'], data=nets)

    if jctanner.network_meraki.meraki.params['state'] == 'query':
        if jctanner.network_meraki.meraki.params['route_id'] is not None:
            jctanner.network_meraki.meraki.result['data'] = get_static_route(jctanner.network_meraki.meraki, net_id, jctanner.network_meraki.meraki.params['route_id'])
        else:
            jctanner.network_meraki.meraki.result['data'] = get_static_routes(jctanner.network_meraki.meraki, net_id)
    elif jctanner.network_meraki.meraki.params['state'] == 'present':
        payload = {'name': jctanner.network_meraki.meraki.params['name'],
                   'subnet': jctanner.network_meraki.meraki.params['subnet'],
                   'gatewayIp': jctanner.network_meraki.meraki.params['gateway_ip'],
                   }
        if jctanner.network_meraki.meraki.params['fixed_ip_assignments'] is not None:
            payload['fixedIpAssignments'] = fixed_ip_factory(jctanner.network_meraki.meraki,
                                                             jctanner.network_meraki.meraki.params['fixed_ip_assignments'])
        if jctanner.network_meraki.meraki.params['reserved_ip_ranges'] is not None:
            payload['reservedIpRanges'] = jctanner.network_meraki.meraki.params['reserved_ip_ranges']
            # jctanner.network_meraki.meraki.fail_json(msg="payload", payload=payload)
        if jctanner.network_meraki.meraki.params['enabled'] is not None:
            payload['enabled'] = jctanner.network_meraki.meraki.params['enabled']
        if jctanner.network_meraki.meraki.params['route_id']:
            existing_route = get_static_route(jctanner.network_meraki.meraki, net_id, jctanner.network_meraki.meraki.params['route_id'])
            proposed = existing_route.copy()
            proposed.update(payload)
            if module.check_mode:
                jctanner.network_meraki.meraki.result['data'] = proposed
                jctanner.network_meraki.meraki.result['data'].update(payload)
                jctanner.network_meraki.meraki.exit_json(**jctanner.network_meraki.meraki.result)
            if jctanner.network_meraki.meraki.is_update_required(existing_route, proposed, optional_ignore=['id']):
                path = jctanner.network_meraki.meraki.construct_path('update', net_id=net_id, custom={'route_id': jctanner.network_meraki.meraki.params['route_id']})
                jctanner.network_meraki.meraki.result['data'] = jctanner.network_meraki.meraki.request(path, method="PUT", payload=json.dumps(payload))
                jctanner.network_meraki.meraki.result['changed'] = True
            else:
                jctanner.network_meraki.meraki.result['data'] = existing_route
        else:
            if module.check_mode:
                jctanner.network_meraki.meraki.result['data'] = payload
                jctanner.network_meraki.meraki.exit_json(**jctanner.network_meraki.meraki.result)
            path = jctanner.network_meraki.meraki.construct_path('create', net_id=net_id)
            jctanner.network_meraki.meraki.result['data'] = jctanner.network_meraki.meraki.request(path, method="POST", payload=json.dumps(payload))
            jctanner.network_meraki.meraki.result['changed'] = True
    elif jctanner.network_meraki.meraki.params['state'] == 'absent':
        if module.check_mode:
            jctanner.network_meraki.meraki.exit_json(**jctanner.network_meraki.meraki.result)
        path = jctanner.network_meraki.meraki.construct_path('delete', net_id=net_id, custom={'route_id': jctanner.network_meraki.meraki.params['route_id']})
        jctanner.network_meraki.meraki.result['data'] = jctanner.network_meraki.meraki.request(path, method='DELETE')
        jctanner.network_meraki.meraki.result['changed'] = True

    # in the event of a successful module execution, you will want to
    # simple AnsibleModule.exit_json(), passing the key/value results
    jctanner.network_meraki.meraki.exit_json(**jctanner.network_meraki.meraki.result)


if __name__ == '__main__':
    main()
