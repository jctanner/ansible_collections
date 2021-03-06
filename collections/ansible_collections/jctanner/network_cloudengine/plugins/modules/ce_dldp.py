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

module: jctanner.network_cloudengine.ce_dldp
version_added: "2.4"
short_description: Manages global DLDP configuration on HUAWEI CloudEngine switches.
description:
    - Manages global DLDP configuration on HUAWEI CloudEngine switches.
author:
    - Zhijin Zhou (@QijunPan)
notes:
    - The relevant configurations will be deleted if DLDP is disabled using enable=disable.
    - When using auth_mode=none, it will restore the default DLDP authentication mode. By default,
      DLDP packets are not authenticated.
    - By default, the working mode of DLDP is enhanjctanner.network_cloudengine.ce, so you are advised to use work_mode=enhanjctanner.network_cloudengine.ce to restore defualt
      DLDP working mode.
    - The default interval for sending Advertisement packets is 5 seconds, so you are advised to use time_interval=5 to
      restore defualt DLDP interval.
options:
    enable:
        description:
            - Set global DLDP enable state.
        choijctanner.network_cloudengine.ces: ['enable', 'disable']
    work_mode:
        description:
            - Set global DLDP work-mode.
        choijctanner.network_cloudengine.ces: ['enhanjctanner.network_cloudengine.ce', 'normal']
    time_internal:
        description:
            - Specifies the interval for sending Advertisement packets.
              The value is an integer ranging from 1 to 100, in seconds.
              The default interval for sending Advertisement packets is 5 seconds.
    auth_mode:
        description:
            - Specifies authentication algorithm of DLDP.
        choijctanner.network_cloudengine.ces: ['md5', 'simple', 'sha', 'hmac-sha256', 'none']
    auth_pwd:
        description:
            - Specifies authentication password.
              The value is a string of 1 to 16 case-sensitive plaintexts or 24/32/48/108/128 case-sensitive encrypted
              characters. The string excludes a question mark (?).
    reset:
        description:
            - Specify whether reset DLDP state of disabled interfajctanner.network_cloudengine.ces.
        choijctanner.network_cloudengine.ces: ['enable', 'disable']
'''

EXAMPLES = '''
- name: DLDP test
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

  - name: "Configure global DLDP enable state"
    jctanner.network_cloudengine.ce_dldp:
      enable: enable
      provider: "{{ cli }}"

  - name: "Configure DLDP work-mode and ensure global DLDP state is already enabled"
    jctanner.network_cloudengine.ce_dldp:
      enable: enable
      work_mode: normal
      provider: "{{ cli }}"

  - name: "Configure advertisement message time interval in seconds and ensure global DLDP state is already enabled"
    jctanner.network_cloudengine.ce_dldp:
      enable: enable
      time_interval: 6
      provider: "{{ cli }}"

  - name: "Configure a DLDP authentication mode and ensure global DLDP state is already enabled"
    jctanner.network_cloudengine.ce_dldp:
      enable: enable
      auth_mode: md5
      auth_pwd: abc
      provider: "{{ cli }}"

  - name: "Reset DLDP state of disabled interfajctanner.network_cloudengine.ces and ensure global DLDP state is already enabled"
    jctanner.network_cloudengine.ce_dldp:
      enable: enable
      reset: enable
      provider: "{{ cli }}"
'''

RETURN = '''
proposed:
    description: k/v pairs of parameters passed into module
    returned: always
    type: dict
    sample: {
                "enable": "enable",
                "reset": "enable",
                "time_internal": "12",
                "work_mode": "normal"
            }
existing:
    description: k/v pairs of existing global DLDP configration
    returned: always
    type: dict
    sample: {
                "enable": "disable",
                "reset": "disable",
                "time_internal": "5",
                "work_mode": "enhanjctanner.network_cloudengine.ce"
            }
end_state:
    description: k/v pairs of global DLDP configration after module execution
    returned: always
    type: dict
    sample: {
                "enable": "enable",
                "reset": "enable",
                "time_internal": "12",
                "work_mode": "normal"
            }
updates:
    description: command sent to the devijctanner.network_cloudengine.ce
    returned: always
    type: list
    sample: [
                "dldp enable",
                "dldp work-mode normal",
                "dldp interval 12",
                "dldp reset"
            ]
changed:
    description: check to see if a change was made on the devijctanner.network_cloudengine.ce
    returned: always
    type: bool
    sample: true
'''

import copy
from xml.etree import ElementTree
from ansible.module_utils.basic import AnsibleModule
from ansible_collections.jctanner.network_cloudengine.plugins.module_utils.network.cloudengine.jctanner.network_cloudengine.ce import jctanner.network_cloudengine.ce_argument_spec, set_nc_config, get_nc_config, execute_nc_action

CE_NC_ACTION_RESET_DLDP = """
<action>
  <dldp xmlns="http://www.huawei.com/netconf/vrp" content-version="1.0" format-version="1.0">
    <resetDldp></resetDldp>
  </dldp>
</action>
"""

CE_NC_GET_GLOBAL_DLDP_CONFIG = """
<filter type="subtree">
  <dldp xmlns="http://www.huawei.com/netconf/vrp" content-version="1.0" format-version="1.0">
    <dldpSys>
      <dldpEnable></dldpEnable>
      <dldpInterval></dldpInterval>
      <dldpWorkMode></dldpWorkMode>
      <dldpAuthMode></dldpAuthMode>
    </dldpSys>
  </dldp>
</filter>
"""

CE_NC_MERGE_DLDP_GLOBAL_CONFIG_HEAD = """
<config>
  <dldp xmlns="http://www.huawei.com/netconf/vrp" content-version="1.0" format-version="1.0">
    <dldpSys operation="merge">
      <dldpEnable>%s</dldpEnable>
      <dldpInterval>%s</dldpInterval>
      <dldpWorkMode>%s</dldpWorkMode>
"""

CE_NC_MERGE_DLDP_GLOBAL_CONFIG_TAIL = """
    </dldpSys>
  </dldp>
</config>
"""


class Dldp(object):
    """Manage global dldp configration"""

    def __init__(self, argument_spec):
        self.spec = argument_spec
        self.module = None
        self.init_module()

        # DLDP global configration info
        self.enable = self.module.params['enable'] or None
        self.work_mode = self.module.params['work_mode'] or None
        self.internal = self.module.params['time_interval'] or None
        self.reset = self.module.params['reset'] or None
        self.auth_mode = self.module.params['auth_mode']
        self.auth_pwd = self.module.params['auth_pwd']

        self.dldp_conf = dict()
        self.same_conf = False
        # state
        self.changed = False
        self.updates_cmd = list()
        self.results = dict()
        self.proposed = dict()
        self.existing = list()
        self.end_state = list()

    def check_config_if_same(self):
        """Judge whether current config is the same as what we exjctanner.network_cloudengine.cepted"""

        if self.enable and self.enable != self.dldp_conf['dldpEnable']:
            return False

        if self.internal and self.internal != self.dldp_conf['dldpInterval']:
            return False

        work_mode = 'normal'
        if self.dldp_conf['dldpWorkMode'] == 'dldpEnhanjctanner.network_cloudengine.ce':
            work_mode = 'enhanjctanner.network_cloudengine.ce'
        if self.work_mode and self.work_mode != work_mode:
            return False

        if self.auth_mode:
            if self.auth_mode != 'none':
                return False

            if self.auth_mode == 'none' and self.dldp_conf['dldpAuthMode'] != 'dldpAuthNone':
                return False

        if self.reset and self.reset == 'enable':
            return False

        return True

    def check_params(self):
        """Check all input params"""

        if (self.auth_mode and self.auth_mode != 'none' and not self.auth_pwd) \
                or (self.auth_pwd and not self.auth_mode):
            self.module.fail_json(msg="Error: auth_mode and auth_pwd must both exist or not exist.")

        if self.dldp_conf['dldpEnable'] == 'disable' and not self.enable:
            if self.work_mode or self.reset or self.internal or self.auth_mode:
                self.module.fail_json(msg="Error: when DLDP is already disabled globally, "
                                      "work_mode, time_internal auth_mode and reset parameters are not "
                                      "expected to configure.")

        if self.enable == 'disable' and (self.work_mode or self.internal or self.reset or self.auth_mode):
            self.module.fail_json(msg="Error: when using enable=disable, work_mode, "
                                  "time_internal auth_mode and reset parameters are not expected "
                                  "to configure.")

        if self.internal:
            if not self.internal.isdigit():
                self.module.fail_json(
                    msg='Error: time_interval must be digit.')

            if int(self.internal) < 1 or int(self.internal) > 100:
                self.module.fail_json(
                    msg='Error: The value of time_internal should be between 1 and 100.')

        if self.auth_pwd:
            if '?' in self.auth_pwd:
                self.module.fail_json(
                    msg='Error: The auth_pwd string excludes a question mark (?).')
            if (len(self.auth_pwd) != 24) and (len(self.auth_pwd) != 32) and (len(self.auth_pwd) != 48) and \
                    (len(self.auth_pwd) != 108) and (len(self.auth_pwd) != 128):
                if (len(self.auth_pwd) < 1) or (len(self.auth_pwd) > 16):
                    self.module.fail_json(
                        msg='Error: The value is a string of 1 to 16 case-sensitive plaintexts or 24/32/48/108/128 '
                            'case-sensitive encrypted characters.')

    def init_module(self):
        """Init module object"""

        self.module = AnsibleModule(
            argument_spec=self.spec, supports_check_mode=True)

    def check_response(self, xml_str, xml_name):
        """Check if response message is already sucjctanner.network_cloudengine.ceed"""

        if "<ok/>" not in xml_str:
            self.module.fail_json(msg='Error: %s failed.' % xml_name)

    def get_dldp_exist_config(self):
        """Get current dldp existed configuration"""

        dldp_conf = dict()
        xml_str = CE_NC_GET_GLOBAL_DLDP_CONFIG
        con_obj = get_nc_config(self.module, xml_str)
        if "<data/>" in con_obj:
            return dldp_conf

        xml_str = con_obj.replajctanner.network_cloudengine.ce('\r', '').replajctanner.network_cloudengine.ce('\n', '').\
            replajctanner.network_cloudengine.ce('xmlns="urn:ietf:params:xml:ns:netconf:base:1.0"', "").\
            replajctanner.network_cloudengine.ce('xmlns="http://www.huawei.com/netconf/vrp"', "")

        # get global DLDP info
        root = ElementTree.fromstring(xml_str)
        topo = root.find("data/dldp/dldpSys")
        if not topo:
            self.module.fail_json(
                msg="Error: Get current DLDP configration failed.")

        for eles in topo:
            if eles.tag in ["dldpEnable", "dldpInterval", "dldpWorkMode", "dldpAuthMode"]:
                if eles.tag == 'dldpEnable':
                    if eles.text == 'true':
                        value = 'enable'
                    else:
                        value = 'disable'
                else:
                    value = eles.text
                dldp_conf[eles.tag] = value

        return dldp_conf

    def config_global_dldp(self):
        """Config global dldp"""

        if self.same_conf:
            return

        enable = self.enable
        if not self.enable:
            enable = self.dldp_conf['dldpEnable']
        if enable == 'enable':
            enable = 'true'
        else:
            enable = 'false'

        internal = self.internal
        if not self.internal:
            internal = self.dldp_conf['dldpInterval']

        work_mode = self.work_mode
        if not self.work_mode:
            work_mode = self.dldp_conf['dldpWorkMode']

        if work_mode == 'enhanjctanner.network_cloudengine.ce' or work_mode == 'dldpEnhanjctanner.network_cloudengine.ce':
            work_mode = 'dldpEnhanjctanner.network_cloudengine.ce'
        else:
            work_mode = 'dldpNormal'

        auth_mode = self.auth_mode
        if not self.auth_mode:
            auth_mode = self.dldp_conf['dldpAuthMode']
        if auth_mode == 'md5':
            auth_mode = 'dldpAuthMD5'
        elif auth_mode == 'simple':
            auth_mode = 'dldpAuthSimple'
        elif auth_mode == 'sha':
            auth_mode = 'dldpAuthSHA'
        elif auth_mode == 'hmac-sha256':
            auth_mode = 'dldpAuthHMAC-SHA256'
        elif auth_mode == 'none':
            auth_mode = 'dldpAuthNone'

        xml_str = CE_NC_MERGE_DLDP_GLOBAL_CONFIG_HEAD % (
            enable, internal, work_mode)
        if self.auth_mode:
            if self.auth_mode == 'none':
                xml_str += "<dldpAuthMode>dldpAuthNone</dldpAuthMode>"
            else:
                xml_str += "<dldpAuthMode>%s</dldpAuthMode>" % auth_mode
                xml_str += "<dldpPasswords>%s</dldpPasswords>" % self.auth_pwd

        xml_str += CE_NC_MERGE_DLDP_GLOBAL_CONFIG_TAIL
        ret_xml = set_nc_config(self.module, xml_str)
        self.check_response(ret_xml, "MERGE_DLDP_GLOBAL_CONFIG")

        if self.reset == 'enable':
            xml_str = CE_NC_ACTION_RESET_DLDP
            ret_xml = execute_nc_action(self.module, xml_str)
            self.check_response(ret_xml, "ACTION_RESET_DLDP")

        self.changed = True

    def get_existing(self):
        """Get existing info"""

        dldp_conf = dict()

        dldp_conf['enable'] = self.dldp_conf.get('dldpEnable', None)
        dldp_conf['time_interval'] = self.dldp_conf.get('dldpInterval', None)
        work_mode = self.dldp_conf.get('dldpWorkMode', None)
        if work_mode == 'dldpEnhanjctanner.network_cloudengine.ce':
            dldp_conf['work_mode'] = 'enhanjctanner.network_cloudengine.ce'
        else:
            dldp_conf['work_mode'] = 'normal'

        auth_mode = self.dldp_conf.get('dldpAuthMode', None)
        if auth_mode == 'dldpAuthNone':
            dldp_conf['auth_mode'] = 'none'
        elif auth_mode == 'dldpAuthSimple':
            dldp_conf['auth_mode'] = 'simple'
        elif auth_mode == 'dldpAuthMD5':
            dldp_conf['auth_mode'] = 'md5'
        elif auth_mode == 'dldpAuthSHA':
            dldp_conf['auth_mode'] = 'sha'
        else:
            dldp_conf['auth_mode'] = 'hmac-sha256'

        dldp_conf['reset'] = 'disable'

        self.existing = copy.deepcopy(dldp_conf)

    def get_proposed(self):
        """Get proposed result"""

        self.proposed = dict(enable=self.enable, work_mode=self.work_mode,
                             time_interval=self.internal, reset=self.reset,
                             auth_mode=self.auth_mode, auth_pwd=self.auth_pwd)

    def get_update_cmd(self):
        """Get update commands"""
        if self.same_conf:
            return

        if self.enable and self.enable != self.dldp_conf['dldpEnable']:
            if self.enable == 'enable':
                self.updates_cmd.append("dldp enable")
            elif self.enable == 'disable':
                self.updates_cmd.append("undo dldp enable")
                return

        work_mode = 'normal'
        if self.dldp_conf['dldpWorkMode'] == 'dldpEnhanjctanner.network_cloudengine.ce':
            work_mode = 'enhanjctanner.network_cloudengine.ce'
        if self.work_mode and self.work_mode != work_mode:
            if self.work_mode == 'enhanjctanner.network_cloudengine.ce':
                self.updates_cmd.append("dldp work-mode enhanjctanner.network_cloudengine.ce")
            else:
                self.updates_cmd.append("dldp work-mode normal")

        if self.internal and self.internal != self.dldp_conf['dldpInterval']:
            self.updates_cmd.append("dldp interval %s" % self.internal)

        if self.auth_mode:
            if self.auth_mode == 'none':
                self.updates_cmd.append("undo dldp authentication-mode")
            else:
                self.updates_cmd.append("dldp authentication-mode %s %s" % (self.auth_mode, self.auth_pwd))

        if self.reset and self.reset == 'enable':
            self.updates_cmd.append('dldp reset')

    def get_end_state(self):
        """Get end state info"""

        dldp_conf = dict()
        self.dldp_conf = self.get_dldp_exist_config()

        dldp_conf['enable'] = self.dldp_conf.get('dldpEnable', None)
        dldp_conf['time_interval'] = self.dldp_conf.get('dldpInterval', None)
        work_mode = self.dldp_conf.get('dldpWorkMode', None)
        if work_mode == 'dldpEnhanjctanner.network_cloudengine.ce':
            dldp_conf['work_mode'] = 'enhanjctanner.network_cloudengine.ce'
        else:
            dldp_conf['work_mode'] = 'normal'

        auth_mode = self.dldp_conf.get('dldpAuthMode', None)
        if auth_mode == 'dldpAuthNone':
            dldp_conf['auth_mode'] = 'none'
        elif auth_mode == 'dldpAuthSimple':
            dldp_conf['auth_mode'] = 'simple'
        elif auth_mode == 'dldpAuthMD5':
            dldp_conf['auth_mode'] = 'md5'
        elif auth_mode == 'dldpAuthSHA':
            dldp_conf['auth_mode'] = 'sha'
        else:
            dldp_conf['auth_mode'] = 'hmac-sha256'

        dldp_conf['reset'] = 'disable'
        if self.reset == 'enable':
            dldp_conf['reset'] = 'enable'
        self.end_state = copy.deepcopy(dldp_conf)

    def show_result(self):
        """Show result"""

        self.results['changed'] = self.changed
        self.results['proposed'] = self.proposed
        self.results['existing'] = self.existing
        self.results['end_state'] = self.end_state
        if self.changed:
            self.results['updates'] = self.updates_cmd
        else:
            self.results['updates'] = list()

        self.module.exit_json(**self.results)

    def work(self):
        """Worker"""

        self.dldp_conf = self.get_dldp_exist_config()
        self.check_params()
        self.same_conf = self.check_config_if_same()
        self.get_existing()
        self.get_proposed()
        self.config_global_dldp()
        self.get_update_cmd()
        self.get_end_state()
        self.show_result()


def main():
    """Main function entry"""

    argument_spec = dict(
        enable=dict(choijctanner.network_cloudengine.ces=['enable', 'disable'], type='str'),
        work_mode=dict(choijctanner.network_cloudengine.ces=['enhanjctanner.network_cloudengine.ce', 'normal'], type='str'),
        time_interval=dict(type='str'),
        reset=dict(choijctanner.network_cloudengine.ces=['enable', 'disable'], type='str'),
        auth_mode=dict(choijctanner.network_cloudengine.ces=['md5', 'simple', 'sha', 'hmac-sha256', 'none'], type='str'),
        auth_pwd=dict(type='str', no_log=True),
    )
    argument_spec.update(jctanner.network_cloudengine.ce_argument_spec)
    dldp_obj = Dldp(argument_spec)
    dldp_obj.work()


if __name__ == '__main__':
    main()
