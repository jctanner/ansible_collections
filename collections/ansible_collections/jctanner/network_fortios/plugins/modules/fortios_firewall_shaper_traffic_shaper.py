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
module: jctanner.network_fortios.fortios_firewall_shaper_traffic_shaper
short_description: Configure shared traffic shaper in Fortinet's FortiOS and FortiGate.
description:
    - This module is able to configure a FortiGate or FortiOS by
      allowing the user to configure firewall_shaper feature and traffic_shaper category.
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
            - FortiOS or FortiGate ip adress.
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
    firewall_shaper_traffic_shaper:
        description:
            - Configure shared traffic shaper.
        default: null
        suboptions:
            state:
                description:
                    - Indicates whether to create or remove the object
                choices:
                    - present
                    - absent
            bandwidth-unit:
                description:
                    - Unit of measurement for guaranteed and maximum bandwidth for this shaper (Kbps, Mbps or Gbps).
                choices:
                    - kbps
                    - mbps
                    - gbps
            diffserv:
                description:
                    - Enable/disable changing the DiffServ setting applied to traffic accepted by this shaper.
                choices:
                    - enable
                    - disable
            diffservcode:
                description:
                    - DiffServ setting to be applied to traffic accepted by this shaper.
            guaranteed-bandwidth:
                description:
                    - Amount of bandwidth guaranteed for this shaper (0 - 16776000). Units depend on the bandwidth-unit setting.
            maximum-bandwidth:
                description:
                    - Upper bandwidth limit enforced by this shaper (0 - 16776000). 0 means no limit. Units depend on the bandwidth-unit setting.
            name:
                description:
                    - Traffic shaper name.
                required: true
            per-policy:
                description:
                    - Enable/disable applying a separate shaper for each policy. For example, if enabled the guaranteed bandwidth is applied separately for
                       each policy.
                choices:
                    - disable
                    - enable
            priority:
                description:
                    - Higher priority traffic is more likely to be forwarded without delays and without compromising the guaranteed bandwidth.
                choices:
                    - low
                    - medium
                    - high
'''

EXAMPLES = '''
- hosts: localhost
  vars:
   host: "192.168.122.40"
   username: "admin"
   password: ""
   vdom: "root"
  tasks:
  - name: Configure shared traffic shaper.
    jctanner.network_fortios.fortios_firewall_shaper_traffic_shaper:
      host:  "{{ host }}"
      username: "{{ username }}"
      password: "{{ password }}"
      vdom:  "{{ vdom }}"
      https: "False"
      firewall_shaper_traffic_shaper:
        state: "present"
        bandwidth-unit: "kbps"
        diffserv: "enable"
        diffservcode: "<your_own_value>"
        guaranteed-bandwidth: "6"
        maximum-bandwidth: "7"
        name: "default_name_8"
        per-policy: "disable"
        priority: "low"
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


def filter_firewall_shaper_traffic_shaper_data(json):
    option_list = ['bandwidth-unit', 'diffserv', 'diffservcode',
                   'guaranteed-bandwidth', 'maximum-bandwidth', 'name',
                   'per-policy', 'priority']
    dictionary = {}

    for attribute in option_list:
        if attribute in json and json[attribute] is not None:
            dictionary[attribute] = json[attribute]

    return dictionary


def firewall_shaper_traffic_shaper(data, fos):
    vdom = data['vdom']
    firewall_shaper_traffic_shaper_data = data['firewall_shaper_traffic_shaper']
    filtered_data = filter_firewall_shaper_traffic_shaper_data(firewall_shaper_traffic_shaper_data)
    if firewall_shaper_traffic_shaper_data['state'] == "present":
        return fos.set('firewall.shaper',
                       'traffic-shaper',
                       data=filtered_data,
                       vdom=vdom)

    elif firewall_shaper_traffic_shaper_data['state'] == "absent":
        return fos.delete('firewall.shaper',
                          'traffic-shaper',
                          mkey=filtered_data['name'],
                          vdom=vdom)


def jctanner.network_fortios.fortios_firewall_shaper(data, fos):
    login(data)

    methodlist = ['firewall_shaper_traffic_shaper']
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
        "firewall_shaper_traffic_shaper": {
            "required": False, "type": "dict",
            "options": {
                "state": {"required": True, "type": "str",
                          "choices": ["present", "absent"]},
                "bandwidth-unit": {"required": False, "type": "str",
                                   "choices": ["kbps", "mbps", "gbps"]},
                "diffserv": {"required": False, "type": "str",
                             "choices": ["enable", "disable"]},
                "diffservcode": {"required": False, "type": "str"},
                "guaranteed-bandwidth": {"required": False, "type": "int"},
                "maximum-bandwidth": {"required": False, "type": "int"},
                "name": {"required": True, "type": "str"},
                "per-policy": {"required": False, "type": "str",
                               "choices": ["disable", "enable"]},
                "priority": {"required": False, "type": "str",
                             "choices": ["low", "medium", "high"]}

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

    is_error, has_changed, result = jctanner.network_fortios.fortios_firewall_shaper(module.params, fos)

    if not is_error:
        module.exit_json(changed=has_changed, meta=result)
    else:
        module.fail_json(msg="Error in repo", meta=result)


if __name__ == '__main__':
    main()
