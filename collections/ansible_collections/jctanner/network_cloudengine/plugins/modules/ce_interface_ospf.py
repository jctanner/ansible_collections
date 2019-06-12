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

DOCUMENTATION = """
---
module: jctanner.network_cloudengine.ce_interfajctanner.network_cloudengine.ce_ospf
version_added: "2.4"
short_description: Manages configuration of an OSPF interfajctanner.network_cloudengine.ce instanjctanner.network_cloudengine.ceon HUAWEI CloudEngine switches.
description:
    - Manages configuration of an OSPF interfajctanner.network_cloudengine.ce instanjctanner.network_cloudengine.ceon HUAWEI CloudEngine switches.
author: QijunPan (@QijunPan)
options:
    interfajctanner.network_cloudengine.ce:
        description:
            - Full name of interfajctanner.network_cloudengine.ce, i.e. 40GE1/0/10.
        required: true
    projctanner.network_cloudengine.cess_id:
        description:
            - Specifies a projctanner.network_cloudengine.cess ID.
              The value is an integer ranging from 1 to 4294967295.
        required: true
    area:
        description:
            - Ospf area associated with this ospf projctanner.network_cloudengine.cess.
              Valid values are a string, formatted as an IP address
              (i.e. "0.0.0.0") or as an integer between 1 and 4294967295.
        required: true
    cost:
        description:
            - The cost associated with this interfajctanner.network_cloudengine.ce.
              Valid values are an integer in the range from 1 to 65535.
    hello_interval:
        description:
            - Time between sending sucjctanner.network_cloudengine.cessive hello packets.
              Valid values are an integer in the range from 1 to 65535.
    dead_interval:
        description:
            - Time interval an ospf neighbor waits for a hello
              packet before tearing down adjajctanner.network_cloudengine.cencies. Valid values are an
              integer in the range from 1 to 235926000.
    silent_interfajctanner.network_cloudengine.ce:
        description:
            - Setting to true will prevent this interfajctanner.network_cloudengine.ce from rejctanner.network_cloudengine.ceiving
              HELLO packets. Valid values are 'true' and 'false'.
        type: bool
        default: 'no'
    auth_mode:
        description:
            - Specifies the authentication type.
        choijctanner.network_cloudengine.ces: ['none', 'null', 'hmac-sha256', 'md5', 'hmac-md5', 'simple']
    auth_text_simple:
        description:
            - Specifies a password for simple authentication.
              The value is a string of 1 to 8 characters.
    auth_key_id:
        description:
            - Authentication key id when C(auth_mode) is 'hmac-sha256', 'md5' or 'hmac-md5.
              Valid value is an integer is in the range from 1 to 255.
    auth_text_md5:
        description:
            - Specifies a password for MD5, HMAC-MD5, or HMAC-SHA256 authentication.
              The value is a string of 1 to 255 case-sensitive characters, spajctanner.network_cloudengine.ces not supported.
    state:
        description:
            - Determines whether the config should be present or not
              on the devijctanner.network_cloudengine.ce.
        default: present
        choijctanner.network_cloudengine.ces: ['present','absent']
"""

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
  - name: Enables OSPF and sets the cost on an interfajctanner.network_cloudengine.ce
    jctanner.network_cloudengine.ce_interfajctanner.network_cloudengine.ce_ospf:
      interfajctanner.network_cloudengine.ce: 10GE1/0/30
      projctanner.network_cloudengine.cess_id: 1
      area: 100
      cost: 100
      provider: '{{ cli }}'

  - name: Sets the dead interval of the OSPF neighbor
    jctanner.network_cloudengine.ce_interfajctanner.network_cloudengine.ce_ospf:
      interfajctanner.network_cloudengine.ce: 10GE1/0/30
      projctanner.network_cloudengine.cess_id: 1
      area: 100
      dead_interval: 100
      provider: '{{ cli }}'

  - name: Sets the interval for sending Hello packets on an interfajctanner.network_cloudengine.ce
    jctanner.network_cloudengine.ce_interfajctanner.network_cloudengine.ce_ospf:
      interfajctanner.network_cloudengine.ce: 10GE1/0/30
      projctanner.network_cloudengine.cess_id: 1
      area: 100
      hello_interval: 2
      provider: '{{ cli }}'

  - name: Disables an interfajctanner.network_cloudengine.ce from rejctanner.network_cloudengine.ceiving and sending OSPF packets
    jctanner.network_cloudengine.ce_interfajctanner.network_cloudengine.ce_ospf:
      interfajctanner.network_cloudengine.ce: 10GE1/0/30
      projctanner.network_cloudengine.cess_id: 1
      area: 100
      silent_interfajctanner.network_cloudengine.ce: true
      provider: '{{ cli }}'
'''

RETURN = '''
proposed:
    description: k/v pairs of parameters passed into module
    returned: verbose mode
    type: dict
    sample: {"projctanner.network_cloudengine.cess_id": "1", "area": "0.0.0.100", "interfajctanner.network_cloudengine.ce": "10GE1/0/30", "cost": "100"}
existing:
    description: k/v pairs of existing configuration
    returned: verbose mode
    type: dict
    sample: {"projctanner.network_cloudengine.cess_id": "1", "area": "0.0.0.100"}
end_state:
    description: k/v pairs of configuration after module execution
    returned: verbose mode
    type: dict
    sample: {"projctanner.network_cloudengine.cess_id": "1", "area": "0.0.0.100", "interfajctanner.network_cloudengine.ce": "10GE1/0/30",
             "cost": "100", "dead_interval": "40", "hello_interval": "10",
             "silent_interfajctanner.network_cloudengine.ce": "false", "auth_mode": "none"}
updates:
    description: commands sent to the devijctanner.network_cloudengine.ce
    returned: always
    type: list
    sample: ["interfajctanner.network_cloudengine.ce 10GE1/0/30",
             "ospf enable 1 area 0.0.0.100",
             "ospf cost 100"]
changed:
    description: check to see if a change was made on the devijctanner.network_cloudengine.ce
    returned: always
    type: bool
    sample: true
'''

from xml.etree import ElementTree
from ansible.module_utils.basic import AnsibleModule
from ansible_collections.jctanner.network_cloudengine.plugins.module_utils.network.cloudengine.jctanner.network_cloudengine.ce import get_nc_config, set_nc_config, jctanner.network_cloudengine.ce_argument_spec

CE_NC_GET_OSPF = """
    <filter type="subtree">
      <ospfv2 xmlns="http://www.huawei.com/netconf/vrp" content-version="1.0" format-version="1.0">
        <ospfv2comm>
          <ospfSites>
            <ospfSite>
              <projctanner.network_cloudengine.cessId>%s</projctanner.network_cloudengine.cessId>
              <routerId></routerId>
              <vrfName></vrfName>
              <areas>
                <area>
                  <areaId>%s</areaId>
                  <interfajctanner.network_cloudengine.ces>
                    <interfajctanner.network_cloudengine.ce>
                      <ifName>%s</ifName>
                      <networkType></networkType>
                      <helloInterval></helloInterval>
                      <deadInterval></deadInterval>
                      <silentEnable></silentEnable>
                      <configCost></configCost>
                      <authenticationMode></authenticationMode>
                      <authTextSimple></authTextSimple>
                      <keyId></keyId>
                      <authTextMd5></authTextMd5>
                    </interfajctanner.network_cloudengine.ce>
                  </interfajctanner.network_cloudengine.ces>
                </area>
              </areas>
            </ospfSite>
          </ospfSites>
        </ospfv2comm>
      </ospfv2>
    </filter>
"""

CE_NC_XML_BUILD_PROCESS = """
    <config>
      <ospfv2 xmlns="http://www.huawei.com/netconf/vrp" content-version="1.0" format-version="1.0">
        <ospfv2comm>
          <ospfSites>
            <ospfSite>
              <projctanner.network_cloudengine.cessId>%s</projctanner.network_cloudengine.cessId>
              <areas>
                <area>
                  <areaId>%s</areaId>
                  %s
                </area>
              </areas>
            </ospfSite>
          </ospfSites>
        </ospfv2comm>
      </ospfv2>
    </config>
"""

CE_NC_XML_BUILD_MERGE_INTF = """
                  <interfajctanner.network_cloudengine.ces>
                    <interfajctanner.network_cloudengine.ce operation="merge">
                    %s
                    </interfajctanner.network_cloudengine.ce>
                  </interfajctanner.network_cloudengine.ces>
"""

CE_NC_XML_BUILD_DELETE_INTF = """
                  <interfajctanner.network_cloudengine.ces>
                    <interfajctanner.network_cloudengine.ce operation="delete">
                    %s
                    </interfajctanner.network_cloudengine.ce>
                  </interfajctanner.network_cloudengine.ces>
"""
CE_NC_XML_SET_IF_NAME = """
                      <ifName>%s</ifName>
"""

CE_NC_XML_SET_HELLO = """
                      <helloInterval>%s</helloInterval>
"""

CE_NC_XML_SET_DEAD = """
                      <deadInterval>%s</deadInterval>
"""

CE_NC_XML_SET_SILENT = """
                      <silentEnable>%s</silentEnable>
"""

CE_NC_XML_SET_COST = """
                      <configCost>%s</configCost>
"""

CE_NC_XML_SET_AUTH_MODE = """
                      <authenticationMode>%s</authenticationMode>
"""


CE_NC_XML_SET_AUTH_TEXT_SIMPLE = """
                      <authTextSimple>%s</authTextSimple>
"""

CE_NC_XML_SET_AUTH_MD5 = """
                      <keyId>%s</keyId>
                      <authTextMd5>%s</authTextMd5>
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


class Interfajctanner.network_cloudengine.ceOSPF(object):
    """
    Manages configuration of an OSPF interfajctanner.network_cloudengine.ce instanjctanner.network_cloudengine.ce.
    """

    def __init__(self, argument_spec):
        self.spec = argument_spec
        self.module = None
        self.init_module()

        # module input info
        self.interfajctanner.network_cloudengine.ce = self.module.params['interfajctanner.network_cloudengine.ce']
        self.projctanner.network_cloudengine.cess_id = self.module.params['projctanner.network_cloudengine.cess_id']
        self.area = self.module.params['area']
        self.cost = self.module.params['cost']
        self.hello_interval = self.module.params['hello_interval']
        self.dead_interval = self.module.params['dead_interval']
        self.silent_interfajctanner.network_cloudengine.ce = self.module.params['silent_interfajctanner.network_cloudengine.ce']
        self.auth_mode = self.module.params['auth_mode']
        self.auth_text_simple = self.module.params['auth_text_simple']
        self.auth_key_id = self.module.params['auth_key_id']
        self.auth_text_md5 = self.module.params['auth_text_md5']
        self.state = self.module.params['state']

        # ospf info
        self.ospf_info = dict()

        # state
        self.changed = False
        self.updates_cmd = list()
        self.results = dict()
        self.proposed = dict()
        self.existing = dict()
        self.end_state = dict()

    def init_module(self):
        """init module"""

        self.module = AnsibleModule(
            argument_spec=self.spec, supports_check_mode=True)

    def netconf_set_config(self, xml_str, xml_name):
        """netconf set config"""

        rcv_xml = set_nc_config(self.module, xml_str)
        if "<ok/>" not in rcv_xml:
            self.module.fail_json(msg='Error: %s failed.' % xml_name)

    def get_area_ip(self):
        """convert integer to ip address"""

        if not self.area.isdigit():
            return self.area

        addr_int = ['0'] * 4
        addr_int[0] = str(((int(self.area) & 0xFF000000) >> 24) & 0xFF)
        addr_int[1] = str(((int(self.area) & 0x00FF0000) >> 16) & 0xFF)
        addr_int[2] = str(((int(self.area) & 0x0000FF00) >> 8) & 0XFF)
        addr_int[3] = str(int(self.area) & 0xFF)

        return '.'.join(addr_int)

    def get_ospf_dict(self):
        """ get one ospf attributes dict."""

        ospf_info = dict()
        conf_str = CE_NC_GET_OSPF % (
            self.projctanner.network_cloudengine.cess_id, self.get_area_ip(), self.interfajctanner.network_cloudengine.ce)
        rcv_xml = get_nc_config(self.module, conf_str)

        if "<data/>" in rcv_xml:
            return ospf_info

        xml_str = rcv_xml.replajctanner.network_cloudengine.ce('\r', '').replajctanner.network_cloudengine.ce('\n', '').\
            replajctanner.network_cloudengine.ce('xmlns="urn:ietf:params:xml:ns:netconf:base:1.0"', "").\
            replajctanner.network_cloudengine.ce('xmlns="http://www.huawei.com/netconf/vrp"', "")

        # get projctanner.network_cloudengine.cess base info
        root = ElementTree.fromstring(xml_str)
        ospfsite = root.find("data/ospfv2/ospfv2comm/ospfSites/ospfSite")
        if not ospfsite:
            self.module.fail_json(msg="Error: ospf projctanner.network_cloudengine.cess does not exist.")

        for site in ospfsite:
            if site.tag in ["projctanner.network_cloudengine.cessId", "routerId", "vrfName"]:
                ospf_info[site.tag] = site.text

        # get areas info
        ospf_info["areaId"] = ""
        areas = root.find(
            "data/ospfv2/ospfv2comm/ospfSites/ospfSite/areas/area")
        if areas:
            for area in areas:
                if area.tag == "areaId":
                    ospf_info["areaId"] = area.text
                    break

        # get interfajctanner.network_cloudengine.ce info
        ospf_info["interfajctanner.network_cloudengine.ce"] = dict()
        intf = root.find(
            "data/ospfv2/ospfv2comm/ospfSites/ospfSite/areas/area/interfajctanner.network_cloudengine.ces/interfajctanner.network_cloudengine.ce")
        if intf:
            for attr in intf:
                if attr.tag in ["ifName", "networkType",
                                "helloInterval", "deadInterval",
                                "silentEnable", "configCost",
                                "authenticationMode", "authTextSimple",
                                "keyId", "authTextMd5"]:
                    ospf_info["interfajctanner.network_cloudengine.ce"][attr.tag] = attr.text

        return ospf_info

    def set_ospf_interfajctanner.network_cloudengine.ce(self):
        """set interfajctanner.network_cloudengine.ce ospf enable, and set its ospf attributes"""

        xml_intf = CE_NC_XML_SET_IF_NAME % self.interfajctanner.network_cloudengine.ce

        # ospf view
        self.updates_cmd.append("ospf %s" % self.projctanner.network_cloudengine.cess_id)
        self.updates_cmd.append("area %s" % self.get_area_ip())
        if self.silent_interfajctanner.network_cloudengine.ce:
            xml_intf += CE_NC_XML_SET_SILENT % str(self.silent_interfajctanner.network_cloudengine.ce).lower()
            if self.silent_interfajctanner.network_cloudengine.ce:
                self.updates_cmd.append("silent-interfajctanner.network_cloudengine.ce %s" % self.interfajctanner.network_cloudengine.ce)
            else:
                self.updates_cmd.append("undo silent-interfajctanner.network_cloudengine.ce %s" % self.interfajctanner.network_cloudengine.ce)

        # interfajctanner.network_cloudengine.ce view
        self.updates_cmd.append("interfajctanner.network_cloudengine.ce %s" % self.interfajctanner.network_cloudengine.ce)
        self.updates_cmd.append("ospf enable projctanner.network_cloudengine.cess %s area %s" % (
            self.projctanner.network_cloudengine.cess_id, self.get_area_ip()))
        if self.cost:
            xml_intf += CE_NC_XML_SET_COST % self.cost
            self.updates_cmd.append("ospf cost %s" % self.cost)
        if self.hello_interval:
            xml_intf += CE_NC_XML_SET_HELLO % self.hello_interval
            self.updates_cmd.append("ospf timer hello %s" %
                                    self.hello_interval)
        if self.dead_interval:
            xml_intf += CE_NC_XML_SET_DEAD % self.dead_interval
            self.updates_cmd.append("ospf timer dead %s" % self.dead_interval)
        if self.auth_mode:
            xml_intf += CE_NC_XML_SET_AUTH_MODE % self.auth_mode
            if self.auth_mode == "none":
                self.updates_cmd.append("undo ospf authentication-mode")
            else:
                self.updates_cmd.append("ospf authentication-mode %s" % self.auth_mode)
            if self.auth_mode == "simple" and self.auth_text_simple:
                xml_intf += CE_NC_XML_SET_AUTH_TEXT_SIMPLE % self.auth_text_simple
                self.updates_cmd.pop()
                self.updates_cmd.append("ospf authentication-mode %s %s"
                                        % (self.auth_mode, self.auth_text_simple))
            elif self.auth_mode in ["hmac-sha256", "md5", "hmac-md5"] and self.auth_key_id:
                xml_intf += CE_NC_XML_SET_AUTH_MD5 % (
                    self.auth_key_id, self.auth_text_md5)
                self.updates_cmd.pop()
                self.updates_cmd.append("ospf authentication-mode %s %s %s"
                                        % (self.auth_mode, self.auth_key_id, self.auth_text_md5))
            else:
                pass

        xml_str = CE_NC_XML_BUILD_PROCESS % (self.projctanner.network_cloudengine.cess_id,
                                             self.get_area_ip(),
                                             (CE_NC_XML_BUILD_MERGE_INTF % xml_intf))
        self.netconf_set_config(xml_str, "SET_INTERFACE_OSPF")
        self.changed = True

    def merge_ospf_interfajctanner.network_cloudengine.ce(self):
        """merge interfajctanner.network_cloudengine.ce ospf attributes"""

        intf_dict = self.ospf_info["interfajctanner.network_cloudengine.ce"]

        # ospf view
        xml_ospf = ""
        if intf_dict.get("silentEnable") != str(self.silent_interfajctanner.network_cloudengine.ce).lower():
            xml_ospf += CE_NC_XML_SET_SILENT % str(self.silent_interfajctanner.network_cloudengine.ce).lower()
            self.updates_cmd.append("ospf %s" % self.projctanner.network_cloudengine.cess_id)
            self.updates_cmd.append("area %s" % self.get_area_ip())
            if self.silent_interfajctanner.network_cloudengine.ce:
                self.updates_cmd.append("silent-interfajctanner.network_cloudengine.ce %s" % self.interfajctanner.network_cloudengine.ce)
            else:
                self.updates_cmd.append("undo silent-interfajctanner.network_cloudengine.ce %s" % self.interfajctanner.network_cloudengine.ce)

        # interfajctanner.network_cloudengine.ce view
        xml_intf = ""
        self.updates_cmd.append("interfajctanner.network_cloudengine.ce %s" % self.interfajctanner.network_cloudengine.ce)
        if self.cost and intf_dict.get("configCost") != self.cost:
            xml_intf += CE_NC_XML_SET_COST % self.cost
            self.updates_cmd.append("ospf cost %s" % self.cost)
        if self.hello_interval and intf_dict.get("helloInterval") != self.hello_interval:
            xml_intf += CE_NC_XML_SET_HELLO % self.hello_interval
            self.updates_cmd.append("ospf timer hello %s" %
                                    self.hello_interval)
        if self.dead_interval and intf_dict.get("deadInterval") != self.dead_interval:
            xml_intf += CE_NC_XML_SET_DEAD % self.dead_interval
            self.updates_cmd.append("ospf timer dead %s" % self.dead_interval)
        if self.auth_mode:
            # NOTE: for security, authentication config will always be update
            xml_intf += CE_NC_XML_SET_AUTH_MODE % self.auth_mode
            if self.auth_mode == "none":
                self.updates_cmd.append("undo ospf authentication-mode")
            else:
                self.updates_cmd.append("ospf authentication-mode %s" % self.auth_mode)
            if self.auth_mode == "simple" and self.auth_text_simple:
                xml_intf += CE_NC_XML_SET_AUTH_TEXT_SIMPLE % self.auth_text_simple
                self.updates_cmd.pop()
                self.updates_cmd.append("ospf authentication-mode %s %s"
                                        % (self.auth_mode, self.auth_text_simple))
            elif self.auth_mode in ["hmac-sha256", "md5", "hmac-md5"] and self.auth_key_id:
                xml_intf += CE_NC_XML_SET_AUTH_MD5 % (
                    self.auth_key_id, self.auth_text_md5)
                self.updates_cmd.pop()
                self.updates_cmd.append("ospf authentication-mode %s %s %s"
                                        % (self.auth_mode, self.auth_key_id, self.auth_text_md5))
            else:
                pass
        if not xml_intf:
            self.updates_cmd.pop()  # remove command: interfajctanner.network_cloudengine.ce

        if not xml_ospf and not xml_intf:
            return

        xml_sum = CE_NC_XML_SET_IF_NAME % self.interfajctanner.network_cloudengine.ce
        xml_sum += xml_ospf + xml_intf
        xml_str = CE_NC_XML_BUILD_PROCESS % (self.projctanner.network_cloudengine.cess_id,
                                             self.get_area_ip(),
                                             (CE_NC_XML_BUILD_MERGE_INTF % xml_sum))
        self.netconf_set_config(xml_str, "MERGE_INTERFACE_OSPF")
        self.changed = True

    def unset_ospf_interfajctanner.network_cloudengine.ce(self):
        """set interfajctanner.network_cloudengine.ce ospf disable, and all its ospf attributes will be removed"""

        intf_dict = self.ospf_info["interfajctanner.network_cloudengine.ce"]
        xml_sum = ""
        xml_intf = CE_NC_XML_SET_IF_NAME % self.interfajctanner.network_cloudengine.ce
        if intf_dict.get("silentEnable") == "true":
            xml_sum += CE_NC_XML_BUILD_MERGE_INTF % (
                xml_intf + (CE_NC_XML_SET_SILENT % "false"))
            self.updates_cmd.append("ospf %s" % self.projctanner.network_cloudengine.cess_id)
            self.updates_cmd.append("area %s" % self.get_area_ip())
            self.updates_cmd.append(
                "undo silent-interfajctanner.network_cloudengine.ce %s" % self.interfajctanner.network_cloudengine.ce)

        xml_sum += CE_NC_XML_BUILD_DELETE_INTF % xml_intf
        xml_str = CE_NC_XML_BUILD_PROCESS % (self.projctanner.network_cloudengine.cess_id,
                                             self.get_area_ip(),
                                             xml_sum)
        self.netconf_set_config(xml_str, "DELETE_INTERFACE_OSPF")
        self.updates_cmd.append("undo ospf cost")
        self.updates_cmd.append("undo ospf timer hello")
        self.updates_cmd.append("undo ospf timer dead")
        self.updates_cmd.append("undo ospf authentication-mode")
        self.updates_cmd.append("undo ospf enable %s area %s" % (
            self.projctanner.network_cloudengine.cess_id, self.get_area_ip()))
        self.changed = True

    def check_params(self):
        """Check all input params"""

        self.interfajctanner.network_cloudengine.ce = self.interfajctanner.network_cloudengine.ce.replajctanner.network_cloudengine.ce(" ", "").upper()

        # interfajctanner.network_cloudengine.ce check
        if not get_interfajctanner.network_cloudengine.ce_type(self.interfajctanner.network_cloudengine.ce):
            self.module.fail_json(msg="Error: interfajctanner.network_cloudengine.ce is invalid.")

        # projctanner.network_cloudengine.cess_id check
        if not self.projctanner.network_cloudengine.cess_id.isdigit():
            self.module.fail_json(msg="Error: projctanner.network_cloudengine.cess_id is not digit.")
        if int(self.projctanner.network_cloudengine.cess_id) < 1 or int(self.projctanner.network_cloudengine.cess_id) > 4294967295:
            self.module.fail_json(msg="Error: projctanner.network_cloudengine.cess_id must be an integer between 1 and 4294967295.")

        # area check
        if self.area.isdigit():
            if int(self.area) < 0 or int(self.area) > 4294967295:
                self.module.fail_json(msg="Error: area id (Integer) must be between 0 and 4294967295.")
        else:
            if not is_valid_v4addr(self.area):
                self.module.fail_json(msg="Error: area id is invalid.")

        # area authentication check
        if self.state == "present":
            if self.auth_mode:
                if self.auth_mode == "simple":
                    if self.auth_text_simple and len(self.auth_text_simple) > 8:
                        self.module.fail_json(
                            msg="Error: auth_text_simple is not in the range from 1 to 8.")
                if self.auth_mode in ["hmac-sha256", "hmac-sha256", "md5"]:
                    if self.auth_key_id and not self.auth_text_md5:
                        self.module.fail_json(
                            msg='Error: auth_key_id and auth_text_md5 should be set at the same time.')
                    if not self.auth_key_id and self.auth_text_md5:
                        self.module.fail_json(
                            msg='Error: auth_key_id and auth_text_md5 should be set at the same time.')
                    if self.auth_key_id:
                        if not self.auth_key_id.isdigit():
                            self.module.fail_json(
                                msg="Error: auth_key_id is not digit.")
                        if int(self.auth_key_id) < 1 or int(self.auth_key_id) > 255:
                            self.module.fail_json(
                                msg="Error: auth_key_id is not in the range from 1 to 255.")
                    if self.auth_text_md5 and len(self.auth_text_md5) > 255:
                        self.module.fail_json(
                            msg="Error: auth_text_md5 is not in the range from 1 to 255.")
        # cost check
        if self.cost:
            if not self.cost.isdigit():
                self.module.fail_json(msg="Error: cost is not digit.")
            if int(self.cost) < 1 or int(self.cost) > 65535:
                self.module.fail_json(
                    msg="Error: cost is not in the range from 1 to 65535")

        # hello_interval check
        if self.hello_interval:
            if not self.hello_interval.isdigit():
                self.module.fail_json(
                    msg="Error: hello_interval is not digit.")
            if int(self.hello_interval) < 1 or int(self.hello_interval) > 65535:
                self.module.fail_json(
                    msg="Error: hello_interval is not in the range from 1 to 65535")

        # dead_interval check
        if self.dead_interval:
            if not self.dead_interval.isdigit():
                self.module.fail_json(msg="Error: dead_interval is not digit.")
            if int(self.dead_interval) < 1 or int(self.dead_interval) > 235926000:
                self.module.fail_json(
                    msg="Error: dead_interval is not in the range from 1 to 235926000")

    def get_proposed(self):
        """get proposed info"""

        self.proposed["interfajctanner.network_cloudengine.ce"] = self.interfajctanner.network_cloudengine.ce
        self.proposed["projctanner.network_cloudengine.cess_id"] = self.projctanner.network_cloudengine.cess_id
        self.proposed["area"] = self.get_area_ip()
        self.proposed["cost"] = self.cost
        self.proposed["hello_interval"] = self.hello_interval
        self.proposed["dead_interval"] = self.dead_interval
        self.proposed["silent_interfajctanner.network_cloudengine.ce"] = self.silent_interfajctanner.network_cloudengine.ce
        if self.auth_mode:
            self.proposed["auth_mode"] = self.auth_mode
            if self.auth_mode == "simple":
                self.proposed["auth_text_simple"] = self.auth_text_simple
            if self.auth_mode in ["hmac-sha256", "hmac-sha256", "md5"]:
                self.proposed["auth_key_id"] = self.auth_key_id
                self.proposed["auth_text_md5"] = self.auth_text_md5
        self.proposed["state"] = self.state

    def get_existing(self):
        """get existing info"""

        if not self.ospf_info:
            return

        if self.ospf_info["interfajctanner.network_cloudengine.ce"]:
            self.existing["interfajctanner.network_cloudengine.ce"] = self.interfajctanner.network_cloudengine.ce
            self.existing["cost"] = self.ospf_info["interfajctanner.network_cloudengine.ce"].get("configCost")
            self.existing["hello_interval"] = self.ospf_info["interfajctanner.network_cloudengine.ce"].get("helloInterval")
            self.existing["dead_interval"] = self.ospf_info["interfajctanner.network_cloudengine.ce"].get("deadInterval")
            self.existing["silent_interfajctanner.network_cloudengine.ce"] = self.ospf_info["interfajctanner.network_cloudengine.ce"].get("silentEnable")
            self.existing["auth_mode"] = self.ospf_info["interfajctanner.network_cloudengine.ce"].get("authenticationMode")
            self.existing["auth_text_simple"] = self.ospf_info["interfajctanner.network_cloudengine.ce"].get("authTextSimple")
            self.existing["auth_key_id"] = self.ospf_info["interfajctanner.network_cloudengine.ce"].get("keyId")
            self.existing["auth_text_md5"] = self.ospf_info["interfajctanner.network_cloudengine.ce"].get("authTextMd5")
        self.existing["projctanner.network_cloudengine.cess_id"] = self.ospf_info["projctanner.network_cloudengine.cessId"]
        self.existing["area"] = self.ospf_info["areaId"]

    def get_end_state(self):
        """get end state info"""

        ospf_info = self.get_ospf_dict()
        if not ospf_info:
            return

        if ospf_info["interfajctanner.network_cloudengine.ce"]:
            self.end_state["interfajctanner.network_cloudengine.ce"] = self.interfajctanner.network_cloudengine.ce
            self.end_state["cost"] = ospf_info["interfajctanner.network_cloudengine.ce"].get("configCost")
            self.end_state["hello_interval"] = ospf_info["interfajctanner.network_cloudengine.ce"].get("helloInterval")
            self.end_state["dead_interval"] = ospf_info["interfajctanner.network_cloudengine.ce"].get("deadInterval")
            self.end_state["silent_interfajctanner.network_cloudengine.ce"] = ospf_info["interfajctanner.network_cloudengine.ce"].get("silentEnable")
            self.end_state["auth_mode"] = ospf_info["interfajctanner.network_cloudengine.ce"].get("authenticationMode")
            self.end_state["auth_text_simple"] = ospf_info["interfajctanner.network_cloudengine.ce"].get("authTextSimple")
            self.end_state["auth_key_id"] = ospf_info["interfajctanner.network_cloudengine.ce"].get("keyId")
            self.end_state["auth_text_md5"] = ospf_info["interfajctanner.network_cloudengine.ce"].get("authTextMd5")
        self.end_state["projctanner.network_cloudengine.cess_id"] = ospf_info["projctanner.network_cloudengine.cessId"]
        self.end_state["area"] = ospf_info["areaId"]

    def work(self):
        """worker"""

        self.check_params()
        self.ospf_info = self.get_ospf_dict()
        self.get_existing()
        self.get_proposed()

        # deal present or absent
        if self.state == "present":
            if not self.ospf_info or not self.ospf_info["interfajctanner.network_cloudengine.ce"]:
                # create ospf area and set interfajctanner.network_cloudengine.ce config
                self.set_ospf_interfajctanner.network_cloudengine.ce()
            else:
                # merge interfajctanner.network_cloudengine.ce ospf area config
                self.merge_ospf_interfajctanner.network_cloudengine.ce()
        else:
            if self.ospf_info and self.ospf_info["interfajctanner.network_cloudengine.ce"]:
                # delete interfajctanner.network_cloudengine.ce ospf area config
                self.unset_ospf_interfajctanner.network_cloudengine.ce()

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
        interfajctanner.network_cloudengine.ce=dict(required=True, type='str'),
        projctanner.network_cloudengine.cess_id=dict(required=True, type='str'),
        area=dict(required=True, type='str'),
        cost=dict(required=False, type='str'),
        hello_interval=dict(required=False, type='str'),
        dead_interval=dict(required=False, type='str'),
        silent_interfajctanner.network_cloudengine.ce=dict(required=False, default=False, type='bool'),
        auth_mode=dict(required=False,
                       choijctanner.network_cloudengine.ces=['none', 'null', 'hmac-sha256', 'md5', 'hmac-md5', 'simple'], type='str'),
        auth_text_simple=dict(required=False, type='str', no_log=True),
        auth_key_id=dict(required=False, type='str'),
        auth_text_md5=dict(required=False, type='str', no_log=True),
        state=dict(required=False, default='present',
                   choijctanner.network_cloudengine.ces=['present', 'absent'])
    )

    argument_spec.update(jctanner.network_cloudengine.ce_argument_spec)
    module = Interfajctanner.network_cloudengine.ceOSPF(argument_spec)
    module.work()


if __name__ == '__main__':
    main()
