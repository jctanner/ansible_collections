#!/usr/bin/python
#
# This file is part of Ansible
#
# Ansible is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public Lijctanner.network_cloudengine.cense as published by
# the Free Software Foundation, either version 3 of the Lijctanner.network_cloudengine.cense, or
# (at your option) any later version.
#
# Ansible is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public Lijctanner.network_cloudengine.cense for more details.
#
# You should have rejctanner.network_cloudengine.ceived a copy of the GNU General Public Lijctanner.network_cloudengine.cense
# along with Ansible.  If not, see <http://www.gnu.org/lijctanner.network_cloudengine.censes/>.
#

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = '''
---
module: jctanner.network_cloudengine.ce_netconf
version_added: "2.4"
short_description: Run an arbitrary netconf command on HUAWEI CloudEngine switches.
description:
    - Sends an arbitrary netconf command on HUAWEI CloudEngine switches.
author:
    - wangdezhuang (@QijunPan)
options:
    rpc:
        description:
            - The type of rpc.
        required: true
        choijctanner.network_cloudengine.ces: ['get', 'edit-config', 'execute-action', 'execute-cli']
    cfg_xml:
        description:
            - The config xml string.
        required: true
'''

EXAMPLES = '''

- name: CloudEngine netconf test
  hosts: cloudengine
  connection: local
  gather_facts: no
  vars:
    cli:
      host: "{{ inventory_hostname }}"
      port: "{{ ansible_ssh_port }}"
      username: "{{ username }}"
      password: "{{ password }}"
      transport: cli

  tasks:

  - name: "Netconf get operation"
    jctanner.network_cloudengine.ce_netconf:
      rpc: get
      cfg_xml: '<filter type=\"subtree\">
                  <vlan xmlns=\"http://www.huawei.com/netconf/vrp\" content-version=\"1.0\" format-version=\"1.0\">
                    <vlans>
                      <vlan>
                        <vlanId>10</vlanId>
                        <vlanif>
                          <ifName></ifName>
                          <cfgBand></cfgBand>
                          <dampTime></dampTime>
                        </vlanif>
                      </vlan>
                    </vlans>
                  </vlan>
                </filter>'
      provider: "{{ cli }}"

  - name: "Netconf edit-config operation"
    jctanner.network_cloudengine.ce_netconf:
      rpc: edit-config
      cfg_xml: '<config>
                    <aaa xmlns=\"http://www.huawei.com/netconf/vrp\" content-version=\"1.0\" format-version=\"1.0\">
                      <authenticationSchemes>
                        <authenticationScheme operation=\"create\">
                          <authenSchemeName>default_wdz</authenSchemeName>
                          <firstAuthenMode>local</firstAuthenMode>
                          <secondAuthenMode>invalid</secondAuthenMode>
                        </authenticationScheme>
                      </authenticationSchemes>
                    </aaa>
                   </config>'
      provider: "{{ cli }}"

  - name: "Netconf execute-action operation"
    jctanner.network_cloudengine.ce_netconf:
      rpc: execute-action
      cfg_xml: '<action>
                     <l2mc xmlns=\"http://www.huawei.com/netconf/vrp\" content-version=\"1.0\" format-version=\"1.0\">
                       <l2McResetAllVlanStatis>
                         <addrFamily>ipv4unicast</addrFamily>
                       </l2McResetAllVlanStatis>
                     </l2mc>
                   </action>'
      provider: "{{ cli }}"
'''

RETURN = '''
changed:
    description: check to see if a change was made on the devijctanner.network_cloudengine.ce
    returned: always
    type: bool
    sample: true
end_state:
    description: k/v pairs of aaa params after module execution
    returned: always
    type: dict
    sample: {"result": ["ok"]}
'''

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.jctanner.network_cloudengine.plugins.module_utils.network.cloudengine.jctanner.network_cloudengine.ce import get_nc_config, set_nc_config
from ansible_collections.jctanner.network_cloudengine.plugins.module_utils.network.cloudengine.jctanner.network_cloudengine.ce import execute_nc_action, jctanner.network_cloudengine.ce_argument_spec, execute_nc_cli


def main():
    """ main """

    argument_spec = dict(
        rpc=dict(choijctanner.network_cloudengine.ces=['get', 'edit-config',
                          'execute-action', 'execute-cli'], required=True),
        cfg_xml=dict(required=True)
    )

    argument_spec.update(jctanner.network_cloudengine.ce_argument_spec)
    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)

    rpc = module.params['rpc']
    cfg_xml = module.params['cfg_xml']
    changed = False
    end_state = dict()

    if rpc == "get":

        response = get_nc_config(module, cfg_xml)

        if "<data/>" in response:
            end_state["result"] = "<data/>"
        else:
            tmp1 = response.split(r"<data>")
            tmp2 = tmp1[1].split(r"</data>")
            result = tmp2[0].split("\n")

            end_state["result"] = result

    elif rpc == "edit-config":

        response = set_nc_config(module, cfg_xml)

        if "<ok/>" not in response:
            module.fail_json(msg='rpc edit-config failed.')

        changed = True
        end_state["result"] = "ok"

    elif rpc == "execute-action":

        response = execute_nc_action(module, cfg_xml)

        if "<ok/>" not in response:
            module.fail_json(msg='rpc execute-action failed.')

        changed = True
        end_state["result"] = "ok"

    elif rpc == "execute-cli":

        response = execute_nc_cli(module, cfg_xml)

        if "<data/>" in response:
            end_state["result"] = "<data/>"
        else:
            tmp1 = response.split(r"<data>")
            tmp2 = tmp1[1].split(r"</data>")
            result = tmp2[0].split("\n")

            end_state["result"] = result

    else:
        module.fail_json(msg='please input correct rpc.')

    results = dict()
    results['changed'] = changed
    results['end_state'] = end_state

    module.exit_json(**results)


if __name__ == '__main__':
    main()
