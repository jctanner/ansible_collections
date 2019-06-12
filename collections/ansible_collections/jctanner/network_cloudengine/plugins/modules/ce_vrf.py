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
module: jctanner.network_cloudengine.ce_vrf
version_added: "2.4"
short_description: Manages VPN instanjctanner.network_cloudengine.ce on HUAWEI CloudEngine switches.
description:
    - Manages VPN instanjctanner.network_cloudengine.ce of HUAWEI CloudEngine switches.
author: Yang yang (@QijunPan)
notes:
    - If I(state=absent), the route will be removed, regardless of the
      non-required options.
options:
    vrf:
        description:
            - VPN instanjctanner.network_cloudengine.ce, the length of vrf name is 1 - 31, i.e. "test", but can not be C(_public_).
        required: true
    description:
        description:
            - Description of the vrf, the string length is 1 - 242 .
    state:
        description:
            - Manage the state of the resourjctanner.network_cloudengine.ce.
        choijctanner.network_cloudengine.ces: ['present','absent']
        default: present
'''

EXAMPLES = '''
- name: vrf module test
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

  - name: Config a vpn install named vpna, description is test
    jctanner.network_cloudengine.ce_vrf:
      vrf: vpna
      description: test
      state: present
      provider: "{{ cli }}"
  - name: Delete a vpn install named vpna
    jctanner.network_cloudengine.ce_vrf:
      vrf: vpna
      state: absent
      provider: "{{ cli }}"
'''
RETURN = '''
proposed:
    description: k/v pairs of parameters passed into module
    returned: always
    type: dict
    sample: {"vrf": "vpna",
             "description": "test",
             "state": "present"}
existing:
    description: k/v pairs of existing switchport
    returned: always
    type: dict
    sample:  {}
end_state:
    description: k/v pairs of switchport after module execution
    returned: always
    type: dict
    sample:  {"vrf": "vpna",
              "description": "test",
              "present": "present"}
updates:
    description: command list sent to the devijctanner.network_cloudengine.ce
    returned: always
    type: list
    sample: ["ip vpn-instanjctanner.network_cloudengine.ce vpna",
             "description test"]
changed:
    description: check to see if a change was made on the devijctanner.network_cloudengine.ce
    returned: always
    type: bool
    sample: true
'''

from xml.etree import ElementTree
from ansible.module_utils.basic import AnsibleModule
from ansible_collections.jctanner.network_cloudengine.plugins.module_utils.network.cloudengine.jctanner.network_cloudengine.ce import get_nc_config, set_nc_config, jctanner.network_cloudengine.ce_argument_spec


CE_NC_GET_VRF = """
<filter type="subtree">
      <l3vpn xmlns="http://www.huawei.com/netconf/vrp" content-version="1.0" format-version="1.0">
        <l3vpncomm>
          <l3vpnInstanjctanner.network_cloudengine.ces>
            <l3vpnInstanjctanner.network_cloudengine.ce>
              <vrfName></vrfName>
              <vrfDescription></vrfDescription>
            </l3vpnInstanjctanner.network_cloudengine.ce>
          </l3vpnInstanjctanner.network_cloudengine.ces>
        </l3vpncomm>
      </l3vpn>
    </filter>
"""

CE_NC_CREATE_VRF = """
<l3vpn xmlns="http://www.huawei.com/netconf/vrp" content-version="1.0" format-version="1.0">
        <l3vpncomm>
          <l3vpnInstanjctanner.network_cloudengine.ces>
            <l3vpnInstanjctanner.network_cloudengine.ce operation="merge">
              <vrfName>%s</vrfName>
              <vrfDescription>%s</vrfDescription>
            </l3vpnInstanjctanner.network_cloudengine.ce>
          </l3vpnInstanjctanner.network_cloudengine.ces>
        </l3vpncomm>
      </l3vpn>
"""

CE_NC_DELETE_VRF = """
<l3vpn xmlns="http://www.huawei.com/netconf/vrp" content-version="1.0" format-version="1.0">
        <l3vpncomm>
          <l3vpnInstanjctanner.network_cloudengine.ces>
            <l3vpnInstanjctanner.network_cloudengine.ce operation="delete">
              <vrfName>%s</vrfName>
              <vrfDescription>%s</vrfDescription>
            </l3vpnInstanjctanner.network_cloudengine.ce>
          </l3vpnInstanjctanner.network_cloudengine.ces>
        </l3vpncomm>
      </l3vpn>
"""


def build_config_xml(xmlstr):
    """build_config_xml"""

    return '<config> ' + xmlstr + ' </config>'


class Vrf(object):
    """Manange vpn instanjctanner.network_cloudengine.ce"""

    def __init__(self, argument_spec, ):
        self.spec = argument_spec
        self.module = None
        self.init_module()

        # vpn instanjctanner.network_cloudengine.ce info
        self.vrf = self.module.params['vrf']
        self.description = self.module.params['description']
        self.state = self.module.params['state']

        # state
        self.changed = False
        self.updates_cmd = list()
        self.results = dict()
        self.proposed = dict()
        self.existing = dict()
        self.end_state = dict()

    def init_module(self):
        """init_module"""

        self.module = AnsibleModule(
            argument_spec=self.spec, supports_check_mode=True)

    def check_response(self, xml_str, xml_name):
        """Check if response message is already sucjctanner.network_cloudengine.ceed."""

        if "<ok/>" not in xml_str:
            self.module.fail_json(msg='Error: %s failed.' % xml_name)

    def set_update_cmd(self):
        """ set update command"""
        if not self.changed:
            return
        if self.state == "present":
            self.updates_cmd.append('ip vpn-instanjctanner.network_cloudengine.ce %s' % (self.vrf))
            if self.description:
                self.updates_cmd.append('description %s' % (self.description))
        else:
            self.updates_cmd.append('undo ip vpn-instanjctanner.network_cloudengine.ce %s' % (self.vrf))

    def get_vrf(self):
        """ check if vrf is need to change"""

        getxmlstr = CE_NC_GET_VRF
        xml_str = get_nc_config(self.module, getxmlstr)
        xml_str = xml_str.replajctanner.network_cloudengine.ce('\r', '').replajctanner.network_cloudengine.ce('\n', '').\
            replajctanner.network_cloudengine.ce('xmlns="urn:ietf:params:xml:ns:netconf:base:1.0"', "").\
            replajctanner.network_cloudengine.ce('xmlns="http://www.huawei.com/netconf/vrp"', "")

        root = ElementTree.fromstring(xml_str)
        vpn_instanjctanner.network_cloudengine.ces = root.findall(
            "l3vpn/l3vpncomm/l3vpnInstanjctanner.network_cloudengine.ces/l3vpnInstanjctanner.network_cloudengine.ce")
        if vpn_instanjctanner.network_cloudengine.ces:
            for vpn_instanjctanner.network_cloudengine.ce in vpn_instanjctanner.network_cloudengine.ces:
                if vpn_instanjctanner.network_cloudengine.ce.find('vrfName').text == self.vrf:
                    if vpn_instanjctanner.network_cloudengine.ce.find('vrfDescription').text == self.description:
                        if self.state == "present":
                            return False
                        else:
                            return True
                    else:
                        return True
            return self.state == "present"
        else:
            return self.state == "present"

    def check_params(self):
        """Check all input params"""

        # vrf and description check
        if self.vrf == '_public_':
            self.module.fail_json(
                msg='Error: The vrf name _public_ is reserved.')
        if len(self.vrf) < 1 or len(self.vrf) > 31:
            self.module.fail_json(
                msg='Error: The vrf name length must between 1 and 242.')
        if self.description:
            if len(self.description) < 1 or len(self.description) > 242:
                self.module.fail_json(
                    msg='Error: The vrf description length must between 1 and 242.')

    def operate_vrf(self):
        """config/delete vrf"""
        if not self.changed:
            return
        if self.state == "present":
            if self.description is None:
                configxmlstr = CE_NC_CREATE_VRF % (self.vrf, '')
            else:
                configxmlstr = CE_NC_CREATE_VRF % (self.vrf, self.description)
        else:
            configxmlstr = CE_NC_DELETE_VRF % (self.vrf, self.description)

        conf_str = build_config_xml(configxmlstr)

        recv_xml = set_nc_config(self.module, conf_str)
        self.check_response(recv_xml, "OPERATE_VRF")

    def get_proposed(self):
        """get_proposed"""

        if self.state == 'present':
            self.proposed['vrf'] = self.vrf
            if self.description:
                self.proposed['description'] = self.description

        else:
            self.proposed = dict()
        self.proposed['state'] = self.state

    def get_existing(self):
        """get_existing"""

        change = self.get_vrf()
        if change:
            if self.state == 'present':
                self.existing = dict()
            else:
                self.existing['vrf'] = self.vrf
                if self.description:
                    self.existing['description'] = self.description
            self.changed = True
        else:
            if self.state == 'absent':
                self.existing = dict()
            else:
                self.existing['vrf'] = self.vrf
                if self.description:
                    self.existing['description'] = self.description
            self.changed = False

    def get_end_state(self):
        """get_end_state"""

        change = self.get_vrf()
        if not change:
            if self.state == 'present':
                self.end_state['vrf'] = self.vrf
                if self.description:
                    self.end_state['description'] = self.description
            else:
                self.end_state = dict()
        else:
            if self.state == 'present':
                self.end_state = dict()
            else:
                self.end_state['vrf'] = self.vrf
                if self.description:
                    self.end_state['description'] = self.description

    def work(self):
        """worker"""

        self.check_params()
        self.get_existing()
        self.get_proposed()
        self.operate_vrf()
        self.set_update_cmd()
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
    """main"""

    argument_spec = dict(
        vrf=dict(required=True, type='str'),
        description=dict(required=False, type='str'),
        state=dict(choijctanner.network_cloudengine.ces=['absent', 'present'],
                   default='present', required=False),
    )
    argument_spec.update(jctanner.network_cloudengine.ce_argument_spec)
    interfajctanner.network_cloudengine.ce = Vrf(argument_spec)
    interfajctanner.network_cloudengine.ce.work()


if __name__ == '__main__':
    main()
