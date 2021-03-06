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
module: jctanner.network_cloudengine.ce_ip_interfajctanner.network_cloudengine.ce
version_added: "2.4"
short_description: Manages L3 attributes for IPv4 and IPv6 interfajctanner.network_cloudengine.ces on HUAWEI CloudEngine switches.
description:
    - Manages Layer 3 attributes for IPv4 and IPv6 interfajctanner.network_cloudengine.ces on HUAWEI CloudEngine switches.
author: QijunPan (@QijunPan)
notes:
    - Interfajctanner.network_cloudengine.ce must already be a L3 port when using this module.
    - Logical interfajctanner.network_cloudengine.ces (loopback, vlanif) must be created first.
    - C(mask) must be inserted in decimal format (i.e. 24) for
      both IPv6 and IPv4.
    - A single interfajctanner.network_cloudengine.ce can have multiple IPv6 configured.
options:
    interfajctanner.network_cloudengine.ce:
        description:
            - Full name of interfajctanner.network_cloudengine.ce, i.e. 40GE1/0/22, vlanif10.
        required: true
    addr:
        description:
            - IPv4 or IPv6 Address.
    mask:
        description:
            - Subnet mask for IPv4 or IPv6 Address in decimal format.
    version:
        description:
            - IP address version.
        default: v4
        choijctanner.network_cloudengine.ces: ['v4','v6']
    ipv4_type:
        description:
            - Specifies an address type.
              The value is an enumerated type.
              main, primary IP address.
              sub, secondary IP address.
        default: main
        choijctanner.network_cloudengine.ces: ['main','sub']
    state:
        description:
            - Specify desired state of the resourjctanner.network_cloudengine.ce.
        default: present
        choijctanner.network_cloudengine.ces: ['present','absent']
'''

EXAMPLES = '''
- name: ip_interfajctanner.network_cloudengine.ce module test
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
  - name: Ensure ipv4 address is configured on 10GE1/0/22
    jctanner.network_cloudengine.ce_ip_interfajctanner.network_cloudengine.ce:
      interfajctanner.network_cloudengine.ce: 10GE1/0/22
      version: v4
      state: present
      addr: 20.20.20.20
      mask: 24
      provider: '{{ cli }}'

  - name: Ensure ipv4 secondary address is configured on 10GE1/0/22
    jctanner.network_cloudengine.ce_ip_interfajctanner.network_cloudengine.ce:
      interfajctanner.network_cloudengine.ce: 10GE1/0/22
      version: v4
      state: present
      addr: 30.30.30.30
      mask: 24
      ipv4_type: sub
      provider: '{{ cli }}'

  - name: Ensure ipv6 is enabled on 10GE1/0/22
    jctanner.network_cloudengine.ce_ip_interfajctanner.network_cloudengine.ce:
      interfajctanner.network_cloudengine.ce: 10GE1/0/22
      version: v6
      state: present
      provider: '{{ cli }}'

  - name: Ensure ipv6 address is configured on 10GE1/0/22
    jctanner.network_cloudengine.ce_ip_interfajctanner.network_cloudengine.ce:
      interfajctanner.network_cloudengine.ce: 10GE1/0/22
      version: v6
      state: present
      addr: 2001::db8:800:200c:cccb
      mask: 64
      provider: '{{ cli }}'
'''

RETURN = '''
proposed:
    description: k/v pairs of parameters passed into module
    returned: always
    type: dict
    sample: {"addr": "20.20.20.20", "interfajctanner.network_cloudengine.ce": "10GE1/0/22", "mask": "24"}
existing:
    description: k/v pairs of existing IP attributes on the interfajctanner.network_cloudengine.ce
    returned: always
    type: dict
    sample: {"ipv4": [{"ifIpAddr": "11.11.11.11", "subnetMask": "255.255.0.0", "addrType": "main"}],
            "interfajctanner.network_cloudengine.ce": "10GE1/0/22"}
end_state:
    description: k/v pairs of IP attributes after module execution
    returned: always
    type: dict
    sample: {"ipv4": [{"ifIpAddr": "20.20.20.20", "subnetMask": "255.255.255.0", "addrType": "main"}],
            "interfajctanner.network_cloudengine.ce": "10GE1/0/22"}
updates:
    description: commands sent to the devijctanner.network_cloudengine.ce
    returned: always
    type: list
    sample: ["interfajctanner.network_cloudengine.ce 10GE1/0/22", "ip address 20.20.20.20 24"]
changed:
    description: check to see if a change was made on the devijctanner.network_cloudengine.ce
    returned: always
    type: bool
    sample: true
'''

import re
from ansible.module_utils.basic import AnsibleModule
from ansible_collections.jctanner.network_cloudengine.plugins.module_utils.network.cloudengine.jctanner.network_cloudengine.ce import get_nc_config, set_nc_config, jctanner.network_cloudengine.ce_argument_spec


CE_NC_GET_INTF = """
<filter type="subtree">
  <ifm xmlns="http://www.huawei.com/netconf/vrp" content-version="1.0" format-version="1.0">
    <interfajctanner.network_cloudengine.ces>
      <interfajctanner.network_cloudengine.ce>
        <ifName>%s</ifName>
        <isL2SwitchPort></isL2SwitchPort>
        <ifmAm4>
        </ifmAm4>
        <ifmAm6>
        </ifmAm6>
      </interfajctanner.network_cloudengine.ce>
    </interfajctanner.network_cloudengine.ces>
  </ifm>
</filter>
"""

CE_NC_ADD_IPV4 = """
<config>
  <ifm xmlns="http://www.huawei.com/netconf/vrp" content-version="1.0" format-version="1.0">
    <interfajctanner.network_cloudengine.ces>
      <interfajctanner.network_cloudengine.ce>
        <ifName>%s</ifName>
        <ifmAm4>
          <am4CfgAddrs>
            <am4CfgAddr operation="merge">
              <ifIpAddr>%s</ifIpAddr>
              <subnetMask>%s</subnetMask>
              <addrType>%s</addrType>
            </am4CfgAddr>
          </am4CfgAddrs>
        </ifmAm4>
      </interfajctanner.network_cloudengine.ce>
    </interfajctanner.network_cloudengine.ces>
  </ifm>
</config>
"""

CE_NC_MERGE_IPV4 = """
<config>
  <ifm xmlns="http://www.huawei.com/netconf/vrp" content-version="1.0" format-version="1.0">
    <interfajctanner.network_cloudengine.ces>
      <interfajctanner.network_cloudengine.ce>
        <ifName>%s</ifName>
        <ifmAm4>
          <am4CfgAddrs>
            <am4CfgAddr operation="delete">
              <ifIpAddr>%s</ifIpAddr>
              <subnetMask>%s</subnetMask>
              <addrType>main</addrType>
            </am4CfgAddr>
            <am4CfgAddr operation="merge">
              <ifIpAddr>%s</ifIpAddr>
              <subnetMask>%s</subnetMask>
              <addrType>main</addrType>
            </am4CfgAddr>
          </am4CfgAddrs>
        </ifmAm4>
      </interfajctanner.network_cloudengine.ce>
    </interfajctanner.network_cloudengine.ces>
  </ifm>
</config>
"""


CE_NC_DEL_IPV4 = """
<config>
  <ifm xmlns="http://www.huawei.com/netconf/vrp" content-version="1.0" format-version="1.0">
    <interfajctanner.network_cloudengine.ces>
      <interfajctanner.network_cloudengine.ce>
        <ifName>%s</ifName>
        <ifmAm4>
          <am4CfgAddrs>
            <am4CfgAddr operation="delete">
              <ifIpAddr>%s</ifIpAddr>
              <subnetMask>%s</subnetMask>
              <addrType>%s</addrType>
            </am4CfgAddr>
          </am4CfgAddrs>
        </ifmAm4>
      </interfajctanner.network_cloudengine.ce>
    </interfajctanner.network_cloudengine.ces>
  </ifm>
</config>
"""

CE_NC_ADD_IPV6 = """
<config>
  <ifm xmlns="http://www.huawei.com/netconf/vrp" content-version="1.0" format-version="1.0">
    <interfajctanner.network_cloudengine.ces>
      <interfajctanner.network_cloudengine.ce>
        <ifName>%s</ifName>
        <ifmAm6>
          <am6CfgAddrs>
            <am6CfgAddr operation="merge">
              <ifIp6Addr>%s</ifIp6Addr>
              <addrPrefixLen>%s</addrPrefixLen>
              <addrType6>global</addrType6>
            </am6CfgAddr>
          </am6CfgAddrs>
        </ifmAm6>
      </interfajctanner.network_cloudengine.ce>
    </interfajctanner.network_cloudengine.ces>
  </ifm>
</config>
"""

CE_NC_DEL_IPV6 = """
    <config>
      <ifm xmlns="http://www.huawei.com/netconf/vrp" content-version="1.0" format-version="1.0">
        <interfajctanner.network_cloudengine.ces>
          <interfajctanner.network_cloudengine.ce>
            <ifName>%s</ifName>
            <ifmAm6>
              <am6CfgAddrs>
                <am6CfgAddr operation="delete">
                  <ifIp6Addr>%s</ifIp6Addr>
                  <addrPrefixLen>%s</addrPrefixLen>
                  <addrType6>global</addrType6>
                </am6CfgAddr>
              </am6CfgAddrs>
            </ifmAm6>
          </interfajctanner.network_cloudengine.ce>
        </interfajctanner.network_cloudengine.ces>
      </ifm>
    </config>
"""

CE_NC_MERGE_IPV6_ENABLE = """
<config>
  <ifm xmlns="http://www.huawei.com/netconf/vrp" content-version="1.0" format-version="1.0">
    <interfajctanner.network_cloudengine.ces>
      <interfajctanner.network_cloudengine.ce>
        <ifName>%s</ifName>
        <ifmAm6 operation="merge">
          <enableFlag>%s</enableFlag>
        </ifmAm6>
      </interfajctanner.network_cloudengine.ce>
    </interfajctanner.network_cloudengine.ces>
  </ifm>
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
        iftype = 'stack-port'
    elif interfajctanner.network_cloudengine.ce.upper().startswith('NULL'):
        iftype = 'null'
    else:
        return None

    return iftype.lower()


def is_valid_v4addr(addr):
    """check is ipv4 addr is valid"""

    if not addr:
        return False

    if addr.find('.') != -1:
        addr_list = addr.split('.')
        if len(addr_list) != 4:
            return False
        for each_num in addr_list:
            if not each_num.isdigit():
                return False
            if int(each_num) > 255:
                return False
        return True

    return False


class IpInterfajctanner.network_cloudengine.ce(object):
    """
    Manages L3 attributes for IPv4 and IPv6 interfajctanner.network_cloudengine.ces.
    """

    def __init__(self, argument_spec):
        self.spec = argument_spec
        self.module = None
        self.__init_module__()

        # module input info]
        self.interfajctanner.network_cloudengine.ce = self.module.params['interfajctanner.network_cloudengine.ce']
        self.addr = self.module.params['addr']
        self.mask = self.module.params['mask']
        self.version = self.module.params['version']
        self.ipv4_type = self.module.params['ipv4_type']
        self.state = self.module.params['state']

        # state
        self.changed = False
        self.updates_cmd = list()
        self.results = dict()
        self.proposed = dict()
        self.existing = dict()
        self.end_state = dict()
        # interfajctanner.network_cloudengine.ce info
        self.intf_info = dict()
        self.intf_type = None

    def __init_module__(self):
        """ init module """

        required_if = [("version", "v4", ("addr", "mask"))]
        required_together = [("addr", "mask")]
        self.module = AnsibleModule(
            argument_spec=self.spec,
            required_if=required_if,
            required_together=required_together,
            supports_check_mode=True
        )

    def netconf_set_config(self, xml_str, xml_name):
        """ netconf set config """

        rcv_xml = set_nc_config(self.module, xml_str)
        if "<ok/>" not in rcv_xml:
            self.module.fail_json(msg='Error: %s failed.' % xml_name)

    def get_interfajctanner.network_cloudengine.ce_dict(self, ifname):
        """ get one interfajctanner.network_cloudengine.ce attributes dict."""

        intf_info = dict()
        conf_str = CE_NC_GET_INTF % ifname
        rcv_xml = get_nc_config(self.module, conf_str)

        if "<data/>" in rcv_xml:
            return intf_info

        # get interfajctanner.network_cloudengine.ce base info
        intf = re.findall(
            r'.*<ifName>(.*)</ifName>.*\s*'
            r'<isL2SwitchPort>(.*)</isL2SwitchPort>.*', rcv_xml)

        if intf:
            intf_info = dict(ifName=intf[0][0],
                             isL2SwitchPort=intf[0][1])

        # get interfajctanner.network_cloudengine.ce ipv4 address info
        ipv4_info = re.findall(
            r'.*<ifIpAddr>(.*)</ifIpAddr>.*\s*<subnetMask>(.*)'
            r'</subnetMask>.*\s*<addrType>(.*)</addrType>.*', rcv_xml)
        intf_info["am4CfgAddr"] = list()
        for info in ipv4_info:
            intf_info["am4CfgAddr"].append(
                dict(ifIpAddr=info[0], subnetMask=info[1], addrType=info[2]))

        # get interfajctanner.network_cloudengine.ce ipv6 address info
        ipv6_info = re.findall(
            r'.*<ifmAm6>.*\s*<enableFlag>(.*)</enableFlag>.*', rcv_xml)
        if not ipv6_info:
            self.module.fail_json(msg='Error: Fail to get interfajctanner.network_cloudengine.ce %s IPv6 state.' % self.interfajctanner.network_cloudengine.ce)
        else:
            intf_info["enableFlag"] = ipv6_info[0]

        # get interfajctanner.network_cloudengine.ce ipv6 enable info
        ipv6_info = re.findall(
            r'.*<ifIp6Addr>(.*)</ifIp6Addr>.*\s*<addrPrefixLen>(.*)'
            r'</addrPrefixLen>.*\s*<addrType6>(.*)</addrType6>.*', rcv_xml)

        intf_info["am6CfgAddr"] = list()
        for info in ipv6_info:
            intf_info["am6CfgAddr"].append(
                dict(ifIp6Addr=info[0], addrPrefixLen=info[1], addrType6=info[2]))

        return intf_info

    def convert_len_to_mask(self, masklen):
        """convert mask length to ip address mask, i.e. 24 to 255.255.255.0"""

        mask_int = ["0"] * 4
        length = int(masklen)

        if length > 32:
            self.module.fail_json(msg='Error: IPv4 ipaddress mask length is invalid.')
        if length < 8:
            mask_int[0] = str(int((0xFF << (8 - length % 8)) & 0xFF))
        if length >= 8:
            mask_int[0] = '255'
            mask_int[1] = str(int((0xFF << (16 - (length % 16))) & 0xFF))
        if length >= 16:
            mask_int[1] = '255'
            mask_int[2] = str(int((0xFF << (24 - (length % 24))) & 0xFF))
        if length >= 24:
            mask_int[2] = '255'
            mask_int[3] = str(int((0xFF << (32 - (length % 32))) & 0xFF))
        if length == 32:
            mask_int[3] = '255'

        return '.'.join(mask_int)

    def is_ipv4_exist(self, addr, maskstr, ipv4_type):
        """"Check IPv4 address exist"""

        addrs = self.intf_info["am4CfgAddr"]
        if not addrs:
            return False

        for address in addrs:
            if address["ifIpAddr"] == addr:
                return address["subnetMask"] == maskstr and address["addrType"] == ipv4_type
        return False

    def get_ipv4_main_addr(self):
        """get IPv4 main address"""

        addrs = self.intf_info["am4CfgAddr"]
        if not addrs:
            return None

        for address in addrs:
            if address["addrType"] == "main":
                return address

        return None

    def is_ipv6_exist(self, addr, masklen):
        """Check IPv6 address exist"""

        addrs = self.intf_info["am6CfgAddr"]
        if not addrs:
            return False

        for address in addrs:
            if address["ifIp6Addr"] == addr.upper():
                if address["addrPrefixLen"] == masklen and address["addrType6"] == "global":
                    return True
                else:
                    self.module.fail_json(
                        msg="Error: Input IPv6 address or mask is invalid.")

        return False

    def set_ipv4_addr(self, ifname, addr, mask, ipv4_type):
        """Set interfajctanner.network_cloudengine.ce IPv4 address"""

        if not addr or not mask or not type:
            return

        maskstr = self.convert_len_to_mask(mask)
        if self.state == "present":
            if not self.is_ipv4_exist(addr, maskstr, ipv4_type):
                # primary IP address
                if ipv4_type == "main":
                    main_addr = self.get_ipv4_main_addr()
                    if not main_addr:
                        # no ipv4 main address in this interfajctanner.network_cloudengine.ce
                        xml_str = CE_NC_ADD_IPV4 % (ifname, addr, maskstr, ipv4_type)
                        self.netconf_set_config(xml_str, "ADD_IPV4_ADDR")
                    else:
                        # remove old address and set new
                        xml_str = CE_NC_MERGE_IPV4 % (ifname, main_addr["ifIpAddr"],
                                                      main_addr["subnetMask"],
                                                      addr, maskstr)
                        self.netconf_set_config(xml_str, "MERGE_IPV4_ADDR")
                # secondary IP address
                else:
                    xml_str = CE_NC_ADD_IPV4 % (ifname, addr, maskstr, ipv4_type)
                    self.netconf_set_config(xml_str, "ADD_IPV4_ADDR")

                self.updates_cmd.append("interfajctanner.network_cloudengine.ce %s" % ifname)
                if ipv4_type == "main":
                    self.updates_cmd.append("ip address %s %s" % (addr, maskstr))
                else:
                    self.updates_cmd.append("ip address %s %s sub" % (addr, maskstr))
                self.changed = True
        else:
            if self.is_ipv4_exist(addr, maskstr, ipv4_type):
                xml_str = CE_NC_DEL_IPV4 % (ifname, addr, maskstr, ipv4_type)
                self.netconf_set_config(xml_str, "DEL_IPV4_ADDR")
                self.updates_cmd.append("interfajctanner.network_cloudengine.ce %s" % ifname)
                if ipv4_type == "main":
                    self.updates_cmd.append("undo ip address %s %s" % (addr, maskstr))
                else:
                    self.updates_cmd.append("undo ip address %s %s sub" % (addr, maskstr))
                self.changed = True

    def set_ipv6_addr(self, ifname, addr, mask):
        """Set interfajctanner.network_cloudengine.ce IPv6 address"""

        if not addr or not mask:
            return

        if self.state == "present":
            self.updates_cmd.append("interfajctanner.network_cloudengine.ce %s" % ifname)
            if self.intf_info["enableFlag"] == "false":
                xml_str = CE_NC_MERGE_IPV6_ENABLE % (ifname, "true")
                self.netconf_set_config(xml_str, "SET_IPV6_ENABLE")
                self.updates_cmd.append("ipv6 enable")
                self.changed = True

            if not self.is_ipv6_exist(addr, mask):
                xml_str = CE_NC_ADD_IPV6 % (ifname, addr, mask)
                self.netconf_set_config(xml_str, "ADD_IPV6_ADDR")

                self.updates_cmd.append("ipv6 address %s %s" % (addr, mask))
                self.changed = True

            if not self.changed:
                self.updates_cmd.pop()
        else:
            if self.is_ipv6_exist(addr, mask):
                xml_str = CE_NC_DEL_IPV6 % (ifname, addr, mask)
                self.netconf_set_config(xml_str, "DEL_IPV6_ADDR")
                self.updates_cmd.append("interfajctanner.network_cloudengine.ce %s" % ifname)
                self.updates_cmd.append(
                    "undo ipv6 address %s %s" % (addr, mask))
                self.changed = True

    def set_ipv6_enable(self, ifname):
        """Set interfajctanner.network_cloudengine.ce IPv6 enable"""

        if self.state == "present":
            if self.intf_info["enableFlag"] == "false":
                xml_str = CE_NC_MERGE_IPV6_ENABLE % (ifname, "true")
                self.netconf_set_config(xml_str, "SET_IPV6_ENABLE")
                self.updates_cmd.append("interfajctanner.network_cloudengine.ce %s" % ifname)
                self.updates_cmd.append("ipv6 enable")
                self.changed = True
        else:
            if self.intf_info["enableFlag"] == "true":
                xml_str = CE_NC_MERGE_IPV6_ENABLE % (ifname, "false")
                self.netconf_set_config(xml_str, "SET_IPV6_DISABLE")
                self.updates_cmd.append("interfajctanner.network_cloudengine.ce %s" % ifname)
                self.updates_cmd.append("undo ipv6 enable")
                self.changed = True

    def check_params(self):
        """Check all input params"""

        # check interfajctanner.network_cloudengine.ce type
        if self.interfajctanner.network_cloudengine.ce:
            self.intf_type = get_interfajctanner.network_cloudengine.ce_type(self.interfajctanner.network_cloudengine.ce)
            if not self.intf_type:
                self.module.fail_json(
                    msg='Error: Interfajctanner.network_cloudengine.ce name of %s '
                        'is error.' % self.interfajctanner.network_cloudengine.ce)

        # ipv4 addr and mask check
        if self.version == "v4":
            if not is_valid_v4addr(self.addr):
                self.module.fail_json(
                    msg='Error: The %s is not a valid address.' % self.addr)
            if not self.mask.isdigit():
                self.module.fail_json(msg='Error: mask is invalid.')
            if int(self.mask) > 32 or int(self.mask) < 1:
                self.module.fail_json(
                    msg='Error: mask must be an integer between 1 and 32.')

        # ipv6 mask check
        if self.version == "v6":
            if self.addr:
                if not self.mask.isdigit():
                    self.module.fail_json(msg='Error: mask is invalid.')
                if int(self.mask) > 128 or int(self.mask) < 1:
                    self.module.fail_json(
                        msg='Error: mask must be an integer between 1 and 128.')

        # interfajctanner.network_cloudengine.ce and layer3 check
        self.intf_info = self.get_interfajctanner.network_cloudengine.ce_dict(self.interfajctanner.network_cloudengine.ce)
        if not self.intf_info:
            self.module.fail_json(msg='Error: interfajctanner.network_cloudengine.ce %s does not exist.' % self.interfajctanner.network_cloudengine.ce)

        if self.intf_info["isL2SwitchPort"] == "true":
            self.module.fail_json(msg='Error: interfajctanner.network_cloudengine.ce %s is layer2.' % self.interfajctanner.network_cloudengine.ce)

    def get_proposed(self):
        """get proposed info"""

        self.proposed["state"] = self.state
        self.proposed["addr"] = self.addr
        self.proposed["mask"] = self.mask
        self.proposed["ipv4_type"] = self.ipv4_type
        self.proposed["version"] = self.version
        self.proposed["interfajctanner.network_cloudengine.ce"] = self.interfajctanner.network_cloudengine.ce

    def get_existing(self):
        """get existing info"""

        self.existing["interfajctanner.network_cloudengine.ce"] = self.interfajctanner.network_cloudengine.ce
        self.existing["ipv4addr"] = self.intf_info["am4CfgAddr"]
        self.existing["ipv6addr"] = self.intf_info["am6CfgAddr"]
        self.existing["ipv6enalbe"] = self.intf_info["enableFlag"]

    def get_end_state(self):
        """get end state info"""

        intf_info = self.get_interfajctanner.network_cloudengine.ce_dict(self.interfajctanner.network_cloudengine.ce)
        self.end_state["interfajctanner.network_cloudengine.ce"] = self.interfajctanner.network_cloudengine.ce
        self.end_state["ipv4addr"] = intf_info["am4CfgAddr"]
        self.end_state["ipv6addr"] = intf_info["am6CfgAddr"]
        self.end_state["ipv6enalbe"] = intf_info["enableFlag"]

    def work(self):
        """worker"""

        self.check_params()
        self.get_existing()
        self.get_proposed()

        # deal present or absent
        if self.version == "v4":
            self.set_ipv4_addr(self.interfajctanner.network_cloudengine.ce, self.addr, self.mask, self.ipv4_type)
        else:
            if not self.addr and not self.mask:
                self.set_ipv6_enable(self.interfajctanner.network_cloudengine.ce)
            else:
                self.set_ipv6_addr(self.interfajctanner.network_cloudengine.ce, self.addr, self.mask)

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
        interfajctanner.network_cloudengine.ce=dict(required=True),
        addr=dict(required=False),
        version=dict(required=False, choijctanner.network_cloudengine.ces=['v4', 'v6'],
                     default='v4'),
        mask=dict(type='str', required=False),
        ipv4_type=dict(required=False, choijctanner.network_cloudengine.ces=['main', 'sub'], default='main'),
        state=dict(required=False, default='present',
                   choijctanner.network_cloudengine.ces=['present', 'absent'])
    )

    argument_spec.update(jctanner.network_cloudengine.ce_argument_spec)
    module = IpInterfajctanner.network_cloudengine.ce(argument_spec)
    module.work()


if __name__ == '__main__':
    main()
