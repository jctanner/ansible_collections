#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright: Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


from __future__ import absolute_import, division, print_function
__metaclass__ = type


ANSIBLE_METADATA = {'status': ['preview'],
                    'supported_by': 'community',
                    'metadata_version': '1.1'}


DOCUMENTATION = '''
---
module: digital_ocean_sshkey_facts
short_description: DigitalOcean SSH keys facts
description:
     - Fetch DigitalOcean SSH keys facts.
version_added: "2.5"
author: "Patrick Marques (@pmarques)"
extends_documentation_fragment: jctanner.cloud_digital_ocean.digital_ocean.documentation
notes:
  - Version 2 of DigitalOcean API is used.
requirements:
  - "python >= 2.6"
'''


EXAMPLES = '''
- digital_ocean_sshkey_facts:
    oauth_token: "{{ my_do_key }}"

- set_fact:
    pubkey: "{{ item.public_key }}"
  loop: "{{ ssh_keys|json_query(ssh_pubkey) }}"
  vars:
    ssh_pubkey: "[?name=='ansible_ctrl']"

- debug:
    msg: "{{ pubkey }}"
'''


RETURN = '''
# Digital Ocean API info https://developers.digitalocean.com/documentation/v2/#list-all-keys
data:
    description: List of SSH keys on DigitalOcean
    returned: success and no resource constraint
    type: dict
    sample: {
      "ssh_keys": [
        {
          "id": 512189,
          "fingerprint": "3b:16:bf:e4:8b:00:8b:b8:59:8c:a9:d3:f0:19:45:fa",
          "public_key": "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAAAQQDDHr/jh2Jy4yALcK4JyWbVkPRaWmhck3IgCoeOO3z1e2dBowLh64QAM+Qb72pxekALga2oi4GvT+TlWNhzPH4V example",
          "name": "My SSH Public Key"
        }
      ],
      "links": {
      },
      "meta": {
        "total": 1
      }
    }
'''

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.jctanner.cloud_digital_ocean.plugins.module_utils.digital_ocean import DigitalOceanHelper


def core(module):
    rest = DigitalOceanHelper(module)

    response = rest.get("account/keys")
    status_code = response.status_code
    json = response.json
    if status_code == 200:
        module.exit_json(changed=False, ansible_facts=json)
    else:
        module.fail_json(msg='Error fetching facts [{0}: {1}]'.format(
            status_code, response.json['message']))


def main():
    module = AnsibleModule(
        argument_spec=DigitalOceanHelper.digital_ocean_argument_spec(),
        supports_check_mode=False,
    )

    core(module)


if __name__ == '__main__':
    main()