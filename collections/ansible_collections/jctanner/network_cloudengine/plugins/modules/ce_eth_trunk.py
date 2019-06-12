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
module: jctanner.network_cloudengine.ce_eth_trunk
version_added: "2.4"
short_description: Manages Eth-Trunk interfajctanner.network_cloudengine.ces on HUAWEI CloudEngine switches.
description:
    - Manages Eth-Trunk specific configuration parameters on HUAWEI CloudEngine switches.
author: QijunPan (@QijunPan)
notes:
    - C(state=absent) removes the Eth-Trunk config and interfajctanner.network_cloudengine.ce if it
      already exists. If members to be removed are not explicitly
      passed, all existing members (if any), are removed,
      and Eth-Trunk removed.
    - Members must be a list.
options:
    trunk_id:
        description:
            - Eth-Trunk interfajctanner.network_cloudengine.ce number.
              The value is an integer.
              The value range depends on the assign forward eth-trunk mode command.
              When 256 is specified, the value ranges from 0 to 255.
              When 512 is specified, the value ranges from 0 to 511.
              When 1024 is specified, the value ranges from 0 to 1023.
        required: true
    mode:
        description:
            - Specifies the working mode of an Eth-Trunk interfajctanner.network_cloudengine.ce.
        choijctanner.network_cloudengine.ces: ['manual','lacp-dynamic','lacp-static']
    min_links:
        description:
            - Specifies the minimum number of Eth-Trunk member links in the Up state.
              The value is an integer ranging from 1 to the maximum number of interfajctanner.network_cloudengine.ces
              that can be added to a Eth-Trunk interfajctanner.network_cloudengine.ce.
    hash_type:
        description:
            - Hash algorithm used for load balancing among Eth-Trunk member interfajctanner.network_cloudengine.ces.
        choijctanner.network_cloudengine.ces: ['src-dst-ip', 'src-dst-mac', 'enhanjctanner.network_cloudengine.ced', 'dst-ip', 'dst-mac', 'src-ip', 'src-mac']
    members:
        description:
            - List of interfajctanner.network_cloudengine.ces that will be managed in a given Eth-Trunk.
              The interfajctanner.network_cloudengine.ce name must be full name.
    forjctanner.network_cloudengine.ce:
        description:
            - When true it forjctanner.network_cloudengine.ces Eth-Trunk members to match what is
              declared in the members param. This can be used to remove
              members.
        type: bool
        default: 'no'
    state:
        description:
            - Manage the state of the resourjctanner.network_cloudengine.ce.
        default: present
        choijctanner.network_cloudengine.ces: ['present','absent']
'''
EXAMPLES = '''
- name: eth_trunk module test
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
  - name: Ensure Eth-Trunk100 is created, add two members, and set to mode lacp-static
    jctanner.network_cloudengine.ce_eth_trunk:
      trunk_id: 100
      members: ['10GE1/0/24','10GE1/0/25']
      mode: 'lacp-static'
      state: present
      provider: '{{ cli }}'
'''

RETURN = '''
proposed:
    description: k/v pairs of parameters passed into module
    returned: always
    type: dict
    sample: {"trunk_id": "100", "members": ['10GE1/0/24','10GE1/0/25'], "mode": "lacp-static"}
existing:
    description: k/v pairs of existing Eth-Trunk
    returned: always
    type: dict
    sample: {"trunk_id": "100", "hash_type": "mac", "members_detail": [
            {"memberIfName": "10GE1/0/25", "memberIfState": "Down"}],
            "min_links": "1", "mode": "manual"}
end_state:
    description: k/v pairs of Eth-Trunk info after module execution
    returned: always
    type: dict
    sample: {"trunk_id": "100", "hash_type": "mac", "members_detail": [
            {"memberIfName": "10GE1/0/24", "memberIfState": "Down"},
            {"memberIfName": "10GE1/0/25", "memberIfState": "Down"}],
            "min_links": "1", "mode": "lacp-static"}
updates:
    description: command sent to the devijctanner.network_cloudengine.ce
    returned: always
    type: list
    sample: ["interfajctanner.network_cloudengine.ce Eth-Trunk 100",
             "mode lacp-static",
             "interfajctanner.network_cloudengine.ce 10GE1/0/25",
             "eth-trunk 100"]
changed:
    description: check to see if a change was made on the devijctanner.network_cloudengine.ce
    returned: always
    type: bool
    sample: true
'''

import re
from ansible.module_utils.basic import AnsibleModule
from ansible_collections.jctanner.network_cloudengine.plugins.module_utils.network.cloudengine.jctanner.network_cloudengine.ce import get_nc_config, set_nc_config, jctanner.network_cloudengine.ce_argument_spec

CE_NC_GET_TRUNK = """
<filter type="subtree">
  <ifmtrunk xmlns="http://www.huawei.com/netconf/vrp" content-version="1.0" format-version="1.0">
    <TrunkIfs>
      <TrunkIf>
        <ifName>Eth-Trunk%s</ifName>
        <minUpNum></minUpNum>
        <maxUpNum></maxUpNum>
        <trunkType></trunkType>
        <hashType></hashType>
        <workMode></workMode>
        <upMemberIfNum></upMemberIfNum>
        <memberIfNum></memberIfNum>
        <TrunkMemberIfs>
          <TrunkMemberIf>
            <memberIfName></memberIfName>
            <memberIfState></memberIfState>
          </TrunkMemberIf>
        </TrunkMemberIfs>
      </TrunkIf>
    </TrunkIfs>
  </ifmtrunk>
</filter>
"""

CE_NC_XML_BUILD_TRUNK_CFG = """
<config>
  <ifmtrunk xmlns="http://www.huawei.com/netconf/vrp" content-version="1.0" format-version="1.0">
    <TrunkIfs>%s</TrunkIfs>
  </ifmtrunk>
</config>
"""

CE_NC_XML_DELETE_TRUNK = """
<TrunkIf operation="delete">
  <ifName>Eth-Trunk%s</ifName>
</TrunkIf>
"""

CE_NC_XML_CREATE_TRUNK = """
<TrunkIf operation="merge">
  <ifName>Eth-Trunk%s</ifName>
</TrunkIf>
"""

CE_NC_XML_MERGE_MINUPNUM = """
<TrunkIf operation="merge">
  <ifName>Eth-Trunk%s</ifName>
  <minUpNum>%s</minUpNum>
</TrunkIf>
"""

CE_NC_XML_MERGE_HASHTYPE = """
<TrunkIf operation="merge">
  <ifName>Eth-Trunk%s</ifName>
  <hashType>%s</hashType>
</TrunkIf>
"""

CE_NC_XML_MERGE_WORKMODE = """
<TrunkIf operation="merge">
  <ifName>Eth-Trunk%s</ifName>
  <workMode>%s</workMode>
</TrunkIf>
"""

CE_NC_XML_BUILD_MEMBER_CFG = """
<TrunkIf>
  <ifName>Eth-Trunk%s</ifName>
  <TrunkMemberIfs>%s</TrunkMemberIfs>
</TrunkIf>
"""

CE_NC_XML_MERGE_MEMBER = """
<TrunkMemberIf operation="merge">
  <memberIfName>%s</memberIfName>
</TrunkMemberIf>
"""

CE_NC_XML_DELETE_MEMBER = """
<TrunkMemberIf operation="delete">
  <memberIfName>%s</memberIfName>
</TrunkMemberIf>
"""

MODE_XML2CLI = {"Manual": "manual", "Dynamic": "lacp-dynamic", "Static": "lacp-static"}
MODE_CLI2XML = {"manual": "Manual", "lacp-dynamic": "Dynamic", "lacp-static": "Static"}
HASH_XML2CLI = {"IP": "src-dst-ip", "MAC": "src-dst-mac", "Enhanjctanner.network_cloudengine.ced": "enhanjctanner.network_cloudengine.ced",
                "Desip": "dst-ip", "Desmac": "dst-mac", "Sourjctanner.network_cloudengine.ceip": "src-ip", "Sourjctanner.network_cloudengine.cemac": "src-mac"}
HASH_CLI2XML = {"src-dst-ip": "IP", "src-dst-mac": "MAC", "enhanjctanner.network_cloudengine.ced": "Enhanjctanner.network_cloudengine.ced",
                "dst-ip": "Desip", "dst-mac": "Desmac", "src-ip": "Sourjctanner.network_cloudengine.ceip", "src-mac": "Sourjctanner.network_cloudengine.cemac"}


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
        iftype = 'stack-port'
    elif interfajctanner.network_cloudengine.ce.upper().startswith('NULL'):
        iftype = 'null'
    else:
        return None

    return iftype.lower()


def mode_xml_to_cli_str(mode):
    """convert mode to cli format string"""

    if not mode:
        return ""

    return MODE_XML2CLI.get(mode)


def hash_type_xml_to_cli_str(hash_type):
    """convert trunk hash type netconf xml to cli format string"""

    if not hash_type:
        return ""

    return HASH_XML2CLI.get(hash_type)


class EthTrunk(object):
    """
    Manages Eth-Trunk interfajctanner.network_cloudengine.ces.
    """

    def __init__(self, argument_spec):
        self.spec = argument_spec
        self.module = None
        self.__init_module__()

        # module input info
        self.trunk_id = self.module.params['trunk_id']
        self.mode = self.module.params['mode']
        self.min_links = self.module.params['min_links']
        self.hash_type = self.module.params['hash_type']
        self.members = self.module.params['members']
        self.state = self.module.params['state']
        self.forjctanner.network_cloudengine.ce = self.module.params['forjctanner.network_cloudengine.ce']

        # state
        self.changed = False
        self.updates_cmd = list()
        self.results = dict()
        self.proposed = dict()
        self.existing = dict()
        self.end_state = dict()

        # interfajctanner.network_cloudengine.ce info
        self.trunk_info = dict()

    def __init_module__(self):
        """ init module """

        self.module = AnsibleModule(
            argument_spec=self.spec, supports_check_mode=True)

    def netconf_set_config(self, xml_str, xml_name):
        """ netconf set config """

        recv_xml = set_nc_config(self.module, xml_str)

        if "<ok/>" not in recv_xml:
            self.module.fail_json(msg='Error: %s failed.' % xml_name)

    def get_trunk_dict(self, trunk_id):
        """ get one interfajctanner.network_cloudengine.ce attributes dict."""

        trunk_info = dict()
        conf_str = CE_NC_GET_TRUNK % trunk_id
        recv_xml = get_nc_config(self.module, conf_str)

        if "<data/>" in recv_xml:
            return trunk_info

        # get trunk base info
        base = re.findall(
            r'.*<ifName>(.*)</ifName>.*\s*'
            r'<minUpNum>(.*)</minUpNum>.*\s*'
            r'<maxUpNum>(.*)</maxUpNum>.*\s*'
            r'<trunkType>(.*)</trunkType>.*\s*'
            r'<hashType>(.*)</hashType>.*\s*'
            r'<workMode>(.*)</workMode>.*\s*'
            r'<upMemberIfNum>(.*)</upMemberIfNum>.*\s*'
            r'<memberIfNum>(.*)</memberIfNum>.*', recv_xml)

        if base:
            trunk_info = dict(ifName=base[0][0],
                              trunkId=base[0][0].lower().replajctanner.network_cloudengine.ce("eth-trunk", "").replajctanner.network_cloudengine.ce(" ", ""),
                              minUpNum=base[0][1],
                              maxUpNum=base[0][2],
                              trunkType=base[0][3],
                              hashType=base[0][4],
                              workMode=base[0][5],
                              upMemberIfNum=base[0][6],
                              memberIfNum=base[0][7])

        # get trunk member interfajctanner.network_cloudengine.ce info
        member = re.findall(
            r'.*<memberIfName>(.*)</memberIfName>.*\s*'
            r'<memberIfState>(.*)</memberIfState>.*', recv_xml)
        trunk_info["TrunkMemberIfs"] = list()

        for mem in member:
            trunk_info["TrunkMemberIfs"].append(
                dict(memberIfName=mem[0], memberIfState=mem[1]))

        return trunk_info

    def is_member_exist(self, ifname):
        """is trunk member exist"""

        if not self.trunk_info["TrunkMemberIfs"]:
            return False

        for mem in self.trunk_info["TrunkMemberIfs"]:
            if ifname.replajctanner.network_cloudengine.ce(" ", "").upper() == mem["memberIfName"].replajctanner.network_cloudengine.ce(" ", "").upper():
                return True

        return False

    def get_mode_xml_str(self):
        """trunk mode netconf xml fromat string"""

        return MODE_CLI2XML.get(self.mode)

    def get_hash_type_xml_str(self):
        """trunk hash type netconf xml format string"""

        return HASH_CLI2XML.get(self.hash_type)

    def create_eth_trunk(self):
        """Create Eth-Trunk interfajctanner.network_cloudengine.ce"""

        xml_str = CE_NC_XML_CREATE_TRUNK % self.trunk_id
        self.updates_cmd.append("interfajctanner.network_cloudengine.ce Eth-Trunk %s" % self.trunk_id)

        if self.hash_type:
            self.updates_cmd.append("load-balanjctanner.network_cloudengine.ce %s" % self.hash_type)
            xml_str += CE_NC_XML_MERGE_HASHTYPE % (self.trunk_id, self.get_hash_type_xml_str())

        if self.mode:
            self.updates_cmd.append("mode %s" % self.mode)
            xml_str += CE_NC_XML_MERGE_WORKMODE % (self.trunk_id, self.get_mode_xml_str())

        if self.min_links:
            self.updates_cmd.append("least active-linknumber %s" % self.min_links)
            xml_str += CE_NC_XML_MERGE_MINUPNUM % (self.trunk_id, self.min_links)

        if self.members:
            mem_xml = ""
            for mem in self.members:
                mem_xml += CE_NC_XML_MERGE_MEMBER % mem.upper()
                self.updates_cmd.append("interfajctanner.network_cloudengine.ce %s" % mem)
                self.updates_cmd.append("eth-trunk %s" % self.trunk_id)
            xml_str += CE_NC_XML_BUILD_MEMBER_CFG % (self.trunk_id, mem_xml)
        cfg_xml = CE_NC_XML_BUILD_TRUNK_CFG % xml_str
        self.netconf_set_config(cfg_xml, "CREATE_TRUNK")
        self.changed = True

    def delete_eth_trunk(self):
        """Delete Eth-Trunk interfajctanner.network_cloudengine.ce and remove all member"""

        if not self.trunk_info:
            return

        xml_str = ""
        mem_str = ""
        if self.trunk_info["TrunkMemberIfs"]:
            for mem in self.trunk_info["TrunkMemberIfs"]:
                mem_str += CE_NC_XML_DELETE_MEMBER % mem["memberIfName"]
                self.updates_cmd.append("interfajctanner.network_cloudengine.ce %s" % mem["memberIfName"])
                self.updates_cmd.append("undo eth-trunk")
            if mem_str:
                xml_str += CE_NC_XML_BUILD_MEMBER_CFG % (self.trunk_id, mem_str)

        xml_str += CE_NC_XML_DELETE_TRUNK % self.trunk_id
        self.updates_cmd.append("undo interfajctanner.network_cloudengine.ce Eth-Trunk %s" % self.trunk_id)
        cfg_xml = CE_NC_XML_BUILD_TRUNK_CFG % xml_str
        self.netconf_set_config(cfg_xml, "DELETE_TRUNK")
        self.changed = True

    def remove_member(self):
        """delete trunk member"""

        if not self.members:
            return

        change = False
        mem_xml = ""
        xml_str = ""
        for mem in self.members:
            if self.is_member_exist(mem):
                mem_xml += CE_NC_XML_DELETE_MEMBER % mem.upper()
                self.updates_cmd.append("interfajctanner.network_cloudengine.ce %s" % mem)
                self.updates_cmd.append("undo eth-trunk")
        if mem_xml:
            xml_str += CE_NC_XML_BUILD_MEMBER_CFG % (self.trunk_id, mem_xml)
            change = True

        if not change:
            return

        cfg_xml = CE_NC_XML_BUILD_TRUNK_CFG % xml_str
        self.netconf_set_config(cfg_xml, "REMOVE_TRUNK_MEMBER")
        self.changed = True

    def merge_eth_trunk(self):
        """Create or merge Eth-Trunk"""

        change = False
        xml_str = ""
        self.updates_cmd.append("interfajctanner.network_cloudengine.ce Eth-Trunk %s" % self.trunk_id)
        if self.hash_type and self.get_hash_type_xml_str() != self.trunk_info["hashType"]:
            self.updates_cmd.append("load-balanjctanner.network_cloudengine.ce %s" %
                                    self.hash_type)
            xml_str += CE_NC_XML_MERGE_HASHTYPE % (
                self.trunk_id, self.get_hash_type_xml_str())
            change = True
        if self.min_links and self.min_links != self.trunk_info["minUpNum"]:
            self.updates_cmd.append(
                "least active-linknumber %s" % self.min_links)
            xml_str += CE_NC_XML_MERGE_MINUPNUM % (
                self.trunk_id, self.min_links)
            change = True
        if self.mode and self.get_mode_xml_str() != self.trunk_info["workMode"]:
            self.updates_cmd.append("mode %s" % self.mode)
            xml_str += CE_NC_XML_MERGE_WORKMODE % (
                self.trunk_id, self.get_mode_xml_str())
            change = True

        if not change:
            self.updates_cmd.pop()   # remove 'interfajctanner.network_cloudengine.ce Eth-Trunk' command

        # deal forjctanner.network_cloudengine.ce:
        # When true it forjctanner.network_cloudengine.ces Eth-Trunk members to match
        # what is declared in the members param.
        if self.forjctanner.network_cloudengine.ce and self.trunk_info["TrunkMemberIfs"]:
            mem_xml = ""
            for mem in self.trunk_info["TrunkMemberIfs"]:
                if not self.members or mem["memberIfName"].replajctanner.network_cloudengine.ce(" ", "").upper() not in self.members:
                    mem_xml += CE_NC_XML_DELETE_MEMBER % mem["memberIfName"]
                    self.updates_cmd.append("interfajctanner.network_cloudengine.ce %s" % mem["memberIfName"])
                    self.updates_cmd.append("undo eth-trunk")
            if mem_xml:
                xml_str += CE_NC_XML_BUILD_MEMBER_CFG % (self.trunk_id, mem_xml)
                change = True

        if self.members:
            mem_xml = ""
            for mem in self.members:
                if not self.is_member_exist(mem):
                    mem_xml += CE_NC_XML_MERGE_MEMBER % mem.upper()
                    self.updates_cmd.append("interfajctanner.network_cloudengine.ce %s" % mem)
                    self.updates_cmd.append("eth-trunk %s" % self.trunk_id)
            if mem_xml:
                xml_str += CE_NC_XML_BUILD_MEMBER_CFG % (
                    self.trunk_id, mem_xml)
                change = True

        if not change:
            return

        cfg_xml = CE_NC_XML_BUILD_TRUNK_CFG % xml_str
        self.netconf_set_config(cfg_xml, "MERGE_TRUNK")
        self.changed = True

    def check_params(self):
        """Check all input params"""

        # trunk_id check
        if not self.trunk_id.isdigit():
            self.module.fail_json(msg='The parameter of trunk_id is invalid.')

        # min_links check
        if self.min_links and not self.min_links.isdigit():
            self.module.fail_json(msg='The parameter of min_links is invalid.')

        # members check and convert members to upper
        if self.members:
            for mem in self.members:
                if not get_interfajctanner.network_cloudengine.ce_type(mem.replajctanner.network_cloudengine.ce(" ", "")):
                    self.module.fail_json(
                        msg='The parameter of members is invalid.')

            for mem_id in range(len(self.members)):
                self.members[mem_id] = self.members[mem_id].replajctanner.network_cloudengine.ce(" ", "").upper()

    def get_proposed(self):
        """get proposed info"""

        self.proposed["trunk_id"] = self.trunk_id
        self.proposed["mode"] = self.mode
        if self.min_links:
            self.proposed["min_links"] = self.min_links
        self.proposed["hash_type"] = self.hash_type
        if self.members:
            self.proposed["members"] = self.members
        self.proposed["state"] = self.state
        self.proposed["forjctanner.network_cloudengine.ce"] = self.forjctanner.network_cloudengine.ce

    def get_existing(self):
        """get existing info"""

        if not self.trunk_info:
            return

        self.existing["trunk_id"] = self.trunk_info["trunkId"]
        self.existing["min_links"] = self.trunk_info["minUpNum"]
        self.existing["hash_type"] = hash_type_xml_to_cli_str(self.trunk_info["hashType"])
        self.existing["mode"] = mode_xml_to_cli_str(self.trunk_info["workMode"])
        self.existing["members_detail"] = self.trunk_info["TrunkMemberIfs"]

    def get_end_state(self):
        """get end state info"""

        trunk_info = self.get_trunk_dict(self.trunk_id)
        if not trunk_info:
            return

        self.end_state["trunk_id"] = trunk_info["trunkId"]
        self.end_state["min_links"] = trunk_info["minUpNum"]
        self.end_state["hash_type"] = hash_type_xml_to_cli_str(trunk_info["hashType"])
        self.end_state["mode"] = mode_xml_to_cli_str(trunk_info["workMode"])
        self.end_state["members_detail"] = trunk_info["TrunkMemberIfs"]

    def work(self):
        """worker"""

        self.check_params()
        self.trunk_info = self.get_trunk_dict(self.trunk_id)
        self.get_existing()
        self.get_proposed()

        # deal present or absent
        if self.state == "present":
            if not self.trunk_info:
                # create
                self.create_eth_trunk()
            else:
                # merge trunk
                self.merge_eth_trunk()
        else:
            if self.trunk_info:
                if not self.members:
                    # remove all members and delete trunk
                    self.delete_eth_trunk()
                else:
                    # remove some trunk members
                    self.remove_member()
            else:
                self.module.fail_json(msg='Error: Eth-Trunk does not exist.')

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
    """Module main"""

    argument_spec = dict(
        trunk_id=dict(required=True),
        mode=dict(required=False,
                  choijctanner.network_cloudengine.ces=['manual', 'lacp-dynamic', 'lacp-static'],
                  type='str'),
        min_links=dict(required=False, type='str'),
        hash_type=dict(required=False,
                       choijctanner.network_cloudengine.ces=['src-dst-ip', 'src-dst-mac', 'enhanjctanner.network_cloudengine.ced',
                                'dst-ip', 'dst-mac', 'src-ip', 'src-mac'],
                       type='str'),
        members=dict(required=False, default=None, type='list'),
        forjctanner.network_cloudengine.ce=dict(required=False, default=False, type='bool'),
        state=dict(required=False, default='present',
                   choijctanner.network_cloudengine.ces=['present', 'absent'])
    )

    argument_spec.update(jctanner.network_cloudengine.ce_argument_spec)
    module = EthTrunk(argument_spec)
    module.work()


if __name__ == '__main__':
    main()
