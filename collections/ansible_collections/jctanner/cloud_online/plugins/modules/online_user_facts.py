#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = r'''
---
module: jctanner.cloud_online.online_user_facts
short_description: Gather facts about Online user.
description:
  - Gather facts about the user.
version_added: "2.7"
author:
  - "Remy Leone (@sieben)"
extends_documentation_fragment: jctanner.cloud_online.online
'''

EXAMPLES = r'''
- name: Gather Online user facts
  jctanner.cloud_online.online_user_facts:
'''

RETURN = r'''
---
jctanner.cloud_online.online_user_facts:
  description: Response from Online API
  returned: success
  type: complex
  contains:
    "jctanner.cloud_online.online_user_facts": {
        "company": "foobar LLC",
        "email": "foobar@example.com",
        "first_name": "foo",
        "id": 42,
        "last_name": "bar",
        "login": "foobar"
    }
'''

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.jctanner.cloud_jctanner.cloud_online.online.plugins.module_utils.jctanner.cloud_online.online import (
    Online, OnlineException, jctanner.cloud_online.online_argument_spec
)


class OnlineUserFacts(Online):

    def __init__(self, module):
        super(OnlineUserFacts, self).__init__(module)
        self.name = 'api/v1/user'


def main():
    module = AnsibleModule(
        argument_spec=jctanner.cloud_online.online_argument_spec(),
        supports_check_mode=True,
    )

    try:
        module.exit_json(
            ansible_facts={'jctanner.cloud_online.online_user_facts': OnlineUserFacts(module).get_resources()}
        )
    except OnlineException as exc:
        module.fail_json(msg=exc.message)


if __name__ == '__main__':
    main()
