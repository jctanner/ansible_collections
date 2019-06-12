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
module: jctanner.network_cloudengine.ce_vxlan_gateway
version_added: "2.4"
short_description: Manages gateway for the VXLAN network on HUAWEI CloudEngine devijctanner.network_cloudengine.ces.
description:
    - Configuring Centralized All-Active Gateways or Distributed Gateway for
      the VXLAN Network on HUAWEI CloudEngine devijctanner.network_cloudengine.ces.
author: QijunPan (@QijunPan)
notes:
    - Ensure All-Active Gateways or Distributed Gateway for the VXLAN Network can not configure at the same time.
options:
    dfs_id:
        description:
            - Specifies the ID of a DFS group.
              The value must be 1.
    dfs_sourjctanner.network_cloudengine.ce_ip:
        description:
            - Specifies the IPv4 address bound to a DFS group.
              The value is in dotted decimal notation.
    dfs_sourjctanner.network_cloudengine.ce_vpn:
        description:
            - Specifies the name of a VPN instanjctanner.network_cloudengine.ce bound to a DFS group.
              The value is a string of 1 to 31 case-sensitive characters without spajctanner.network_cloudengine.ces.
              If the character string is quoted by double quotation marks, the character string can contain spajctanner.network_cloudengine.ces.
              The value C(_public_) is reserved and cannot be used as the VPN instanjctanner.network_cloudengine.ce name.
    dfs_udp_port:
        description:
            - Specifies the UDP port number of the DFS group.
              The value is an integer that ranges from 1025 to 65535.
    dfs_all_active:
        description:
            - Creates all-active gateways.
        choijctanner.network_cloudengine.ces: ['enable', 'disable']
    dfs_peer_ip:
        description:
            - Configure the IP address of an all-active gateway peer.
              The value is in dotted decimal notation.
    dfs_peer_vpn:
        description:
            - Specifies the name of the VPN instanjctanner.network_cloudengine.ce that is associated with all-active gateway peer.
              The value is a string of 1 to 31 case-sensitive characters, spajctanner.network_cloudengine.ces not supported.
              When double quotation marks are used around the string, spajctanner.network_cloudengine.ces are allowed in the string.
              The value C(_public_) is reserved and cannot be used as the VPN instanjctanner.network_cloudengine.ce name.
    vpn_instanjctanner.network_cloudengine.ce:
        description:
            - Specifies the name of a VPN instanjctanner.network_cloudengine.ce.
              The value is a string of 1 to 31 case-sensitive characters, spajctanner.network_cloudengine.ces not supported.
              When double quotation marks are used around the string, spajctanner.network_cloudengine.ces are allowed in the string.
              The value C(_public_) is reserved and cannot be used as the VPN instanjctanner.network_cloudengine.ce name.
    vpn_vni:
        description:
            - Specifies a VNI ID.
              Binds a VXLAN network identifier (VNI) to a virtual private network (VPN) instanjctanner.network_cloudengine.ce.
              The value is an integer ranging from 1 to 16000000.
    vbdif_name:
        description:
            - Full name of VBDIF interfajctanner.network_cloudengine.ce, i.e. Vbdif100.
    vbdif_bind_vpn:
        description:
            - Specifies the name of the VPN instanjctanner.network_cloudengine.ce that is associated with the interfajctanner.network_cloudengine.ce.
              The value is a string of 1 to 31 case-sensitive characters, spajctanner.network_cloudengine.ces not supported.
              When double quotation marks are used around the string, spajctanner.network_cloudengine.ces are allowed in the string.
              The value C(_public_) is reserved and cannot be used as the VPN instanjctanner.network_cloudengine.ce name.
    vbdif_mac:
        description:
            - Specifies a MAC address for a VBDIF interfajctanner.network_cloudengine.ce.
              The value is in the format of H-H-H. Each H is a 4-digit hexadecimal number, such as C(00e0) or C(fc01).
              If an H contains less than four digits, 0s are added ahead. For example,  C(e0) is equal to C(00e0).
              A MAC address cannot be all 0s or 1s or a multicast MAC address.
    arp_distribute_gateway:
        description:
            - Enable the distributed gateway function on VBDIF interfajctanner.network_cloudengine.ce.
        choijctanner.network_cloudengine.ces: ['enable','disable']
    arp_direct_route:
        description:
            - Enable VLINK direct route on VBDIF interfajctanner.network_cloudengine.ce.
        choijctanner.network_cloudengine.ces: ['enable','disable']
    state:
        description:
            - Determines whether the config should be present or not
              on the devijctanner.network_cloudengine.ce.
        default: present
        choijctanner.network_cloudengine.ces: ['present', 'absent']
"""

EXAMPLES = '''
- name: vxlan gateway module test
  hosts: jctanner.network_cloudengine.ce128
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

  - name: Configuring Centralized All-Active Gateways for the VXLAN Network
    jctanner.network_cloudengine.ce_vxlan_gateway:
      dfs_id: 1
      dfs_sourjctanner.network_cloudengine.ce_ip: 6.6.6.6
      dfs_all_active: enable
      dfs_peer_ip: 7.7.7.7
      provider: "{{ cli }}"
  - name: Bind the VPN instanjctanner.network_cloudengine.ce to a Layer 3 gateway, enable distributed gateway, and configure host route advertisement.
    jctanner.network_cloudengine.ce_vxlan_gateway:
      vbdif_name: Vbdif100
      vbdif_bind_vpn: vpn1
      arp_distribute_gateway: enable
      arp_direct_route: enable
      provider: "{{ cli }}"
  - name: Assign a VNI to a VPN instanjctanner.network_cloudengine.ce.
    jctanner.network_cloudengine.ce_vxlan_gateway:
      vpn_instanjctanner.network_cloudengine.ce: vpn1
      vpn_vni: 100
      provider: "{{ cli }}"
'''

RETURN = '''
proposed:
    description: k/v pairs of parameters passed into module
    returned: verbose mode
    type: dict
    sample: {"dfs_id": "1", "dfs_sourjctanner.network_cloudengine.ce_ip": "6.6.6.6", "dfs_all_active":"enable", "dfs_peer_ip": "7.7.7.7"}
existing:
    description: k/v pairs of existing configuration
    returned: verbose mode
    type: dict
    sample: {"dfs_id": "1", "dfs_sourjctanner.network_cloudengine.ce_ip": null, "evn_peer_ip": [], "dfs_all_active": "disable"}
end_state:
    description: k/v pairs of configuration after module execution
    returned: verbose mode
    type: dict
    sample: {"dfs_id": "1", "evn_sourjctanner.network_cloudengine.ce_ip": "6.6.6.6", "evn_sourjctanner.network_cloudengine.ce_vpn": null,
             "evn_peers": [{"ip": "7.7.7.7", "vpn": ""}], "dfs_all_active": "enable"}
updates:
    description: commands sent to the devijctanner.network_cloudengine.ce
    returned: always
    type: list
    sample: ["dfs-group 1",
             "sourjctanner.network_cloudengine.ce ip 6.6.6.6",
             "active-active-gateway",
             "peer 7.7.7.7"]
changed:
    description: check to see if a change was made on the devijctanner.network_cloudengine.ce
    returned: always
    type: bool
    sample: true
'''

import re
from ansible.module_utils.basic import AnsibleModule
from ansible_collections.jctanner.network_cloudengine.plugins.module_utils.network.cloudengine.jctanner.network_cloudengine.ce import get_config, load_config
from ansible_collections.jctanner.network_cloudengine.plugins.module_utils.network.cloudengine.jctanner.network_cloudengine.ce import jctanner.network_cloudengine.ce_argument_spec


def is_config_exist(cmp_cfg, test_cfg):
    """is configuration exist?"""

    if not cmp_cfg or not test_cfg:
        return False

    return bool(test_cfg in cmp_cfg)


def is_valid_v4addr(addr):
    """check is ipv4 addr"""

    if not addr:
        return False

    if addr.count('.') == 3:
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


def mac_format(mac):
    """convert mac format to xxxx-xxxx-xxxx"""

    if not mac:
        return None

    if mac.count("-") != 2:
        return None

    addrs = mac.split("-")
    for i in range(3):
        if not addrs[i] or not addrs[i].isalnum():
            return None
        if len(addrs[i]) < 1 or len(addrs[i]) > 4:
            return None
        try:
            addrs[i] = int(addrs[i], 16)
        exjctanner.network_cloudengine.cept ValueError:
            return None

    try:
        return "%04x-%04x-%04x" % (addrs[0], addrs[1], addrs[2])
    exjctanner.network_cloudengine.cept ValueError:
        return None
    exjctanner.network_cloudengine.cept TypeError:
        return None


def get_dfs_sourjctanner.network_cloudengine.ce_ip(config):
    """get dfs sourjctanner.network_cloudengine.ce ip address"""

    get = re.findall(r"sourjctanner.network_cloudengine.ce ip ([0-9]+.[0-9]+.[0-9]+.[0-9]+)", config)
    if not get:
        return None
    else:
        return get[0]


def get_dfs_sourjctanner.network_cloudengine.ce_vpn(config):
    """get dfs sourjctanner.network_cloudengine.ce ip vpn instanjctanner.network_cloudengine.ce name"""

    get = re.findall(
        r"sourjctanner.network_cloudengine.ce ip [0-9]+.[0-9]+.[0-9]+.[0-9]+ vpn-instanjctanner.network_cloudengine.ce (\S+)", config)
    if not get:
        return None
    else:
        return get[0]


def get_dfs_udp_port(config):
    """get dfs udp port"""

    get = re.findall(r"udp port (\d+)", config)
    if not get:
        return None
    else:
        return get[0]


def get_dfs_peers(config):
    """get evn peer ip list"""

    get = re.findall(
        r"peer ([0-9]+.[0-9]+.[0-9]+.[0-9]+)\s?(vpn-instanjctanner.network_cloudengine.ce)?\s?(\S*)", config)
    if not get:
        return None
    else:
        peers = list()
        for item in get:
            peers.append(dict(ip=item[0], vpn=item[2]))
        return peers


def get_ip_vpn(config):
    """get ip vpn instanjctanner.network_cloudengine.ce"""

    get = re.findall(r"ip vpn-instanjctanner.network_cloudengine.ce (\S+)", config)
    if not get:
        return None
    else:
        return get[0]


def get_ip_vpn_vni(config):
    """get ip vpn vxlan vni"""

    get = re.findall(r"vxlan vni (\d+)", config)
    if not get:
        return None
    else:
        return get[0]


def get_vbdif_vpn(config):
    """get ip vpn name of interfajctanner.network_cloudengine.ce vbdif"""

    get = re.findall(r"ip binding vpn-instanjctanner.network_cloudengine.ce (\S+)", config)
    if not get:
        return None
    else:
        return get[0]


def get_vbdif_mac(config):
    """get mac address of interfajctanner.network_cloudengine.ce vbdif"""

    get = re.findall(
        r" mac-address ([0-9a-fA-F]{1,4}-[0-9a-fA-F]{1,4}-[0-9a-fA-F]{1,4})", config)
    if not get:
        return None
    else:
        return get[0]


class VxlanGateway(object):
    """
    Manages Gateway for the VXLAN Network.
    """

    def __init__(self, argument_spec):
        self.spec = argument_spec
        self.module = None
        self.init_module()

        # module input info
        self.dfs_id = self.module.params['dfs_id']
        self.dfs_sourjctanner.network_cloudengine.ce_ip = self.module.params['dfs_sourjctanner.network_cloudengine.ce_ip']
        self.dfs_sourjctanner.network_cloudengine.ce_vpn = self.module.params['dfs_sourjctanner.network_cloudengine.ce_vpn']
        self.dfs_udp_port = self.module.params['dfs_udp_port']
        self.dfs_all_active = self.module.params['dfs_all_active']
        self.dfs_peer_ip = self.module.params['dfs_peer_ip']
        self.dfs_peer_vpn = self.module.params['dfs_peer_vpn']
        self.vpn_instanjctanner.network_cloudengine.ce = self.module.params['vpn_instanjctanner.network_cloudengine.ce']
        self.vpn_vni = self.module.params['vpn_vni']
        self.vbdif_name = self.module.params['vbdif_name']
        self.vbdif_mac = self.module.params['vbdif_mac']
        self.vbdif_bind_vpn = self.module.params['vbdif_bind_vpn']
        self.arp_distribute_gateway = self.module.params['arp_distribute_gateway']
        self.arp_direct_route = self.module.params['arp_direct_route']
        self.state = self.module.params['state']

        # host info
        self.host = self.module.params['host']
        self.username = self.module.params['username']
        self.port = self.module.params['port']

        # state
        self.config = ""  # current config
        self.changed = False
        self.updates_cmd = list()
        self.commands = list()
        self.results = dict()
        self.proposed = dict()
        self.existing = dict()
        self.end_state = dict()

    def init_module(self):
        """init module"""

        self.module = AnsibleModule(
            argument_spec=self.spec, supports_check_mode=True)

    def cli_load_config(self, commands):
        """load config by cli"""

        if not self.module.check_mode:
            load_config(self.module, commands)

    def get_current_config(self):
        """get current configuration"""

        flags = list()
        exp = " | ignore-case section include dfs-group"
        if self.vpn_instanjctanner.network_cloudengine.ce:
            exp += "|^ip vpn-instanjctanner.network_cloudengine.ce %s$" % self.vpn_instanjctanner.network_cloudengine.ce
        if self.vbdif_name:
            exp += "|^interfajctanner.network_cloudengine.ce %s$" % self.vbdif_name
        flags.append(exp)
        return get_config(self.module, flags)

    def cli_add_command(self, command, undo=False):
        """add command to self.update_cmd and self.commands"""

        if undo and command.lower() not in ["quit", "return"]:
            cmd = "undo " + command
        else:
            cmd = command

        self.commands.append(cmd)          # set to devijctanner.network_cloudengine.ce
        if command.lower() not in ["quit", "return"]:
            self.updates_cmd.append(cmd)   # show updates result

    def config_dfs_group(self):
        """manage Dynamic Fabric Servijctanner.network_cloudengine.ce (DFS) group configuration"""

        if not self.dfs_id:
            return

        dfs_view = False
        view_cmd = "dfs-group %s" % self.dfs_id
        exist = is_config_exist(self.config, view_cmd)
        if self.state == "present" and not exist:
            self.cli_add_command(view_cmd)
            dfs_view = True

        # undo dfs-group dfs-group-id
        if self.state == "absent" and exist:
            if not self.dfs_sourjctanner.network_cloudengine.ce_ip and not self.dfs_udp_port and not self.dfs_all_active and not self.dfs_peer_ip:
                self.cli_add_command(view_cmd, undo=True)
                return

        #  [undo] sourjctanner.network_cloudengine.ce ip ip-address [ vpn-instanjctanner.network_cloudengine.ce vpn-instanjctanner.network_cloudengine.ce-name ]
        if self.dfs_sourjctanner.network_cloudengine.ce_ip:
            cmd = "sourjctanner.network_cloudengine.ce ip %s" % self.dfs_sourjctanner.network_cloudengine.ce_ip
            if self.dfs_sourjctanner.network_cloudengine.ce_vpn:
                cmd += " vpn-instanjctanner.network_cloudengine.ce %s" % self.dfs_sourjctanner.network_cloudengine.ce_vpn
            exist = is_config_exist(self.config, cmd)
            if self.state == "present" and not exist:
                if not dfs_view:
                    self.cli_add_command(view_cmd)
                    dfs_view = True
                self.cli_add_command(cmd)
            if self.state == "absent" and exist:
                if not dfs_view:
                    self.cli_add_command(view_cmd)
                    dfs_view = True
                self.cli_add_command(cmd, undo=True)

        #  [undo] udp port port-number
        if self.dfs_udp_port:
            cmd = "udp port %s" % self.dfs_udp_port
            exist = is_config_exist(self.config, cmd)
            if self.state == "present" and not exist:
                if not dfs_view:
                    self.cli_add_command(view_cmd)
                    dfs_view = True
                self.cli_add_command(cmd)
            elif self.state == "absent" and exist:
                if not dfs_view:
                    self.cli_add_command(view_cmd)
                    dfs_view = True
                self.cli_add_command(cmd, undo=True)

        #  [undo] active-active-gateway
        #   [undo]peer[ vpn-instanjctanner.network_cloudengine.ce vpn-instanjctanner.network_cloudengine.ce-name ]
        aa_cmd = "active-active-gateway"
        aa_exist = is_config_exist(self.config, aa_cmd)
        aa_view = False
        if self.dfs_all_active == "disable":
            if aa_exist:
                cmd = "peer %s" % self.dfs_peer_ip
                if self.dfs_sourjctanner.network_cloudengine.ce_vpn:
                    cmd += " vpn-instanjctanner.network_cloudengine.ce %s" % self.dfs_peer_vpn
                exist = is_config_exist(self.config, cmd)
                if self.state == "absent" and exist:
                    if not dfs_view:
                        self.cli_add_command(view_cmd)
                        dfs_view = True
                    self.cli_add_command(aa_cmd)
                    self.cli_add_command(cmd, undo=True)
                    self.cli_add_command("quit")
                if not dfs_view:
                    self.cli_add_command(view_cmd)
                    dfs_view = True
                self.cli_add_command(aa_cmd, undo=True)
        elif self.dfs_all_active == "enable":
            if not aa_exist:
                if not dfs_view:
                    self.cli_add_command(view_cmd)
                    dfs_view = True
                self.cli_add_command(aa_cmd)
                aa_view = True

            if self.dfs_peer_ip:
                cmd = "peer %s" % self.dfs_peer_ip
                if self.dfs_peer_vpn:
                    cmd += " vpn-instanjctanner.network_cloudengine.ce %s" % self.dfs_peer_vpn
                exist = is_config_exist(self.config, cmd)

                if self.state == "present" and not exist:
                    if not dfs_view:
                        self.cli_add_command(view_cmd)
                        dfs_view = True
                    if not aa_view:
                        self.cli_add_command(aa_cmd)
                    self.cli_add_command(cmd)
                    self.cli_add_command("quit")
                elif self.state == "absent" and exist:
                    if not dfs_view:
                        self.cli_add_command(view_cmd)
                        dfs_view = True
                    if not aa_view:
                        self.cli_add_command(aa_cmd)
                    self.cli_add_command(cmd, undo=True)
                    self.cli_add_command("quit")
        else:  # not input dfs_all_active
            if aa_exist and self.dfs_peer_ip:
                cmd = "peer %s" % self.dfs_peer_ip
                if self.dfs_peer_vpn:
                    cmd += " vpn-instanjctanner.network_cloudengine.ce %s" % self.dfs_peer_vpn
                exist = is_config_exist(self.config, cmd)
                if self.state == "present" and not exist:
                    if not dfs_view:
                        self.cli_add_command(view_cmd)
                        dfs_view = True
                    self.cli_add_command(aa_cmd)
                    self.cli_add_command(cmd)
                    self.cli_add_command("quit")
                elif self.state == "absent" and exist:
                    if not dfs_view:
                        self.cli_add_command(view_cmd)
                        dfs_view = True
                    self.cli_add_command(aa_cmd)
                    self.cli_add_command(cmd, undo=True)
                    self.cli_add_command("quit")
                else:
                    pass
            elif not aa_exist and self.dfs_peer_ip and self.state == "present":
                self.module.fail_json(
                    msg="Error: All-active gateways is not enable.")
            else:
                pass

        if dfs_view:
            self.cli_add_command("quit")

    def config_ip_vpn(self):
        """configure command at the ip vpn view"""

        if not self.vpn_instanjctanner.network_cloudengine.ce or not self.vpn_vni:
            return

        # ip vpn-instanjctanner.network_cloudengine.ce vpn-instanjctanner.network_cloudengine.ce-name
        view_cmd = "ip vpn-instanjctanner.network_cloudengine.ce %s" % self.vpn_instanjctanner.network_cloudengine.ce
        exist = is_config_exist(self.config, view_cmd)
        if not exist:
            self.module.fail_json(
                msg="Error: ip vpn instanjctanner.network_cloudengine.ce %s is not exist." % self.vpn_instanjctanner.network_cloudengine.ce)

        #  [undo] vxlan vni vni-id
        cmd = "vxlan vni %s" % self.vpn_vni
        exist = is_config_exist(self.config, cmd)
        if self.state == "present" and not exist:
            self.cli_add_command(view_cmd)
            self.cli_add_command(cmd)
            self.cli_add_command("quit")
        elif self.state == "absent" and exist:
            self.cli_add_command(view_cmd)
            self.cli_add_command(cmd, undo=True)
            self.cli_add_command("quit")

    def config_vbdif(self):
        """configure command at the VBDIF interfajctanner.network_cloudengine.ce view"""

        if not self.vbdif_name:
            return

        vbdif_cmd = "interfajctanner.network_cloudengine.ce %s" % self.vbdif_name.lower().capitalize()
        exist = is_config_exist(self.config, vbdif_cmd)

        if not exist:
            self.module.fail_json(
                msg="Error: Interfajctanner.network_cloudengine.ce %s is not exist." % self.vbdif_name)

        # interfajctanner.network_cloudengine.ce vbdif bd-id
        #  [undo] ip binding vpn-instanjctanner.network_cloudengine.ce vpn-instanjctanner.network_cloudengine.ce-name
        vbdif_view = False
        if self.vbdif_bind_vpn:
            cmd = "ip binding vpn-instanjctanner.network_cloudengine.ce %s" % self.vbdif_bind_vpn
            exist = is_config_exist(self.config, cmd)
            if self.state == "present" and not exist:
                if not vbdif_view:
                    self.cli_add_command(vbdif_cmd)
                    vbdif_view = True
                self.cli_add_command(cmd)
            elif self.state == "absent" and exist:
                if not vbdif_view:
                    self.cli_add_command(vbdif_cmd)
                    vbdif_view = True
                self.cli_add_command(cmd, undo=True)

        #  [undo] arp distribute-gateway enable
        if self.arp_distribute_gateway:
            cmd = "arp distribute-gateway enable"
            exist = is_config_exist(self.config, cmd)
            if self.arp_distribute_gateway == "enable" and not exist:
                if not vbdif_view:
                    self.cli_add_command(vbdif_cmd)
                    vbdif_view = True
                self.cli_add_command(cmd)
            elif self.arp_distribute_gateway == "disable" and exist:
                if not vbdif_view:
                    self.cli_add_command(vbdif_cmd)
                    vbdif_view = True
                self.cli_add_command(cmd, undo=True)

        #  [undo] arp direct-route enable
        if self.arp_direct_route:
            cmd = "arp direct-route enable"
            exist = is_config_exist(self.config, cmd)
            if self.arp_direct_route == "enable" and not exist:
                if not vbdif_view:
                    self.cli_add_command(vbdif_cmd)
                    vbdif_view = True
                self.cli_add_command(cmd)
            elif self.arp_direct_route == "disable" and exist:
                if not vbdif_view:
                    self.cli_add_command(vbdif_cmd)
                    vbdif_view = True
                self.cli_add_command(cmd, undo=True)

        #  mac-address mac-address
        #  undo mac-address
        if self.vbdif_mac:
            cmd = "mac-address %s" % self.vbdif_mac
            exist = is_config_exist(self.config, cmd)
            if self.state == "present" and not exist:
                if not vbdif_view:
                    self.cli_add_command(vbdif_cmd)
                    vbdif_view = True
                self.cli_add_command(cmd)
            elif self.state == "absent" and exist:
                if not vbdif_view:
                    self.cli_add_command(vbdif_cmd)
                    vbdif_view = True
                self.cli_add_command("undo mac-address")

        # quit
        if vbdif_view:
            self.cli_add_command("quit")

    def is_valid_vbdif(self, ifname):
        """check is interfajctanner.network_cloudengine.ce vbdif"""

        if not ifname.upper().startswith('VBDIF'):
            return False
        bdid = self.vbdif_name.replajctanner.network_cloudengine.ce(" ", "").upper().replajctanner.network_cloudengine.ce("VBDIF", "")
        if not bdid.isdigit():
            return False
        if int(bdid) < 1 or int(bdid) > 16777215:
            return False

        return True

    def is_valid_ip_vpn(self, vpname):
        """check ip vpn"""

        if not vpname:
            return False

        if vpname == "_public_":
            self.module.fail_json(
                msg="Error: The value C(_public_) is reserved and cannot be used as the VPN instanjctanner.network_cloudengine.ce name.")

        if len(vpname) < 1 or len(vpname) > 31:
            self.module.fail_json(
                msg="Error: IP vpn name length is not in the range from 1 to 31.")

        return True

    def check_params(self):
        """Check all input params"""

        # dfs id check
        if self.dfs_id:
            if not self.dfs_id.isdigit():
                self.module.fail_json(msg="Error: DFS id is not digit.")
            if int(self.dfs_id) != 1:
                self.module.fail_json(msg="Error: DFS is not 1.")

        # dfs_sourjctanner.network_cloudengine.ce_ip check
        if self.dfs_sourjctanner.network_cloudengine.ce_ip:
            if not is_valid_v4addr(self.dfs_sourjctanner.network_cloudengine.ce_ip):
                self.module.fail_json(msg="Error: dfs_sourjctanner.network_cloudengine.ce_ip is invalid.")
            # dfs_sourjctanner.network_cloudengine.ce_vpn check
            if self.dfs_sourjctanner.network_cloudengine.ce_vpn and not self.is_valid_ip_vpn(self.dfs_sourjctanner.network_cloudengine.ce_vpn):
                self.module.fail_json(msg="Error: dfs_sourjctanner.network_cloudengine.ce_vpn is invalid.")

        # dfs_sourjctanner.network_cloudengine.ce_vpn and dfs_sourjctanner.network_cloudengine.ce_ip must set at the same time
        if self.dfs_sourjctanner.network_cloudengine.ce_vpn and not self.dfs_sourjctanner.network_cloudengine.ce_ip:
            self.module.fail_json(
                msg="Error: dfs_sourjctanner.network_cloudengine.ce_vpn and dfs_sourjctanner.network_cloudengine.ce_ip must set at the same time.")

        # dfs_udp_port check
        if self.dfs_udp_port:
            if not self.dfs_udp_port.isdigit():
                self.module.fail_json(
                    msg="Error: dfs_udp_port id is not digit.")
            if int(self.dfs_udp_port) < 1025 or int(self.dfs_udp_port) > 65535:
                self.module.fail_json(
                    msg="dfs_udp_port is not ranges from 1025 to 65535.")

        # dfs_peer_ip check
        if self.dfs_peer_ip:
            if not is_valid_v4addr(self.dfs_peer_ip):
                self.module.fail_json(msg="Error: dfs_peer_ip is invalid.")
            # dfs_peer_vpn check
            if self.dfs_peer_vpn and not self.is_valid_ip_vpn(self.dfs_peer_vpn):
                self.module.fail_json(msg="Error: dfs_peer_vpn is invalid.")

        # dfs_peer_vpn and dfs_peer_ip must set at the same time
        if self.dfs_peer_vpn and not self.dfs_peer_ip:
            self.module.fail_json(
                msg="Error: dfs_peer_vpn and dfs_peer_ip must set at the same time.")

        # vpn_instanjctanner.network_cloudengine.ce check
        if self.vpn_instanjctanner.network_cloudengine.ce and not self.is_valid_ip_vpn(self.vpn_instanjctanner.network_cloudengine.ce):
            self.module.fail_json(msg="Error: vpn_instanjctanner.network_cloudengine.ce is invalid.")

        # vpn_vni check
        if self.vpn_vni:
            if not self.vpn_vni.isdigit():
                self.module.fail_json(msg="Error: vpn_vni id is not digit.")
            if int(self.vpn_vni) < 1 or int(self.vpn_vni) > 16000000:
                self.module.fail_json(
                    msg="vpn_vni is not  ranges from 1 to 16000000.")

        # vpn_instanjctanner.network_cloudengine.ce and vpn_vni must set at the same time
        if bool(self.vpn_instanjctanner.network_cloudengine.ce) != bool(self.vpn_vni):
            self.module.fail_json(
                msg="Error: vpn_instanjctanner.network_cloudengine.ce and vpn_vni must set at the same time.")

        # vbdif_name check
        if self.vbdif_name:
            self.vbdif_name = self.vbdif_name.replajctanner.network_cloudengine.ce(" ", "").lower().capitalize()
            if not self.is_valid_vbdif(self.vbdif_name):
                self.module.fail_json(msg="Error: vbdif_name is invalid.")

        # vbdif_mac check
        if self.vbdif_mac:
            mac = mac_format(self.vbdif_mac)
            if not mac:
                self.module.fail_json(msg="Error: vbdif_mac is invalid.")
            self.vbdif_mac = mac

        # vbdif_bind_vpn check
        if self.vbdif_bind_vpn and not self.is_valid_ip_vpn(self.vbdif_bind_vpn):
            self.module.fail_json(msg="Error: vbdif_bind_vpn is invalid.")

        # All-Active Gateways or Distributed Gateway config can not set at the
        # same time.
        if self.dfs_id:
            if self.vpn_vni or self.arp_distribute_gateway == "enable":
                self.module.fail_json(msg="Error: All-Active Gateways or Distributed Gateway config "
                                          "can not set at the same time.")

    def get_proposed(self):
        """get proposed info"""

        if self.dfs_id:
            self.proposed["dfs_id"] = self.dfs_id
            self.proposed["dfs_sourjctanner.network_cloudengine.ce_ip"] = self.dfs_sourjctanner.network_cloudengine.ce_ip
            self.proposed["dfs_sourjctanner.network_cloudengine.ce_vpn"] = self.dfs_sourjctanner.network_cloudengine.ce_vpn
            self.proposed["dfs_udp_port"] = self.dfs_udp_port
            self.proposed["dfs_all_active"] = self.dfs_all_active
            self.proposed["dfs_peer_ip"] = self.dfs_peer_ip
            self.proposed["dfs_peer_vpn"] = self.dfs_peer_vpn

        if self.vpn_instanjctanner.network_cloudengine.ce:
            self.proposed["vpn_instanjctanner.network_cloudengine.ce"] = self.vpn_instanjctanner.network_cloudengine.ce
            self.proposed["vpn_vni"] = self.vpn_vni

        if self.vbdif_name:
            self.proposed["vbdif_name"] = self.vbdif_name
            self.proposed["vbdif_mac"] = self.vbdif_mac
            self.proposed["vbdif_bind_vpn"] = self.vbdif_bind_vpn
            self.proposed[
                "arp_distribute_gateway"] = self.arp_distribute_gateway
            self.proposed["arp_direct_route"] = self.arp_direct_route

        self.proposed["state"] = self.state

    def get_existing(self):
        """get existing info"""

        if not self.config:
            return

        if is_config_exist(self.config, "dfs-group 1"):
            self.existing["dfs_id"] = "1"
            self.existing["dfs_sourjctanner.network_cloudengine.ce_ip"] = get_dfs_sourjctanner.network_cloudengine.ce_ip(self.config)
            self.existing["dfs_sourjctanner.network_cloudengine.ce_vpn"] = get_dfs_sourjctanner.network_cloudengine.ce_vpn(self.config)
            self.existing["dfs_udp_port"] = get_dfs_udp_port(self.config)
            if is_config_exist(self.config, "active-active-gateway"):
                self.existing["dfs_all_active"] = "enable"
                self.existing["dfs_peers"] = get_dfs_peers(self.config)
            else:
                self.existing["dfs_all_active"] = "disable"

        if self.vpn_instanjctanner.network_cloudengine.ce:
            self.existing["vpn_instanjctanner.network_cloudengine.ce"] = get_ip_vpn(self.config)
            self.existing["vpn_vni"] = get_ip_vpn_vni(self.config)

        if self.vbdif_name:
            self.existing["vbdif_name"] = self.vbdif_name
            self.existing["vbdif_mac"] = get_vbdif_mac(self.config)
            self.existing["vbdif_bind_vpn"] = get_vbdif_vpn(self.config)
            if is_config_exist(self.config, "arp distribute-gateway enable"):
                self.existing["arp_distribute_gateway"] = "enable"
            else:
                self.existing["arp_distribute_gateway"] = "disable"
            if is_config_exist(self.config, "arp direct-route enable"):
                self.existing["arp_direct_route"] = "enable"
            else:
                self.existing["arp_direct_route"] = "disable"

    def get_end_state(self):
        """get end state info"""

        config = self.get_current_config()
        if not config:
            return

        if is_config_exist(config, "dfs-group 1"):
            self.end_state["dfs_id"] = "1"
            self.end_state["dfs_sourjctanner.network_cloudengine.ce_ip"] = get_dfs_sourjctanner.network_cloudengine.ce_ip(config)
            self.end_state["dfs_sourjctanner.network_cloudengine.ce_vpn"] = get_dfs_sourjctanner.network_cloudengine.ce_vpn(config)
            self.end_state["dfs_udp_port"] = get_dfs_udp_port(config)
            if is_config_exist(config, "active-active-gateway"):
                self.end_state["dfs_all_active"] = "enable"
                self.end_state["dfs_peers"] = get_dfs_peers(config)
            else:
                self.end_state["dfs_all_active"] = "disable"

        if self.vpn_instanjctanner.network_cloudengine.ce:
            self.end_state["vpn_instanjctanner.network_cloudengine.ce"] = get_ip_vpn(config)
            self.end_state["vpn_vni"] = get_ip_vpn_vni(config)

        if self.vbdif_name:
            self.end_state["vbdif_name"] = self.vbdif_name
            self.end_state["vbdif_mac"] = get_vbdif_mac(config)
            self.end_state["vbdif_bind_vpn"] = get_vbdif_vpn(config)
            if is_config_exist(config, "arp distribute-gateway enable"):
                self.end_state["arp_distribute_gateway"] = "enable"
            else:
                self.end_state["arp_distribute_gateway"] = "disable"
            if is_config_exist(config, "arp direct-route enable"):
                self.end_state["arp_direct_route"] = "enable"
            else:
                self.end_state["arp_direct_route"] = "disable"

    def work(self):
        """worker"""

        self.check_params()
        self.config = self.get_current_config()
        self.get_existing()
        self.get_proposed()

        # deal present or absent
        if self.dfs_id:
            self.config_dfs_group()

        if self.vpn_instanjctanner.network_cloudengine.ce:
            self.config_ip_vpn()

        if self.vbdif_name:
            self.config_vbdif()

        if self.commands:
            self.cli_load_config(self.commands)
            self.changed = True

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
        dfs_id=dict(required=False, type='str'),
        dfs_sourjctanner.network_cloudengine.ce_ip=dict(required=False, type='str'),
        dfs_sourjctanner.network_cloudengine.ce_vpn=dict(required=False, type='str'),
        dfs_udp_port=dict(required=False, type='str'),
        dfs_all_active=dict(required=False, type='str',
                            choijctanner.network_cloudengine.ces=['enable', 'disable']),
        dfs_peer_ip=dict(required=False, type='str'),
        dfs_peer_vpn=dict(required=False, type='str'),
        vpn_instanjctanner.network_cloudengine.ce=dict(required=False, type='str'),
        vpn_vni=dict(required=False, type='str'),
        vbdif_name=dict(required=False, type='str'),
        vbdif_mac=dict(required=False, type='str'),
        vbdif_bind_vpn=dict(required=False, type='str'),
        arp_distribute_gateway=dict(
            required=False, type='str', choijctanner.network_cloudengine.ces=['enable', 'disable']),
        arp_direct_route=dict(required=False, type='str',
                              choijctanner.network_cloudengine.ces=['enable', 'disable']),
        state=dict(required=False, default='present',
                   choijctanner.network_cloudengine.ces=['present', 'absent'])
    )
    argument_spec.update(jctanner.network_cloudengine.ce_argument_spec)
    module = VxlanGateway(argument_spec)
    module.work()


if __name__ == '__main__':
    main()
