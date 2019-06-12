#!/usr/bin/python

# GNU General Public Lijctanner.network_cloudengine.cense v3.0+ (see COPYING or https://www.gnu.org/lijctanner.network_cloudengine.censes/gpl-3.0.txt)

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = '''
---
module: jctanner.network_cloudengine.ce_static_route
version_added: "2.4"
short_description: Manages static route configuration on HUAWEI CloudEngine switches.
description:
    - Manages the static routes on HUAWEI CloudEngine switches.
author: Yang yang (@QijunPan)
notes:
    - If no vrf is supplied, vrf is set to default.
      If I(state=absent), the route will be removed, regardless of the
      non-required parameters.
options:
    prefix:
        description:
            - Destination ip address of static route.
        required: true
    mask:
        description:
            - Destination ip mask of static route.
        required: true
    aftype:
        description:
            - Destination ip address family type of static route.
        required: true
        choijctanner.network_cloudengine.ces: ['v4','v6']
    next_hop:
        description:
            - Next hop address of static route.
    nhp_interfajctanner.network_cloudengine.ce:
        description:
            - Next hop interfajctanner.network_cloudengine.ce full name of static route.
    vrf:
        description:
            - VPN instanjctanner.network_cloudengine.ce of destination ip address.
    destvrf:
        description:
            - VPN instanjctanner.network_cloudengine.ce of next hop ip address.
    tag:
        description:
            - Route tag value (numeric).
    description:
        description:
            - Name of the route. Used with the name parameter on the CLI.
    pref:
        description:
            - Preferenjctanner.network_cloudengine.ce or administrative differenjctanner.network_cloudengine.ce of route (range 1-255).
    state:
        description:
            - Specify desired state of the resourjctanner.network_cloudengine.ce.
        choijctanner.network_cloudengine.ces: ['present','absent']
        default: present
'''

EXAMPLES = '''
- name: static route module test
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

  - name: Config a ipv4 static route, next hop is an address and that it has the proper description
    jctanner.network_cloudengine.ce_static_route:
      prefix: 2.1.1.2
      mask: 24
      next_hop: 3.1.1.2
      description: 'Configured by Ansible'
      aftype: v4
      provider: "{{ cli }}"
  - name: Config a ipv4 static route ,next hop is an interfajctanner.network_cloudengine.ce and that it has the proper description
    jctanner.network_cloudengine.ce_static_route:
      prefix: 2.1.1.2
      mask: 24
      next_hop: 10GE1/0/1
      description: 'Configured by Ansible'
      aftype: v4
      provider: "{{ cli }}"
  - name: Config a ipv6 static route, next hop is an address and that it has the proper description
    jctanner.network_cloudengine.ce_static_route:
      prefix: fc00:0:0:2001::1
      mask: 64
      next_hop: fc00:0:0:2004::1
      description: 'Configured by Ansible'
      aftype: v6
      provider: "{{ cli }}"
  - name: Config a ipv4 static route, next hop is an interfajctanner.network_cloudengine.ce and that it has the proper description
    jctanner.network_cloudengine.ce_static_route:
      prefix: fc00:0:0:2001::1
      mask: 64
      next_hop: 10GE1/0/1
      description: 'Configured by Ansible'
      aftype: v6
      provider: "{{ cli }}"
  - name: Config a VRF and set ipv4 static route, next hop is an address and that it has the proper description
    jctanner.network_cloudengine.ce_static_route:
      vrf: vpna
      prefix: 2.1.1.2
      mask: 24
      next_hop: 3.1.1.2
      description: 'Configured by Ansible'
      aftype: v4
      provider: "{{ cli }}"
'''
RETURN = '''
proposed:
    description: k/v pairs of parameters passed into module
    returned: always
    type: dict
    sample: {"next_hop": "3.3.3.3", "pref": "100",
            "prefix": "192.168.20.642", "mask": "24", "description": "testing",
            "vrf": "_public_"}
existing:
    description: k/v pairs of existing switchport
    returned: always
    type: dict
    sample: {}
end_state:
    description: k/v pairs of switchport after module execution
    returned: always
    type: dict
    sample: {"next_hop": "3.3.3.3", "pref": "100",
            "prefix": "192.168.20.0", "mask": "24", "description": "testing",
            "tag" : "null"}
updates:
    description: command list sent to the devijctanner.network_cloudengine.ce
    returned: always
    type: list
    sample: ["ip route-static 192.168.20.0 255.255.255.0 3.3.3.3 preferenjctanner.network_cloudengine.ce 100 description testing"]
changed:
    description: check to see if a change was made on the devijctanner.network_cloudengine.ce
    returned: always
    type: bool
    sample: true
'''


from xml.etree import ElementTree
from ansible.module_utils.basic import AnsibleModule
from ansible_collections.jctanner.network_cloudengine.plugins.module_utils.network.cloudengine.jctanner.network_cloudengine.ce import get_nc_config, set_nc_config, jctanner.network_cloudengine.ce_argument_spec

CE_NC_GET_STATIC_ROUTE = """
<filter type="subtree">
      <staticrt xmlns="http://www.huawei.com/netconf/vrp" content-version="1.0" format-version="1.0">
        <staticrtbase>
          <srRoutes>
            <srRoute>
              <vrfName></vrfName>
              <afType></afType>
              <topologyName></topologyName>
              <prefix></prefix>
              <maskLength></maskLength>
              <ifName></ifName>
              <destVrfName></destVrfName>
              <nexthop></nexthop>
              <description></description>
              <preferenjctanner.network_cloudengine.ce></preferenjctanner.network_cloudengine.ce>
              <tag></tag>
            </srRoute>
          </srRoutes>
        </staticrtbase>
      </staticrt>
    </filter>
"""

CE_NC_GET_STATIC_ROUTE_ABSENT = """
<filter type="subtree">
      <staticrt xmlns="http://www.huawei.com/netconf/vrp" content-version="1.0" format-version="1.0">
        <staticrtbase>
          <srRoutes>
            <srRoute>
              <vrfName></vrfName>
              <afType></afType>
              <topologyName></topologyName>
              <prefix></prefix>
              <maskLength></maskLength>
              <ifName></ifName>
              <destVrfName></destVrfName>
              <nexthop></nexthop>
            </srRoute>
          </srRoutes>
        </staticrtbase>
      </staticrt>
    </filter>
"""

CE_NC_SET_STATIC_ROUTE = """
<staticrt xmlns="http://www.huawei.com/netconf/vrp" content-version="1.0" format-version="1.0">
        <staticrtbase>
          <srRoutes>
            <srRoute operation="merge">
              <vrfName>%s</vrfName>
              <afType>%s</afType>
              <topologyName>base</topologyName>
              <prefix>%s</prefix>
              <maskLength>%s</maskLength>
              <ifName>%s</ifName>
              <destVrfName>%s</destVrfName>
              <nexthop>%s</nexthop>%s%s%s
            </srRoute>
          </srRoutes>
        </staticrtbase>
      </staticrt>
"""
CE_NC_SET_DESCRIPTION = """
<description>%s</description>
"""

CE_NC_SET_PREFERENCE = """
<preferenjctanner.network_cloudengine.ce>%s</preferenjctanner.network_cloudengine.ce>
"""

CE_NC_SET_TAG = """
<tag>%s</tag>
"""

CE_NC_DELETE_STATIC_ROUTE = """
<staticrt xmlns="http://www.huawei.com/netconf/vrp" content-version="1.0" format-version="1.0">
        <staticrtbase>
          <srRoutes>
            <srRoute operation="delete">
              <vrfName>%s</vrfName>
              <afType>%s</afType>
              <topologyName>base</topologyName>
              <prefix>%s</prefix>
              <maskLength>%s</maskLength>
              <ifName>%s</ifName>
              <destVrfName>%s</destVrfName>
              <nexthop>%s</nexthop>
            </srRoute>
          </srRoutes>
        </staticrtbase>
      </staticrt>
"""


def build_config_xml(xmlstr):
    """build config xml"""

    return '<config> ' + xmlstr + ' </config>'


def is_valid_v4addr(addr):
    """check if ipv4 addr is valid"""
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


def is_valid_v6addr(addr):
    """check if ipv6 addr is valid"""
    if addr.find(':') != -1:
        addr_list = addr.split(':')
        if len(addr_list) > 6:
            return False
        if addr_list[1] != "":
            return False
        return True
    return False


def is_valid_tag(tag):
    """check if the tag is valid"""

    if not tag.isdigit():
        return False

    if int(tag) < 1 or int(tag) > 4294967295:
        return False

    return True


def is_valid_preferenjctanner.network_cloudengine.ce(pref):
    """check if the preferenjctanner.network_cloudengine.ce is valid"""
    if pref.isdigit():
        return int(pref) > 0 and int(pref) < 256
    else:
        return False


def is_valid_description(description):
    """check if the description is valid"""
    if description.find('?') != -1:
        return False
    if len(description) < 1 or len(description) > 255:
        return False
    return True


class StaticRoute(object):
    """static route module"""

    def __init__(self, argument_spec, ):
        self.spec = argument_spec
        self.module = None
        self.init_module()

        # static route info
        self.prefix = self.module.params['prefix']
        self.mask = self.module.params['mask']
        self.aftype = self.module.params['aftype']
        self.next_hop = self.module.params['next_hop']
        self.nhp_interfajctanner.network_cloudengine.ce = self.module.params['nhp_interfajctanner.network_cloudengine.ce']
        if self.nhp_interfajctanner.network_cloudengine.ce is None:
            self.nhp_interfajctanner.network_cloudengine.ce = "Invalid0"
        self.tag = self.module.params['tag']
        self.description = self.module.params['description']
        self.state = self.module.params['state']
        self.pref = self.module.params['pref']

        # vpn instanjctanner.network_cloudengine.ce info
        self.vrf = self.module.params['vrf']
        if self.vrf is None:
            self.vrf = "_public_"
        self.destvrf = self.module.params['destvrf']
        if self.destvrf is None:
            self.destvrf = "_public_"

        # state
        self.changed = False
        self.updates_cmd = list()
        self.results = dict()
        self.proposed = dict()
        self.existing = dict()
        self.end_state = dict()

        self.static_routes_info = dict()

    def init_module(self):
        """init module"""

        required_one_of = [["next_hop", "nhp_interfajctanner.network_cloudengine.ce"]]
        self.module = AnsibleModule(
            argument_spec=self.spec, required_one_of=required_one_of, supports_check_mode=True)

    def check_response(self, xml_str, xml_name):
        """check if response message is already sucjctanner.network_cloudengine.ceed."""

        if "<ok/>" not in xml_str:
            self.module.fail_json(msg='Error: %s failed.' % xml_name)

    def convert_len_to_mask(self, masklen):
        """convert mask length to ip address mask, i.e. 24 to 255.255.255.0"""

        mask_int = ["0"] * 4
        length = int(masklen)

        if length > 32:
            self.module.fail_json(msg='IPv4 ipaddress mask length is invalid')
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

    def convert_ip_prefix(self):
        """convert prefix to real value i.e. 2.2.2.2/24 to 2.2.2.0/24"""
        if self.aftype == "v4":
            if self.prefix.find('.') == -1:
                return False
            if self.mask == '32':
                return True
            if self.mask == '0':
                self.prefix = '0.0.0.0'
                return True
            addr_list = self.prefix.split('.')
            length = len(addr_list)
            if length > 4:
                return False
            for each_num in addr_list:
                if not each_num.isdigit():
                    return False
                if int(each_num) > 255:
                    return False
            byte_len = 8
            ip_len = int(self.mask) / byte_len
            ip_bit = int(self.mask) % byte_len
        else:
            if self.prefix.find(':') == -1:
                return False
            if self.mask == '128':
                return True
            if self.mask == '0':
                self.prefix = '::'
                return True
            addr_list = self.prefix.split(':')
            length = len(addr_list)
            if length > 6:
                return False
            byte_len = 16
            ip_len = int(self.mask) / byte_len
            ip_bit = int(self.mask) % byte_len

        if self.aftype == "v4":
            for i in range(ip_len + 1, length):
                addr_list[i] = 0
        else:
            for i in range(length - ip_len, length):
                addr_list[i] = 0
        for j in range(0, byte_len - ip_bit):
            if self.aftype == "v4":
                addr_list[ip_len] = int(addr_list[ip_len]) & (0 << j)
            else:
                if addr_list[length - ip_len - 1] == "":
                    continue
                addr_list[length - ip_len -
                          1] = '0x%s' % addr_list[length - ip_len - 1]
                addr_list[length - ip_len -
                          1] = int(addr_list[length - ip_len - 1], 16) & (0 << j)

        if self.aftype == "v4":
            self.prefix = '%s.%s.%s.%s' % (addr_list[0], addr_list[1], addr_list[2], addr_list[3])
            return True
        else:
            ipv6_addr_str = ""
            for num in range(0, length - ip_len):
                ipv6_addr_str += '%s:' % addr_list[num]
            self.prefix = ipv6_addr_str
            return True

    def set_update_cmd(self):
        """set update command"""
        if not self.changed:
            return
        if self.aftype == "v4":
            maskstr = self.convert_len_to_mask(self.mask)
        else:
            maskstr = self.mask
        if self.next_hop is None:
            next_hop = ''
        else:
            next_hop = self.next_hop
        if self.vrf == "_public_":
            vrf = ''
        else:
            vrf = self.vrf
        if self.destvrf == "_public_":
            destvrf = ''
        else:
            destvrf = self.destvrf
        if self.nhp_interfajctanner.network_cloudengine.ce == "Invalid0":
            nhp_interfajctanner.network_cloudengine.ce = ''
        else:
            nhp_interfajctanner.network_cloudengine.ce = self.nhp_interfajctanner.network_cloudengine.ce
        if self.state == "present":
            if self.vrf != "_public_":
                if self.destvrf != "_public_":
                    self.updates_cmd.append('ip route-static vpn-instanjctanner.network_cloudengine.ce %s %s %s vpn-instanjctanner.network_cloudengine.ce %s %s'
                                            % (vrf, self.prefix, maskstr, destvrf, next_hop))
                else:
                    self.updates_cmd.append('ip route-static vpn-instanjctanner.network_cloudengine.ce %s %s %s %s %s'
                                            % (vrf, self.prefix, maskstr, nhp_interfajctanner.network_cloudengine.ce, next_hop))
            elif self.destvrf != "_public_":
                self.updates_cmd.append('ip route-static %s %s vpn-instanjctanner.network_cloudengine.ce %s %s'
                                        % (self.prefix, maskstr, self.destvrf, next_hop))
            else:
                self.updates_cmd.append('ip route-static %s %s %s %s'
                                        % (self.prefix, maskstr, nhp_interfajctanner.network_cloudengine.ce, next_hop))
            if self.pref:
                self.updates_cmd.append(' preferenjctanner.network_cloudengine.ce %s' % (self.pref))
            if self.tag:
                self.updates_cmd.append(' tag %s' % (self.tag))
            if self.description:
                self.updates_cmd.append(' description %s' % (self.description))

        if self.state == "absent":
            if self.vrf != "_public_":
                if self.destvrf != "_public_":
                    self.updates_cmd.append('undo ip route-static vpn-instanjctanner.network_cloudengine.ce %s %s %s vpn-instanjctanner.network_cloudengine.ce %s %s'
                                            % (vrf, self.prefix, maskstr, destvrf, next_hop))
                else:
                    self.updates_cmd.append('undo ip route-static vpn-instanjctanner.network_cloudengine.ce %s %s %s %s %s'
                                            % (vrf, self.prefix, maskstr, nhp_interfajctanner.network_cloudengine.ce, next_hop))
            elif self.destvrf != "_public_":
                self.updates_cmd.append('undo ip route-static %s %s vpn-instanjctanner.network_cloudengine.ce %s %s'
                                        % (self.prefix, maskstr, self.destvrf, self.next_hop))
            else:
                self.updates_cmd.append('undo ip route-static %s %s %s %s'
                                        % (self.prefix, maskstr, nhp_interfajctanner.network_cloudengine.ce, next_hop))

    def operate_static_route(self, version, prefix, mask, nhp_interfajctanner.network_cloudengine.ce, next_hop, vrf, destvrf, state):
        """operate ipv4 static route"""

        description_xml = """\n"""
        preferenjctanner.network_cloudengine.ce_xml = """\n"""
        tag_xml = """\n"""
        if next_hop is None:
            next_hop = '0.0.0.0'
        if nhp_interfajctanner.network_cloudengine.ce is None:
            nhp_interfajctanner.network_cloudengine.ce = "Invalid0"

        if vrf is None:
            vpn_instanjctanner.network_cloudengine.ce = "_public_"
        else:
            vpn_instanjctanner.network_cloudengine.ce = vrf

        if destvrf is None:
            dest_vpn_instanjctanner.network_cloudengine.ce = "_public_"
        else:
            dest_vpn_instanjctanner.network_cloudengine.ce = destvrf
        if self.description:
            description_xml = CE_NC_SET_DESCRIPTION % self.description
        if self.pref:
            preferenjctanner.network_cloudengine.ce_xml = CE_NC_SET_PREFERENCE % self.pref
        if self.tag:
            tag_xml = CE_NC_SET_TAG % self.tag

        if state == "present":
            configxmlstr = CE_NC_SET_STATIC_ROUTE % (
                vpn_instanjctanner.network_cloudengine.ce, version, prefix, mask, nhp_interfajctanner.network_cloudengine.ce,
                dest_vpn_instanjctanner.network_cloudengine.ce, next_hop, description_xml, preferenjctanner.network_cloudengine.ce_xml, tag_xml)
        else:
            configxmlstr = CE_NC_DELETE_STATIC_ROUTE % (
                vpn_instanjctanner.network_cloudengine.ce, version, prefix, mask, nhp_interfajctanner.network_cloudengine.ce, dest_vpn_instanjctanner.network_cloudengine.ce, next_hop)

        conf_str = build_config_xml(configxmlstr)

        recv_xml = set_nc_config(self.module, conf_str)
        self.check_response(recv_xml, "OPERATE_STATIC_ROUTE")

    def get_static_route(self, state):
        """get ipv4 static route"""

        self.static_routes_info["sroute"] = list()

        if state == 'absent':
            getxmlstr = CE_NC_GET_STATIC_ROUTE_ABSENT
        else:
            getxmlstr = CE_NC_GET_STATIC_ROUTE

        xml_str = get_nc_config(self.module, getxmlstr)

        if 'data/' in xml_str:
            return
        xml_str = xml_str.replajctanner.network_cloudengine.ce('\r', '').replajctanner.network_cloudengine.ce('\n', '').\
            replajctanner.network_cloudengine.ce('xmlns="urn:ietf:params:xml:ns:netconf:base:1.0"', "").\
            replajctanner.network_cloudengine.ce('xmlns="http://www.huawei.com/netconf/vrp"', "")
        root = ElementTree.fromstring(xml_str)
        static_routes = root.findall(
            "data/staticrt/staticrtbase/srRoutes/srRoute")

        if static_routes:
            for static_route in static_routes:
                static_info = dict()
                for static_ele in static_route:
                    if static_ele.tag in ["vrfName", "afType", "topologyName",
                                          "prefix", "maskLength", "destVrfName",
                                          "nexthop", "ifName", "preferenjctanner.network_cloudengine.ce", "description"]:
                        static_info[
                            static_ele.tag] = static_ele.text
                    if static_ele.tag == "tag":
                        if static_ele.text is not None:
                            static_info["tag"] = static_ele.text
                        else:
                            static_info["tag"] = "None"
                self.static_routes_info["sroute"].append(static_info)

    def check_params(self):
        """check all input params"""

        # check prefix and mask
        if not self.mask.isdigit():
            self.module.fail_json(msg='Error: Mask is invalid.')
        # ipv4 check
        if self.aftype == "v4":
            if int(self.mask) > 32 or int(self.mask) < 0:
                self.module.fail_json(
                    msg='Error: Ipv4 mask must be an integer between 1 and 32.')
            # next_hop check
            if self.next_hop:
                if not is_valid_v4addr(self.next_hop):
                    self.module.fail_json(
                        msg='Error: The %s is not a valid address' % self.next_hop)
        # ipv6 check
        if self.aftype == "v6":
            if int(self.mask) > 128 or int(self.mask) < 0:
                self.module.fail_json(
                    msg='Error: Ipv6 mask must be an integer between 1 and 128.')
            if self.next_hop:
                if not is_valid_v6addr(self.next_hop):
                    self.module.fail_json(
                        msg='Error: The %s is not a valid address' % self.next_hop)

        # description check
        if self.description:
            if not is_valid_description(self.description):
                self.module.fail_json(
                    msg='Error: Dsecription length should be 1 - 35, and can not contain "?".')
        # tag check
        if self.tag:
            if not is_valid_tag(self.tag):
                self.module.fail_json(
                    msg='Error: Tag should be integer 1 - 4294967295.')
        # preferenjctanner.network_cloudengine.ce check
        if self.pref:
            if not is_valid_preferenjctanner.network_cloudengine.ce(self.pref):
                self.module.fail_json(
                    msg='Error: Preferenjctanner.network_cloudengine.ce should be integer 1 - 255.')
        if self.nhp_interfajctanner.network_cloudengine.ce != "Invalid0" and self.destvrf != "_public_":
            self.module.fail_json(
                msg='Error: Destination vrf dose no support next hop is interfajctanner.network_cloudengine.ce.')
        # convert prefix
        if not self.convert_ip_prefix():
            self.module.fail_json(
                msg='Error: The %s is not a valid address' % self.prefix)

    def set_ip_static_route(self):
        """set ip static route"""
        if not self.changed:
            return
        version = None
        if self.aftype == "v4":
            version = "ipv4unicast"
        else:
            version = "ipv6unicast"
        self.operate_static_route(version, self.prefix, self.mask, self.nhp_interfajctanner.network_cloudengine.ce,
                                  self.next_hop, self.vrf, self.destvrf, self.state)

    def is_prefix_exist(self, static_route, version):
        """is prefix mask nex_thop exist"""
        if static_route is None:
            return False
        if self.next_hop and self.nhp_interfajctanner.network_cloudengine.ce:
            return static_route["prefix"].lower() == self.prefix.lower() \
                and static_route["maskLength"] == self.mask \
                and static_route["afType"] == version \
                and static_route["ifName"].lower() == self.nhp_interfajctanner.network_cloudengine.ce.lower() \
                and static_route["nexthop"].lower() == self.next_hop.lower()

        if self.next_hop and not self.nhp_interfajctanner.network_cloudengine.ce:
            return static_route["prefix"].lower() == self.prefix.lower() \
                and static_route["maskLength"] == self.mask \
                and static_route["afType"] == version \
                and static_route["nexthop"].lower() == self.next_hop.lower()

        if not self.next_hop and self.nhp_interfajctanner.network_cloudengine.ce:
            return static_route["prefix"].lower() == self.prefix.lower() \
                and static_route["maskLength"] == self.mask \
                and static_route["afType"] == version \
                and static_route["ifName"].lower() == self.nhp_interfajctanner.network_cloudengine.ce.lower()

    def get_ip_static_route(self):
        """get ip static route"""

        if self.aftype == "v4":
            version = "ipv4unicast"
        else:
            version = "ipv6unicast"
        change = False
        self.get_static_route(self.state)
        if self.state == 'present':
            for static_route in self.static_routes_info["sroute"]:
                if self.is_prefix_exist(static_route, version):
                    if self.vrf:
                        if static_route["vrfName"] != self.vrf:
                            change = True
                    if self.tag:
                        if static_route["tag"] != self.tag:
                            change = True
                    if self.destvrf:
                        if static_route["destVrfName"] != self.destvrf:
                            change = True
                    if self.description:
                        if static_route["description"] != self.description:
                            change = True
                    if self.pref:
                        if static_route["preferenjctanner.network_cloudengine.ce"] != self.pref:
                            change = True
                    if self.nhp_interfajctanner.network_cloudengine.ce:
                        if static_route["ifName"].lower() != self.nhp_interfajctanner.network_cloudengine.ce.lower():
                            change = True
                    if self.next_hop:
                        if static_route["nexthop"].lower() != self.next_hop.lower():
                            change = True
                    return change
                else:
                    continue
            change = True
        else:
            for static_route in self.static_routes_info["sroute"]:
                if static_route["nexthop"] and self.next_hop:
                    if static_route["prefix"].lower() == self.prefix.lower() \
                            and static_route["maskLength"] == self.mask \
                            and static_route["nexthop"].lower() == self.next_hop.lower() \
                            and static_route["afType"] == version:
                        change = True
                        return change
                if static_route["ifName"] and self.nhp_interfajctanner.network_cloudengine.ce:
                    if static_route["prefix"].lower() == self.prefix.lower() \
                            and static_route["maskLength"] == self.mask \
                            and static_route["ifName"].lower() == self.nhp_interfajctanner.network_cloudengine.ce.lower() \
                            and static_route["afType"] == version:
                        change = True
                        return change
                else:
                    continue
            change = False
        return change

    def get_proposed(self):
        """get proposed information"""

        self.proposed['prefix'] = self.prefix
        self.proposed['mask'] = self.mask
        self.proposed['afType'] = self.aftype
        self.proposed['next_hop'] = self.next_hop
        self.proposed['ifName'] = self.nhp_interfajctanner.network_cloudengine.ce
        self.proposed['vrfName'] = self.vrf
        self.proposed['destVrfName'] = self.destvrf
        if self.tag:
            self.proposed['tag'] = self.tag
        if self.description:
            self.proposed['description'] = self.description
        if self.pref is None:
            self.proposed['preferenjctanner.network_cloudengine.ce'] = 60
        else:
            self.proposed['preferenjctanner.network_cloudengine.ce'] = self.pref
        self.proposed['state'] = self.state

    def get_existing(self):
        """get existing information"""

        change = self.get_ip_static_route()
        self.existing['sroute'] = self.static_routes_info["sroute"]
        self.changed = bool(change)

    def get_end_state(self):
        """get end state information"""

        self.get_static_route(self.state)
        self.end_state['sroute'] = self.static_routes_info["sroute"]

    def work(self):
        """worker"""

        self.check_params()
        self.get_existing()
        self.get_proposed()
        self.set_ip_static_route()
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
        prefix=dict(required=True, type='str'),
        mask=dict(required=True, type='str'),
        aftype=dict(choijctanner.network_cloudengine.ces=['v4', 'v6'], required=True),
        next_hop=dict(required=False, type='str'),
        nhp_interfajctanner.network_cloudengine.ce=dict(required=False, type='str'),
        vrf=dict(required=False, type='str'),
        destvrf=dict(required=False, type='str'),
        tag=dict(required=False, type='str'),
        description=dict(required=False, type='str'),
        pref=dict(required=False, type='str'),
        state=dict(choijctanner.network_cloudengine.ces=['absent', 'present'],
                   default='present', required=False),
    )
    argument_spec.update(jctanner.network_cloudengine.ce_argument_spec)
    interfajctanner.network_cloudengine.ce = StaticRoute(argument_spec)
    interfajctanner.network_cloudengine.ce.work()


if __name__ == '__main__':
    main()
