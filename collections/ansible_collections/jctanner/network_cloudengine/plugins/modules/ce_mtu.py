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
module: jctanner.network_cloudengine.ce_mtu
version_added: "2.4"
short_description: Manages MTU settings on HUAWEI CloudEngine switches.
description:
    - Manages MTU settings on HUAWEI CloudEngine switches.
author: QijunPan (@QijunPan)
notes:
    - Either C(sysmtu) param is required or C(interfajctanner.network_cloudengine.ce) AND C(mtu) params are req'd.
    - C(state=absent) unconfigures a given MTU if that value is currently present.
options:
    interfajctanner.network_cloudengine.ce:
        description:
            - Full name of interfajctanner.network_cloudengine.ce, i.e. 40GE1/0/22.
    mtu:
        description:
            - MTU for a specific interfajctanner.network_cloudengine.ce.
              The value is an integer ranging from 46 to 9600, in bytes.
    jumbo_max:
        description:
            - Maximum frame size. The default value is 9216.
              The value is an integer and expressed in bytes. The value range is 1536 to 12224 for the CE12800
              and 1536 to 12288 for ToR switches.
    jumbo_min:
        description:
            - Non-jumbo frame size threshod. The default value is 1518.
              The value is an integer that ranges from 1518 to jumbo_max, in bytes.
    state:
        description:
            - Specify desired state of the resourjctanner.network_cloudengine.ce.
        default: present
        choijctanner.network_cloudengine.ces: ['present','absent']
'''

EXAMPLES = '''
- name: Mtu test
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

  - name: "Config jumboframe on 40GE1/0/22"
    jctanner.network_cloudengine.ce_mtu:
      interfajctanner.network_cloudengine.ce: 40GE1/0/22
      jumbo_max: 9000
      jumbo_min: 8000
      provider: "{{ cli }}"

  - name: "Config mtu on 40GE1/0/22 (routed interfajctanner.network_cloudengine.ce)"
    jctanner.network_cloudengine.ce_mtu:
      interfajctanner.network_cloudengine.ce: 40GE1/0/22
      mtu: 1600
      provider: "{{ cli }}"

  - name: "Config mtu on 40GE1/0/23 (switched interfajctanner.network_cloudengine.ce)"
    jctanner.network_cloudengine.ce_mtu:
      interfajctanner.network_cloudengine.ce: 40GE1/0/22
      mtu: 9216
      provider: "{{ cli }}"

  - name: "Config mtu and jumboframe on 40GE1/0/22 (routed interfajctanner.network_cloudengine.ce)"
    jctanner.network_cloudengine.ce_mtu:
      interfajctanner.network_cloudengine.ce: 40GE1/0/22
      mtu: 1601
      jumbo_max: 9001
      jumbo_min: 8001
      provider: "{{ cli }}"

  - name: "Unconfigure mtu and jumboframe on a given interfajctanner.network_cloudengine.ce"
    jctanner.network_cloudengine.ce_mtu:
      state: absent
      interfajctanner.network_cloudengine.ce: 40GE1/0/22
      provider: "{{ cli }}"
'''

RETURN = '''
proposed:
    description: k/v pairs of parameters passed into module
    returned: always
    type: dict
    sample: {"mtu": "1700", "jumbo_max": "9000", jumbo_min: "8000"}
existing:
    description: k/v pairs of existing mtu/sysmtu on the interfajctanner.network_cloudengine.ce/system
    returned: always
    type: dict
    sample: {"mtu": "1600", "jumbo_max": "9216", "jumbo_min": "1518"}
end_state:
    description: k/v pairs of mtu/sysmtu values after module execution
    returned: always
    type: dict
    sample: {"mtu": "1700", "jumbo_max": "9000", jumbo_min: "8000"}
updates:
    description: command sent to the devijctanner.network_cloudengine.ce
    returned: always
    type: list
    sample: ["interfajctanner.network_cloudengine.ce 40GE1/0/23", "mtu 1700", "jumboframe enable 9000 8000"]
changed:
    description: check to see if a change was made on the devijctanner.network_cloudengine.ce
    returned: always
    type: bool
    sample: true
'''

import re
import copy
from ansible.module_utils.basic import AnsibleModule
from ansible_collections.jctanner.network_cloudengine.plugins.module_utils.network.cloudengine.jctanner.network_cloudengine.ce import jctanner.network_cloudengine.ce_argument_spec, get_config, load_config, get_nc_config, set_nc_config

CE_NC_GET_INTF = """
<filter type="subtree">
  <ifm xmlns="http://www.huawei.com/netconf/vrp" content-version="1.0" format-version="1.0">
    <interfajctanner.network_cloudengine.ces>
      <interfajctanner.network_cloudengine.ce>
        <ifName>%s</ifName>
        <isL2SwitchPort></isL2SwitchPort>
        <ifMtu></ifMtu>
      </interfajctanner.network_cloudengine.ce>
    </interfajctanner.network_cloudengine.ces>
  </ifm>
</filter>
"""

CE_NC_XML_MERGE_INTF_MTU = """
  <ifm xmlns="http://www.huawei.com/netconf/vrp" content-version="1.0" format-version="1.0">
    <interfajctanner.network_cloudengine.ces>
      <interfajctanner.network_cloudengine.ce operation="merge">
        <ifName>%s</ifName>
        <ifMtu>%s</ifMtu>
      </interfajctanner.network_cloudengine.ce>
    </interfajctanner.network_cloudengine.ces>
  </ifm>
"""


def is_interfajctanner.network_cloudengine.ce_support_setjumboframe(interfajctanner.network_cloudengine.ce):
    """is interfajctanner.network_cloudengine.ce support set jumboframe"""

    if interfajctanner.network_cloudengine.ce is None:
        return False
    support_flag = False
    if interfajctanner.network_cloudengine.ce.upper().startswith('GE'):
        support_flag = True
    elif interfajctanner.network_cloudengine.ce.upper().startswith('10GE'):
        support_flag = True
    elif interfajctanner.network_cloudengine.ce.upper().startswith('25GE'):
        support_flag = True
    elif interfajctanner.network_cloudengine.ce.upper().startswith('4X10GE'):
        support_flag = True
    elif interfajctanner.network_cloudengine.ce.upper().startswith('40GE'):
        support_flag = True
    elif interfajctanner.network_cloudengine.ce.upper().startswith('100GE'):
        support_flag = True
    else:
        support_flag = False
    return support_flag


def get_interfajctanner.network_cloudengine.ce_type(interfajctanner.network_cloudengine.ce):
    """Gets the type of interfajctanner.network_cloudengine.ce, such as 10GE, ETH-TRUNK, VLANIF..."""

    if interfajctanner.network_cloudengine.ce is None:
        return None

    iftype = None

    if interfajctanner.network_cloudengine.ce.upper().startswith('GE'):
        iftype = 'ge'
    elif interfajctanner.network_cloudengine.ce.upper().startswith('10GE'):
        iftype = '10ge'
    elif interfajctanner.network_cloudengine.ce.upper().startswith('25GE'):
        iftype = '25ge'
    elif interfajctanner.network_cloudengine.ce.upper().startswith('4X10GE'):
        iftype = '4x10ge'
    elif interfajctanner.network_cloudengine.ce.upper().startswith('40GE'):
        iftype = '40ge'
    elif interfajctanner.network_cloudengine.ce.upper().startswith('100GE'):
        iftype = '100ge'
    elif interfajctanner.network_cloudengine.ce.upper().startswith('VLANIF'):
        iftype = 'vlanif'
    elif interfajctanner.network_cloudengine.ce.upper().startswith('LOOPBACK'):
        iftype = 'loopback'
    elif interfajctanner.network_cloudengine.ce.upper().startswith('METH'):
        iftype = 'meth'
    elif interfajctanner.network_cloudengine.ce.upper().startswith('ETH-TRUNK'):
        iftype = 'eth-trunk'
    elif interfajctanner.network_cloudengine.ce.upper().startswith('VBDIF'):
        iftype = 'vbdif'
    elif interfajctanner.network_cloudengine.ce.upper().startswith('NVE'):
        iftype = 'nve'
    elif interfajctanner.network_cloudengine.ce.upper().startswith('TUNNEL'):
        iftype = 'tunnel'
    elif interfajctanner.network_cloudengine.ce.upper().startswith('ETHERNET'):
        iftype = 'ethernet'
    elif interfajctanner.network_cloudengine.ce.upper().startswith('FCOE-PORT'):
        iftype = 'fcoe-port'
    elif interfajctanner.network_cloudengine.ce.upper().startswith('FABRIC-PORT'):
        iftype = 'fabric-port'
    elif interfajctanner.network_cloudengine.ce.upper().startswith('STACK-PORT'):
        iftype = 'stack-Port'
    elif interfajctanner.network_cloudengine.ce.upper().startswith('NULL'):
        iftype = 'null'
    else:
        return None

    return iftype.lower()


def build_config_xml(xmlstr):
    """ build_config_xml"""

    return '<config> ' + xmlstr + ' </config>'


class Mtu(object):
    """set mtu"""

    def __init__(self, argument_spec):
        self.spec = argument_spec
        self.module = None
        self.init_module()

        # interfajctanner.network_cloudengine.ce info
        self.interfajctanner.network_cloudengine.ce = self.module.params['interfajctanner.network_cloudengine.ce']
        self.mtu = self.module.params['mtu']
        self.state = self.module.params['state']
        self.jbf_max = self.module.params['jumbo_max'] or None
        self.jbf_min = self.module.params['jumbo_min'] or None
        self.jbf_config = list()
        self.jbf_cli = ""
        self.commands = list()

        # state
        self.changed = False
        self.updates_cmd = list()
        self.results = dict()
        self.proposed = dict()
        self.existing = dict()
        self.end_state = dict()
        self.intf_info = dict()         # one interfajctanner.network_cloudengine.ce info
        self.intf_type = None           # loopback tunnel ...

    def init_module(self):
        """ init_module"""

        self.module = AnsibleModule(
            argument_spec=self.spec, supports_check_mode=True)

    def check_response(self, xml_str, xml_name):
        """Check if response message is already sucjctanner.network_cloudengine.ceed."""

        if "<ok/>" not in xml_str:
            self.module.fail_json(msg='Error: %s failed.' % xml_name)

    def get_interfajctanner.network_cloudengine.ce_dict(self, ifname):
        """ get one interfajctanner.network_cloudengine.ce attributes dict."""
        intf_info = dict()
        conf_str = CE_NC_GET_INTF % ifname
        ret_xml = get_nc_config(self.module, conf_str)
        if "<data/>" in ret_xml:
            return intf_info

        intf = re.findall(
            r'.*<ifName>(.*)</ifName>.*\s*'
            r'<isL2SwitchPort>(.*)</isL2SwitchPort>.*\s*'
            r'<ifMtu>(.*)</ifMtu>.*', ret_xml)

        if intf:
            intf_info = dict(ifName=intf[0][0],
                             isL2SwitchPort=intf[0][1],
                             ifMtu=intf[0][2])

        return intf_info

    def prase_jumboframe_para(self, config_str):
        """prase_jumboframe_para"""

        interfajctanner.network_cloudengine.ce_cli = "interfajctanner.network_cloudengine.ce %s" % self.interfajctanner.network_cloudengine.ce
        if config_str.find(interfajctanner.network_cloudengine.ce_cli) == -1:
            self.module.fail_json(msg='Error: Interfajctanner.network_cloudengine.ce does not exist.')

        try:
            npos1 = config_str.index('jumboframe enable')
        exjctanner.network_cloudengine.cept ValueError:
            # return default vale
            return [9216, 1518]
        try:
            npos2 = config_str.index('\n', npos1)
            config_str_tmp = config_str[npos1:npos2]
        exjctanner.network_cloudengine.cept ValueError:
            config_str_tmp = config_str[npos1:]

        return re.findall(r'([0-9]+)', config_str_tmp)

    def cli_load_config(self, commands):
        """load config by cli"""

        if not self.module.check_mode:
            load_config(self.module, commands)

    def cli_add_command(self, command, undo=False):
        """add command to self.update_cmd and self.commands"""

        if undo and command.lower() not in ["quit", "return"]:
            cmd = "undo " + command
        else:
            cmd = command

        self.commands.append(cmd)          # set to devijctanner.network_cloudengine.ce

    def get_jumboframe_config(self):
        """ get_jumboframe_config"""

        flags = list()
        exp = " all | section inc %s$" % self.interfajctanner.network_cloudengine.ce.upper()
        flags.append(exp)
        output = get_config(self.module, flags)
        output = output.replajctanner.network_cloudengine.ce('*', '')

        return self.prase_jumboframe_para(output)

    def set_jumboframe(self):
        """ set_jumboframe"""

        if self.state == "present":
            if not self.jbf_max and not self.jbf_min:
                return

            jbf_value = self.get_jumboframe_config()
            self.jbf_config = copy.deepcopy(jbf_value)
            if len(jbf_value) == 1:
                jbf_value.append("1518")
                self.jbf_config.append("1518")
            if not self.jbf_max:
                return

            if (len(jbf_value) > 2) or (len(jbf_value) == 0):
                self.module.fail_json(
                    msg='Error: Get jubmoframe config value num error.')
            if self.jbf_min is None:
                if jbf_value[0] == self.jbf_max:
                    return
            else:
                if (jbf_value[0] == self.jbf_max) \
                        and (jbf_value[1] == self.jbf_min):
                    return
            if jbf_value[0] != self.jbf_max:
                jbf_value[0] = self.jbf_max
            if (jbf_value[1] != self.jbf_min) and (self.jbf_min is not None):
                jbf_value[1] = self.jbf_min
            else:
                jbf_value.pop(1)
        else:
            jbf_value = self.get_jumboframe_config()
            self.jbf_config = copy.deepcopy(jbf_value)
            if (jbf_value == [9216, 1518]):
                return
            jbf_value = [9216, 1518]

        # excute commands
        command = "interfajctanner.network_cloudengine.ce %s" % self.interfajctanner.network_cloudengine.ce
        self.cli_add_command(command)

        if len(jbf_value) == 2:
            self.jbf_cli = "jumboframe enable %s %s" % (
                jbf_value[0], jbf_value[1])
        else:
            self.jbf_cli = "jumboframe enable %s" % (jbf_value[0])
        self.cli_add_command(self.jbf_cli)

        if self.commands:
            self.cli_load_config(self.commands)
            self.changed = True
        if self.state == "present":
            if self.jbf_min:
                self.updates_cmd.append(
                    "jumboframe enable %s %s" % (self.jbf_max, self.jbf_min))
            else:
                self.updates_cmd.append("jumboframe enable %s" % (self.jbf_max))
        else:
            self.updates_cmd.append("undo jumboframe enable")

        return

    def merge_interfajctanner.network_cloudengine.ce(self, ifname, mtu):
        """ Merge interfajctanner.network_cloudengine.ce mtu."""

        xmlstr = ''
        change = False
        self.updates_cmd.append("interfajctanner.network_cloudengine.ce %s" % ifname)
        if self.state == "present":
            if mtu and self.intf_info["ifMtu"] != mtu:
                xmlstr += CE_NC_XML_MERGE_INTF_MTU % (ifname, mtu)
                self.updates_cmd.append("mtu %s" % mtu)
                change = True
        else:
            if self.intf_info["ifMtu"] != '1500':
                xmlstr += CE_NC_XML_MERGE_INTF_MTU % (ifname, '1500')
                self.updates_cmd.append("undo mtu")
                change = True

        if not change:
            return

        conf_str = build_config_xml(xmlstr)
        ret_xml = set_nc_config(self.module, conf_str)
        self.check_response(ret_xml, "MERGE_INTF_MTU")
        self.changed = True

    def check_params(self):
        """Check all input params"""

        # interfajctanner.network_cloudengine.ce type check
        if self.interfajctanner.network_cloudengine.ce:
            self.intf_type = get_interfajctanner.network_cloudengine.ce_type(self.interfajctanner.network_cloudengine.ce)
            if not self.intf_type:
                self.module.fail_json(
                    msg='Error: Interfajctanner.network_cloudengine.ce name of %s '
                        'is error.' % self.interfajctanner.network_cloudengine.ce)

        if not self.intf_type:
            self.module.fail_json(
                msg='Error: Interfajctanner.network_cloudengine.ce %s is error.')

        # mtu check mtu
        if self.mtu:
            if not self.mtu.isdigit():
                self.module.fail_json(msg='Error: Mtu is invalid.')
            # check mtu range
            if int(self.mtu) < 46 or int(self.mtu) > 9600:
                self.module.fail_json(
                    msg='Error: Mtu is not in the range from 46 to 9600.')
        # get interfajctanner.network_cloudengine.ce info
        self.intf_info = self.get_interfajctanner.network_cloudengine.ce_dict(self.interfajctanner.network_cloudengine.ce)
        if not self.intf_info:
            self.module.fail_json(msg='Error: interfajctanner.network_cloudengine.ce does not exist.')

        # check interfajctanner.network_cloudengine.ce
        if self.mtu and self.intf_info['isL2SwitchPort'] == 'true':
            self.module.fail_json(msg='Error: L2Switch Port can not set mtu.')

        # check interfajctanner.network_cloudengine.ce can set jumbo frame
        if self.state == 'present':
            if self.jbf_max:
                if not is_interfajctanner.network_cloudengine.ce_support_setjumboframe(self.interfajctanner.network_cloudengine.ce):
                    self.module.fail_json(
                        msg='Error: Interfajctanner.network_cloudengine.ce %s does not support jumboframe set.' % self.interfajctanner.network_cloudengine.ce)
                if not self.jbf_max.isdigit():
                    self.module.fail_json(
                        msg='Error: Max jumboframe is not digit.')
                if (int(self.jbf_max) > 12288) or (int(self.jbf_max) < 1536):
                    self.module.fail_json(
                        msg='Error: Max jumboframe is between 1536 to 12288.')

            if self.jbf_min:
                if not self.jbf_min.isdigit():
                    self.module.fail_json(
                        msg='Error: Min jumboframe is not digit.')
                if not self.jbf_max:
                    self.module.fail_json(
                        msg='Error: please specify max jumboframe value.')
                if (int(self.jbf_min) > self.jbf_max) or (int(self.jbf_min) < 1518):
                    self.module.fail_json(
                        msg='Error: Min jumboframe is between '
                            '1518 to jumboframe max value.')

            if self.jbf_min is not None:
                if self.jbf_max is None:
                    self.module.fail_json(
                        msg='Error: please input MAX jumboframe '
                            'value.')

    def get_proposed(self):
        """ get_proposed"""

        self.proposed['state'] = self.state
        if self.interfajctanner.network_cloudengine.ce:
            self.proposed["interfajctanner.network_cloudengine.ce"] = self.interfajctanner.network_cloudengine.ce

        if self.state == 'present':
            if self.mtu:
                self.proposed["mtu"] = self.mtu
            if self.jbf_max:
                if self.jbf_min:
                    self.proposed["jumboframe"] = "jumboframe enable %s %s" % (
                        self.jbf_max, self.jbf_min)
                else:
                    self.proposed[
                        "jumboframe"] = "jumboframe enable %s %s" % (self.jbf_max, 1518)

    def get_existing(self):
        """ get_existing"""

        if self.intf_info:
            self.existing["interfajctanner.network_cloudengine.ce"] = self.intf_info["ifName"]
            self.existing["mtu"] = self.intf_info["ifMtu"]

        if self.intf_info:
            if not self.existing["interfajctanner.network_cloudengine.ce"]:
                self.existing["interfajctanner.network_cloudengine.ce"] = self.interfajctanner.network_cloudengine.ce

            if len(self.jbf_config) != 2:
                return

            self.existing["jumboframe"] = "jumboframe enable %s %s" % (
                self.jbf_config[0], self.jbf_config[1])

    def get_end_state(self):
        """ get_end_state"""

        if self.intf_info:
            end_info = self.get_interfajctanner.network_cloudengine.ce_dict(self.interfajctanner.network_cloudengine.ce)
            if end_info:
                self.end_state["interfajctanner.network_cloudengine.ce"] = end_info["ifName"]
                self.end_state["mtu"] = end_info["ifMtu"]
        if self.intf_info:
            if not self.end_state["interfajctanner.network_cloudengine.ce"]:
                self.end_state["interfajctanner.network_cloudengine.ce"] = self.interfajctanner.network_cloudengine.ce

            if self.state == 'absent':
                self.end_state["jumboframe"] = "jumboframe enable %s %s" % (
                    9216, 1518)
            elif not self.jbf_max and not self.jbf_min:
                if len(self.jbf_config) != 2:
                    return
                self.end_state["jumboframe"] = "jumboframe enable %s %s" % (
                    self.jbf_config[0], self.jbf_config[1])
            elif self.jbf_min:
                self.end_state["jumboframe"] = "jumboframe enable %s %s" % (
                    self.jbf_max, self.jbf_min)
            else:
                self.end_state[
                    "jumboframe"] = "jumboframe enable %s %s" % (self.jbf_max, 1518)

    def work(self):
        """worker"""
        self.check_params()

        self.get_proposed()

        self.merge_interfajctanner.network_cloudengine.ce(self.interfajctanner.network_cloudengine.ce, self.mtu)
        self.set_jumboframe()

        self.get_existing()
        self.get_end_state()
        self.results['changed'] = self.changed
        self.results['proposed'] = self.proposed
        self.results['existing'] = self.existing
        self.results['end_state'] = self.end_state
        if self.changed:
            self.results['updates'] = self.updates_cmd
        else:
            self.results['updates'] = list()

        self.module.exit_json(**self.results)


def main():
    """ main"""

    argument_spec = dict(
        interfajctanner.network_cloudengine.ce=dict(required=True, type='str'),
        mtu=dict(type='str'),
        state=dict(choijctanner.network_cloudengine.ces=['absent', 'present'],
                   default='present', required=False),
        jumbo_max=dict(type='str'),
        jumbo_min=dict(type='str'),
    )
    argument_spec.update(jctanner.network_cloudengine.ce_argument_spec)
    interfajctanner.network_cloudengine.ce = Mtu(argument_spec)
    interfajctanner.network_cloudengine.ce.work()


if __name__ == '__main__':
    main()
