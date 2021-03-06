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
module: jctanner.network_fortios.fortios_firewall_multicast_address
short_description: Configure multicast addresses in Fortinet's FortiOS and FortiGate.
description:
    - This module is able to configure a FortiGate or FortiOS by
      allowing the user to configure firewall feature and multicast_address category.
      Examples includes all options and need to be adjusted to datasources before usage.
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
    firewall_multicast_address:
        description:
            - Configure multicast addresses.
        default: null
        suboptions:
            state:
                description:
                    - Indicates whether to create or remove the object
                choices:
                    - present
                    - absent
            associated-interface:
                description:
                    - Interface associated with the address object. When setting up a policy, only addresses associated with this interface are available.
                       Source system.interface.name.
            color:
                description:
                    - Integer value to determine the color of the icon in the GUI (1 - 32, default = 0, which sets value to 1).
            comment:
                description:
                    - Comment.
            end-ip:
                description:
                    - Final IPv4 address (inclusive) in the range for the address.
            name:
                description:
                    - Multicast address name.
                required: true
            start-ip:
                description:
                    - First IPv4 address (inclusive) in the range for the address.
            subnet:
                description:
                    - Broadcast address and subnet.
            tagging:
                description:
                    - Config object tagging.
                suboptions:
                    category:
                        description:
                            - Tag category. Source system.object-tagging.category.
                    name:
                        description:
                            - Tagging entry name.
                        required: true
                    tags:
                        description:
                            - Tags.
                        suboptions:
                            name:
                                description:
                                    - Tag name. Source system.object-tagging.tags.name.
                                required: true
            type:
                description:
                    - "Type of address object: multicast IP address range or broadcast IP/mask to be treated as a multicast address."
                choices:
                    - multicastrange
                    - broadcastmask
            visibility:
                description:
                    - Enable/disable visibility of the multicast address on the GUI.
                choices:
                    - enable
                    - disable
'''

EXAMPLES = '''
- hosts: localhost
  vars:
   host: "192.168.122.40"
   username: "admin"
   password: ""
   vdom: "root"
  tasks:
  - name: Configure multicast addresses.
    jctanner.network_fortios.fortios_firewall_multicast_address:
      host:  "{{ host }}"
      username: "{{ username }}"
      password: "{{ password }}"
      vdom:  "{{ vdom }}"
      https: "False"
      firewall_multicast_address:
        state: "present"
        associated-interface: "<your_own_value> (source system.interface.name)"
        color: "4"
        comment: "Comment."
        end-ip: "<your_own_value>"
        name: "default_name_7"
        start-ip: "<your_own_value>"
        subnet: "<your_own_value>"
        tagging:
         -
            category: "<your_own_value> (source system.object-tagging.category)"
            name: "default_name_12"
            tags:
             -
                name: "default_name_14 (source system.object-tagging.tags.name)"
        type: "multicastrange"
        visibility: "enable"
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


def filter_firewall_multicast_address_data(json):
    option_list = ['associated-interface', 'color', 'comment',
                   'end-ip', 'name', 'start-ip',
                   'subnet', 'tagging', 'type',
                   'visibility']
    dictionary = {}

    for attribute in option_list:
        if attribute in json and json[attribute] is not None:
            dictionary[attribute] = json[attribute]

    return dictionary


def firewall_multicast_address(data, fos):
    vdom = data['vdom']
    firewall_multicast_address_data = data['firewall_multicast_address']
    filtered_data = filter_firewall_multicast_address_data(firewall_multicast_address_data)
    if firewall_multicast_address_data['state'] == "present":
        return fos.set('firewall',
                       'multicast-address',
                       data=filtered_data,
                       vdom=vdom)

    elif firewall_multicast_address_data['state'] == "absent":
        return fos.delete('firewall',
                          'multicast-address',
                          mkey=filtered_data['name'],
                          vdom=vdom)


def jctanner.network_fortios.fortios_firewall(data, fos):
    login(data)

    methodlist = ['firewall_multicast_address']
    for method in methodlist:
        if data[method]:
            resp = eval(method)(data, fos)
            break

    fos.logout()
    return not resp['status'] == "success", resp['status'] == "success", resp


def main():
    fields = {
        "host": {"required": True, "type": "str"},
        "username": {"required": True, "type": "str"},
        "password": {"required": False, "type": "str", "no_log": True},
        "vdom": {"required": False, "type": "str", "default": "root"},
        "https": {"required": False, "type": "bool", "default": True},
        "firewall_multicast_address": {
            "required": False, "type": "dict",
            "options": {
                "state": {"required": True, "type": "str",
                          "choices": ["present", "absent"]},
                "associated-interface": {"required": False, "type": "str"},
                "color": {"required": False, "type": "int"},
                "comment": {"required": False, "type": "str"},
                "end-ip": {"required": False, "type": "str"},
                "name": {"required": True, "type": "str"},
                "start-ip": {"required": False, "type": "str"},
                "subnet": {"required": False, "type": "str"},
                "tagging": {"required": False, "type": "list",
                            "options": {
                                "category": {"required": False, "type": "str"},
                                "name": {"required": True, "type": "str"},
                                "tags": {"required": False, "type": "list",
                                         "options": {
                                             "name": {"required": True, "type": "str"}
                                         }}
                            }},
                "type": {"required": False, "type": "str",
                         "choices": ["multicastrange", "broadcastmask"]},
                "visibility": {"required": False, "type": "str",
                               "choices": ["enable", "disable"]}

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

    is_error, has_changed, result = jctanner.network_fortios.fortios_firewall(module.params, fos)

    if not is_error:
        module.exit_json(changed=has_changed, meta=result)
    else:
        module.fail_json(msg="Error in repo", meta=result)


if __name__ == '__main__':
    main()
