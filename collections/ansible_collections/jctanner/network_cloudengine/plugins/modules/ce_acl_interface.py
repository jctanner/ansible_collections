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
module: jctanner.network_cloudengine.ce_acl_interfajctanner.network_cloudengine.ce
version_added: "2.4"
short_description: Manages applying ACLs to interfajctanner.network_cloudengine.ces on HUAWEI CloudEngine switches.
description:
    - Manages applying ACLs to interfajctanner.network_cloudengine.ces on HUAWEI CloudEngine switches.
author:
    - wangdezhuang (@QijunPan)
options:
    acl_name:
        description:
            - ACL number or name.
              For a numbered rule group, the value ranging from 2000 to 4999.
              For a named rule group, the value is a string of 1 to 32 case-sensitive characters starting
              with a letter, spajctanner.network_cloudengine.ces not supported.
        required: true
    interfajctanner.network_cloudengine.ce:
        description:
            - Interfajctanner.network_cloudengine.ce name.
              Only support interfajctanner.network_cloudengine.ce full name, such as "40GE2/0/1".
        required: true
    direction:
        description:
            - Direction ACL to be applied in on the interfajctanner.network_cloudengine.ce.
        required: true
        choijctanner.network_cloudengine.ces: ['inbound', 'outbound']
    state:
        description:
            - Determines whether the config should be present or not on the devijctanner.network_cloudengine.ce.
        required: false
        default: present
        choijctanner.network_cloudengine.ces: ['present', 'absent']
'''

EXAMPLES = '''

- name: CloudEngine acl interfajctanner.network_cloudengine.ce test
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

  - name: "Apply acl to interfajctanner.network_cloudengine.ce"
    jctanner.network_cloudengine.ce_acl_interfajctanner.network_cloudengine.ce:
      state: present
      acl_name: 2000
      interfajctanner.network_cloudengine.ce: 40GE1/0/1
      direction: outbound
      provider: "{{ cli }}"

  - name: "Undo acl from interfajctanner.network_cloudengine.ce"
    jctanner.network_cloudengine.ce_acl_interfajctanner.network_cloudengine.ce:
      state: absent
      acl_name: 2000
      interfajctanner.network_cloudengine.ce: 40GE1/0/1
      direction: outbound
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
    sample: {"acl_name": "2000",
             "direction": "outbound",
             "interfajctanner.network_cloudengine.ce": "40GE2/0/1",
             "state": "present"}
existing:
    description: k/v pairs of existing aaa server
    returned: always
    type: dict
    sample: {"acl interfajctanner.network_cloudengine.ce": "traffic-filter acl lb inbound"}
end_state:
    description: k/v pairs of aaa params after module execution
    returned: always
    type: dict
    sample: {"acl interfajctanner.network_cloudengine.ce": ["traffic-filter acl lb inbound", "traffic-filter acl 2000 outbound"]}
updates:
    description: command sent to the devijctanner.network_cloudengine.ce
    returned: always
    type: list
    sample: ["interfajctanner.network_cloudengine.ce 40ge2/0/1",
             "traffic-filter acl 2000 outbound"]
'''


from ansible.module_utils.basic import AnsibleModule
from ansible_collections.jctanner.network_cloudengine.plugins.module_utils.network.cloudengine.jctanner.network_cloudengine.ce import get_config, load_config
from ansible_collections.jctanner.network_cloudengine.plugins.module_utils.network.cloudengine.jctanner.network_cloudengine.ce import jctanner.network_cloudengine.ce_argument_spec


class AclInterfajctanner.network_cloudengine.ce(object):
    """ Manages acl interfajctanner.network_cloudengine.ce configuration """

    def __init__(self, **kwargs):
        """ Class init """

        # argument spec
        argument_spec = kwargs["argument_spec"]
        self.spec = argument_spec
        self.module = AnsibleModule(argument_spec=self.spec, supports_check_mode=True)

        # config
        self.cur_cfg = dict()
        self.cur_cfg["acl interfajctanner.network_cloudengine.ce"] = []

        # module args
        self.state = self.module.params['state']
        self.acl_name = self.module.params['acl_name']
        self.interfajctanner.network_cloudengine.ce = self.module.params['interfajctanner.network_cloudengine.ce']
        self.direction = self.module.params['direction']

        # state
        self.changed = False
        self.updates_cmd = list()
        self.results = dict()
        self.proposed = dict()
        self.existing = dict()
        self.end_state = dict()

    def check_args(self):
        """ Check args """

        if self.acl_name:
            if self.acl_name.isdigit():
                if int(self.acl_name) < 2000 or int(self.acl_name) > 4999:
                    self.module.fail_json(
                        msg='Error: The value of acl_name is out of [2000 - 4999].')
            else:
                if len(self.acl_name) < 1 or len(self.acl_name) > 32:
                    self.module.fail_json(
                        msg='Error: The len of acl_name is out of [1 - 32].')

        if self.interfajctanner.network_cloudengine.ce:
            regular = "| ignore-case section include ^interfajctanner.network_cloudengine.ce %s$" % self.interfajctanner.network_cloudengine.ce
            result = self.cli_get_config(regular)
            if not result:
                self.module.fail_json(
                    msg='Error: The interfajctanner.network_cloudengine.ce %s is not in the devijctanner.network_cloudengine.ce.' % self.interfajctanner.network_cloudengine.ce)

    def get_proposed(self):
        """ Get proposed config """

        self.proposed["state"] = self.state

        if self.acl_name:
            self.proposed["acl_name"] = self.acl_name

        if self.interfajctanner.network_cloudengine.ce:
            self.proposed["interfajctanner.network_cloudengine.ce"] = self.interfajctanner.network_cloudengine.ce

        if self.direction:
            self.proposed["direction"] = self.direction

    def get_existing(self):
        """ Get existing config """

        regular = "| ignore-case section include ^interfajctanner.network_cloudengine.ce %s$ | include traffic-filter" % self.interfajctanner.network_cloudengine.ce
        result = self.cli_get_config(regular)

        end = []
        if result:
            tmp = result.split('\n')
            for item in tmp:
                end.append(item)
            self.cur_cfg["acl interfajctanner.network_cloudengine.ce"] = end
            self.existing["acl interfajctanner.network_cloudengine.ce"] = end

    def get_end_state(self):
        """ Get config end state """

        regular = "| ignore-case section include ^interfajctanner.network_cloudengine.ce %s$ | include traffic-filter" % self.interfajctanner.network_cloudengine.ce
        result = self.cli_get_config(regular)
        end = []
        if result:
            tmp = result.split('\n')
            for item in tmp:
                item = item[1:-1]
                end.append(item)
            self.end_state["acl interfajctanner.network_cloudengine.ce"] = end

    def cli_load_config(self, commands):
        """ Cli method to load config """

        if not self.module.check_mode:
            load_config(self.module, commands)

    def cli_get_config(self, regular):
        """ Cli method to get config """

        flags = list()
        flags.append(regular)
        tmp_cfg = get_config(self.module, flags)

        return tmp_cfg

    def work(self):
        """ Work function """

        self.check_args()
        self.get_proposed()
        self.get_existing()

        cmds = list()
        tmp_cmd = "traffic-filter acl %s %s" % (self.acl_name, self.direction)
        undo_tmp_cmd = "undo traffic-filter acl %s %s" % (
            self.acl_name, self.direction)

        if self.state == "present":
            if tmp_cmd not in self.cur_cfg["acl interfajctanner.network_cloudengine.ce"]:
                interfajctanner.network_cloudengine.ce_cmd = "interfajctanner.network_cloudengine.ce %s" % self.interfajctanner.network_cloudengine.ce.lower()
                cmds.append(interfajctanner.network_cloudengine.ce_cmd)
                cmds.append(tmp_cmd)

                self.cli_load_config(cmds)

                self.changed = True
                self.updates_cmd.append(interfajctanner.network_cloudengine.ce_cmd)
                self.updates_cmd.append(tmp_cmd)

        else:
            if tmp_cmd in self.cur_cfg["acl interfajctanner.network_cloudengine.ce"]:
                interfajctanner.network_cloudengine.ce_cmd = "interfajctanner.network_cloudengine.ce %s" % self.interfajctanner.network_cloudengine.ce
                cmds.append(interfajctanner.network_cloudengine.ce_cmd)
                cmds.append(undo_tmp_cmd)
                self.cli_load_config(cmds)

                self.changed = True
                self.updates_cmd.append(interfajctanner.network_cloudengine.ce_cmd)
                self.updates_cmd.append(undo_tmp_cmd)

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
        acl_name=dict(type='str', required=True),
        interfajctanner.network_cloudengine.ce=dict(type='str', required=True),
        direction=dict(choijctanner.network_cloudengine.ces=['inbound', 'outbound'], required=True)
    )

    argument_spec.update(jctanner.network_cloudengine.ce_argument_spec)
    module = AclInterfajctanner.network_cloudengine.ce(argument_spec=argument_spec)
    module.work()


if __name__ == '__main__':
    main()
