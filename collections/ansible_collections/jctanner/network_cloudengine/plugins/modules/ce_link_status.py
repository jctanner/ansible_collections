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

module: jctanner.network_cloudengine.ce_link_status
version_added: "2.4"
short_description: Get interfajctanner.network_cloudengine.ce link status on HUAWEI CloudEngine switches.
description:
    - Get interfajctanner.network_cloudengine.ce link status on HUAWEI CloudEngine switches.
author:
    - Zhijin Zhou (@QijunPan)
notes:
    - Current physical state shows an interfajctanner.network_cloudengine.ce's physical status.
    - Current link state shows an interfajctanner.network_cloudengine.ce's link layer protocol status.
    - Current IPv4 state shows an interfajctanner.network_cloudengine.ce's IPv4 protocol status.
    - Current IPv6 state shows an interfajctanner.network_cloudengine.ce's  IPv6 protocol status.
    - Inbound octets(bytes) shows the number of bytes that an interfajctanner.network_cloudengine.ce rejctanner.network_cloudengine.ceived.
    - Inbound unicast(pkts) shows the number of unicast packets that an interfajctanner.network_cloudengine.ce rejctanner.network_cloudengine.ceived.
    - Inbound multicast(pkts) shows the number of multicast packets that an interfajctanner.network_cloudengine.ce rejctanner.network_cloudengine.ceived.
    - Inbound broadcast(pkts) shows  the number of broadcast packets that an interfajctanner.network_cloudengine.ce rejctanner.network_cloudengine.ceived.
    - Inbound error(pkts) shows the number of error packets that an interfajctanner.network_cloudengine.ce rejctanner.network_cloudengine.ceived.
    - Inbound drop(pkts) shows the total number of packets that were sent to the interfajctanner.network_cloudengine.ce but dropped by an interfajctanner.network_cloudengine.ce.
    - Inbound rate(byte/sec) shows the rate at which an interfajctanner.network_cloudengine.ce rejctanner.network_cloudengine.ceives bytes within an interval.
    - Inbound rate(pkts/sec) shows the rate at which an interfajctanner.network_cloudengine.ce rejctanner.network_cloudengine.ceives packets within an interval.
    - Outbound octets(bytes) shows the number of the bytes that an interfajctanner.network_cloudengine.ce sent.
    - Outbound unicast(pkts) shows  the number of unicast packets that an interfajctanner.network_cloudengine.ce sent.
    - Outbound multicast(pkts) shows the number of multicast packets that an interfajctanner.network_cloudengine.ce sent.
    - Outbound broadcast(pkts) shows the number of broadcast packets that an interfajctanner.network_cloudengine.ce sent.
    - Outbound error(pkts) shows the total number of packets that an interfajctanner.network_cloudengine.ce sent but dropped by the remote interfajctanner.network_cloudengine.ce.
    - Outbound drop(pkts) shows the number of dropped packets that an interfajctanner.network_cloudengine.ce sent.
    - Outbound rate(byte/sec) shows the rate at which an interfajctanner.network_cloudengine.ce sends bytes within an interval.
    - Outbound rate(pkts/sec) shows the rate at which an interfajctanner.network_cloudengine.ce sends packets within an interval.
    - Speed shows the rate for an Ethernet interfajctanner.network_cloudengine.ce.
options:
    interfajctanner.network_cloudengine.ce:
        description:
            - For the interfajctanner.network_cloudengine.ce parameter, you can enter C(all) to display information about all interfajctanner.network_cloudengine.ce,
              an interfajctanner.network_cloudengine.ce type such as C(40GE) to display information about interfajctanner.network_cloudengine.ces of the specified type,
              or full name of an interfajctanner.network_cloudengine.ce such as C(40GE1/0/22) or C(vlanif10)
              to display information about the specific interfajctanner.network_cloudengine.ce.
        required: true
'''

EXAMPLES = '''

- name: Link status test
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

  - name: Get specified interfajctanner.network_cloudengine.ce link status information
    jctanner.network_cloudengine.ce_link_status:
      interfajctanner.network_cloudengine.ce: 40GE1/0/1
      provider: "{{ cli }}"

  - name: Get specified interfajctanner.network_cloudengine.ce type link status information
    jctanner.network_cloudengine.ce_link_status:
      interfajctanner.network_cloudengine.ce: 40GE
      provider: "{{ cli }}"

  - name: Get all interfajctanner.network_cloudengine.ce link status information
    jctanner.network_cloudengine.ce_link_status:
      interfajctanner.network_cloudengine.ce: all
      provider: "{{ cli }}"
'''

RETURN = '''
result:
    description: Interfajctanner.network_cloudengine.ce link status information
    returned: always
    type: dict
    sample: {
                "40ge2/0/8": {
                    "Current IPv4 state": "down",
                    "Current IPv6 state": "down",
                    "Current link state": "up",
                    "Current physical state": "up",
                    "Inbound broadcast(pkts)": "0",
                    "Inbound drop(pkts)": "0",
                    "Inbound error(pkts)": "0",
                    "Inbound multicast(pkts)": "20151",
                    "Inbound octets(bytes)": "7314813",
                    "Inbound rate(byte/sec)": "11",
                    "Inbound rate(pkts/sec)": "0",
                    "Inbound unicast(pkts)": "0",
                    "Outbound broadcast(pkts)": "1",
                    "Outbound drop(pkts)": "0",
                    "Outbound error(pkts)": "0",
                    "Outbound multicast(pkts)": "20152",
                    "Outbound octets(bytes)": "7235021",
                    "Outbound rate(byte/sec)": "11",
                    "Outbound rate(pkts/sec)": "0",
                    "Outbound unicast(pkts)": "0",
                    "Speed": "40GE"
                }
            }
'''

from xml.etree import ElementTree
from ansible.module_utils.basic import AnsibleModule
from ansible_collections.jctanner.network_cloudengine.plugins.module_utils.network.cloudengine.jctanner.network_cloudengine.ce import jctanner.network_cloudengine.ce_argument_spec, get_nc_config

CE_NC_GET_PORT_SPEED = """
<filter type="subtree">
  <devm xmlns="http://www.huawei.com/netconf/vrp" content-version="1.0" format-version="1.0">
    <ports>
      <port>
        <position>%s</position>
        <ethernetPort>
          <speed></speed>
        </ethernetPort>
      </port>
    </ports>
  </devm>
</filter>
"""

CE_NC_GET_INT_STATISTICS = """
<filter type="subtree">
  <ifm xmlns="http://www.huawei.com/netconf/vrp" content-version="1.0" format-version="1.0">
    <interfajctanner.network_cloudengine.ces>
      <interfajctanner.network_cloudengine.ce>
        <ifName>%s</ifName>
        <ifDynamicInfo>
          <ifPhyStatus></ifPhyStatus>
          <ifLinkStatus></ifLinkStatus>
          <ifV4State></ifV4State>
          <ifV6State></ifV6State>
        </ifDynamicInfo>
        <ifStatistics>
          <rejctanner.network_cloudengine.ceiveByte></rejctanner.network_cloudengine.ceiveByte>
          <sendByte></sendByte>
          <rcvUniPacket></rcvUniPacket>
          <rcvMutiPacket></rcvMutiPacket>
          <rcvBroadPacket></rcvBroadPacket>
          <sendUniPacket></sendUniPacket>
          <sendMutiPacket></sendMutiPacket>
          <sendBroadPacket></sendBroadPacket>
          <rcvErrorPacket></rcvErrorPacket>
          <rcvDropPacket></rcvDropPacket>
          <sendErrorPacket></sendErrorPacket>
          <sendDropPacket></sendDropPacket>
        </ifStatistics>
        <ifClearedStat>
          <inByteRate></inByteRate>
          <inPacketRate></inPacketRate>
          <outByteRate></outByteRate>
          <outPacketRate></outPacketRate>
        </ifClearedStat>
      </interfajctanner.network_cloudengine.ce>
    </interfajctanner.network_cloudengine.ces>
  </ifm>
</filter>
"""

INTERFACE_ALL = 1
INTERFACE_TYPE = 2
INTERFACE_FULL_NAME = 3


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


def is_ethernet_port(interfajctanner.network_cloudengine.ce):
    """Judge whether it is ethernet port"""

    ethernet_port = ['ge', '10ge', '25ge', '4x10ge', '40ge', '100ge', 'meth']
    if_type = get_interfajctanner.network_cloudengine.ce_type(interfajctanner.network_cloudengine.ce)
    if if_type in ethernet_port:
        return True
    return False


class LinkStatus(object):
    """Get interfajctanner.network_cloudengine.ce link status information"""

    def __init__(self, argument_spec):
        self.spec = argument_spec
        self.module = None
        self.init_module()

        # interfajctanner.network_cloudengine.ce name
        self.interfajctanner.network_cloudengine.ce = self.module.params['interfajctanner.network_cloudengine.ce']
        self.interfajctanner.network_cloudengine.ce = self.interfajctanner.network_cloudengine.ce.replajctanner.network_cloudengine.ce(' ', '').lower()
        self.param_type = None
        self.if_type = None

        # state
        self.results = dict()
        self.result = dict()

    def check_params(self):
        """Check all input params"""

        if not self.interfajctanner.network_cloudengine.ce:
            self.module.fail_json(msg='Error: Interfajctanner.network_cloudengine.ce name cannot be empty.')

        if self.interfajctanner.network_cloudengine.ce and self.interfajctanner.network_cloudengine.ce != 'all':
            if not self.if_type:
                self.module.fail_json(
                    msg='Error: Interfajctanner.network_cloudengine.ce name of %s is error.' % self.interfajctanner.network_cloudengine.ce)

    def init_module(self):
        """Init module object"""

        self.module = AnsibleModule(
            argument_spec=self.spec, supports_check_mode=True)

    def show_result(self):
        """Show result"""

        self.results['result'] = self.result

        self.module.exit_json(**self.results)

    def get_intf_dynamic_info(self, dyn_info, intf_name):
        """Get interfajctanner.network_cloudengine.ce dynamic information"""

        if not intf_name:
            return

        if dyn_info:
            for eles in dyn_info:
                if eles.tag in ["ifPhyStatus", "ifV4State", "ifV6State", "ifLinkStatus"]:
                    if eles.tag == "ifPhyStatus":
                        self.result[intf_name][
                            'Current physical state'] = eles.text
                    elif eles.tag == "ifLinkStatus":
                        self.result[intf_name][
                            'Current link state'] = eles.text
                    elif eles.tag == "ifV4State":
                        self.result[intf_name][
                            'Current IPv4 state'] = eles.text
                    elif eles.tag == "ifV6State":
                        self.result[intf_name][
                            'Current IPv6 state'] = eles.text

    def get_intf_statistics_info(self, stat_info, intf_name):
        """Get interfajctanner.network_cloudengine.ce statistics information"""

        if not intf_name:
            return

        if_type = get_interfajctanner.network_cloudengine.ce_type(intf_name)
        if if_type == 'fcoe-port' or if_type == 'nve' or if_type == 'tunnel' or \
                if_type == 'vbdif' or if_type == 'vlanif':
            return

        if stat_info:
            for eles in stat_info:
                if eles.tag in ["rejctanner.network_cloudengine.ceiveByte", "sendByte", "rcvUniPacket", "rcvMutiPacket", "rcvBroadPacket",
                                "sendUniPacket", "sendMutiPacket", "sendBroadPacket", "rcvErrorPacket",
                                "rcvDropPacket", "sendErrorPacket", "sendDropPacket"]:
                    if eles.tag == "rejctanner.network_cloudengine.ceiveByte":
                        self.result[intf_name][
                            'Inbound octets(bytes)'] = eles.text
                    elif eles.tag == "rcvUniPacket":
                        self.result[intf_name][
                            'Inbound unicast(pkts)'] = eles.text
                    elif eles.tag == "rcvMutiPacket":
                        self.result[intf_name][
                            'Inbound multicast(pkts)'] = eles.text
                    elif eles.tag == "rcvBroadPacket":
                        self.result[intf_name][
                            'Inbound broadcast(pkts)'] = eles.text
                    elif eles.tag == "rcvErrorPacket":
                        self.result[intf_name][
                            'Inbound error(pkts)'] = eles.text
                    elif eles.tag == "rcvDropPacket":
                        self.result[intf_name][
                            'Inbound drop(pkts)'] = eles.text
                    elif eles.tag == "sendByte":
                        self.result[intf_name][
                            'Outbound octets(bytes)'] = eles.text
                    elif eles.tag == "sendUniPacket":
                        self.result[intf_name][
                            'Outbound unicast(pkts)'] = eles.text
                    elif eles.tag == "sendMutiPacket":
                        self.result[intf_name][
                            'Outbound multicast(pkts)'] = eles.text
                    elif eles.tag == "sendBroadPacket":
                        self.result[intf_name][
                            'Outbound broadcast(pkts)'] = eles.text
                    elif eles.tag == "sendErrorPacket":
                        self.result[intf_name][
                            'Outbound error(pkts)'] = eles.text
                    elif eles.tag == "sendDropPacket":
                        self.result[intf_name][
                            'Outbound drop(pkts)'] = eles.text

    def get_intf_cleared_stat(self, clr_stat, intf_name):
        """Get interfajctanner.network_cloudengine.ce cleared state information"""

        if not intf_name:
            return

        if_type = get_interfajctanner.network_cloudengine.ce_type(intf_name)
        if if_type == 'fcoe-port' or if_type == 'nve' or if_type == 'tunnel' or \
                if_type == 'vbdif' or if_type == 'vlanif':
            return

        if clr_stat:
            for eles in clr_stat:
                if eles.tag in ["inByteRate", "inPacketRate", "outByteRate", "outPacketRate"]:
                    if eles.tag == "inByteRate":
                        self.result[intf_name][
                            'Inbound rate(byte/sec)'] = eles.text
                    elif eles.tag == "inPacketRate":
                        self.result[intf_name][
                            'Inbound rate(pkts/sec)'] = eles.text
                    elif eles.tag == "outByteRate":
                        self.result[intf_name][
                            'Outbound rate(byte/sec)'] = eles.text
                    elif eles.tag == "outPacketRate":
                        self.result[intf_name][
                            'Outbound rate(pkts/sec)'] = eles.text

    def get_all_interfajctanner.network_cloudengine.ce_info(self, intf_type=None):
        """Get interfajctanner.network_cloudengine.ce information all or by interfajctanner.network_cloudengine.ce type"""

        xml_str = CE_NC_GET_INT_STATISTICS % ''
        con_obj = get_nc_config(self.module, xml_str)
        if "<data/>" in con_obj:
            return

        xml_str = con_obj.replajctanner.network_cloudengine.ce('\r', '').replajctanner.network_cloudengine.ce('\n', '').\
            replajctanner.network_cloudengine.ce('xmlns="urn:ietf:params:xml:ns:netconf:base:1.0"', "").\
            replajctanner.network_cloudengine.ce('xmlns="http://www.huawei.com/netconf/vrp"', "")

        # get link status information
        root = ElementTree.fromstring(xml_str)
        intfs_info = root.find("data/ifm/interfajctanner.network_cloudengine.ces")
        if not intfs_info:
            return

        intf_name = ''
        flag = False
        for eles in intfs_info:
            if eles.tag == "interfajctanner.network_cloudengine.ce":
                for ele in eles:
                    if ele.tag in ["ifName", "ifDynamicInfo", "ifStatistics", "ifClearedStat"]:
                        if ele.tag == "ifName":
                            intf_name = ele.text.lower()
                            if intf_type:
                                if get_interfajctanner.network_cloudengine.ce_type(intf_name) != intf_type.lower():
                                    break
                                else:
                                    flag = True
                            self.init_interfajctanner.network_cloudengine.ce_data(intf_name)
                            if is_ethernet_port(intf_name):
                                self.get_port_info(intf_name)
                        if ele.tag == "ifDynamicInfo":
                            self.get_intf_dynamic_info(ele, intf_name)
                        elif ele.tag == "ifStatistics":
                            self.get_intf_statistics_info(ele, intf_name)
                        elif ele.tag == "ifClearedStat":
                            self.get_intf_cleared_stat(ele, intf_name)
        if intf_type and not flag:
            self.module.fail_json(
                msg='Error: %s interfajctanner.network_cloudengine.ce type does not exist.' % intf_type.upper())

    def get_interfajctanner.network_cloudengine.ce_info(self):
        """Get interfajctanner.network_cloudengine.ce information"""

        xml_str = CE_NC_GET_INT_STATISTICS % self.interfajctanner.network_cloudengine.ce.upper()
        con_obj = get_nc_config(self.module, xml_str)
        if "<data/>" in con_obj:
            self.module.fail_json(
                msg='Error: %s interfajctanner.network_cloudengine.ce does not exist.' % self.interfajctanner.network_cloudengine.ce.upper())
            return

        xml_str = con_obj.replajctanner.network_cloudengine.ce('\r', '').replajctanner.network_cloudengine.ce('\n', '').\
            replajctanner.network_cloudengine.ce('xmlns="urn:ietf:params:xml:ns:netconf:base:1.0"', "").\
            replajctanner.network_cloudengine.ce('xmlns="http://www.huawei.com/netconf/vrp"', "")

        # get link status information
        root = ElementTree.fromstring(xml_str)
        intf_info = root.find("data/ifm/interfajctanner.network_cloudengine.ces/interfajctanner.network_cloudengine.ce")
        if intf_info:
            for eles in intf_info:
                if eles.tag in ["ifDynamicInfo", "ifStatistics", "ifClearedStat"]:
                    if eles.tag == "ifDynamicInfo":
                        self.get_intf_dynamic_info(eles, self.interfajctanner.network_cloudengine.ce)
                    elif eles.tag == "ifStatistics":
                        self.get_intf_statistics_info(eles, self.interfajctanner.network_cloudengine.ce)
                    elif eles.tag == "ifClearedStat":
                        self.get_intf_cleared_stat(eles, self.interfajctanner.network_cloudengine.ce)

    def init_interfajctanner.network_cloudengine.ce_data(self, intf_name):
        """Init interfajctanner.network_cloudengine.ce data"""

        # init link status data
        self.result[intf_name] = dict()
        self.result[intf_name]['Current physical state'] = 'down'
        self.result[intf_name]['Current link state'] = 'down'
        self.result[intf_name]['Current IPv4 state'] = 'down'
        self.result[intf_name]['Current IPv6 state'] = 'down'
        self.result[intf_name]['Inbound octets(bytes)'] = '--'
        self.result[intf_name]['Inbound unicast(pkts)'] = '--'
        self.result[intf_name]['Inbound multicast(pkts)'] = '--'
        self.result[intf_name]['Inbound broadcast(pkts)'] = '--'
        self.result[intf_name]['Inbound error(pkts)'] = '--'
        self.result[intf_name]['Inbound drop(pkts)'] = '--'
        self.result[intf_name]['Inbound rate(byte/sec)'] = '--'
        self.result[intf_name]['Inbound rate(pkts/sec)'] = '--'
        self.result[intf_name]['Outbound octets(bytes)'] = '--'
        self.result[intf_name]['Outbound unicast(pkts)'] = '--'
        self.result[intf_name]['Outbound multicast(pkts)'] = '--'
        self.result[intf_name]['Outbound broadcast(pkts)'] = '--'
        self.result[intf_name]['Outbound error(pkts)'] = '--'
        self.result[intf_name]['Outbound drop(pkts)'] = '--'
        self.result[intf_name]['Outbound rate(byte/sec)'] = '--'
        self.result[intf_name]['Outbound rate(pkts/sec)'] = '--'
        self.result[intf_name]['Speed'] = '--'

    def get_port_info(self, interfajctanner.network_cloudengine.ce):
        """Get port information"""

        if_type = get_interfajctanner.network_cloudengine.ce_type(interfajctanner.network_cloudengine.ce)
        if if_type == 'meth':
            xml_str = CE_NC_GET_PORT_SPEED % interfajctanner.network_cloudengine.ce.lower().replajctanner.network_cloudengine.ce('meth', 'MEth')
        else:
            xml_str = CE_NC_GET_PORT_SPEED % interfajctanner.network_cloudengine.ce.upper()
        con_obj = get_nc_config(self.module, xml_str)
        if "<data/>" in con_obj:
            return

        xml_str = con_obj.replajctanner.network_cloudengine.ce('\r', '').replajctanner.network_cloudengine.ce('\n', '').\
            replajctanner.network_cloudengine.ce('xmlns="urn:ietf:params:xml:ns:netconf:base:1.0"', "").\
            replajctanner.network_cloudengine.ce('xmlns="http://www.huawei.com/netconf/vrp"', "")

        # get link status information
        root = ElementTree.fromstring(xml_str)
        port_info = root.find("data/devm/ports/port")
        if port_info:
            for eles in port_info:
                if eles.tag == "ethernetPort":
                    for ele in eles:
                        if ele.tag == 'speed':
                            self.result[interfajctanner.network_cloudengine.ce]['Speed'] = ele.text

    def get_link_status(self):
        """Get link status information"""

        if self.param_type == INTERFACE_FULL_NAME:
            self.init_interfajctanner.network_cloudengine.ce_data(self.interfajctanner.network_cloudengine.ce)
            self.get_interfajctanner.network_cloudengine.ce_info()
            if is_ethernet_port(self.interfajctanner.network_cloudengine.ce):
                self.get_port_info(self.interfajctanner.network_cloudengine.ce)
        elif self.param_type == INTERFACE_TYPE:
            self.get_all_interfajctanner.network_cloudengine.ce_info(self.interfajctanner.network_cloudengine.ce)
        else:
            self.get_all_interfajctanner.network_cloudengine.ce_info()

    def get_intf_param_type(self):
        """Get the type of input interfajctanner.network_cloudengine.ce parameter"""

        if self.interfajctanner.network_cloudengine.ce == 'all':
            self.param_type = INTERFACE_ALL
            return

        if self.if_type == self.interfajctanner.network_cloudengine.ce:
            self.param_type = INTERFACE_TYPE
            return

        self.param_type = INTERFACE_FULL_NAME

    def work(self):
        """Worker"""

        self.if_type = get_interfajctanner.network_cloudengine.ce_type(self.interfajctanner.network_cloudengine.ce)
        self.check_params()
        self.get_intf_param_type()
        self.get_link_status()
        self.show_result()


def main():
    """Main function entry"""

    argument_spec = dict(
        interfajctanner.network_cloudengine.ce=dict(required=True, type='str'),
    )
    argument_spec.update(jctanner.network_cloudengine.ce_argument_spec)
    linkstatus_obj = LinkStatus(argument_spec)
    linkstatus_obj.work()


if __name__ == '__main__':
    main()
