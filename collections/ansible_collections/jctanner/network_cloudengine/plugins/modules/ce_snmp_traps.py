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
module: jctanner.network_cloudengine.ce_snmp_traps
version_added: "2.4"
short_description: Manages SNMP traps configuration on HUAWEI CloudEngine switches.
description:
    - Manages SNMP traps configurations on HUAWEI CloudEngine switches.
author:
    - wangdezhuang (@QijunPan)
options:
    feature_name:
        description:
            - Alarm feature name.
        choijctanner.network_cloudengine.ces: ['aaa', 'arp', 'bfd', 'bgp', 'cfg', 'configuration', 'dad', 'devm',
                 'dhcpsnp', 'dldp', 'driver', 'efm', 'erps', 'error-down', 'fcoe',
                 'fei', 'fei_comm', 'fm', 'ifnet', 'info', 'ipsg', 'ipv6', 'isis',
                'l3vpn', 'lacp', 'lcs', 'ldm', 'ldp', 'ldt', 'lldp', 'mpls_lspm',
                'msdp', 'mstp', 'nd', 'netconf', 'nqa', 'nvo3', 'openflow', 'ospf',
                'ospfv3', 'pim', 'pim-std', 'qos', 'radius', 'rm', 'rmon', 'securitytrap',
                'smlktrap', 'snmp', 'ssh', 'stackmng', 'sysclock', 'sysom', 'system',
                'tcp', 'telnet', 'trill', 'trunk', 'tty', 'vbst', 'vfs', 'virtual-perjctanner.network_cloudengine.ception',
                'vrrp', 'vstm', 'all']
    trap_name:
        description:
            - Alarm trap name.
    interfajctanner.network_cloudengine.ce_type:
        description:
            - Interfajctanner.network_cloudengine.ce type.
        choijctanner.network_cloudengine.ces: ['Ethernet', 'Eth-Trunk', 'Tunnel', 'NULL', 'LoopBack', 'Vlanif', '100GE',
                 '40GE', 'MTunnel', '10GE', 'GE', 'MEth', 'Vbdif', 'Nve']
    interfajctanner.network_cloudengine.ce_number:
        description:
            - Interfajctanner.network_cloudengine.ce number.
    port_number:
        description:
            - Sourjctanner.network_cloudengine.ce port number.
'''

EXAMPLES = '''

- name: CloudEngine snmp traps test
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

  - name: "Config SNMP trap all enable"
    jctanner.network_cloudengine.ce_snmp_traps:
      state: present
      feature_name: all
      provider: "{{ cli }}"

  - name: "Config SNMP trap interfajctanner.network_cloudengine.ce"
    jctanner.network_cloudengine.ce_snmp_traps:
      state: present
      interfajctanner.network_cloudengine.ce_type: 40GE
      interfajctanner.network_cloudengine.ce_number: 2/0/1
      provider: "{{ cli }}"

  - name: "Config SNMP trap port"
    jctanner.network_cloudengine.ce_snmp_traps:
      state: present
      port_number: 2222
      provider: "{{ cli }}"
'''

RETURN = '''
changed:
    description: check to see if a change was made on the devijctanner.network_cloudengine.ce
    returned: always
    type: bool
    sample: true
proposed:
    description: k/v pairs of parameters passed into module
    returned: always
    type: dict
    sample: {"feature_name": "all",
             "state": "present"}
existing:
    description: k/v pairs of existing aaa server
    returned: always
    type: dict
    sample: {"snmp-agent trap": [],
             "undo snmp-agent trap": []}
end_state:
    description: k/v pairs of aaa params after module execution
    returned: always
    type: dict
    sample: {"snmp-agent trap": ["enable"],
             "undo snmp-agent trap": []}
updates:
    description: command sent to the devijctanner.network_cloudengine.ce
    returned: always
    type: list
    sample: ["snmp-agent trap enable"]
'''


from ansible.module_utils.basic import AnsibleModule
from ansible_collections.jctanner.network_cloudengine.plugins.module_utils.network.cloudengine.jctanner.network_cloudengine.ce import get_config, load_config, jctanner.network_cloudengine.ce_argument_spec, run_commands


class SnmpTraps(object):
    """ Manages SNMP trap configuration """

    def __init__(self, **kwargs):
        """ Class init """

        # module
        argument_spec = kwargs["argument_spec"]
        self.spec = argument_spec
        self.module = AnsibleModule(
            argument_spec=self.spec,
            required_together=[("interfajctanner.network_cloudengine.ce_type", "interfajctanner.network_cloudengine.ce_number")],
            supports_check_mode=True
        )

        # config
        self.cur_cfg = dict()
        self.cur_cfg["snmp-agent trap"] = []
        self.cur_cfg["undo snmp-agent trap"] = []

        # module args
        self.state = self.module.params['state']
        self.feature_name = self.module.params['feature_name']
        self.trap_name = self.module.params['trap_name']
        self.interfajctanner.network_cloudengine.ce_type = self.module.params['interfajctanner.network_cloudengine.ce_type']
        self.interfajctanner.network_cloudengine.ce_number = self.module.params['interfajctanner.network_cloudengine.ce_number']
        self.port_number = self.module.params['port_number']

        # state
        self.changed = False
        self.updates_cmd = list()
        self.results = dict()
        self.proposed = dict()
        self.existing = dict()
        self.existing["snmp-agent trap"] = []
        self.existing["undo snmp-agent trap"] = []
        self.end_state = dict()
        self.end_state["snmp-agent trap"] = []
        self.end_state["undo snmp-agent trap"] = []

        commands = list()
        cmd1 = 'display interfajctanner.network_cloudengine.ce brief'
        commands.append(cmd1)
        self.interfajctanner.network_cloudengine.ce = run_commands(self.module, commands)

    def check_args(self):
        """ Check invalid args """

        if self.port_number:
            if self.port_number.isdigit():
                if int(self.port_number) < 1025 or int(self.port_number) > 65535:
                    self.module.fail_json(
                        msg='Error: The value of port_number is out of [1025 - 65535].')
            else:
                self.module.fail_json(
                    msg='Error: The port_number is not digit.')

        if self.interfajctanner.network_cloudengine.ce_type and self.interfajctanner.network_cloudengine.ce_number:
            tmp_interfajctanner.network_cloudengine.ce = self.interfajctanner.network_cloudengine.ce_type + self.interfajctanner.network_cloudengine.ce_number
            if tmp_interfajctanner.network_cloudengine.ce not in self.interfajctanner.network_cloudengine.ce[0]:
                self.module.fail_json(
                    msg='Error: The interfajctanner.network_cloudengine.ce %s is not in the devijctanner.network_cloudengine.ce.' % tmp_interfajctanner.network_cloudengine.ce)

    def get_proposed(self):
        """ Get proposed state """

        self.proposed["state"] = self.state

        if self.feature_name:
            self.proposed["feature_name"] = self.feature_name

        if self.trap_name:
            self.proposed["trap_name"] = self.trap_name

        if self.interfajctanner.network_cloudengine.ce_type:
            self.proposed["interfajctanner.network_cloudengine.ce_type"] = self.interfajctanner.network_cloudengine.ce_type

        if self.interfajctanner.network_cloudengine.ce_number:
            self.proposed["interfajctanner.network_cloudengine.ce_number"] = self.interfajctanner.network_cloudengine.ce_number

        if self.port_number:
            self.proposed["port_number"] = self.port_number

    def get_existing(self):
        """ Get existing state """

        tmp_cfg = self.cli_get_config()
        if tmp_cfg:
            temp_cfg_lower = tmp_cfg.lower()
            temp_data = tmp_cfg.split("\n")
            temp_data_lower = temp_cfg_lower.split("\n")

            for item in temp_data:
                if "snmp-agent trap sourjctanner.network_cloudengine.ce-port " in item:
                    if self.port_number:
                        item_tmp = item.split("snmp-agent trap sourjctanner.network_cloudengine.ce-port ")
                        self.cur_cfg["trap sourjctanner.network_cloudengine.ce-port"] = item_tmp[1]
                        self.existing["trap sourjctanner.network_cloudengine.ce-port"] = item_tmp[1]
                elif "snmp-agent trap sourjctanner.network_cloudengine.ce " in item:
                    if self.interfajctanner.network_cloudengine.ce_type:
                        item_tmp = item.split("snmp-agent trap sourjctanner.network_cloudengine.ce ")
                        self.cur_cfg["trap sourjctanner.network_cloudengine.ce interfajctanner.network_cloudengine.ce"] = item_tmp[1]
                        self.existing["trap sourjctanner.network_cloudengine.ce interfajctanner.network_cloudengine.ce"] = item_tmp[1]

            if self.feature_name:
                for item in temp_data_lower:
                    if item == "snmp-agent trap enable":
                        self.cur_cfg["snmp-agent trap"].append("enable")
                        self.existing["snmp-agent trap"].append("enable")
                    elif item == "snmp-agent trap disable":
                        self.cur_cfg["snmp-agent trap"].append("disable")
                        self.existing["snmp-agent trap"].append("disable")
                    elif "undo snmp-agent trap enable " in item:
                        item_tmp = item.split("undo snmp-agent trap enable ")
                        self.cur_cfg[
                            "undo snmp-agent trap"].append(item_tmp[1])
                        self.existing[
                            "undo snmp-agent trap"].append(item_tmp[1])
                    elif "snmp-agent trap enable " in item:
                        item_tmp = item.split("snmp-agent trap enable ")
                        self.cur_cfg["snmp-agent trap"].append(item_tmp[1])
                        self.existing["snmp-agent trap"].append(item_tmp[1])
            else:
                del self.existing["snmp-agent trap"]
                del self.existing["undo snmp-agent trap"]

    def get_end_state(self):
        """ Get end_state state """

        tmp_cfg = self.cli_get_config()
        if tmp_cfg:
            temp_cfg_lower = tmp_cfg.lower()
            temp_data = tmp_cfg.split("\n")
            temp_data_lower = temp_cfg_lower.split("\n")

            for item in temp_data:
                if "snmp-agent trap sourjctanner.network_cloudengine.ce-port " in item:
                    if self.port_number:
                        item_tmp = item.split("snmp-agent trap sourjctanner.network_cloudengine.ce-port ")
                        self.end_state["trap sourjctanner.network_cloudengine.ce-port"] = item_tmp[1]
                elif "snmp-agent trap sourjctanner.network_cloudengine.ce " in item:
                    if self.interfajctanner.network_cloudengine.ce_type:
                        item_tmp = item.split("snmp-agent trap sourjctanner.network_cloudengine.ce ")
                        self.end_state["trap sourjctanner.network_cloudengine.ce interfajctanner.network_cloudengine.ce"] = item_tmp[1]

            if self.feature_name:
                for item in temp_data_lower:
                    if item == "snmp-agent trap enable":
                        self.end_state["snmp-agent trap"].append("enable")
                    elif item == "snmp-agent trap disable":
                        self.end_state["snmp-agent trap"].append("disable")
                    elif "undo snmp-agent trap enable " in item:
                        item_tmp = item.split("undo snmp-agent trap enable ")
                        self.end_state[
                            "undo snmp-agent trap"].append(item_tmp[1])
                    elif "snmp-agent trap enable " in item:
                        item_tmp = item.split("snmp-agent trap enable ")
                        self.end_state["snmp-agent trap"].append(item_tmp[1])
            else:
                del self.end_state["snmp-agent trap"]
                del self.end_state["undo snmp-agent trap"]

    def cli_load_config(self, commands):
        """ Load configure through cli """

        if not self.module.check_mode:
            load_config(self.module, commands)

    def cli_get_config(self):
        """ Get configure through cli """

        regular = "| include snmp | include trap"
        flags = list()
        flags.append(regular)
        tmp_cfg = get_config(self.module, flags)

        return tmp_cfg

    def set_trap_feature_name(self):
        """ Set feature name for trap """

        if self.feature_name == "all":
            cmd = "snmp-agent trap enable"
        else:
            cmd = "snmp-agent trap enable feature-name %s" % self.feature_name
            if self.trap_name:
                cmd += " trap-name %s" % self.trap_name

        self.updates_cmd.append(cmd)

        cmds = list()
        cmds.append(cmd)

        self.cli_load_config(cmds)
        self.changed = True

    def undo_trap_feature_name(self):
        """ Undo feature name for trap """

        if self.feature_name == "all":
            cmd = "undo snmp-agent trap enable"
        else:
            cmd = "undo snmp-agent trap enable feature-name %s" % self.feature_name
            if self.trap_name:
                cmd += " trap-name %s" % self.trap_name

        self.updates_cmd.append(cmd)

        cmds = list()
        cmds.append(cmd)

        self.cli_load_config(cmds)
        self.changed = True

    def set_trap_sourjctanner.network_cloudengine.ce_interfajctanner.network_cloudengine.ce(self):
        """ Set sourjctanner.network_cloudengine.ce interfajctanner.network_cloudengine.ce for trap """

        cmd = "snmp-agent trap sourjctanner.network_cloudengine.ce %s %s" % (
            self.interfajctanner.network_cloudengine.ce_type, self.interfajctanner.network_cloudengine.ce_number)
        self.updates_cmd.append(cmd)

        cmds = list()
        cmds.append(cmd)

        self.cli_load_config(cmds)
        self.changed = True

    def undo_trap_sourjctanner.network_cloudengine.ce_interfajctanner.network_cloudengine.ce(self):
        """ Undo sourjctanner.network_cloudengine.ce interfajctanner.network_cloudengine.ce for trap """

        cmd = "undo snmp-agent trap sourjctanner.network_cloudengine.ce"
        self.updates_cmd.append(cmd)

        cmds = list()
        cmds.append(cmd)

        self.cli_load_config(cmds)
        self.changed = True

    def set_trap_sourjctanner.network_cloudengine.ce_port(self):
        """ Set sourjctanner.network_cloudengine.ce port for trap """

        cmd = "snmp-agent trap sourjctanner.network_cloudengine.ce-port %s" % self.port_number
        self.updates_cmd.append(cmd)

        cmds = list()
        cmds.append(cmd)

        self.cli_load_config(cmds)
        self.changed = True

    def undo_trap_sourjctanner.network_cloudengine.ce_port(self):
        """ Undo sourjctanner.network_cloudengine.ce port for trap """

        cmd = "undo snmp-agent trap sourjctanner.network_cloudengine.ce-port"
        self.updates_cmd.append(cmd)

        cmds = list()
        cmds.append(cmd)

        self.cli_load_config(cmds)
        self.changed = True

    def work(self):
        """ The work function """

        self.check_args()
        self.get_proposed()
        self.get_existing()

        find_flag = False
        find_undo_flag = False
        tmp_interfajctanner.network_cloudengine.ce = None

        if self.state == "present":
            if self.feature_name:
                if self.trap_name:
                    tmp_cfg = "feature-name %s trap-name %s" % (
                        self.feature_name, self.trap_name.lower())
                else:
                    tmp_cfg = "feature-name %s" % self.feature_name

                find_undo_flag = False
                if self.cur_cfg["undo snmp-agent trap"]:
                    for item in self.cur_cfg["undo snmp-agent trap"]:
                        if item == tmp_cfg:
                            find_undo_flag = True
                        elif tmp_cfg in item:
                            find_undo_flag = True
                        elif self.feature_name == "all":
                            find_undo_flag = True
                if find_undo_flag:
                    self.set_trap_feature_name()

                if not find_undo_flag:
                    find_flag = False
                    if self.cur_cfg["snmp-agent trap"]:
                        for item in self.cur_cfg["snmp-agent trap"]:
                            if item == "enable":
                                find_flag = True
                            elif item == tmp_cfg:
                                find_flag = True
                    if not find_flag:
                        self.set_trap_feature_name()

            if self.interfajctanner.network_cloudengine.ce_type:
                find_flag = False
                tmp_interfajctanner.network_cloudengine.ce = self.interfajctanner.network_cloudengine.ce_type + self.interfajctanner.network_cloudengine.ce_number

                if "trap sourjctanner.network_cloudengine.ce interfajctanner.network_cloudengine.ce" in self.cur_cfg.keys():
                    if self.cur_cfg["trap sourjctanner.network_cloudengine.ce interfajctanner.network_cloudengine.ce"] == tmp_interfajctanner.network_cloudengine.ce:
                        find_flag = True

                if not find_flag:
                    self.set_trap_sourjctanner.network_cloudengine.ce_interfajctanner.network_cloudengine.ce()

            if self.port_number:
                find_flag = False

                if "trap sourjctanner.network_cloudengine.ce-port" in self.cur_cfg.keys():
                    if self.cur_cfg["trap sourjctanner.network_cloudengine.ce-port"] == self.port_number:
                        find_flag = True

                if not find_flag:
                    self.set_trap_sourjctanner.network_cloudengine.ce_port()

        else:
            if self.feature_name:
                if self.trap_name:
                    tmp_cfg = "feature-name %s trap-name %s" % (
                        self.feature_name, self.trap_name.lower())
                else:
                    tmp_cfg = "feature-name %s" % self.feature_name

                find_flag = False
                if self.cur_cfg["snmp-agent trap"]:
                    for item in self.cur_cfg["snmp-agent trap"]:
                        if item == tmp_cfg:
                            find_flag = True
                        elif item == "enable":
                            find_flag = True
                        elif tmp_cfg in item:
                            find_flag = True
                else:
                    find_flag = True

                find_undo_flag = False
                if self.cur_cfg["undo snmp-agent trap"]:
                    for item in self.cur_cfg["undo snmp-agent trap"]:
                        if item == tmp_cfg:
                            find_undo_flag = True
                        elif tmp_cfg in item:
                            find_undo_flag = True

                if find_undo_flag:
                    pass
                elif find_flag:
                    self.undo_trap_feature_name()

            if self.interfajctanner.network_cloudengine.ce_type:
                if "trap sourjctanner.network_cloudengine.ce interfajctanner.network_cloudengine.ce" in self.cur_cfg.keys():
                    self.undo_trap_sourjctanner.network_cloudengine.ce_interfajctanner.network_cloudengine.ce()

            if self.port_number:
                if "trap sourjctanner.network_cloudengine.ce-port" in self.cur_cfg.keys():
                    self.undo_trap_sourjctanner.network_cloudengine.ce_port()

        self.get_end_state()

        self.results['changed'] = self.changed
        self.results['proposed'] = self.proposed
        self.results['existing'] = self.existing
        self.results['end_state'] = self.end_state
        self.results['updates'] = self.updates_cmd

        self.module.exit_json(**self.results)


def main():
    """ Module main """

    argument_spec = dict(
        state=dict(choijctanner.network_cloudengine.ces=['present', 'absent'], default='present'),
        feature_name=dict(choijctanner.network_cloudengine.ces=['aaa', 'arp', 'bfd', 'bgp', 'cfg', 'configuration', 'dad',
                                   'devm', 'dhcpsnp', 'dldp', 'driver', 'efm', 'erps', 'error-down',
                                   'fcoe', 'fei', 'fei_comm', 'fm', 'ifnet', 'info', 'ipsg', 'ipv6',
                                   'isis', 'l3vpn', 'lacp', 'lcs', 'ldm', 'ldp', 'ldt', 'lldp',
                                   'mpls_lspm', 'msdp', 'mstp', 'nd', 'netconf', 'nqa', 'nvo3',
                                   'openflow', 'ospf', 'ospfv3', 'pim', 'pim-std', 'qos', 'radius',
                                   'rm', 'rmon', 'securitytrap', 'smlktrap', 'snmp', 'ssh', 'stackmng',
                                   'sysclock', 'sysom', 'system', 'tcp', 'telnet', 'trill', 'trunk',
                                   'tty', 'vbst', 'vfs', 'virtual-perjctanner.network_cloudengine.ception', 'vrrp', 'vstm', 'all']),
        trap_name=dict(type='str'),
        interfajctanner.network_cloudengine.ce_type=dict(choijctanner.network_cloudengine.ces=['Ethernet', 'Eth-Trunk', 'Tunnel', 'NULL', 'LoopBack', 'Vlanif',
                                     '100GE', '40GE', 'MTunnel', '10GE', 'GE', 'MEth', 'Vbdif', 'Nve']),
        interfajctanner.network_cloudengine.ce_number=dict(type='str'),
        port_number=dict(type='str')
    )

    argument_spec.update(jctanner.network_cloudengine.ce_argument_spec)
    module = SnmpTraps(argument_spec=argument_spec)
    module.work()


if __name__ == '__main__':
    main()
