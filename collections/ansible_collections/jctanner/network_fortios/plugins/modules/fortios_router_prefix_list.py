#!/usr/bin/python
from __future__ import (absolute_import, division, print_function)
# Copyright 2019 Fortinet, Inc.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
# the lib use python logging can get it if the following is set in your
# Ansible config.

__metaclass__ = type

ANSIBLE_METADATA = {'status': ['preview'],
                    'supported_by': 'community',
                    'metadata_version': '1.1'}

DOCUMENTATION = '''
---
module: jctanner.network_fortios.fortios_router_prefix_list
short_description: Configure IPv4 prefix lists in Fortinet's FortiOS and FortiGate.
description:
    - This module is able to configure a FortiGate or FortiOS by allowing the
      user to set and modify router feature and prefix_list category.
      Examples include all parameters and values need to be adjusted to datasources before usage.
      Tested with FOS v6.0.2
version_added: "2.8"
author:
    - Miguel Angel Munoz (@mamunozgonzalez)
    - Nicolas Thomas (@thomnico)
notes:
    - Requires jctanner.network_fortios.fortiosapi library developed by Fortinet
    - Run as a local_action in your playbook
requirements:
    - jctanner.network_fortios.fortiosapi>=0.9.8
options:
    host:
       description:
            - FortiOS or FortiGate ip address.
       required: true
    username:
        description:
            - FortiOS or FortiGate username.
        required: true
    password:
        description:
            - FortiOS or FortiGate password.
        default: ""
    vdom:
        description:
            - Virtual domain, among those defined previously. A vdom is a
              virtual instance of the FortiGate that can be configured and
              used as a different unit.
        default: root
    https:
        description:
            - Indicates if the requests towards FortiGate must use HTTPS
              protocol
        type: bool
        default: true
    router_prefix_list:
        description:
            - Configure IPv4 prefix lists.
        default: null
        suboptions:
            state:
                description:
                    - Indicates whether to create or remove the object
                choices:
                    - present
                    - absent
            comments:
                description:
                    - Comment.
            name:
                description:
                    - Name.
                required: true
            rule:
                description:
                    - IPv4 prefix list rule.
                suboptions:
                    action:
                        description:
                            - Permit or deny this IP address and netmask prefix.
                        choices:
                            - permit
                            - deny
                    flags:
                        description:
                            - Flags.
                    ge:
                        description:
                            - Minimum prefix length to be matched (0 - 32).
                    id:
                        description:
                            - Rule ID.
                        required: true
                    le:
                        description:
                            - Maximum prefix length to be matched (0 - 32).
                    prefix:
                        description:
                            - IPv4 prefix to define regular filter criteria, such as "any" or subnets.
'''

EXAMPLES = '''
- hosts: localhost
  vars:
   host: "192.168.122.40"
   username: "admin"
   password: ""
   vdom: "root"
  tasks:
  - name: Configure IPv4 prefix lists.
    jctanner.network_fortios.fortios_router_prefix_list:
      host:  "{{ host }}"
      username: "{{ username }}"
      password: "{{ password }}"
      vdom:  "{{ vdom }}"
      https: "False"
      router_prefix_list:
        state: "present"
        comments: "<your_own_value>"
        name: "default_name_4"
        rule:
         -
            action: "permit"
            flags: "7"
            ge: "8"
            id:  "9"
            le: "10"
            prefix: "<your_own_value>"
'''

RETURN = '''
build:
  description: Build number of the fortigate image
  returned: always
  type: str
  sample: '1547'
http_method:
  description: Last method used to provision the content into FortiGate
  returned: always
  type: str
  sample: 'PUT'
http_status:
  description: Last result given by FortiGate on last operation applied
  returned: always
  type: str
  sample: "200"
mkey:
  description: Master key (id) used in the last call to FortiGate
  returned: success
  type: str
  sample: "id"
name:
  description: Name of the table used to fulfill the request
  returned: always
  type: str
  sample: "urlfilter"
path:
  description: Path of the table used to fulfill the request
  returned: always
  type: str
  sample: "webfilter"
revision:
  description: Internal revision number
  returned: always
  type: str
  sample: "17.0.2.10658"
serial:
  description: Serial number of the unit
  returned: always
  type: str
  sample: "FGVMEVYYQT3AB5352"
status:
  description: Indication of the operation's result
  returned: always
  type: str
  sample: "success"
vdom:
  description: Virtual domain used
  returned: always
  type: str
  sample: "root"
version:
  description: Version of the FortiGate
  returned: always
  type: str
  sample: "v5.6.3"

'''

from ansible.module_utils.basic import AnsibleModule

fos = None


def login(data):
    host = data['host']
    username = data['username']
    password = data['password']

    fos.debug('on')
    if 'https' in data and not data['https']:
        fos.https('off')
    else:
        fos.https('on')

    fos.login(host, username, password)


def filter_router_prefix_list_data(json):
    option_list = ['comments', 'name', 'rule']
    dictionary = {}

    for attribute in option_list:
        if attribute in json and json[attribute] is not None:
            dictionary[attribute] = json[attribute]

    return dictionary


def flatten_multilists_attributes(data):
    multilist_attrs = []

    for attr in multilist_attrs:
        try:
            path = "data['" + "']['".join(elem for elem in attr) + "']"
            current_val = eval(path)
            flattened_val = ' '.join(elem for elem in current_val)
            exec(path + '= flattened_val')
        except BaseException:
            pass

    return data


def router_prefix_list(data, fos):
    vdom = data['vdom']
    router_prefix_list_data = data['router_prefix_list']
    flattened_data = flatten_multilists_attributes(router_prefix_list_data)
    filtered_data = filter_router_prefix_list_data(flattened_data)
    if router_prefix_list_data['state'] == "present":
        return fos.set('router',
                       'prefix-list',
                       data=filtered_data,
                       vdom=vdom)

    elif router_prefix_list_data['state'] == "absent":
        return fos.delete('router',
                          'prefix-list',
                          mkey=filtered_data['name'],
                          vdom=vdom)


def jctanner.network_fortios.fortios_router(data, fos):
    login(data)

    if data['router_prefix_list']:
        resp = router_prefix_list(data, fos)

    fos.logout()
    return not resp['status'] == "success", resp['status'] == "success", resp


def main():
    fields = {
        "host": {"required": True, "type": "str"},
        "username": {"required": True, "type": "str"},
        "password": {"required": False, "type": "str", "no_log": True},
        "vdom": {"required": False, "type": "str", "default": "root"},
        "https": {"required": False, "type": "bool", "default": True},
        "router_prefix_list": {
            "required": False, "type": "dict",
            "options": {
                "state": {"required": True, "type": "str",
                          "choices": ["present", "absent"]},
                "comments": {"required": False, "type": "str"},
                "name": {"required": True, "type": "str"},
                "rule": {"required": False, "type": "list",
                         "options": {
                             "action": {"required": False, "type": "str",
                                        "choices": ["permit", "deny"]},
                             "flags": {"required": False, "type": "int"},
                             "ge": {"required": False, "type": "int"},
                             "id": {"required": True, "type": "int"},
                             "le": {"required": False, "type": "int"},
                             "prefix": {"required": False, "type": "str"}
                         }}

            }
        }
    }

    module = AnsibleModule(argument_spec=fields,
                           supports_check_mode=False)
    try:
        from jctanner.network_fortios.fortiosapi import FortiOSAPI
    except ImportError:
        module.fail_json(msg="jctanner.network_fortios.fortiosapi module is required")

    global fos
    fos = FortiOSAPI()

    is_error, has_changed, result = jctanner.network_fortios.fortios_router(module.params, fos)

    if not is_error:
        module.exit_json(changed=has_changed, meta=result)
    else:
        module.fail_json(msg="Error in repo", meta=result)


if __name__ == '__main__':
    main()
