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
module: jctanner.network_cloudengine.ce_ospf
version_added: "2.4"
short_description: Manages configuration of an OSPF instanjctanner.network_cloudengine.ce on HUAWEI CloudEngine switches.
description:
    - Manages configuration of an OSPF instanjctanner.network_cloudengine.ce on HUAWEI CloudEngine switches.
author: QijunPan (@QijunPan)
options:
    projctanner.network_cloudengine.cess_id:
        description:
            - Specifies a projctanner.network_cloudengine.cess ID.
              The value is an integer ranging from 1 to 4294967295.
        required: true
    area:
        description:
            - Specifies the area ID. The area with the area-id being 0 is a backbone area.
              Valid values are a string, formatted as an IP address
              (i.e. "0.0.0.0") or as an integer between 1 and 4294967295.
    addr:
        description:
            - Specifies the address of the network segment where the interfajctanner.network_cloudengine.ce resides.
              The value is in dotted decimal notation.
    mask:
        description:
            - IP network wildcard bits in decimal format between 0 and 32.
    auth_mode:
        description:
            - Specifies the authentication type.
        choijctanner.network_cloudengine.ces: ['none', 'hmac-sha256', 'md5', 'hmac-md5', 'simple']
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
    nexthop_addr:
        description:
            - IPv4 address for configure next-hop address's weight.
              Valid values are a string, formatted as an IP address.
    nexthop_weight:
        description:
            - Indicates the weight of the next hop.
              The smaller the value is, the higher the preferenjctanner.network_cloudengine.ce of the route is.
              It is an integer that ranges from 1 to 254.
    max_load_balanjctanner.network_cloudengine.ce:
        description:
            - The maximum number of paths for forward packets over multiple paths.
              Valid value is an integer in the range from 1 to 64.
    state:
        description:
            - Determines whether the config should be present or not
              on the devijctanner.network_cloudengine.ce.
        default: present
        choijctanner.network_cloudengine.ces: ['present','absent']
'''

EXAMPLES = '''
- name: ospf module test
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

  - name: Configure ospf
    jctanner.network_cloudengine.ce_ospf:
      projctanner.network_cloudengine.cess_id: 1
      area: 100
      state: present
      provider: "{{ cli }}"
'''

RETURN = '''
proposed:
    description: k/v pairs of parameters passed into module
    returned: verbose mode
    type: dict
    sample: {"projctanner.network_cloudengine.cess_id": "1", "area": "100"}
existing:
    description: k/v pairs of existing configuration
    returned: verbose mode
    type: dict
    sample: {"projctanner.network_cloudengine.cess_id": "1", "areas": [], "nexthops":[], "max_load_balanjctanner.network_cloudengine.ce": "32"}
end_state:
    description: k/v pairs of configuration after module execution
    returned: verbose mode
    type: dict
    sample: {"projctanner.network_cloudengine.cess_id": "1",
             "areas": [{"areaId": "0.0.0.100", "areaType": "Normal"}],
             "nexthops":[], "max_load_balanjctanner.network_cloudengine.ce": "32"}
updates:
    description: commands sent to the devijctanner.network_cloudengine.ce
    returned: always
    type: list
    sample: ["ospf 1", "area 0.0.0.100"]
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
              <Projctanner.network_cloudengine.cessTopologys>
                <Projctanner.network_cloudengine.cessTopology>
                  <nexthopMTs></nexthopMTs>
                  <maxLoadBalancing></maxLoadBalancing>
                </Projctanner.network_cloudengine.cessTopology>
              </Projctanner.network_cloudengine.cessTopologys>
              <areas>
                <area>
                  <areaId></areaId>
                  <areaType></areaType>
                  <authenticationMode></authenticationMode>
                  <authTextSimple></authTextSimple>
                  <keyId></keyId>
                  <authTextMd5></authTextMd5>
                  <networks>
                    <network>
                      <ipAddress></ipAddress>
                      <wildcardMask></wildcardMask>
                    </network>
                  </networks>
                </area>
              </areas>
            </ospfSite>
          </ospfSites>
        </ospfv2comm>
      </ospfv2>
    </filter>
"""

CE_NC_CREATE_PROCESS = """
    <config>
      <ospfv2 xmlns="http://www.huawei.com/netconf/vrp" content-version="1.0" format-version="1.0">
        <ospfv2comm>
          <ospfSites>
            <ospfSite operation="merge">
              <projctanner.network_cloudengine.cessId>%s</projctanner.network_cloudengine.cessId>
            </ospfSite>
          </ospfSites>
        </ospfv2comm>
      </ospfv2>
    </config>
"""

CE_NC_DELETE_PROCESS = """
    <config>
      <ospfv2 xmlns="http://www.huawei.com/netconf/vrp" content-version="1.0" format-version="1.0">
        <ospfv2comm>
          <ospfSites>
            <ospfSite operation="delete">
              <projctanner.network_cloudengine.cessId>%s</projctanner.network_cloudengine.cessId>
            </ospfSite>
          </ospfSites>
        </ospfv2comm>
      </ospfv2>
    </config>
"""

CE_NC_XML_BUILD_MERGE_PROCESS = """
    <config>
      <ospfv2 xmlns="http://www.huawei.com/netconf/vrp" content-version="1.0" format-version="1.0">
        <ospfv2comm>
          <ospfSites>
            <ospfSite operation="merge">
              <projctanner.network_cloudengine.cessId>%s</projctanner.network_cloudengine.cessId>
              %s
            </ospfSite>
          </ospfSites>
        </ospfv2comm>
      </ospfv2>
    </config>
"""

CE_NC_XML_BUILD_PROCESS = """
    <config>
      <ospfv2 xmlns="http://www.huawei.com/netconf/vrp" content-version="1.0" format-version="1.0">
        <ospfv2comm>
          <ospfSites>
            <ospfSite>
              <projctanner.network_cloudengine.cessId>%s</projctanner.network_cloudengine.cessId>
              %s
            </ospfSite>
          </ospfSites>
        </ospfv2comm>
      </ospfv2>
    </config>
"""

CE_NC_XML_BUILD_MERGE_AREA = """
              <areas>
                <area operation="merge">
                  <areaId>%s</areaId>
                  %s
                </area>
              </areas>
"""

CE_NC_XML_BUILD_DELETE_AREA = """
              <areas>
                <area operation="delete">
                  <areaId>%s</areaId>
                  %s
                </area>
              </areas>
"""

CE_NC_XML_BUILD_AREA = """
              <areas>
                <area>
                  <areaId>%s</areaId>
                  %s
                </area>
              </areas>
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


CE_NC_XML_MERGE_NETWORKS = """
                  <networks>
                    <network operation="merge">
                      <ipAddress>%s</ipAddress>
                      <wildcardMask>%s</wildcardMask>
                    </network>
                  </networks>
"""

CE_NC_XML_DELETE_NETWORKS = """
                  <networks>
                    <network operation="delete">
                      <ipAddress>%s</ipAddress>
                      <wildcardMask>%s</wildcardMask>
                    </network>
                  </networks>
"""

CE_NC_XML_SET_LB = """
                <maxLoadBalancing>%s</maxLoadBalancing>
"""


CE_NC_XML_BUILD_MERGE_TOPO = """
            <Projctanner.network_cloudengine.cessTopologys>
              <Projctanner.network_cloudengine.cessTopology operation="merge">
              <topoName>base</topoName>
              %s
              </Projctanner.network_cloudengine.cessTopology>
            </Projctanner.network_cloudengine.cessTopologys>

"""

CE_NC_XML_BUILD_TOPO = """
            <Projctanner.network_cloudengine.cessTopologys>
              <Projctanner.network_cloudengine.cessTopology >
              <topoName>base</topoName>
              %s
              </Projctanner.network_cloudengine.cessTopology>
            </Projctanner.network_cloudengine.cessTopologys>

"""

CE_NC_XML_MERGE_NEXTHOP = """
                <nexthopMTs>
                  <nexthopMT operation="merge">
                    <ipAddress>%s</ipAddress>
                    <weight>%s</weight>
                  </nexthopMT>
                </nexthopMTs>
"""

CE_NC_XML_DELETE_NEXTHOP = """
                <nexthopMTs>
                  <nexthopMT operation="delete">
                    <ipAddress>%s</ipAddress>
                  </nexthopMT>
                </nexthopMTs>
"""


class OSPF(object):
    """
    Manages configuration of an ospf instanjctanner.network_cloudengine.ce.
    """

    def __init__(self, argument_spec):
        self.spec = argument_spec
        self.module = None
        self.init_module()

        # module input info
        self.projctanner.network_cloudengine.cess_id = self.module.params['projctanner.network_cloudengine.cess_id']
        self.area = self.module.params['area']
        self.addr = self.module.params['addr']
        self.mask = self.module.params['mask']
        self.auth_mode = self.module.params['auth_mode']
        self.auth_text_simple = self.module.params['auth_text_simple']
        self.auth_key_id = self.module.params['auth_key_id']
        self.auth_text_md5 = self.module.params['auth_text_md5']
        self.nexthop_addr = self.module.params['nexthop_addr']
        self.nexthop_weight = self.module.params['nexthop_weight']
        self.max_load_balanjctanner.network_cloudengine.ce = self.module.params['max_load_balanjctanner.network_cloudengine.ce']
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
        """ init module """

        required_together = [
            ("addr", "mask"),
            ("auth_key_id", "auth_text_md5"),
            ("nexthop_addr", "nexthop_weight")
        ]
        self.module = AnsibleModule(
            argument_spec=self.spec, required_together=required_together, supports_check_mode=True)

    def check_response(self, xml_str, xml_name):
        """Check if response message is already sucjctanner.network_cloudengine.ceed."""

        if "<ok/>" not in xml_str:
            self.module.fail_json(msg='Error: %s failed.' % xml_name)

    def get_wildcard_mask(self):
        """convert mask length to ip address wildcard mask, i.e. 24 to 0.0.0.255"""

        mask_int = ["255"] * 4
        length = int(self.mask)

        if length > 32:
            self.module.fail_json(msg='IPv4 ipaddress mask length is invalid')
        if length < 8:
            mask_int[0] = str(int(~(0xFF << (8 - length % 8)) & 0xFF))
        if length >= 8:
            mask_int[0] = '0'
            mask_int[1] = str(int(~(0xFF << (16 - (length % 16))) & 0xFF))
        if length >= 16:
            mask_int[1] = '0'
            mask_int[2] = str(int(~(0xFF << (24 - (length % 24))) & 0xFF))
        if length >= 24:
            mask_int[2] = '0'
            mask_int[3] = str(int(~(0xFF << (32 - (length % 32))) & 0xFF))
        if length == 32:
            mask_int[3] = '0'

        return '.'.join(mask_int)

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

    def get_ospf_dict(self, projctanner.network_cloudengine.cess_id):
        """ get one ospf attributes dict."""

        ospf_info = dict()
        conf_str = CE_NC_GET_OSPF % projctanner.network_cloudengine.cess_id
        xml_str = get_nc_config(self.module, conf_str)
        if "<data/>" in xml_str:
            return ospf_info

        xml_str = xml_str.replajctanner.network_cloudengine.ce('\r', '').replajctanner.network_cloudengine.ce('\n', '').\
            replajctanner.network_cloudengine.ce('xmlns="urn:ietf:params:xml:ns:netconf:base:1.0"', "").\
            replajctanner.network_cloudengine.ce('xmlns="http://www.huawei.com/netconf/vrp"', "")

        # get projctanner.network_cloudengine.cess base info
        root = ElementTree.fromstring(xml_str)
        ospfsite = root.find("ospfv2/ospfv2comm/ospfSites/ospfSite")
        if ospfsite:
            for site in ospfsite:
                if site.tag in ["projctanner.network_cloudengine.cessId", "routerId", "vrfName"]:
                    ospf_info[site.tag] = site.text

        # get Topology info
        topo = root.find(
            "ospfv2/ospfv2comm/ospfSites/ospfSite/Projctanner.network_cloudengine.cessTopologys/Projctanner.network_cloudengine.cessTopology")
        if topo:
            for eles in topo:
                if eles.tag in ["maxLoadBalancing"]:
                    ospf_info[eles.tag] = eles.text

        # get nexthop info
        ospf_info["nexthops"] = list()
        nexthops = root.findall(
            "ospfv2/ospfv2comm/ospfSites/ospfSite/Projctanner.network_cloudengine.cessTopologys/Projctanner.network_cloudengine.cessTopology/nexthopMTs/nexthopMT")
        if nexthops:
            for nexthop in nexthops:
                nh_dict = dict()
                for ele in nexthop:
                    if ele.tag in ["ipAddress", "weight"]:
                        nh_dict[ele.tag] = ele.text
                ospf_info["nexthops"].append(nh_dict)

        # get areas info
        ospf_info["areas"] = list()
        areas = root.findall(
            "ospfv2/ospfv2comm/ospfSites/ospfSite/areas/area")
        if areas:
            for area in areas:
                area_dict = dict()
                for ele in area:
                    if ele.tag in ["areaId", "authTextSimple", "areaType",
                                   "authenticationMode", "keyId", "authTextMd5"]:
                        area_dict[ele.tag] = ele.text
                    if ele.tag == "networks":
                        # get networks info
                        area_dict["networks"] = list()
                        for net in ele:
                            net_dict = dict()
                            for net_ele in net:
                                if net_ele.tag in ["ipAddress", "wildcardMask"]:
                                    net_dict[net_ele.tag] = net_ele.text
                            area_dict["networks"].append(net_dict)

                ospf_info["areas"].append(area_dict)
        return ospf_info

    def is_area_exist(self):
        """is ospf area exist"""
        if not self.ospf_info:
            return False
        for area in self.ospf_info["areas"]:
            if area["areaId"] == self.get_area_ip():
                return True

        return False

    def is_network_exist(self):
        """is ospf area network exist"""
        if not self.ospf_info:
            return False

        for area in self.ospf_info["areas"]:
            if area["areaId"] == self.get_area_ip():
                if not area.get("networks"):
                    return False
                for network in area.get("networks"):
                    if network["ipAddress"] == self.addr and network["wildcardMask"] == self.get_wildcard_mask():
                        return True
            else:
                break

        return False

    def is_nexthop_exist(self):
        """is ospf nexthop exist"""

        if not self.ospf_info:
            return False
        for nexthop in self.ospf_info["nexthops"]:
            if nexthop["ipAddress"] == self.nexthop_addr:
                return True

        return False

    def is_nexthop_change(self):
        """is ospf nexthop change"""
        if not self.ospf_info:
            return True

        for nexthop in self.ospf_info["nexthops"]:
            if nexthop["ipAddress"] == self.nexthop_addr:
                if nexthop["weight"] == self.nexthop_weight:
                    return False
                else:
                    return True

        return True

    def create_projctanner.network_cloudengine.cess(self):
        """Create ospf projctanner.network_cloudengine.cess"""

        xml_area = ""
        self.updates_cmd.append("ospf %s" % self.projctanner.network_cloudengine.cess_id)
        xml_create = CE_NC_CREATE_PROCESS % self.projctanner.network_cloudengine.cess_id
        set_nc_config(self.module, xml_create)

        # nexthop weight
        xml_nh = ""
        if self.nexthop_addr:
            xml_nh = CE_NC_XML_MERGE_NEXTHOP % (
                self.nexthop_addr, self.nexthop_weight)
            self.updates_cmd.append("nexthop %s weight %s" % (
                self.nexthop_addr, self.nexthop_weight))

        # max load balanjctanner.network_cloudengine.ce
        xml_lb = ""
        if self.max_load_balanjctanner.network_cloudengine.ce:
            xml_lb = CE_NC_XML_SET_LB % self.max_load_balanjctanner.network_cloudengine.ce
            self.updates_cmd.append(
                "maximum load-balancing %s" % self.max_load_balanjctanner.network_cloudengine.ce)

        xml_topo = ""
        if xml_lb or xml_nh:
            xml_topo = CE_NC_XML_BUILD_TOPO % (xml_nh + xml_lb)

        if self.area:
            self.updates_cmd.append("area %s" % self.get_area_ip())
            xml_auth = ""
            xml_network = ""

            # networks
            if self.addr and self.mask:
                xml_network = CE_NC_XML_MERGE_NETWORKS % (
                    self.addr, self.get_wildcard_mask())
                self.updates_cmd.append("network %s %s" % (
                    self.addr, self.get_wildcard_mask()))

            # authentication mode
            if self.auth_mode:
                xml_auth += CE_NC_XML_SET_AUTH_MODE % self.auth_mode
                if self.auth_mode == "none":
                    self.updates_cmd.append("undo authentication-mode")
                else:
                    self.updates_cmd.append(
                        "authentication-mode %s" % self.auth_mode)
                if self.auth_mode == "simple" and self.auth_text_simple:
                    xml_auth += CE_NC_XML_SET_AUTH_TEXT_SIMPLE % self.auth_text_simple
                    self.updates_cmd.pop()
                    self.updates_cmd.append(
                        "authentication-mode %s %s" % (self.auth_mode, self.auth_text_simple))
                if self.auth_mode in ["hmac-sha256", "hmac-sha256", "md5"]:
                    if self.auth_key_id and self.auth_text_md5:
                        xml_auth += CE_NC_XML_SET_AUTH_MD5 % (
                            self.auth_key_id, self.auth_text_md5)
                        self.updates_cmd.pop()
                        self.updates_cmd.append(
                            "authentication-mode %s %s %s" % (self.auth_mode, self.auth_key_id, self.auth_text_md5))
            if xml_network or xml_auth or not self.is_area_exist():
                xml_area += CE_NC_XML_BUILD_MERGE_AREA % (
                    self.get_area_ip(), xml_network + xml_auth)

        xml_str = CE_NC_XML_BUILD_MERGE_PROCESS % (
            self.projctanner.network_cloudengine.cess_id, xml_topo + xml_area)
        recv_xml = set_nc_config(self.module, xml_str)
        self.check_response(recv_xml, "CREATE_PROCESS")
        self.changed = True

    def delete_projctanner.network_cloudengine.cess(self):
        """Delete ospf projctanner.network_cloudengine.cess"""

        xml_str = CE_NC_DELETE_PROCESS % self.projctanner.network_cloudengine.cess_id
        recv_xml = set_nc_config(self.module, xml_str)
        self.check_response(recv_xml, "DELETE_PROCESS")
        self.updates_cmd.append("undo ospf %s" % self.projctanner.network_cloudengine.cess_id)
        self.changed = True

    def merge_projctanner.network_cloudengine.cess(self):
        """merge ospf projctanner.network_cloudengine.cess"""

        xml_area = ""
        xml_str = ""
        self.updates_cmd.append("ospf %s" % self.projctanner.network_cloudengine.cess_id)

        # nexthop weight
        xml_nh = ""
        if self.nexthop_addr and self.is_nexthop_change():
            xml_nh = CE_NC_XML_MERGE_NEXTHOP % (
                self.nexthop_addr, self.nexthop_weight)
            self.updates_cmd.append("nexthop %s weight %s" % (
                self.nexthop_addr, self.nexthop_weight))

        # max load balanjctanner.network_cloudengine.ce
        xml_lb = ""
        if self.max_load_balanjctanner.network_cloudengine.ce and self.ospf_info.get("maxLoadBalancing") != self.max_load_balanjctanner.network_cloudengine.ce:
            xml_lb = CE_NC_XML_SET_LB % self.max_load_balanjctanner.network_cloudengine.ce
            self.updates_cmd.append(
                "maximum load-balancing %s" % self.max_load_balanjctanner.network_cloudengine.ce)

        xml_topo = ""
        if xml_lb or xml_nh:
            xml_topo = CE_NC_XML_BUILD_MERGE_TOPO % (xml_nh + xml_lb)

        if self.area:
            self.updates_cmd.append("area %s" % self.get_area_ip())
            xml_network = ""
            xml_auth = ""
            if self.addr and self.mask:
                if not self.is_network_exist():
                    xml_network += CE_NC_XML_MERGE_NETWORKS % (
                        self.addr, self.get_wildcard_mask())
                    self.updates_cmd.append("network %s %s" % (
                        self.addr, self.get_wildcard_mask()))

            # NOTE: for security, authentication config will always be update
            if self.auth_mode:
                xml_auth += CE_NC_XML_SET_AUTH_MODE % self.auth_mode
                if self.auth_mode == "none":
                    self.updates_cmd.append("undo authentication-mode")
                else:
                    self.updates_cmd.append(
                        "authentication-mode %s" % self.auth_mode)
                if self.auth_mode == "simple" and self.auth_text_simple:
                    xml_auth += CE_NC_XML_SET_AUTH_TEXT_SIMPLE % self.auth_text_simple
                    self.updates_cmd.pop()
                    self.updates_cmd.append(
                        "authentication-mode %s %s" % (self.auth_mode, self.auth_text_simple))
                if self.auth_mode in ["hmac-sha256", "hmac-sha256", "md5"]:
                    if self.auth_key_id and self.auth_text_md5:
                        xml_auth += CE_NC_XML_SET_AUTH_MD5 % (
                            self.auth_key_id, self.auth_text_md5)
                        self.updates_cmd.pop()
                        self.updates_cmd.append(
                            "authentication-mode %s %s %s" % (self.auth_mode, self.auth_key_id, self.auth_text_md5))
            if xml_network or xml_auth or not self.is_area_exist():
                xml_area += CE_NC_XML_BUILD_MERGE_AREA % (
                    self.get_area_ip(), xml_network + xml_auth)
            elif self.is_area_exist():
                self.updates_cmd.pop()  # remove command: area
            else:
                pass

        if xml_area or xml_topo:
            xml_str = CE_NC_XML_BUILD_MERGE_PROCESS % (
                self.projctanner.network_cloudengine.cess_id, xml_topo + xml_area)
            recv_xml = set_nc_config(self.module, xml_str)
            self.check_response(recv_xml, "MERGE_PROCESS")
            self.changed = True

    def remove_area_network(self):
        """remvoe ospf area network"""

        if not self.is_network_exist():
            return

        xml_network = CE_NC_XML_DELETE_NETWORKS % (
            self.addr, self.get_wildcard_mask())
        xml_area = CE_NC_XML_BUILD_AREA % (self.get_area_ip(), xml_network)
        xml_str = CE_NC_XML_BUILD_PROCESS % (self.projctanner.network_cloudengine.cess_id, xml_area)
        recv_xml = set_nc_config(self.module, xml_str)
        self.check_response(recv_xml, "DELETE_AREA_NETWORK")
        self.updates_cmd.append("ospf %s" % self.projctanner.network_cloudengine.cess_id)
        self.updates_cmd.append("area %s" % self.get_area_ip())
        self.updates_cmd.append("undo network %s %s" %
                                (self.addr, self.get_wildcard_mask()))
        self.changed = True

    def remove_area(self):
        """remove ospf area"""

        if not self.is_area_exist():
            return

        xml_area = CE_NC_XML_BUILD_DELETE_AREA % (self.get_area_ip(), "")
        xml_str = CE_NC_XML_BUILD_PROCESS % (self.projctanner.network_cloudengine.cess_id, xml_area)
        recv_xml = set_nc_config(self.module, xml_str)
        self.check_response(recv_xml, "DELETE_AREA")
        self.updates_cmd.append("ospf %s" % self.projctanner.network_cloudengine.cess_id)
        self.updates_cmd.append("undo area %s" % self.get_area_ip())
        self.changed = True

    def remove_nexthop(self):
        """remove ospf nexthop weight"""

        if not self.is_nexthop_exist():
            return

        xml_nh = CE_NC_XML_DELETE_NEXTHOP % self.nexthop_addr
        xml_topo = CE_NC_XML_BUILD_TOPO % xml_nh
        xml_str = CE_NC_XML_BUILD_PROCESS % (self.projctanner.network_cloudengine.cess_id, xml_topo)
        recv_xml = set_nc_config(self.module, xml_str)
        self.check_response(recv_xml, "DELETE_NEXTHOP_WEIGHT")
        self.updates_cmd.append("ospf %s" % self.projctanner.network_cloudengine.cess_id)
        self.updates_cmd.append("undo nexthop %s" % self.nexthop_addr)
        self.changed = True

    def is_valid_v4addr(self, addr):
        """check is ipv4 addr is valid"""

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

    def convert_ip_to_network(self):
        """convert ip to subnet address"""

        ip_list = self.addr.split('.')
        mask_list = self.get_wildcard_mask().split('.')

        for i in range(len(ip_list)):
            ip_list[i] = str((int(ip_list[i]) & (~int(mask_list[i]))) & 0xff)

        self.addr = '.'.join(ip_list)

    def check_params(self):
        """Check all input params"""

        # projctanner.network_cloudengine.cess_id check
        if not self.projctanner.network_cloudengine.cess_id.isdigit():
            self.module.fail_json(msg="Error: projctanner.network_cloudengine.cess_id is not digit.")
        if int(self.projctanner.network_cloudengine.cess_id) < 1 or int(self.projctanner.network_cloudengine.cess_id) > 4294967295:
            self.module.fail_json(
                msg="Error: projctanner.network_cloudengine.cess_id must be an integer between 1 and 4294967295.")

        if self.area:
            # area check
            if self.area.isdigit():
                if int(self.area) < 0 or int(self.area) > 4294967295:
                    self.module.fail_json(
                        msg="Error: area id (Integer) must be between 0 and 4294967295.")

            else:
                if not self.is_valid_v4addr(self.area):
                    self.module.fail_json(msg="Error: area id is invalid.")

            # area network check
            if self.addr:
                if not self.is_valid_v4addr(self.addr):
                    self.module.fail_json(
                        msg="Error: network addr is invalid.")
                if not self.mask.isdigit():
                    self.module.fail_json(
                        msg="Error: network mask is not digit.")
                if int(self.mask) < 0 or int(self.mask) > 32:
                    self.module.fail_json(
                        msg="Error: network mask is invalid.")

            # area authentication check
            if self.state == "present" and self.auth_mode:
                if self.auth_mode == "simple":
                    if self.auth_text_simple and len(self.auth_text_simple) > 8:
                        self.module.fail_json(
                            msg="Error: auth_text_simple is not in the range from 1 to 8.")
                if self.auth_mode in ["hmac-sha256", "hmac-sha256", "md5"]:
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

        # projctanner.network_cloudengine.cess max load balanjctanner.network_cloudengine.ce check
        if self.state == "present" and self.max_load_balanjctanner.network_cloudengine.ce:
            if not self.max_load_balanjctanner.network_cloudengine.ce.isdigit():
                self.module.fail_json(
                    msg="Error: max_load_balanjctanner.network_cloudengine.ce is not digit.")
            if int(self.max_load_balanjctanner.network_cloudengine.ce) < 1 or int(self.max_load_balanjctanner.network_cloudengine.ce) > 64:
                self.module.fail_json(
                    msg="Error: max_load_balanjctanner.network_cloudengine.ce is not in the range from 1 to 64.")

        # projctanner.network_cloudengine.cess nexthop weight check
        if self.nexthop_addr:
            if not self.is_valid_v4addr(self.nexthop_addr):
                self.module.fail_json(msg="Error: nexthop_addr is invalid.")
            if not self.nexthop_weight.isdigit():
                self.module.fail_json(
                    msg="Error: nexthop_weight is not digit.")
            if int(self.nexthop_weight) < 1 or int(self.nexthop_weight) > 254:
                self.module.fail_json(
                    msg="Error: nexthop_weight is not in the range from 1 to 254.")

        if self.addr:
            self.convert_ip_to_network()

    def get_proposed(self):
        """get proposed info"""

        self.proposed["projctanner.network_cloudengine.cess_id"] = self.projctanner.network_cloudengine.cess_id
        self.proposed["area"] = self.area
        if self.area:
            self.proposed["addr"] = self.addr
            self.proposed["mask"] = self.mask
            if self.auth_mode:
                self.proposed["auth_mode"] = self.auth_mode
                if self.auth_mode == "simple":
                    self.proposed["auth_text_simple"] = self.auth_text_simple
                if self.auth_mode in ["hmac-sha256", "hmac-sha256", "md5"]:
                    self.proposed["auth_key_id"] = self.auth_key_id
                    self.proposed["auth_text_md5"] = self.auth_text_md5

        if self.nexthop_addr:
            self.proposed["nexthop_addr"] = self.nexthop_addr
            self.proposed["nexthop_weight"] = self.nexthop_weight
        self.proposed["max_load_balanjctanner.network_cloudengine.ce"] = self.max_load_balanjctanner.network_cloudengine.ce
        self.proposed["state"] = self.state

    def get_existing(self):
        """get existing info"""

        if not self.ospf_info:
            return

        self.existing["projctanner.network_cloudengine.cess_id"] = self.projctanner.network_cloudengine.cess_id
        self.existing["areas"] = self.ospf_info["areas"]
        self.existing["nexthops"] = self.ospf_info["nexthops"]
        self.existing["max_load_balanjctanner.network_cloudengine.ce"] = self.ospf_info.get(
            "maxLoadBalancing")

    def get_end_state(self):
        """get end state info"""

        ospf_info = self.get_ospf_dict(self.projctanner.network_cloudengine.cess_id)

        if not ospf_info:
            return

        self.end_state["projctanner.network_cloudengine.cess_id"] = self.projctanner.network_cloudengine.cess_id
        self.end_state["areas"] = ospf_info["areas"]
        self.end_state["nexthops"] = ospf_info["nexthops"]
        self.end_state["max_load_balanjctanner.network_cloudengine.ce"] = ospf_info.get("maxLoadBalancing")

        if self.end_state == self.existing:
            self.changed = False

    def work(self):
        """worker"""

        self.check_params()
        self.ospf_info = self.get_ospf_dict(self.projctanner.network_cloudengine.cess_id)
        self.get_existing()
        self.get_proposed()

        # deal present or absent
        if self.state == "present":
            if not self.ospf_info:
                # create ospf projctanner.network_cloudengine.cess
                self.create_projctanner.network_cloudengine.cess()
            else:
                # merge ospf
                self.merge_projctanner.network_cloudengine.cess()
        else:
            if self.ospf_info:
                if self.area:
                    if self.addr:
                        # remove ospf area network
                        self.remove_area_network()
                    else:
                        # remove ospf area
                        self.remove_area()
                if self.nexthop_addr:
                    # remove ospf nexthop weight
                    self.remove_nexthop()

                if not self.area and not self.nexthop_addr:
                    # remove ospf projctanner.network_cloudengine.cess
                    self.delete_projctanner.network_cloudengine.cess()
            else:
                self.module.fail_json(msg='Error: ospf projctanner.network_cloudengine.cess does not exist')

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
        projctanner.network_cloudengine.cess_id=dict(required=True, type='str'),
        area=dict(required=False, type='str'),
        addr=dict(required=False, type='str'),
        mask=dict(required=False, type='str'),
        auth_mode=dict(required=False,
                       choijctanner.network_cloudengine.ces=['none', 'hmac-sha256', 'md5', 'hmac-md5', 'simple'], type='str'),
        auth_text_simple=dict(required=False, type='str', no_log=True),
        auth_key_id=dict(required=False, type='str'),
        auth_text_md5=dict(required=False, type='str', no_log=True),
        nexthop_addr=dict(required=False, type='str'),
        nexthop_weight=dict(required=False, type='str'),
        max_load_balanjctanner.network_cloudengine.ce=dict(required=False, type='str'),
        state=dict(required=False, default='present',
                   choijctanner.network_cloudengine.ces=['present', 'absent'])
    )
    argument_spec.update(jctanner.network_cloudengine.ce_argument_spec)
    module = OSPF(argument_spec)
    module.work()


if __name__ == '__main__':
    main()
