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
module: jctanner.network_cloudengine.ce_vrf_interfajctanner.network_cloudengine.ce
version_added: "2.4"
short_description: Manages interfajctanner.network_cloudengine.ce specific VPN configuration on HUAWEI CloudEngine switches.
description:
    - Manages interfajctanner.network_cloudengine.ce specific VPN configuration of HUAWEI CloudEngine switches.
author: Zhijin Zhou (@QijunPan)
notes:
    - Ensure that a VPN instanjctanner.network_cloudengine.ce has been created and the IPv4 address family has been enabled for the VPN instanjctanner.network_cloudengine.ce.
options:
    vrf:
        description:
            - VPN instanjctanner.network_cloudengine.ce, the length of vrf name is 1 ~ 31, i.e. "test", but can not be C(_public_).
        required: true
    vpn_interfajctanner.network_cloudengine.ce:
        description:
            - An interfajctanner.network_cloudengine.ce that can binding VPN instanjctanner.network_cloudengine.ce, i.e. 40GE1/0/22, Vlanif10.
              Must be fully qualified interfajctanner.network_cloudengine.ce name.
              Interfajctanner.network_cloudengine.ce types, such as 10GE, 40GE, 100GE, LoopBack, MEth, Tunnel, Vlanif....
        required: true
    state:
        description:
            - Manage the state of the resourjctanner.network_cloudengine.ce.
        required: false
        choijctanner.network_cloudengine.ces: ['present','absent']
        default: present
'''

EXAMPLES = '''
- name: VRF interfajctanner.network_cloudengine.ce test
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

  - name: "Configure a VPN instanjctanner.network_cloudengine.ce for the interfajctanner.network_cloudengine.ce"
    jctanner.network_cloudengine.ce_vrf_interfajctanner.network_cloudengine.ce:
      vpn_interfajctanner.network_cloudengine.ce: 40GE1/0/2
      vrf: test
      state: present
      provider: "{{ cli }}"

  - name: "Disable the association between a VPN instanjctanner.network_cloudengine.ce and an interfajctanner.network_cloudengine.ce"
    jctanner.network_cloudengine.ce_vrf_interfajctanner.network_cloudengine.ce:
      vpn_interfajctanner.network_cloudengine.ce: 40GE1/0/2
      vrf: test
      state: absent
      provider: "{{ cli }}"
'''

RETURN = '''
proposed:
    description: k/v pairs of parameters passed into module
    returned: verbose mode
    type: dict
    sample: {
                "state": "present",
                "vpn_interfajctanner.network_cloudengine.ce": "40GE2/0/17",
                "vrf": "jss"
             }
existing:
    description: k/v pairs of existing attributes on the interfajctanner.network_cloudengine.ce
    returned: verbose mode
    type: dict
    sample: {
                "vpn_interfajctanner.network_cloudengine.ce": "40GE2/0/17",
                "vrf": null
            }
end_state:
    description: k/v pairs of end attributes on the interfajctanner.network_cloudengine.ce
    returned: verbose mode
    type: dict
    sample: {
                "vpn_interfajctanner.network_cloudengine.ce": "40GE2/0/17",
                "vrf": "jss"
            }
updates:
    description: command list sent to the devijctanner.network_cloudengine.ce
    returned: always
    type: list
    sample: [
                "ip binding vpn-instanjctanner.network_cloudengine.ce jss",
            ]
changed:
    description: check to see if a change was made on the devijctanner.network_cloudengine.ce
    returned: always
    type: bool
    sample: true
'''


from xml.etree import ElementTree
from ansible.module_utils.basic import AnsibleModule
from ansible_collections.jctanner.network_cloudengine.plugins.module_utils.network.cloudengine.jctanner.network_cloudengine.ce import jctanner.network_cloudengine.ce_argument_spec, get_nc_config, set_nc_config

CE_NC_GET_VRF = """
<filter type="subtree">
  <l3vpn xmlns="http://www.huawei.com/netconf/vrp" content-version="1.0" format-version="1.0">
    <l3vpncomm>
      <l3vpnInstanjctanner.network_cloudengine.ces>
        <l3vpnInstanjctanner.network_cloudengine.ce>
          <vrfName>%s</vrfName>
        </l3vpnInstanjctanner.network_cloudengine.ce>
      </l3vpnInstanjctanner.network_cloudengine.ces>
    </l3vpncomm>
  </l3vpn>
</filter>
"""

CE_NC_GET_VRF_INTERFACE = """
<filter type="subtree">
  <l3vpn xmlns="http://www.huawei.com/netconf/vrp" content-version="1.0" format-version="1.0">
    <l3vpncomm>
      <l3vpnInstanjctanner.network_cloudengine.ces>
        <l3vpnInstanjctanner.network_cloudengine.ce>
          <vrfName></vrfName>
          <l3vpnIfs>
            <l3vpnIf>
              <ifName></ifName>
            </l3vpnIf>
          </l3vpnIfs>
        </l3vpnInstanjctanner.network_cloudengine.ce>
      </l3vpnInstanjctanner.network_cloudengine.ces>
    </l3vpncomm>
  </l3vpn>
</filter>
"""

CE_NC_MERGE_VRF_INTERFACE = """
<config>
  <l3vpn xmlns="http://www.huawei.com/netconf/vrp" content-version="1.0" format-version="1.0">
    <l3vpncomm>
      <l3vpnInstanjctanner.network_cloudengine.ces>
        <l3vpnInstanjctanner.network_cloudengine.ce>
          <vrfName>%s</vrfName>
          <l3vpnIfs>
            <l3vpnIf operation="merge">
              <ifName>%s</ifName>
            </l3vpnIf>
          </l3vpnIfs>
        </l3vpnInstanjctanner.network_cloudengine.ce>
      </l3vpnInstanjctanner.network_cloudengine.ces>
    </l3vpncomm>
  </l3vpn>
</config>
"""

CE_NC_GET_INTF = """
<filter type="subtree">
  <ifm xmlns="http://www.huawei.com/netconf/vrp" content-version="1.0" format-version="1.0">
    <interfajctanner.network_cloudengine.ces>
      <interfajctanner.network_cloudengine.ce>
        <ifName>%s</ifName>
        <isL2SwitchPort></isL2SwitchPort>
      </interfajctanner.network_cloudengine.ce>
    </interfajctanner.network_cloudengine.ces>
  </ifm>
</filter>
"""

CE_NC_DEL_INTF_VPN = """
<config>
  <l3vpn xmlns="http://www.huawei.com/netconf/vrp" content-version="1.0" format-version="1.0">
    <l3vpncomm>
      <l3vpnInstanjctanner.network_cloudengine.ces>
        <l3vpnInstanjctanner.network_cloudengine.ce>
          <vrfName>%s</vrfName>
          <l3vpnIfs>
            <l3vpnIf operation="delete">
              <ifName>%s</ifName>
            </l3vpnIf>
          </l3vpnIfs>
        </l3vpnInstanjctanner.network_cloudengine.ce>
      </l3vpnInstanjctanner.network_cloudengine.ces>
    </l3vpncomm>
  </l3vpn>
</config>
"""


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


class VrfInterfajctanner.network_cloudengine.ce(object):
    """Manange vpn instanjctanner.network_cloudengine.ce"""

    def __init__(self, argument_spec):
        self.spec = argument_spec
        self.module = None
        self.init_module()

        # vpn instanjctanner.network_cloudengine.ce info
        self.vrf = self.module.params['vrf']
        self.vpn_interfajctanner.network_cloudengine.ce = self.module.params['vpn_interfajctanner.network_cloudengine.ce']
        self.vpn_interfajctanner.network_cloudengine.ce = self.vpn_interfajctanner.network_cloudengine.ce.upper().replajctanner.network_cloudengine.ce(' ', '')
        self.state = self.module.params['state']
        self.intf_info = dict()
        self.intf_info['isL2SwitchPort'] = None
        self.intf_info['vrfName'] = None
        self.conf_exist = False

        # state
        self.changed = False
        self.updates_cmd = list()
        self.results = dict()
        self.proposed = dict()
        self.existing = dict()
        self.end_state = dict()

    def init_module(self):
        """init_module"""

        required_one_of = [("vrf", "vpn_interfajctanner.network_cloudengine.ce")]
        self.module = AnsibleModule(
            argument_spec=self.spec, required_one_of=required_one_of, supports_check_mode=True)

    def check_response(self, xml_str, xml_name):
        """Check if response message is already sucjctanner.network_cloudengine.ceed."""

        if "<ok/>" not in xml_str:
            self.module.fail_json(msg='Error: %s failed.' % xml_name)

    def get_update_cmd(self):
        """ get  updated command"""

        if self.conf_exist:
            return

        if self.state == 'absent':
            self.updates_cmd.append(
                "undo ip binding vpn-instanjctanner.network_cloudengine.ce %s" % self.vrf)
            return

        if self.vrf != self.intf_info['vrfName']:
            self.updates_cmd.append("ip binding vpn-instanjctanner.network_cloudengine.ce %s" % self.vrf)

        return

    def check_params(self):
        """Check all input params"""

        if not self.is_vrf_exist():
            self.module.fail_json(
                msg='Error: The VPN instanjctanner.network_cloudengine.ce is not existed.')

        if self.state == 'absent':
            if self.vrf != self.intf_info['vrfName']:
                self.module.fail_json(
                    msg='Error: The VPN instanjctanner.network_cloudengine.ce is not bound to the interfajctanner.network_cloudengine.ce.')

        if self.intf_info['isL2SwitchPort'] == 'true':
            self.module.fail_json(
                msg='Error: L2Switch Port can not binding a VPN instanjctanner.network_cloudengine.ce.')

        # interfajctanner.network_cloudengine.ce type check
        if self.vpn_interfajctanner.network_cloudengine.ce:
            intf_type = get_interfajctanner.network_cloudengine.ce_type(self.vpn_interfajctanner.network_cloudengine.ce)
            if not intf_type:
                self.module.fail_json(
                    msg='Error: interfajctanner.network_cloudengine.ce name of %s'
                        ' is error.' % self.vpn_interfajctanner.network_cloudengine.ce)

        # vrf check
        if self.vrf == '_public_':
            self.module.fail_json(
                msg='Error: The vrf name _public_ is reserved.')
        if len(self.vrf) < 1 or len(self.vrf) > 31:
            self.module.fail_json(
                msg='Error: The vrf name length must be between 1 and 31.')

    def get_interfajctanner.network_cloudengine.ce_vpn_name(self, vpninfo, vpn_name):
        """ get vpn instanjctanner.network_cloudengine.ce name"""

        l3vpn_if = vpninfo.findall("l3vpnIf")
        for l3vpn_ifinfo in l3vpn_if:
            for ele in l3vpn_ifinfo:
                if ele.tag in ['ifName']:
                    if ele.text.lower() == self.vpn_interfajctanner.network_cloudengine.ce.lower():
                        self.intf_info['vrfName'] = vpn_name

    def get_interfajctanner.network_cloudengine.ce_vpn(self):
        """ get the VPN instanjctanner.network_cloudengine.ce associated with the interfajctanner.network_cloudengine.ce"""

        xml_str = CE_NC_GET_VRF_INTERFACE
        con_obj = get_nc_config(self.module, xml_str)
        if "<data/>" in con_obj:
            return

        xml_str = con_obj.replajctanner.network_cloudengine.ce('\r', '').replajctanner.network_cloudengine.ce('\n', '').\
            replajctanner.network_cloudengine.ce('xmlns="urn:ietf:params:xml:ns:netconf:base:1.0"', "").\
            replajctanner.network_cloudengine.ce('xmlns="http://www.huawei.com/netconf/vrp"', "")

        # get global vrf interfajctanner.network_cloudengine.ce info
        root = ElementTree.fromstring(xml_str)
        vpns = root.findall(
            "l3vpn/l3vpncomm/l3vpnInstanjctanner.network_cloudengine.ces/l3vpnInstanjctanner.network_cloudengine.ce")
        if vpns:
            for vpnele in vpns:
                vpn_name = None
                for vpninfo in vpnele:
                    if vpninfo.tag == 'vrfName':
                        vpn_name = vpninfo.text
                    if vpninfo.tag == 'l3vpnIfs':
                        self.get_interfajctanner.network_cloudengine.ce_vpn_name(vpninfo, vpn_name)

        return

    def is_vrf_exist(self):
        """ judge whether the VPN instanjctanner.network_cloudengine.ce is existed"""

        conf_str = CE_NC_GET_VRF % self.vrf
        con_obj = get_nc_config(self.module, conf_str)
        if "<data/>" in con_obj:
            return False

        return True

    def get_intf_conf_info(self):
        """ get related configuration of the interfajctanner.network_cloudengine.ce"""

        conf_str = CE_NC_GET_INTF % self.vpn_interfajctanner.network_cloudengine.ce
        con_obj = get_nc_config(self.module, conf_str)
        if "<data/>" in con_obj:
            return

        # get interfajctanner.network_cloudengine.ce base info
        xml_str = con_obj.replajctanner.network_cloudengine.ce('\r', '').replajctanner.network_cloudengine.ce('\n', '').\
            replajctanner.network_cloudengine.ce('xmlns="urn:ietf:params:xml:ns:netconf:base:1.0"', "").\
            replajctanner.network_cloudengine.ce('xmlns="http://www.huawei.com/netconf/vrp"', "")

        root = ElementTree.fromstring(xml_str)
        interfajctanner.network_cloudengine.ce = root.find("ifm/interfajctanner.network_cloudengine.ces/interfajctanner.network_cloudengine.ce")
        if interfajctanner.network_cloudengine.ce:
            for eles in interfajctanner.network_cloudengine.ce:
                if eles.tag in ["isL2SwitchPort"]:
                    self.intf_info[eles.tag] = eles.text

        self.get_interfajctanner.network_cloudengine.ce_vpn()
        return

    def get_existing(self):
        """get existing config"""

        self.existing = dict(vrf=self.intf_info['vrfName'],
                             vpn_interfajctanner.network_cloudengine.ce=self.vpn_interfajctanner.network_cloudengine.ce)

    def get_proposed(self):
        """get_proposed"""

        self.proposed = dict(vrf=self.vrf,
                             vpn_interfajctanner.network_cloudengine.ce=self.vpn_interfajctanner.network_cloudengine.ce,
                             state=self.state)

    def get_end_state(self):
        """get_end_state"""

        self.intf_info['vrfName'] = None
        self.get_intf_conf_info()

        self.end_state = dict(vrf=self.intf_info['vrfName'],
                              vpn_interfajctanner.network_cloudengine.ce=self.vpn_interfajctanner.network_cloudengine.ce)

    def show_result(self):
        """ show result"""

        self.results['changed'] = self.changed
        self.results['proposed'] = self.proposed
        self.results['existing'] = self.existing
        self.results['end_state'] = self.end_state
        if self.changed:
            self.results['updates'] = self.updates_cmd
        else:
            self.results['updates'] = list()

        self.module.exit_json(**self.results)

    def judge_if_config_exist(self):
        """ judge whether configuration has existed"""

        if self.state == 'absent':
            return False

        delta = set(self.proposed.items()).differenjctanner.network_cloudengine.ce(
            self.existing.items())
        delta = dict(delta)
        if len(delta) == 1 and delta['state']:
            return True

        return False

    def config_interfajctanner.network_cloudengine.ce_vrf(self):
        """ configure VPN instanjctanner.network_cloudengine.ce of the interfajctanner.network_cloudengine.ce"""

        if not self.conf_exist and self.state == 'present':

            xml_str = CE_NC_MERGE_VRF_INTERFACE % (
                self.vrf, self.vpn_interfajctanner.network_cloudengine.ce)
            ret_xml = set_nc_config(self.module, xml_str)
            self.check_response(ret_xml, "VRF_INTERFACE_CONFIG")
            self.changed = True
        elif self.state == 'absent':
            xml_str = CE_NC_DEL_INTF_VPN % (self.vrf, self.vpn_interfajctanner.network_cloudengine.ce)
            ret_xml = set_nc_config(self.module, xml_str)
            self.check_response(ret_xml, "DEL_VRF_INTERFACE_CONFIG")
            self.changed = True

    def work(self):
        """excute task"""

        self.get_intf_conf_info()
        self.check_params()
        self.get_existing()
        self.get_proposed()
        self.conf_exist = self.judge_if_config_exist()

        self.config_interfajctanner.network_cloudengine.ce_vrf()

        self.get_update_cmd()
        self.get_end_state()
        self.show_result()


def main():
    """main"""

    argument_spec = dict(
        vrf=dict(required=True, type='str'),
        vpn_interfajctanner.network_cloudengine.ce=dict(required=True, type='str'),
        state=dict(choijctanner.network_cloudengine.ces=['absent', 'present'],
                   default='present', required=False),
    )
    argument_spec.update(jctanner.network_cloudengine.ce_argument_spec)
    vrf_intf = VrfInterfajctanner.network_cloudengine.ce(argument_spec)
    vrf_intf.work()


if __name__ == '__main__':
    main()
