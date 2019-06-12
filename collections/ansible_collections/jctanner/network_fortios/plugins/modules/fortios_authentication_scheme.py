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
module: jctanner.network_fortios.fortios_authentication_scheme
short_description: Configure Authentication Schemes in Fortinet's FortiOS and FortiGate.
description:
    - This module is able to configure a FortiGate or FortiOS by
      allowing the user to configure authentication feature and scheme category.
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
    authentication_scheme:
        description:
            - Configure Authentication Schemes.
        default: null
        suboptions:
            state:
                description:
                    - Indicates whether to create or remove the object
                choices:
                    - present
                    - absent
            domain-controller:
                description:
                    - Domain controller setting. Source user.domain-controller.name.
            fsso-agent-for-ntlm:
                description:
                    - FSSO agent to use for NTLM authentication. Source user.fsso.name.
            fsso-guest:
                description:
                    - Enable/disable user fsso-guest authentication (default = disable).
                choices:
                    - enable
                    - disable
            kerberos-keytab:
                description:
                    - Kerberos keytab setting. Source user.krb-keytab.name.
            method:
                description:
                    - Authentication methods (default = basic).
                choices:
                    - ntlm
                    - basic
                    - digest
                    - form
                    - negotiate
                    - fsso
                    - rsso
                    - ssh-publickey
            name:
                description:
                    - Authentication scheme name.
                required: true
            negotiate-ntlm:
                description:
                    - Enable/disable negotiate authentication for NTLM (default = disable).
                choices:
                    - enable
                    - disable
            require-tfa:
                description:
                    - Enable/disable two-factor authentication (default = disable).
                choices:
                    - enable
                    - disable
            ssh-ca:
                description:
                    - SSH CA name. Source firewall.ssh.local-ca.name.
            user-database:
                description:
                    - Authentication server to contain user information; "local" (default) or "123" (for LDAP).
                suboptions:
                    name:
                        description:
                            - Authentication server name. Source system.datasource.name user.radius.name user.tacacs+.name user.ldap.name user.group.name.
                        required: true
'''

EXAMPLES = '''
- hosts: localhost
  vars:
   host: "192.168.122.40"
   username: "admin"
   password: ""
   vdom: "root"
  tasks:
  - name: Configure Authentication Schemes.
    jctanner.network_fortios.fortios_authentication_scheme:
      host:  "{{ host }}"
      username: "{{ username }}"
      password: "{{ password }}"
      vdom:  "{{ vdom }}"
      authentication_scheme:
        state: "present"
        domain-controller: "<your_own_value> (source user.domain-controller.name)"
        fsso-agent-for-ntlm: "<your_own_value> (source user.fsso.name)"
        fsso-guest: "enable"
        kerberos-keytab: "<your_own_value> (source user.krb-keytab.name)"
        method: "ntlm"
        name: "default_name_8"
        negotiate-ntlm: "enable"
        require-tfa: "enable"
        ssh-ca: "<your_own_value> (source firewall.ssh.local-ca.name)"
        user-database:
         -
            name: "default_name_13 (source system.datasource.name user.radius.name user.tacacs+.name user.ldap.name user.group.name)"
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


def filter_authentication_scheme_data(json):
    option_list = ['domain-controller', 'fsso-agent-for-ntlm', 'fsso-guest',
                   'kerberos-keytab', 'method', 'name',
                   'negotiate-ntlm', 'require-tfa', 'ssh-ca',
                   'user-database']
    dictionary = {}

    for attribute in option_list:
        if attribute in json and json[attribute] is not None:
            dictionary[attribute] = json[attribute]

    return dictionary


def authentication_scheme(data, fos):
    vdom = data['vdom']
    authentication_scheme_data = data['authentication_scheme']
    filtered_data = filter_authentication_scheme_data(authentication_scheme_data)
    if authentication_scheme_data['state'] == "present":
        return fos.set('authentication',
                       'scheme',
                       data=filtered_data,
                       vdom=vdom)

    elif authentication_scheme_data['state'] == "absent":
        return fos.delete('authentication',
                          'scheme',
                          mkey=filtered_data['name'],
                          vdom=vdom)


def jctanner.network_fortios.fortios_authentication(data, fos):
    login(data)

    methodlist = ['authentication_scheme']
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
        "authentication_scheme": {
            "required": False, "type": "dict",
            "options": {
                "state": {"required": True, "type": "str",
                          "choices": ["present", "absent"]},
                "domain-controller": {"required": False, "type": "str"},
                "fsso-agent-for-ntlm": {"required": False, "type": "str"},
                "fsso-guest": {"required": False, "type": "str",
                               "choices": ["enable", "disable"]},
                "kerberos-keytab": {"required": False, "type": "str"},
                "method": {"required": False, "type": "str",
                           "choices": ["ntlm", "basic", "digest",
                                       "form", "negotiate", "fsso",
                                       "rsso", "ssh-publickey"]},
                "name": {"required": True, "type": "str"},
                "negotiate-ntlm": {"required": False, "type": "str",
                                   "choices": ["enable", "disable"]},
                "require-tfa": {"required": False, "type": "str",
                                "choices": ["enable", "disable"]},
                "ssh-ca": {"required": False, "type": "str"},
                "user-database": {"required": False, "type": "list",
                                  "options": {
                                      "name": {"required": True, "type": "str"}
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

    is_error, has_changed, result = jctanner.network_fortios.fortios_authentication(module.params, fos)

    if not is_error:
        module.exit_json(changed=has_changed, meta=result)
    else:
        module.fail_json(msg="Error in repo", meta=result)


if __name__ == '__main__':
    main()
