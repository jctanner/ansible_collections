#!/usr/bin/python
from __future__ import (absolute_import, division, print_function)
# Copyright 2018 Fortinet, Inc.
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
module: jctanner.network_fortios.fortios_application_custom
short_description: Configure custom application signatures in Fortinet's FortiOS and FortiGate.
description:
    - This module is able to configure a FortiGate or FortiOS by
      allowing the user to configure application feature and custom category.
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
        default: false
    application_custom:
        description:
            - Configure custom application signatures.
        default: null
        suboptions:
            state:
                description:
                    - Indicates whether to create or remove the object
                choices:
                    - present
                    - absent
            behavior:
                description:
                    - Custom application signature behavior.
            category:
                description:
                    - Custom application category ID (use ? to view available options).
            comment:
                description:
                    - Comment.
            id:
                description:
                    - Custom application category ID (use ? to view available options).
            name:
                description:
                    - Name of this custom application signature.
            protocol:
                description:
                    - Custom application signature protocol.
            signature:
                description:
                    - The text that makes up the actual custom application signature.
            tag:
                description:
                    - Signature tag.
                required: true
            technology:
                description:
                    - Custom application signature technology.
            vendor:
                description:
                    - Custom application signature vendor.
'''

EXAMPLES = '''
- hosts: localhost
  vars:
   host: "192.168.122.40"
   username: "admin"
   password: ""
   vdom: "root"
  tasks:
  - name: Configure custom application signatures.
    jctanner.network_fortios.fortios_application_custom:
      host:  "{{ host }}"
      username: "{{ username }}"
      password: "{{ password }}"
      vdom:  "{{ vdom }}"
      application_custom:
        state: "present"
        behavior: "<your_own_value>"
        category: "4"
        comment: "Comment."
        id:  "6"
        name: "default_name_7"
        protocol: "<your_own_value>"
        signature: "<your_own_value>"
        tag: "<your_own_value>"
        technology: "<your_own_value>"
        vendor: "<your_own_value>"
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


def filter_application_custom_data(json):
    option_list = ['behavior', 'category', 'comment',
                   'id', 'name', 'protocol',
                   'signature', 'tag', 'technology',
                   'vendor']
    dictionary = {}

    for attribute in option_list:
        if attribute in json and json[attribute] is not None:
            dictionary[attribute] = json[attribute]

    return dictionary


def application_custom(data, fos):
    vdom = data['vdom']
    application_custom_data = data['application_custom']
    filtered_data = filter_application_custom_data(application_custom_data)
    if application_custom_data['state'] == "present":
        return fos.set('application',
                       'custom',
                       data=filtered_data,
                       vdom=vdom)

    elif application_custom_data['state'] == "absent":
        return fos.delete('application',
                          'custom',
                          mkey=filtered_data['tag'],
                          vdom=vdom)


def jctanner.network_fortios.fortios_application(data, fos):
    login(data)

    methodlist = ['application_custom']
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
        "https": {"required": False, "type": "bool", "default": "False"},
        "application_custom": {
            "required": False, "type": "dict",
            "options": {
                "state": {"required": True, "type": "str",
                          "choices": ["present", "absent"]},
                "behavior": {"required": False, "type": "str"},
                "category": {"required": False, "type": "int"},
                "comment": {"required": False, "type": "str"},
                "id": {"required": False, "type": "int"},
                "name": {"required": False, "type": "str"},
                "protocol": {"required": False, "type": "str"},
                "signature": {"required": False, "type": "str"},
                "tag": {"required": True, "type": "str"},
                "technology": {"required": False, "type": "str"},
                "vendor": {"required": False, "type": "str"}

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

    is_error, has_changed, result = jctanner.network_fortios.fortios_application(module.params, fos)

    if not is_error:
        module.exit_json(changed=has_changed, meta=result)
    else:
        module.fail_json(msg="Error in repo", meta=result)


if __name__ == '__main__':
    main()