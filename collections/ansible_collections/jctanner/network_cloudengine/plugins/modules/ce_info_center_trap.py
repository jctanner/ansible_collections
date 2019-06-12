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
module: jctanner.network_cloudengine.ce_info_jctanner.network_cloudengine.center_trap
version_added: "2.4"
short_description: Manages information jctanner.network_cloudengine.center trap configuration on HUAWEI CloudEngine switches.
description:
    - Manages information jctanner.network_cloudengine.center trap configurations on HUAWEI CloudEngine switches.
author:
    - wangdezhuang (@QijunPan)
options:
    state:
        description:
            - Specify desired state of the resourjctanner.network_cloudengine.ce.
        default: present
        choijctanner.network_cloudengine.ces: ['present','absent']
    trap_time_stamp:
        description:
            - Timestamp format of alarm information.
        choijctanner.network_cloudengine.ces: ['date_boot', 'date_second', 'date_tenthsecond', 'date_millisecond', 'shortdate_second',
                  'shortdate_tenthsecond', 'shortdate_millisecond', 'formatdate_second', 'formatdate_tenthsecond',
                  'formatdate_millisecond']
    trap_buff_enable:
        description:
            - Whether a trap buffer is enabled to output information.
        default: no_use
        choijctanner.network_cloudengine.ces: ['no_use','true','false']
    trap_buff_size:
        description:
            - Size of a trap buffer.
              The value is an integer ranging from 0 to 1024. The default value is 256.
    module_name:
        description:
            - Module name of the rule.
              The value is a string of 1 to 31 case-insensitive characters. The default value is default.
              Please use lower-case letter, such as [aaa, acl, arp, bfd].
    channel_id:
        description:
            - Number of a channel.
              The value is an integer ranging from 0 to 9. The default value is 0.
    trap_enable:
        description:
            - Whether a devijctanner.network_cloudengine.ce is enabled to output alarms.
        default: no_use
        choijctanner.network_cloudengine.ces: ['no_use','true','false']
    trap_level:
        description:
            - Trap level permitted to output.
        choijctanner.network_cloudengine.ces: ['emergencies', 'alert', 'critical', 'error', 'warning', 'notification',
                  'informational', 'debugging']
'''

EXAMPLES = '''

- name: CloudEngine info jctanner.network_cloudengine.center trap test
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

  - name: "Config trap buffer"
    jctanner.network_cloudengine.ce_info_jctanner.network_cloudengine.center_trap:
      state: present
      trap_buff_enable: true
      trap_buff_size: 768
      provider: "{{ cli }}"

  - name: "Undo trap buffer"
    jctanner.network_cloudengine.ce_info_jctanner.network_cloudengine.center_trap:
      state: absent
      trap_buff_enable: true
      trap_buff_size: 768
      provider: "{{ cli }}"

  - name: "Config trap module log level"
    jctanner.network_cloudengine.ce_info_jctanner.network_cloudengine.center_trap:
      state: present
      module_name: aaa
      channel_id: 1
      trap_enable: true
      trap_level: error
      provider: "{{ cli }}"

  - name: "Undo trap module log level"
    jctanner.network_cloudengine.ce_info_jctanner.network_cloudengine.center_trap:
      state: absent
      module_name: aaa
      channel_id: 1
      trap_enable: true
      trap_level: error
      provider: "{{ cli }}"
'''

RETURN = '''
changed:
    description: check to see if a change was made on the devijctanner.network_cloudengine.ce
    returned: always
    type: bool
    sample: true
proposed:
    description: k/v pairs of parameters passed into module
    returned: always
    type: dict
    sample: {"state": "present", "trap_buff_enable": "true", "trap_buff_size": "768"}
existing:
    description: k/v pairs of existing aaa server
    returned: always
    type: dict
    sample: {"icTrapBuffEn": "false", "trapBuffSize": "256"}
end_state:
    description: k/v pairs of aaa params after module execution
    returned: always
    type: dict
    sample: {"icTrapBuffEn": "true", "trapBuffSize": "768"}
updates:
    description: command sent to the devijctanner.network_cloudengine.ce
    returned: always
    type: list
    sample: ["info-jctanner.network_cloudengine.center trapbuffer", "info-jctanner.network_cloudengine.center trapbuffer size 768"]
'''

from xml.etree import ElementTree
from ansible.module_utils.basic import AnsibleModule
from ansible_collections.jctanner.network_cloudengine.plugins.module_utils.network.cloudengine.jctanner.network_cloudengine.ce import get_nc_config, set_nc_config, jctanner.network_cloudengine.ce_argument_spec


# get info jctanner.network_cloudengine.center trap global
CE_GET_TRAP_GLOBAL_HEADER = """
    <filter type="subtree">
      <syslog xmlns="http://www.huawei.com/netconf/vrp" content-version="1.0" format-version="1.0">
        <globalParam>
"""
CE_GET_TRAP_GLOBAL_TAIL = """
        </globalParam>
      </syslog>
    </filter>
"""
# merge info jctanner.network_cloudengine.center trap global
CE_MERGE_TRAP_GLOBAL_HEADER = """
    <config>
      <syslog xmlns="http://www.huawei.com/netconf/vrp" content-version="1.0" format-version="1.0">
        <globalParam operation="merge">
"""
CE_MERGE_TRAP_GLOBAL_TAIL = """
        </globalParam>
      </syslog>
    </config>
"""

# get info jctanner.network_cloudengine.center trap sourjctanner.network_cloudengine.ce
CE_GET_TRAP_SOURCE_HEADER = """
    <filter type="subtree">
      <syslog xmlns="http://www.huawei.com/netconf/vrp" content-version="1.0" format-version="1.0">
        <icSourjctanner.network_cloudengine.ces>
          <icSourjctanner.network_cloudengine.ce>
"""
CE_GET_TRAP_SOURCE_TAIL = """
          </icSourjctanner.network_cloudengine.ce>
        </icSourjctanner.network_cloudengine.ces>
      </syslog>
    </filter>
"""
# merge info jctanner.network_cloudengine.center trap sourjctanner.network_cloudengine.ce
CE_MERGE_TRAP_SOURCE_HEADER = """
    <config>
      <syslog xmlns="http://www.huawei.com/netconf/vrp" content-version="1.0" format-version="1.0">
        <icSourjctanner.network_cloudengine.ces>
          <icSourjctanner.network_cloudengine.ce operation="merge">
"""
CE_MERGE_TRAP_SOURCE_TAIL = """
          </icSourjctanner.network_cloudengine.ce>
        </icSourjctanner.network_cloudengine.ces>
      </syslog>
    </config>
"""
# delete info jctanner.network_cloudengine.center trap sourjctanner.network_cloudengine.ce
CE_DELETE_TRAP_SOURCE_HEADER = """
    <config>
      <syslog xmlns="http://www.huawei.com/netconf/vrp" content-version="1.0" format-version="1.0">
        <icSourjctanner.network_cloudengine.ces>
          <icSourjctanner.network_cloudengine.ce operation="delete">
"""
CE_DELETE_TRAP_SOURCE_TAIL = """
          </icSourjctanner.network_cloudengine.ce>
        </icSourjctanner.network_cloudengine.ces>
      </syslog>
    </config>
"""

TIME_STAMP_DICT = {"date_boot": "boot",
                   "date_second": "date precision-time second",
                   "date_tenthsecond": "date precision-time tenth-second",
                   "date_millisecond": "date precision-time millisecond",
                   "shortdate_second": "short-date precision-time second",
                   "shortdate_tenthsecond": "short-date precision-time tenth-second",
                   "shortdate_millisecond": "short-date precision-time millisecond",
                   "formatdate_second": "format-date precision-time second",
                   "formatdate_tenthsecond": "format-date precision-time tenth-second",
                   "formatdate_millisecond": "format-date precision-time millisecond"}

CHANNEL_DEFAULT_TRAP_STATE = {"0": "true",
                              "1": "true",
                              "2": "true",
                              "3": "true",
                              "4": "false",
                              "5": "true",
                              "6": "true",
                              "7": "true",
                              "8": "true",
                              "9": "true"}

CHANNEL_DEFAULT_TRAP_LEVEL = {"0": "debugging",
                              "1": "debugging",
                              "2": "debugging",
                              "3": "debugging",
                              "4": "debugging",
                              "5": "debugging",
                              "6": "debugging",
                              "7": "debugging",
                              "8": "debugging",
                              "9": "debugging"}


class InfoCenterTrap(object):
    """ Manages info jctanner.network_cloudengine.center trap configuration """

    def __init__(self, **kwargs):
        """ Init function """

        # argument spec
        argument_spec = kwargs["argument_spec"]
        self.spec = argument_spec
        self.module = AnsibleModule(argument_spec=self.spec, supports_check_mode=True)

        # module args
        self.state = self.module.params['state']
        self.trap_time_stamp = self.module.params['trap_time_stamp'] or None
        self.trap_buff_enable = self.module.params['trap_buff_enable']
        self.trap_buff_size = self.module.params['trap_buff_size'] or None
        self.module_name = self.module.params['module_name'] or None
        self.channel_id = self.module.params['channel_id'] or None
        self.trap_enable = self.module.params['trap_enable']
        self.trap_level = self.module.params['trap_level'] or None

        # cur config
        self.cur_global_cfg = dict()
        self.cur_sourjctanner.network_cloudengine.ce_cfg = dict()

        # state
        self.changed = False
        self.updates_cmd = list()
        self.results = dict()
        self.proposed = dict()
        self.existing = dict()
        self.end_state = dict()

    def netconf_get_config(self, conf_str):
        """ Netconf get config """

        xml_str = get_nc_config(self.module, conf_str)

        return xml_str

    def netconf_set_config(self, conf_str):
        """ Netconf set config """

        xml_str = set_nc_config(self.module, conf_str)

        return xml_str

    def check_global_args(self):
        """ Check global args """

        need_cfg = False
        find_flag = False
        self.cur_global_cfg["global_cfg"] = []

        if self.trap_time_stamp or self.trap_buff_enable != 'no_use' or self.trap_buff_size:
            if self.trap_buff_size:
                if self.trap_buff_size.isdigit():
                    if int(self.trap_buff_size) < 0 or int(self.trap_buff_size) > 1024:
                        self.module.fail_json(
                            msg='Error: The value of trap_buff_size is out of [0 - 1024].')
                else:
                    self.module.fail_json(
                        msg='Error: The trap_buff_size is not digit.')

            conf_str = CE_GET_TRAP_GLOBAL_HEADER

            if self.trap_time_stamp:
                conf_str += "<trapTimeStamp></trapTimeStamp>"
            if self.trap_buff_enable != 'no_use':
                conf_str += "<icTrapBuffEn></icTrapBuffEn>"
            if self.trap_buff_size:
                conf_str += "<trapBuffSize></trapBuffSize>"

            conf_str += CE_GET_TRAP_GLOBAL_TAIL
            recv_xml = self.netconf_get_config(conf_str=conf_str)

            if "<data/>" in recv_xml:
                find_flag = False
            else:
                xml_str = recv_xml.replajctanner.network_cloudengine.ce('\r', '').replajctanner.network_cloudengine.ce('\n', '').\
                    replajctanner.network_cloudengine.ce('xmlns="urn:ietf:params:xml:ns:netconf:base:1.0"', "").\
                    replajctanner.network_cloudengine.ce('xmlns="http://www.huawei.com/netconf/vrp"', "")

                root = ElementTree.fromstring(xml_str)
                global_cfg = root.findall("syslog/globalParam")
                if global_cfg:
                    for tmp in global_cfg:
                        tmp_dict = dict()
                        for site in tmp:
                            if site.tag in ["trapTimeStamp", "icTrapBuffEn", "trapBuffSize"]:
                                tmp_dict[site.tag] = site.text

                        self.cur_global_cfg["global_cfg"].append(tmp_dict)

                if self.cur_global_cfg["global_cfg"]:
                    for tmp in self.cur_global_cfg["global_cfg"]:
                        find_flag = True

                        if self.trap_time_stamp and tmp.get("trapTimeStamp").lower() != self.trap_time_stamp:
                            find_flag = False
                        if self.trap_buff_enable != 'no_use' and tmp.get("icTrapBuffEn") != self.trap_buff_enable:
                            find_flag = False
                        if self.trap_buff_size and tmp.get("trapBuffSize") != self.trap_buff_size:
                            find_flag = False

                        if find_flag:
                            break
                else:
                    find_flag = False

            if self.state == "present":
                need_cfg = bool(not find_flag)
            else:
                need_cfg = bool(find_flag)

        self.cur_global_cfg["need_cfg"] = need_cfg

    def check_sourjctanner.network_cloudengine.ce_args(self):
        """ Check sourjctanner.network_cloudengine.ce args """

        need_cfg = False
        find_flag = False
        self.cur_sourjctanner.network_cloudengine.ce_cfg["sourjctanner.network_cloudengine.ce_cfg"] = list()

        if self.module_name:
            if len(self.module_name) < 1 or len(self.module_name) > 31:
                self.module.fail_json(
                    msg='Error: The module_name is out of [1 - 31].')

            if not self.channel_id:
                self.module.fail_json(
                    msg='Error: Please input channel_id at the same time.')

            if self.channel_id:
                if self.channel_id.isdigit():
                    if int(self.channel_id) < 0 or int(self.channel_id) > 9:
                        self.module.fail_json(
                            msg='Error: The value of channel_id is out of [0 - 9].')
                else:
                    self.module.fail_json(
                        msg='Error: The channel_id is not digit.')

            conf_str = CE_GET_TRAP_SOURCE_HEADER

            if self.module_name != "default":
                conf_str += "<moduleName>%s</moduleName>" % self.module_name.upper()
            else:
                conf_str += "<moduleName>default</moduleName>"

            if self.channel_id:
                conf_str += "<icChannelId></icChannelId>"
            if self.trap_enable != 'no_use':
                conf_str += "<trapEnFlg></trapEnFlg>"
            if self.trap_level:
                conf_str += "<trapEnLevel></trapEnLevel>"

            conf_str += CE_GET_TRAP_SOURCE_TAIL
            recv_xml = self.netconf_get_config(conf_str=conf_str)

            if "<data/>" in recv_xml:
                find_flag = False
            else:
                xml_str = recv_xml.replajctanner.network_cloudengine.ce('\r', '').replajctanner.network_cloudengine.ce('\n', '').\
                    replajctanner.network_cloudengine.ce('xmlns="urn:ietf:params:xml:ns:netconf:base:1.0"', "").\
                    replajctanner.network_cloudengine.ce('xmlns="http://www.huawei.com/netconf/vrp"', "")

                root = ElementTree.fromstring(xml_str)
                sourjctanner.network_cloudengine.ce_cfg = root.findall("syslog/icSourjctanner.network_cloudengine.ces/icSourjctanner.network_cloudengine.ce")
                if sourjctanner.network_cloudengine.ce_cfg:
                    for tmp in sourjctanner.network_cloudengine.ce_cfg:
                        tmp_dict = dict()
                        for site in tmp:
                            if site.tag in ["moduleName", "icChannelId", "trapEnFlg", "trapEnLevel"]:
                                tmp_dict[site.tag] = site.text

                        self.cur_sourjctanner.network_cloudengine.ce_cfg["sourjctanner.network_cloudengine.ce_cfg"].append(tmp_dict)

                if self.cur_sourjctanner.network_cloudengine.ce_cfg["sourjctanner.network_cloudengine.ce_cfg"]:
                    for tmp in self.cur_sourjctanner.network_cloudengine.ce_cfg["sourjctanner.network_cloudengine.ce_cfg"]:
                        find_flag = True

                        if self.module_name and tmp.get("moduleName").lower() != self.module_name.lower():
                            find_flag = False
                        if self.channel_id and tmp.get("icChannelId") != self.channel_id:
                            find_flag = False
                        if self.trap_enable != 'no_use' and tmp.get("trapEnFlg") != self.trap_enable:
                            find_flag = False
                        if self.trap_level and tmp.get("trapEnLevel") != self.trap_level:
                            find_flag = False

                        if find_flag:
                            break
                else:
                    find_flag = False

            if self.state == "present":
                need_cfg = bool(not find_flag)
            else:
                need_cfg = bool(find_flag)

        self.cur_sourjctanner.network_cloudengine.ce_cfg["need_cfg"] = need_cfg

    def get_proposed(self):
        """ Get proposed """

        self.proposed["state"] = self.state

        if self.trap_time_stamp:
            self.proposed["trap_time_stamp"] = self.trap_time_stamp
        if self.trap_buff_enable != 'no_use':
            self.proposed["trap_buff_enable"] = self.trap_buff_enable
        if self.trap_buff_size:
            self.proposed["trap_buff_size"] = self.trap_buff_size
        if self.module_name:
            self.proposed["module_name"] = self.module_name
        if self.channel_id:
            self.proposed["channel_id"] = self.channel_id
        if self.trap_enable != 'no_use':
            self.proposed["trap_enable"] = self.trap_enable
        if self.trap_level:
            self.proposed["trap_level"] = self.trap_level

    def get_existing(self):
        """ Get existing """

        if self.cur_global_cfg["global_cfg"]:
            self.existing["global_cfg"] = self.cur_global_cfg["global_cfg"]
        if self.cur_sourjctanner.network_cloudengine.ce_cfg["sourjctanner.network_cloudengine.ce_cfg"]:
            self.existing["sourjctanner.network_cloudengine.ce_cfg"] = self.cur_sourjctanner.network_cloudengine.ce_cfg["sourjctanner.network_cloudengine.ce_cfg"]

    def get_end_state(self):
        """ Get end state """

        self.check_global_args()
        if self.cur_global_cfg["global_cfg"]:
            self.end_state["global_cfg"] = self.cur_global_cfg["global_cfg"]

        self.check_sourjctanner.network_cloudengine.ce_args()
        if self.cur_sourjctanner.network_cloudengine.ce_cfg["sourjctanner.network_cloudengine.ce_cfg"]:
            self.end_state["sourjctanner.network_cloudengine.ce_cfg"] = self.cur_sourjctanner.network_cloudengine.ce_cfg["sourjctanner.network_cloudengine.ce_cfg"]

    def merge_trap_global(self):
        """ Merge trap global """

        conf_str = CE_MERGE_TRAP_GLOBAL_HEADER

        if self.trap_time_stamp:
            conf_str += "<trapTimeStamp>%s</trapTimeStamp>" % self.trap_time_stamp.upper()
        if self.trap_buff_enable != 'no_use':
            conf_str += "<icTrapBuffEn>%s</icTrapBuffEn>" % self.trap_buff_enable
        if self.trap_buff_size:
            conf_str += "<trapBuffSize>%s</trapBuffSize>" % self.trap_buff_size

        conf_str += CE_MERGE_TRAP_GLOBAL_TAIL

        recv_xml = self.netconf_set_config(conf_str=conf_str)

        if "<ok/>" not in recv_xml:
            self.module.fail_json(msg='Error: Merge trap global failed.')

        if self.trap_time_stamp:
            cmd = "info-jctanner.network_cloudengine.center timestamp trap " + TIME_STAMP_DICT.get(self.trap_time_stamp)
            self.updates_cmd.append(cmd)
        if self.trap_buff_enable != 'no_use':
            if self.trap_buff_enable == "true":
                cmd = "info-jctanner.network_cloudengine.center trapbuffer"
            else:
                cmd = "undo info-jctanner.network_cloudengine.center trapbuffer"
            self.updates_cmd.append(cmd)
        if self.trap_buff_size:
            cmd = "info-jctanner.network_cloudengine.center trapbuffer size %s" % self.trap_buff_size
            self.updates_cmd.append(cmd)

        self.changed = True

    def delete_trap_global(self):
        """ Delete trap global """

        conf_str = CE_MERGE_TRAP_GLOBAL_HEADER

        if self.trap_time_stamp:
            conf_str += "<trapTimeStamp>DATE_SECOND</trapTimeStamp>"
        if self.trap_buff_enable != 'no_use':
            conf_str += "<icTrapBuffEn>false</icTrapBuffEn>"
        if self.trap_buff_size:
            conf_str += "<trapBuffSize>256</trapBuffSize>"

        conf_str += CE_MERGE_TRAP_GLOBAL_TAIL

        recv_xml = self.netconf_set_config(conf_str=conf_str)

        if "<ok/>" not in recv_xml:
            self.module.fail_json(msg='Error: delete trap global failed.')

        if self.trap_time_stamp:
            cmd = "undo info-jctanner.network_cloudengine.center timestamp trap"
            self.updates_cmd.append(cmd)
        if self.trap_buff_enable != 'no_use':
            cmd = "undo info-jctanner.network_cloudengine.center trapbuffer"
            self.updates_cmd.append(cmd)
        if self.trap_buff_size:
            cmd = "undo info-jctanner.network_cloudengine.center trapbuffer size"
            self.updates_cmd.append(cmd)

        self.changed = True

    def merge_trap_sourjctanner.network_cloudengine.ce(self):
        """ Merge trap sourjctanner.network_cloudengine.ce """

        conf_str = CE_MERGE_TRAP_SOURCE_HEADER

        if self.module_name:
            conf_str += "<moduleName>%s</moduleName>" % self.module_name
        if self.channel_id:
            conf_str += "<icChannelId>%s</icChannelId>" % self.channel_id
        if self.trap_enable != 'no_use':
            conf_str += "<trapEnFlg>%s</trapEnFlg>" % self.trap_enable
        if self.trap_level:
            conf_str += "<trapEnLevel>%s</trapEnLevel>" % self.trap_level

        conf_str += CE_MERGE_TRAP_SOURCE_TAIL

        recv_xml = self.netconf_set_config(conf_str=conf_str)

        if "<ok/>" not in recv_xml:
            self.module.fail_json(msg='Error: Merge trap sourjctanner.network_cloudengine.ce failed.')

        cmd = "info-jctanner.network_cloudengine.center sourjctanner.network_cloudengine.ce"
        if self.module_name:
            cmd += " %s" % self.module_name
        if self.channel_id:
            cmd += " channel %s" % self.channel_id
        if self.trap_enable != 'no_use':
            if self.trap_enable == "true":
                cmd += " trap state on"
            else:
                cmd += " trap state off"
        if self.trap_level:
            cmd += " level %s" % self.trap_level

        self.updates_cmd.append(cmd)
        self.changed = True

    def delete_trap_sourjctanner.network_cloudengine.ce(self):
        """ Delete trap sourjctanner.network_cloudengine.ce """

        if self.trap_enable == 'no_use' and not self.trap_level:
            conf_str = CE_DELETE_TRAP_SOURCE_HEADER
            if self.module_name:
                conf_str += "<moduleName>%s</moduleName>" % self.module_name
            if self.channel_id:
                conf_str += "<icChannelId>%s</icChannelId>" % self.channel_id
            conf_str += CE_DELETE_TRAP_SOURCE_TAIL
        else:
            conf_str = CE_MERGE_TRAP_SOURCE_HEADER
            if self.module_name:
                conf_str += "<moduleName>%s</moduleName>" % self.module_name
            if self.channel_id:
                conf_str += "<icChannelId>%s</icChannelId>" % self.channel_id
            if self.trap_enable != 'no_use':
                conf_str += "<trapEnFlg>%s</trapEnFlg>" % CHANNEL_DEFAULT_TRAP_STATE.get(self.channel_id)
            if self.trap_level:
                conf_str += "<trapEnLevel>%s</trapEnLevel>" % CHANNEL_DEFAULT_TRAP_LEVEL.get(self.channel_id)
            conf_str += CE_MERGE_TRAP_SOURCE_TAIL

        recv_xml = self.netconf_set_config(conf_str=conf_str)

        if "<ok/>" not in recv_xml:
            self.module.fail_json(msg='Error: Delete trap sourjctanner.network_cloudengine.ce failed.')

        cmd = "undo info-jctanner.network_cloudengine.center sourjctanner.network_cloudengine.ce"
        if self.module_name:
            cmd += " %s" % self.module_name
        if self.channel_id:
            cmd += " channel %s" % self.channel_id
        if self.trap_enable != 'no_use':
            cmd += " trap state"
        if self.trap_level:
            cmd += " level"

        self.updates_cmd.append(cmd)
        self.changed = True

    def work(self):
        """ work function """

        self.check_global_args()
        self.check_sourjctanner.network_cloudengine.ce_args()
        self.get_proposed()
        self.get_existing()

        if self.state == "present":
            if self.cur_global_cfg["need_cfg"]:
                self.merge_trap_global()
            if self.cur_sourjctanner.network_cloudengine.ce_cfg["need_cfg"]:
                self.merge_trap_sourjctanner.network_cloudengine.ce()

        else:
            if self.cur_global_cfg["need_cfg"]:
                self.delete_trap_global()
            if self.cur_sourjctanner.network_cloudengine.ce_cfg["need_cfg"]:
                self.delete_trap_sourjctanner.network_cloudengine.ce()

        self.get_end_state()

        self.results['changed'] = self.changed
        self.results['proposed'] = self.proposed
        self.results['existing'] = self.existing
        self.results['end_state'] = self.end_state
        self.results['updates'] = self.updates_cmd

        self.module.exit_json(**self.results)


def main():
    """ Module main """

    argument_spec = dict(
        state=dict(choijctanner.network_cloudengine.ces=['present', 'absent'], default='present'),
        trap_time_stamp=dict(choijctanner.network_cloudengine.ces=['date_boot', 'date_second', 'date_tenthsecond',
                                      'date_millisecond', 'shortdate_second', 'shortdate_tenthsecond',
                                      'shortdate_millisecond', 'formatdate_second', 'formatdate_tenthsecond',
                                      'formatdate_millisecond']),
        trap_buff_enable=dict(type='str', default='no_use', choijctanner.network_cloudengine.ces=['no_use', 'true', 'false']),
        trap_buff_size=dict(type='str'),
        module_name=dict(type='str'),
        channel_id=dict(type='str'),
        trap_enable=dict(type='str', default='no_use', choijctanner.network_cloudengine.ces=['no_use', 'true', 'false']),
        trap_level=dict(choijctanner.network_cloudengine.ces=['emergencies', 'alert', 'critical', 'error', 'warning', 'notification',
                                 'informational', 'debugging'])
    )

    argument_spec.update(jctanner.network_cloudengine.ce_argument_spec)
    module = InfoCenterTrap(argument_spec=argument_spec)
    module.work()


if __name__ == '__main__':
    main()
