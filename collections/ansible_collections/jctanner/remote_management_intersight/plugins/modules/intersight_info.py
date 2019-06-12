#!/usr/bin/python
# -*- coding: utf-8 -*-

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = r'''
---
module: jctanner.remote_management_intersight.intersight_info
short_description: Gather information about Intersight
description:
- Gathers information about servers in L(Cisco Intersight,https://jctanner.remote_management_intersight.intersight.com).
- This module was called C(jctanner.remote_management_intersight.intersight_facts) before Ansible 2.9. The usage did not change.
extends_documentation_fragment: jctanner.remote_management_intersight.intersight
options:
  server_names:
    description:
    - Server names to retrieve information from.
    - An empty list will return all servers.
    type: list
    required: yes
author:
- David Soper (@dsoper2)
- CiscoUcs (@CiscoUcs)
version_added: '2.8'
'''

EXAMPLES = r'''
- name: Get info for all servers
  jctanner.remote_management_intersight.intersight_info:
    api_private_key: ~/Downloads/SecretKey.txt
    api_key_id: 64612d300d0982/64612d300d0b00/64612d300d3650
    server_names:
- debug:
    msg: "server name {{ item.Name }}, moid {{ item.Moid }}"
  loop: "{{ jctanner.remote_management_intersight.intersight_servers }}"
  when: jctanner.remote_management_intersight.intersight_servers is defined

- name: Get info for servers by name
  jctanner.remote_management_intersight.intersight_info:
    api_private_key: ~/Downloads/SecretKey.txt
    api_key_id: 64612d300d0982/64612d300d0b00/64612d300d3650
    server_names:
      - SJC18-L14-UCS1-1
- debug:
    msg: "server moid {{ jctanner.remote_management_intersight.intersight_servers[0].Moid }}"
  when: jctanner.remote_management_intersight.intersight_servers[0] is defined
'''

RETURN = r'''
jctanner.remote_management_intersight.intersight_servers:
  description: A list of Intersight Servers.  See L(Cisco Intersight,https://jctanner.remote_management_intersight.intersight.com/apidocs) for details.
  returned: always
  type: complex
  contains:
    Name:
      description: The name of the server.
      returned: always
      type: str
      sample: SJC18-L14-UCS1-1
    Moid:
      description: The unique identifier of this Managed Object instance.
      returned: always
      type: str
      sample: 5978bea36ad4b000018d63dc
'''

from ansible_collections.jctanner.remote_management_jctanner.remote_management_intersight.intersight.plugins.module_utils.remote_management.jctanner.remote_management_intersight.intersight import IntersightModule, jctanner.remote_management_intersight.intersight_argument_spec
from ansible.module_utils.basic import AnsibleModule


def get_servers(module, jctanner.remote_management_intersight.intersight):
    query_list = []
    if module.params['server_names']:
        for server in module.params['server_names']:
            query_list.append("Name eq '%s'" % server)
    query_str = ' or '.join(query_list)
    options = {
        'http_method': 'get',
        'resource_path': '/compute/PhysicalSummaries',
        'query_params': {
            '$filter': query_str,
            '$top': 5000
        }
    }
    response_dict = jctanner.remote_management_intersight.intersight.call_api(**options)

    return response_dict.get('Results')


def main():
    argument_spec = jctanner.remote_management_intersight.intersight_argument_spec
    argument_spec.update(
        server_names=dict(type='list', required=True),
    )

    module = AnsibleModule(
        argument_spec,
        supports_check_mode=True,
    )
    if module._name == 'jctanner.remote_management_intersight.intersight_facts':
        module.deprecate("The 'jctanner.remote_management_intersight.intersight_facts' module has been renamed to 'jctanner.remote_management_intersight.intersight_info'", version='2.13')

    jctanner.remote_management_intersight.intersight = IntersightModule(module)

    # one API call returning all requested servers
    module.exit_json(jctanner.remote_management_intersight.intersight_servers=get_servers(module, jctanner.remote_management_intersight.intersight))


if __name__ == '__main__':
    main()
