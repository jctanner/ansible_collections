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
module: jctanner.network_fortios.fortios_router_multicast6
short_description: Configure IPv6 multicast in Fortinet's FortiOS and FortiGate.
description:
    - This module is able to configure a FortiGate or FortiOS by allowing the
      user to set and modify router feature and multicast6 category.
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
    router_multicast6:
        description:
            - Configure IPv6 multicast.
        default: null
        suboptions:
            interface:
                description:
                    - Protocol Independent Multicast (PIM) interfaces.
                suboptions:
                    hello-holdtime:
                        description:
                            - Time before old neighbour information expires (1 - 65535 sec, default = 105).
                    hello-interval:
                        description:
                            - Interval between sending PIM hello messages  (1 - 65535 sec, default = 30)..
                    name:
                        description:
                            - Interface name. Source system.interface.name.
                        required: true
            multicast-pmtu:
                description:
                    - Enable/disable PMTU for IPv6 multicast.
                choices:
                    - enable
                    - disable
            multicast-routing:
                description:
                    - Enable/disable IPv6 multicast routing.
                choices:
                    - enable
                    - disable
            pim-sm-global:
                description:
                    - PIM sparse-mode global settings.
                suboptions:
                    register-rate-limit:
                        description:
                            - Limit of packets/sec per source registered through this RP (0 means unlimited).
                    rp-address:
                        description:
                            - Statically configured RP addresses.
                        suboptions:
                            id:
                                description:
                                    - ID of the entry.
                                required: true
                            ip6-address:
                                description:
                                    - RP router IPv6 address.
'''

EXAMPLES = '''
- hosts: localhost
  vars:
   host: "192.168.122.40"
   username: "admin"
   password: ""
   vdom: "root"
  tasks:
  - name: Configure IPv6 multicast.
    jctanner.network_fortios.fortios_router_multicast6:
      host:  "{{ host }}"
      username: "{{ username }}"
      password: "{{ password }}"
      vdom:  "{{ vdom }}"
      https: "False"
      router_multicast6:
        interface:
         -
            hello-holdtime: "4"
            hello-interval: "5"
            name: "default_name_6 (source system.interface.name)"
        multicast-pmtu: "enable"
        multicast-routing: "enable"
        pim-sm-global:
            register-rate-limit: "10"
            rp-address:
             -
                id:  "12"
                ip6-address: "<your_own_value>"
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


def filter_router_multicast6_data(json):
    option_list = ['interface', 'multicast-pmtu', 'multicast-routing',
                   'pim-sm-global']
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


def router_multicast6(data, fos):
    vdom = data['vdom']
    router_multicast6_data = data['router_multicast6']
    flattened_data = flatten_multilists_attributes(router_multicast6_data)
    filtered_data = filter_router_multicast6_data(flattened_data)
    return fos.set('router',
                   'multicast6',
                   data=filtered_data,
                   vdom=vdom)


def jctanner.network_fortios.fortios_router(data, fos):
    login(data)

    if data['router_multicast6']:
        resp = router_multicast6(data, fos)

    fos.logout()
    return not resp['status'] == "success", resp['status'] == "success", resp


def main():
    fields = {
        "host": {"required": True, "type": "str"},
        "username": {"required": True, "type": "str"},
        "password": {"required": False, "type": "str", "no_log": True},
        "vdom": {"required": False, "type": "str", "default": "root"},
        "https": {"required": False, "type": "bool", "default": True},
        "router_multicast6": {
            "required": False, "type": "dict",
            "options": {
                "interface": {"required": False, "type": "list",
                              "options": {
                                  "hello-holdtime": {"required": False, "type": "int"},
                                  "hello-interval": {"required": False, "type": "int"},
                                  "name": {"required": True, "type": "str"}
                              }},
                "multicast-pmtu": {"required": False, "type": "str",
                                   "choices": ["enable", "disable"]},
                "multicast-routing": {"required": False, "type": "str",
                                      "choices": ["enable", "disable"]},
                "pim-sm-global": {"required": False, "type": "dict",
                                  "options": {
                                      "register-rate-limit": {"required": False, "type": "int"},
                                      "rp-address": {"required": False, "type": "list",
                                                     "options": {
                                                         "id": {"required": True, "type": "int"},
                                                         "ip6-address": {"required": False, "type": "str"}
                                                     }}
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
