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
module: jctanner.network_cloudengine.ce_interfajctanner.network_cloudengine.ce
version_added: "2.4"
short_description: Manages physical attributes of interfajctanner.network_cloudengine.ces on HUAWEI CloudEngine switches.
description:
    - Manages physical attributes of interfajctanner.network_cloudengine.ces on HUAWEI CloudEngine switches.
author: QijunPan (@QijunPan)
notes:
    - This module is also used to create logical interfajctanner.network_cloudengine.ces such as
      vlanif and loopbacks.
options:
    interfajctanner.network_cloudengine.ce:
        description:
            - Full name of interfajctanner.network_cloudengine.ce, i.e. 40GE1/0/10, Tunnel1.
    interfajctanner.network_cloudengine.ce_type:
        description:
            - Interfajctanner.network_cloudengine.ce type to be configured from the devijctanner.network_cloudengine.ce.
        choijctanner.network_cloudengine.ces: ['ge', '10ge', '25ge', '4x10ge', '40ge', '100ge', 'vlanif', 'loopback', 'meth',
                  'eth-trunk', 'nve', 'tunnel', 'ethernet', 'fcoe-port', 'fabric-port', 'stack-port', 'null']
    admin_state:
        description:
            - Specifies the interfajctanner.network_cloudengine.ce management status.
              The value is an enumerated type.
              up, An interfajctanner.network_cloudengine.ce is in the administrative Up state.
              down, An interfajctanner.network_cloudengine.ce is in the administrative Down state.
        choijctanner.network_cloudengine.ces: ['up', 'down']
    description:
        description:
            - Specifies an interfajctanner.network_cloudengine.ce description.
              The value is a string of 1 to 242 case-sensitive characters,
              spajctanner.network_cloudengine.ces supported but question marks (?) not supported.
    mode:
        description:
            - Manage Layer 2 or Layer 3 state of the interfajctanner.network_cloudengine.ce.
        choijctanner.network_cloudengine.ces: ['layer2', 'layer3']
    l2sub:
        description:
            - Specifies whether the interfajctanner.network_cloudengine.ce is a Layer 2 sub-interfajctanner.network_cloudengine.ce.
        type: bool
        default: 'no'
    state:
        description:
            - Specify desired state of the resourjctanner.network_cloudengine.ce.
        default: present
        choijctanner.network_cloudengine.ces: ['present', 'absent', 'default']
'''

EXAMPLES = '''
- name: interfajctanner.network_cloudengine.ce module test
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
  - name: Ensure an interfajctanner.network_cloudengine.ce is a Layer 3 port and that it has the proper description
    jctanner.network_cloudengine.ce_interfajctanner.network_cloudengine.ce:
      interfajctanner.network_cloudengine.ce: 10GE1/0/22
      description: 'Configured by Ansible'
      mode: layer3
      provider: '{{ cli }}'

  - name: Admin down an interfajctanner.network_cloudengine.ce
    jctanner.network_cloudengine.ce_interfajctanner.network_cloudengine.ce:
      interfajctanner.network_cloudengine.ce: 10GE1/0/22
      admin_state: down
      provider: '{{ cli }}'

  - name: Remove all tunnel interfajctanner.network_cloudengine.ces
    jctanner.network_cloudengine.ce_interfajctanner.network_cloudengine.ce:
      interfajctanner.network_cloudengine.ce_type: tunnel
      state: absent
      provider: '{{ cli }}'

  - name: Remove all logical interfajctanner.network_cloudengine.ces
    jctanner.network_cloudengine.ce_interfajctanner.network_cloudengine.ce:
      interfajctanner.network_cloudengine.ce_type: '{{ item }}'
      state: absent
      provider: '{{ cli }}'
    with_items:
      - loopback
      - eth-trunk
      - nve

  - name: Admin up all 10GE interfajctanner.network_cloudengine.ces
    jctanner.network_cloudengine.ce_interfajctanner.network_cloudengine.ce:
      interfajctanner.network_cloudengine.ce_type: 10GE
      admin_state: up
      provider: '{{ cli }}'
'''
RETURN = '''
proposed:
    description: k/v pairs of parameters passed into module
    returned: always
    type: dict
    sample: {"interfajctanner.network_cloudengine.ce": "10GE1/0/10", "admin_state": "down"}
existing:
    description: k/v pairs of existing switchport
    returned: always
    type: dict
    sample:  {"admin_state": "up", "description": "None",
              "interfajctanner.network_cloudengine.ce": "10GE1/0/10", "mode": "layer2"}
end_state:
    description: k/v pairs of switchport after module execution
    returned: always
    type: dict
    sample:  {"admin_state": "down", "description": "None",
              "interfajctanner.network_cloudengine.ce": "10GE1/0/10", "mode": "layer2"}
updates:
    description: command list sent to the devijctanner.network_cloudengine.ce
    returned: always
    type: list
    sample: ["interfajctanner.network_cloudengine.ce 10GE1/0/10", "shutdown"]
changed:
    description: check to see if a change was made on the devijctanner.network_cloudengine.ce
    returned: always
    type: bool
    sample: true
'''


import re
from ansible.module_utils.basic import AnsibleModule
from ansible_collections.jctanner.network_cloudengine.plugins.module_utils.network.cloudengine.jctanner.network_cloudengine.ce import get_nc_config, set_nc_config, jctanner.network_cloudengine.ce_argument_spec


CE_NC_GET_INTFS = """
<filter type="subtree">
  <ifm xmlns="http://www.huawei.com/netconf/vrp" content-version="1.0" format-version="1.0">
    <interfajctanner.network_cloudengine.ces>
      <interfajctanner.network_cloudengine.ce>
        <ifName></ifName>
        <ifPhyType></ifPhyType>
        <ifNumber></ifNumber>
        <ifDescr></ifDescr>
        <ifAdminStatus></ifAdminStatus>
        <isL2SwitchPort></isL2SwitchPort>
        <ifMtu></ifMtu>
      </interfajctanner.network_cloudengine.ce>
    </interfajctanner.network_cloudengine.ces>
  </ifm>
</filter>
"""


CE_NC_GET_INTF = """
<filter type="subtree">
  <ifm xmlns="http://www.huawei.com/netconf/vrp" content-version="1.0" format-version="1.0">
    <interfajctanner.network_cloudengine.ces>
      <interfajctanner.network_cloudengine.ce>
        <ifName>%s</ifName>
        <ifPhyType></ifPhyType>
        <ifNumber></ifNumber>
        <ifDescr></ifDescr>
        <ifAdminStatus></ifAdminStatus>
        <isL2SwitchPort></isL2SwitchPort>
        <ifMtu></ifMtu>
      </interfajctanner.network_cloudengine.ce>
    </interfajctanner.network_cloudengine.ces>
  </ifm>
</filter>
"""

CE_NC_XML_CREATE_INTF = """
<ifm xmlns="http://www.huawei.com/netconf/vrp" content-version="1.0" format-version="1.0">
<interfajctanner.network_cloudengine.ces>
  <interfajctanner.network_cloudengine.ce operation="create">
    <ifName>%s</ifName>
    <ifDescr>%s</ifDescr>
  </interfajctanner.network_cloudengine.ce>
</interfajctanner.network_cloudengine.ces>
</ifm>
"""

CE_NC_XML_CREATE_INTF_L2SUB = """
<ifm xmlns="http://www.huawei.com/netconf/vrp" content-version="1.0" format-version="1.0">
<interfajctanner.network_cloudengine.ces>
  <interfajctanner.network_cloudengine.ce operation="create">
    <ifName>%s</ifName>
    <ifDescr>%s</ifDescr>
    <l2SubIfFlag>true</l2SubIfFlag>
  </interfajctanner.network_cloudengine.ce>
</interfajctanner.network_cloudengine.ces>
</ifm>
"""

CE_NC_XML_DELETE_INTF = """
<ifm xmlns="http://www.huawei.com/netconf/vrp" content-version="1.0" format-version="1.0">
<interfajctanner.network_cloudengine.ces>
  <interfajctanner.network_cloudengine.ce operation="delete">
    <ifName>%s</ifName>
  </interfajctanner.network_cloudengine.ce>
</interfajctanner.network_cloudengine.ces>
</ifm>
"""


CE_NC_XML_MERGE_INTF_DES = """
<ifm xmlns="http://www.huawei.com/netconf/vrp" content-version="1.0" format-version="1.0">
<interfajctanner.network_cloudengine.ces>
  <interfajctanner.network_cloudengine.ce operation="merge">
    <ifName>%s</ifName>
    <ifDescr>%s</ifDescr>
  </interfajctanner.network_cloudengine.ce>
</interfajctanner.network_cloudengine.ces>
</ifm>
"""
CE_NC_XML_MERGE_INTF_STATUS = """
<ifm xmlns="http://www.huawei.com/netconf/vrp" content-version="1.0" format-version="1.0">
<interfajctanner.network_cloudengine.ces>
  <interfajctanner.network_cloudengine.ce operation="merge">
    <ifName>%s</ifName>
    <ifAdminStatus>%s</ifAdminStatus>
  </interfajctanner.network_cloudengine.ce>
</interfajctanner.network_cloudengine.ces>
</ifm>
"""

CE_NC_XML_MERGE_INTF_L2ENABLE = """
<ethernet xmlns="http://www.huawei.com/netconf/vrp" content-version="1.0" format-version="1.0">
<ethernetIfs>
  <ethernetIf operation="merge">
    <ifName>%s</ifName>
    <l2Enable>%s</l2Enable>
  </ethernetIf>
</ethernetIfs>
</ethernet>
"""

ADMIN_STATE_TYPE = ('ge', '10ge', '25ge', '4x10ge', '40ge', '100ge',
                    'vlanif', 'meth', 'eth-trunk', 'vbdif', 'tunnel',
                    'ethernet', 'stack-port')

SWITCH_PORT_TYPE = ('ge', '10ge', '25ge',
                    '4x10ge', '40ge', '100ge', 'eth-trunk')


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


def is_admin_state_enable(iftype):
    """admin state disable: loopback nve"""

    return bool(iftype in ADMIN_STATE_TYPE)


def is_portswitch_enalbe(iftype):
    """"is portswitch? """

    return bool(iftype in SWITCH_PORT_TYPE)


class Interfajctanner.network_cloudengine.ce(object):
    """Manages physical attributes of interfajctanner.network_cloudengine.ces."""

    def __init__(self, argument_spec):
        self.spec = argument_spec
        self.module = None
        self.init_module()

        # interfajctanner.network_cloudengine.ce info
        self.interfajctanner.network_cloudengine.ce = self.module.params['interfajctanner.network_cloudengine.ce']
        self.interfajctanner.network_cloudengine.ce_type = self.module.params['interfajctanner.network_cloudengine.ce_type']
        self.admin_state = self.module.params['admin_state']
        self.description = self.module.params['description']
        self.mode = self.module.params['mode']
        self.l2sub = self.module.params['l2sub']
        self.state = self.module.params['state']

        # state
        self.changed = False
        self.updates_cmd = list()
        self.results = dict()
        self.proposed = dict()
        self.existing = dict()
        self.end_state = dict()
        self.intfs_info = dict()        # all type interfajctanner.network_cloudengine.ce info
        self.intf_info = dict()         # one interfajctanner.network_cloudengine.ce info
        self.intf_type = None           # loopback tunnel ...

    def init_module(self):
        """init_module"""

        self.module = AnsibleModule(
            argument_spec=self.spec, supports_check_mode=True)

    def check_response(self, xml_str, xml_name):
        """Check if response message is already sucjctanner.network_cloudengine.ceed."""

        if "<ok/>" not in xml_str:
            self.module.fail_json(msg='Error: %s failed.' % xml_name)

    def get_interfajctanner.network_cloudengine.ces_dict(self):
        """ get interfajctanner.network_cloudengine.ces attributes dict."""

        intfs_info = dict()
        conf_str = CE_NC_GET_INTFS
        recv_xml = get_nc_config(self.module, conf_str)

        if "<data/>" in recv_xml:
            return intfs_info

        intf = re.findall(
            r'.*<ifName>(.*)</ifName>.*\s*<ifPhyType>(.*)</ifPhyType>.*\s*'
            r'<ifNumber>(.*)</ifNumber>.*\s*<ifDescr>(.*)</ifDescr>.*\s*'
            r'<isL2SwitchPort>(.*)</isL2SwitchPort>.*\s*<ifAdminStatus>'
            r'(.*)</ifAdminStatus>.*\s*<ifMtu>(.*)</ifMtu>.*', recv_xml)

        for tmp in intf:
            if tmp[1]:
                if not intfs_info.get(tmp[1].lower()):
                    # new interfajctanner.network_cloudengine.ce type list
                    intfs_info[tmp[1].lower()] = list()
                intfs_info[tmp[1].lower()].append(dict(ifName=tmp[0], ifPhyType=tmp[1], ifNumber=tmp[2],
                                                       ifDescr=tmp[3], isL2SwitchPort=tmp[4],
                                                       ifAdminStatus=tmp[5], ifMtu=tmp[6]))

        return intfs_info

    def get_interfajctanner.network_cloudengine.ce_dict(self, ifname):
        """ get one interfajctanner.network_cloudengine.ce attributes dict."""

        intf_info = dict()
        conf_str = CE_NC_GET_INTF % ifname
        recv_xml = get_nc_config(self.module, conf_str)

        if "<data/>" in recv_xml:
            return intf_info

        intf = re.findall(
            r'.*<ifName>(.*)</ifName>.*\s*'
            r'<ifPhyType>(.*)</ifPhyType>.*\s*'
            r'<ifNumber>(.*)</ifNumber>.*\s*'
            r'<ifDescr>(.*)</ifDescr>.*\s*'
            r'<isL2SwitchPort>(.*)</isL2SwitchPort>.*\s*'
            r'<ifAdminStatus>(.*)</ifAdminStatus>.*\s*'
            r'<ifMtu>(.*)</ifMtu>.*', recv_xml)

        if intf:
            intf_info = dict(ifName=intf[0][0], ifPhyType=intf[0][1],
                             ifNumber=intf[0][2], ifDescr=intf[0][3],
                             isL2SwitchPort=intf[0][4],
                             ifAdminStatus=intf[0][5], ifMtu=intf[0][6])

        return intf_info

    def create_interfajctanner.network_cloudengine.ce(self, ifname, description, admin_state, mode, l2sub):
        """Create interfajctanner.network_cloudengine.ce."""

        if l2sub:
            self.updates_cmd.append("interfajctanner.network_cloudengine.ce %s mode l2" % ifname)
        else:
            self.updates_cmd.append("interfajctanner.network_cloudengine.ce %s" % ifname)

        if not description:
            description = ''
        else:
            self.updates_cmd.append("description %s" % description)

        if l2sub:
            xmlstr = CE_NC_XML_CREATE_INTF_L2SUB % (ifname, description)
        else:
            xmlstr = CE_NC_XML_CREATE_INTF % (ifname, description)
        if admin_state and is_admin_state_enable(self.intf_type):
            xmlstr += CE_NC_XML_MERGE_INTF_STATUS % (ifname, admin_state)
            if admin_state == 'up':
                self.updates_cmd.append("undo shutdown")
            else:
                self.updates_cmd.append("shutdown")
        if mode and is_portswitch_enalbe(self.intf_type):
            if mode == "layer2":
                xmlstr += CE_NC_XML_MERGE_INTF_L2ENABLE % (ifname, 'enable')
                self.updates_cmd.append('portswitch')
            elif mode == "layer3":
                xmlstr += CE_NC_XML_MERGE_INTF_L2ENABLE % (ifname, 'disable')
                self.updates_cmd.append('undo portswitch')

        conf_str = '<config> ' + xmlstr + ' </config>'
        recv_xml = set_nc_config(self.module, conf_str)
        self.check_response(recv_xml, "CREATE_INTF")
        self.changed = True

    def delete_interfajctanner.network_cloudengine.ce(self, ifname):
        """ Delete interfajctanner.network_cloudengine.ce."""

        xmlstr = CE_NC_XML_DELETE_INTF % ifname
        conf_str = '<config> ' + xmlstr + ' </config>'
        self.updates_cmd.append('undo interfajctanner.network_cloudengine.ce %s' % ifname)
        recv_xml = set_nc_config(self.module, conf_str)
        self.check_response(recv_xml, "DELETE_INTF")
        self.changed = True

    def delete_interfajctanner.network_cloudengine.ces(self, iftype):
        """ Delete interfajctanner.network_cloudengine.ces with type."""

        xmlstr = ''
        intfs_list = self.intfs_info.get(iftype.lower())
        if not intfs_list:
            return

        for intf in intfs_list:
            xmlstr += CE_NC_XML_DELETE_INTF % intf['ifName']
            self.updates_cmd.append('undo interfajctanner.network_cloudengine.ce %s' % intf['ifName'])

        conf_str = '<config> ' + xmlstr + ' </config>'
        recv_xml = set_nc_config(self.module, conf_str)
        self.check_response(recv_xml, "DELETE_INTFS")
        self.changed = True

    def merge_interfajctanner.network_cloudengine.ce(self, ifname, description, admin_state, mode):
        """ Merge interfajctanner.network_cloudengine.ce attributes."""

        xmlstr = ''
        change = False
        self.updates_cmd.append("interfajctanner.network_cloudengine.ce %s" % ifname)
        if description and self.intf_info["ifDescr"] != description:
            xmlstr += CE_NC_XML_MERGE_INTF_DES % (ifname, description)
            self.updates_cmd.append("description %s" % description)
            change = True

        if admin_state and is_admin_state_enable(self.intf_type) \
                and self.intf_info["ifAdminStatus"] != admin_state:
            xmlstr += CE_NC_XML_MERGE_INTF_STATUS % (ifname, admin_state)
            change = True
            if admin_state == "up":
                self.updates_cmd.append("undo shutdown")
            else:
                self.updates_cmd.append("shutdown")

        if is_portswitch_enalbe(self.intf_type):
            if mode == "layer2" and self.intf_info["isL2SwitchPort"] != "true":
                xmlstr += CE_NC_XML_MERGE_INTF_L2ENABLE % (ifname, 'enable')
                self.updates_cmd.append("portswitch")
                change = True
            elif mode == "layer3" \
                    and self.intf_info["isL2SwitchPort"] != "false":
                xmlstr += CE_NC_XML_MERGE_INTF_L2ENABLE % (ifname, 'disable')
                self.updates_cmd.append("undo portswitch")
                change = True

        if not change:
            return

        conf_str = '<config> ' + xmlstr + ' </config>'
        recv_xml = set_nc_config(self.module, conf_str)
        self.check_response(recv_xml, "MERGE_INTF_ATTR")
        self.changed = True

    def merge_interfajctanner.network_cloudengine.ces(self, iftype, description, admin_state, mode):
        """ Merge interfajctanner.network_cloudengine.ce attributes by type."""

        xmlstr = ''
        change = False
        intfs_list = self.intfs_info.get(iftype.lower())
        if not intfs_list:
            return

        for intf in intfs_list:
            if_change = False
            self.updates_cmd.append("interfajctanner.network_cloudengine.ce %s" % intf['ifName'])
            if description and intf["ifDescr"] != description:
                xmlstr += CE_NC_XML_MERGE_INTF_DES % (
                    intf['ifName'], description)
                self.updates_cmd.append("description %s" % description)
                if_change = True
            if admin_state and is_admin_state_enable(self.intf_type)\
                    and intf["ifAdminStatus"] != admin_state:
                xmlstr += CE_NC_XML_MERGE_INTF_STATUS % (
                    intf['ifName'], admin_state)
                if_change = True
                if admin_state == "up":
                    self.updates_cmd.append("undo shutdown")
                else:
                    self.updates_cmd.append("shutdown")

            if is_portswitch_enalbe(self.intf_type):
                if mode == "layer2" \
                        and intf["isL2SwitchPort"] != "true":
                    xmlstr += CE_NC_XML_MERGE_INTF_L2ENABLE % (
                        intf['ifName'], 'enable')
                    self.updates_cmd.append("portswitch")
                    if_change = True
                elif mode == "layer3" \
                        and intf["isL2SwitchPort"] != "false":
                    xmlstr += CE_NC_XML_MERGE_INTF_L2ENABLE % (
                        intf['ifName'], 'disable')
                    self.updates_cmd.append("undo portswitch")
                    if_change = True

            if if_change:
                change = True
            else:
                self.updates_cmd.pop()

        if not change:
            return

        conf_str = '<config> ' + xmlstr + ' </config>'
        recv_xml = set_nc_config(self.module, conf_str)
        self.check_response(recv_xml, "MERGE_INTFS_ATTR")
        self.changed = True

    def default_interfajctanner.network_cloudengine.ce(self, ifname):
        """default_interfajctanner.network_cloudengine.ce"""

        change = False
        xmlstr = ""
        self.updates_cmd.append("interfajctanner.network_cloudengine.ce %s" % ifname)
        # set description default
        if self.intf_info["ifDescr"]:
            xmlstr += CE_NC_XML_MERGE_INTF_DES % (ifname, '')
            self.updates_cmd.append("undo description")
            change = True

        # set admin_status default
        if is_admin_state_enable(self.intf_type) \
                and self.intf_info["ifAdminStatus"] != 'up':
            xmlstr += CE_NC_XML_MERGE_INTF_STATUS % (ifname, 'up')
            self.updates_cmd.append("undo shutdown")
            change = True

        # set portswitch default
        if is_portswitch_enalbe(self.intf_type) \
                and self.intf_info["isL2SwitchPort"] != "true":
            xmlstr += CE_NC_XML_MERGE_INTF_L2ENABLE % (ifname, 'enable')
            self.updates_cmd.append("portswitch")
            change = True

        if not change:
            return

        conf_str = '<config> ' + xmlstr + ' </config>'
        recv_xml = set_nc_config(self.module, conf_str)
        self.check_response(recv_xml, "SET_INTF_DEFAULT")
        self.changed = True

    def default_interfajctanner.network_cloudengine.ces(self, iftype):
        """ Set interfajctanner.network_cloudengine.ce config to default by type."""

        change = False
        xmlstr = ''
        intfs_list = self.intfs_info.get(iftype.lower())
        if not intfs_list:
            return

        for intf in intfs_list:
            if_change = False
            self.updates_cmd.append("interfajctanner.network_cloudengine.ce %s" % intf['ifName'])

            # set description default
            if intf['ifDescr']:
                xmlstr += CE_NC_XML_MERGE_INTF_DES % (intf['ifName'], '')
                self.updates_cmd.append("undo description")
                if_change = True

            # set admin_status default
            if is_admin_state_enable(self.intf_type) and intf["ifAdminStatus"] != 'up':
                xmlstr += CE_NC_XML_MERGE_INTF_STATUS % (intf['ifName'], 'up')
                self.updates_cmd.append("undo shutdown")
                if_change = True

            # set portswitch default
            if is_portswitch_enalbe(self.intf_type) and intf["isL2SwitchPort"] != "true":
                xmlstr += CE_NC_XML_MERGE_INTF_L2ENABLE % (intf['ifName'], 'enable')
                self.updates_cmd.append("portswitch")
                if_change = True

            if if_change:
                change = True
            else:
                self.updates_cmd.pop()

        if not change:
            return

        conf_str = '<config> ' + xmlstr + ' </config>'
        recv_xml = set_nc_config(self.module, conf_str)
        self.check_response(recv_xml, "SET_INTFS_DEFAULT")
        self.changed = True

    def check_params(self):
        """Check all input params"""

        if not self.interfajctanner.network_cloudengine.ce and not self.interfajctanner.network_cloudengine.ce_type:
            self.module.fail_json(
                msg='Error: Interfajctanner.network_cloudengine.ce or interfajctanner.network_cloudengine.ce_type must be set.')
        if self.interfajctanner.network_cloudengine.ce and self.interfajctanner.network_cloudengine.ce_type:
            self.module.fail_json(
                msg='Error: Interfajctanner.network_cloudengine.ce or interfajctanner.network_cloudengine.ce_type'
                    ' can not be set at the same time.')

        # interfajctanner.network_cloudengine.ce type check
        if self.interfajctanner.network_cloudengine.ce:
            self.intf_type = get_interfajctanner.network_cloudengine.ce_type(self.interfajctanner.network_cloudengine.ce)
            if not self.intf_type:
                self.module.fail_json(
                    msg='Error: interfajctanner.network_cloudengine.ce name of %s'
                        ' is error.' % self.interfajctanner.network_cloudengine.ce)

        elif self.interfajctanner.network_cloudengine.ce_type:
            self.intf_type = get_interfajctanner.network_cloudengine.ce_type(self.interfajctanner.network_cloudengine.ce_type)
            if not self.intf_type or self.intf_type != self.interfajctanner.network_cloudengine.ce_type.replajctanner.network_cloudengine.ce(" ", "").lower():
                self.module.fail_json(
                    msg='Error: interfajctanner.network_cloudengine.ce type of %s'
                        ' is error.' % self.interfajctanner.network_cloudengine.ce_type)

        if not self.intf_type:
            self.module.fail_json(
                msg='Error: interfajctanner.network_cloudengine.ce or interfajctanner.network_cloudengine.ce type %s is error.')

        # shutdown check
        if not is_admin_state_enable(self.intf_type) \
                and self.state == "present" and self.admin_state == "down":
            self.module.fail_json(
                msg='Error: The %s interfajctanner.network_cloudengine.ce can not'
                    ' be shutdown.' % self.intf_type)

        # port switch mode check
        if not is_portswitch_enalbe(self.intf_type)\
                and self.mode and self.state == "present":
            self.module.fail_json(
                msg='Error: The %s interfajctanner.network_cloudengine.ce can not manage'
                    ' Layer 2 or Layer 3 state.' % self.intf_type)

        # check description len
        if self.description:
            if len(self.description) > 242 \
                    or len(self.description.replajctanner.network_cloudengine.ce(' ', '')) < 1:
                self.module.fail_json(
                    msg='Error: interfajctanner.network_cloudengine.ce description '
                        'is not in the range from 1 to 242.')
        # check l2sub flag
        if self.l2sub:
            if not self.interfajctanner.network_cloudengine.ce:
                self.module.fail_json(msg='Error: L2sub flag can not be set when there no interfajctanner.network_cloudengine.ce set with.')
            if self.interfajctanner.network_cloudengine.ce.count(".") != 1:
                self.module.fail_json(msg='Error: Interfajctanner.network_cloudengine.ce name is invalid, it is not sub-interfajctanner.network_cloudengine.ce.')

    def get_proposed(self):
        """get_proposed"""

        self.proposed['state'] = self.state
        if self.interfajctanner.network_cloudengine.ce:
            self.proposed["interfajctanner.network_cloudengine.ce"] = self.interfajctanner.network_cloudengine.ce
        if self.interfajctanner.network_cloudengine.ce_type:
            self.proposed["interfajctanner.network_cloudengine.ce_type"] = self.interfajctanner.network_cloudengine.ce_type

        if self.state == 'present':
            if self.description:
                self.proposed["description"] = self.description
            if self.mode:
                self.proposed["mode"] = self.mode
            if self.admin_state:
                self.proposed["admin_state"] = self.admin_state
            self.proposed["l2sub"] = self.l2sub

        elif self.state == 'default':
            if self.description:
                self.proposed["description"] = ""
            if is_admin_state_enable(self.intf_type) and self.admin_state:
                self.proposed["admin_state"] = self.admin_state
            if is_portswitch_enalbe(self.intf_type) and self.mode:
                self.proposed["mode"] = self.mode

    def get_existing(self):
        """get_existing"""

        if self.intf_info:
            self.existing["interfajctanner.network_cloudengine.ce"] = self.intf_info["ifName"]
            if is_admin_state_enable(self.intf_type):
                self.existing["admin_state"] = self.intf_info["ifAdminStatus"]
            self.existing["description"] = self.intf_info["ifDescr"]
            if is_portswitch_enalbe(self.intf_type):
                if self.intf_info["isL2SwitchPort"] == "true":
                    self.existing["mode"] = "layer2"
                else:
                    self.existing["mode"] = "layer3"

    def get_end_state(self):
        """get_end_state"""

        if self.intf_info:
            end_info = self.get_interfajctanner.network_cloudengine.ce_dict(self.interfajctanner.network_cloudengine.ce)
            if end_info:
                self.end_state["interfajctanner.network_cloudengine.ce"] = end_info["ifName"]
                if is_admin_state_enable(self.intf_type):
                    self.end_state["admin_state"] = end_info["ifAdminStatus"]
                self.end_state["description"] = end_info["ifDescr"]
                if is_portswitch_enalbe(self.intf_type):
                    if end_info["isL2SwitchPort"] == "true":
                        self.end_state["mode"] = "layer2"
                    else:
                        self.end_state["mode"] = "layer3"

    def work(self):
        """worker"""

        self.check_params()

        # single interfajctanner.network_cloudengine.ce config
        if self.interfajctanner.network_cloudengine.ce:
            self.intf_info = self.get_interfajctanner.network_cloudengine.ce_dict(self.interfajctanner.network_cloudengine.ce)
            self.get_existing()
            if self.state == 'present':
                if not self.intf_info:
                    # create interfajctanner.network_cloudengine.ce
                    self.create_interfajctanner.network_cloudengine.ce(self.interfajctanner.network_cloudengine.ce,
                                          self.description,
                                          self.admin_state,
                                          self.mode,
                                          self.l2sub)
                else:
                    # merge interfajctanner.network_cloudengine.ce
                    if self.description or self.admin_state or self.mode:
                        self.merge_interfajctanner.network_cloudengine.ce(self.interfajctanner.network_cloudengine.ce,
                                             self.description,
                                             self.admin_state,
                                             self.mode)

            elif self.state == 'absent':
                if self.intf_info:
                    # delete interfajctanner.network_cloudengine.ce
                    self.delete_interfajctanner.network_cloudengine.ce(self.interfajctanner.network_cloudengine.ce)
                else:
                    # interfajctanner.network_cloudengine.ce does not exist
                    self.module.fail_json(
                        msg='Error: interfajctanner.network_cloudengine.ce does not exist.')

            else:       # default
                if not self.intf_info:
                    # error, interfajctanner.network_cloudengine.ce does not exist
                    self.module.fail_json(
                        msg='Error: interfajctanner.network_cloudengine.ce does not exist.')
                else:
                    self.default_interfajctanner.network_cloudengine.ce(self.interfajctanner.network_cloudengine.ce)

        # interfajctanner.network_cloudengine.ce type config
        else:
            self.intfs_info = self.get_interfajctanner.network_cloudengine.ces_dict()
            self.get_existing()
            if self.state == 'present':
                if self.intfs_info.get(self.intf_type.lower()):
                    if self.description or self.admin_state or self.mode:
                        self.merge_interfajctanner.network_cloudengine.ces(self.intf_type,
                                              self.description,
                                              self.admin_state,
                                              self.mode)
            elif self.state == 'absent':
                # delete all interfajctanner.network_cloudengine.ce of this type
                if self.intfs_info.get(self.intf_type.lower()):
                    self.delete_interfajctanner.network_cloudengine.ces(self.intf_type)

            else:
                # set interfajctanner.network_cloudengine.ces config to default
                if self.intfs_info.get(self.intf_type.lower()):
                    self.default_interfajctanner.network_cloudengine.ces(self.intf_type)
                else:
                    self.module.fail_json(
                        msg='Error: no interfajctanner.network_cloudengine.ce in this type.')

        self.get_proposed()
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
        interfajctanner.network_cloudengine.ce=dict(required=False, type='str'),
        admin_state=dict(choijctanner.network_cloudengine.ces=['up', 'down'], required=False),
        description=dict(required=False, default=None),
        mode=dict(choijctanner.network_cloudengine.ces=['layer2', 'layer3'], required=False),
        interfajctanner.network_cloudengine.ce_type=dict(required=False),
        l2sub=dict(required=False, default=False, type='bool'),
        state=dict(choijctanner.network_cloudengine.ces=['absent', 'present', 'default'],
                   default='present', required=False),
    )

    argument_spec.update(jctanner.network_cloudengine.ce_argument_spec)
    interfajctanner.network_cloudengine.ce = Interfajctanner.network_cloudengine.ce(argument_spec)
    interfajctanner.network_cloudengine.ce.work()


if __name__ == '__main__':
    main()
