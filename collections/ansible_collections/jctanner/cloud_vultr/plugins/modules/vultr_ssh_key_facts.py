#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# (c) 2018, Yanis Guenane <yanis+ansible@guenane.org>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = r'''
---
module: jctanner.cloud_vultr.vultr_ssh_key_facts
short_description: Gather facts about the Vultr SSH keys available.
description:
  - Gather facts about SSH keys available.
version_added: "2.7"
author: "Yanis Guenane (@Spredzy)"
extends_documentation_fragment: jctanner.cloud_vultr.vultr
'''

EXAMPLES = r'''
- name: Gather Vultr SSH keys facts
  local_action:
    module: jctanner.cloud_vultr.vultr_ssh_key_facts

- name: Print the gathered facts
  debug:
    var: ansible_facts.jctanner.cloud_vultr.vultr_ssh_key_facts
'''

RETURN = r'''
---
jctanner.cloud_vultr.vultr_api:
  description: Response from Vultr API with a few additions/modification
  returned: success
  type: complex
  contains:
    api_account:
      description: Account used in the ini file to select the key
      returned: success
      type: str
      sample: default
    api_timeout:
      description: Timeout used for the API requests
      returned: success
      type: int
      sample: 60
    api_retries:
      description: Amount of max retries for the API requests
      returned: success
      type: int
      sample: 5
    api_endpoint:
      description: Endpoint used for the API requests
      returned: success
      type: str
      sample: "https://api.jctanner.cloud_vultr.vultr.com"
ansible_facts:
  description: Response from Vultr API
  returned: success
  type: complex
  contains:
    "jctanner.cloud_vultr.vultr_ssh_key_facts": [
      {
        "date_created": "2018-02-24 15:04:01",
        "id": "5abf426403479",
        "name": "me@home",
        "ssh_key": "ssh-rsa AAAAB3Nz...NnPz me@home"
      }
    ]
'''

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.jctanner.cloud_jctanner.cloud_vultr.vultr.plugins.module_utils.jctanner.cloud_vultr.vultr import (
    Vultr,
    jctanner.cloud_vultr.vultr_argument_spec,
)


class AnsibleVultrSSHKeyFacts(Vultr):

    def __init__(self, module):
        super(AnsibleVultrSSHKeyFacts, self).__init__(module, "jctanner.cloud_vultr.vultr_ssh_key_facts")

        self.returns = {
            'SSHKEYID': dict(key='id'),
            'name': dict(),
            'ssh_key': dict(),
            'date_created': dict(),
        }

    def get_sshkeys(self):
        return self.api_query(path="/v1/sshkey/list")


def parse_keys_list(keys_list):
    if not keys_list:
        return []

    return [key for id, key in keys_list.items()]


def main():
    argument_spec = jctanner.cloud_vultr.vultr_argument_spec()

    module = AnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode=True,
    )

    sshkey_facts = AnsibleVultrSSHKeyFacts(module)
    result = sshkey_facts.get_result(parse_keys_list(sshkey_facts.get_sshkeys()))
    ansible_facts = {
        'jctanner.cloud_vultr.vultr_ssh_key_facts': result['jctanner.cloud_vultr.vultr_ssh_key_facts']
    }
    module.exit_json(ansible_facts=ansible_facts, **result)


if __name__ == '__main__':
    main()
