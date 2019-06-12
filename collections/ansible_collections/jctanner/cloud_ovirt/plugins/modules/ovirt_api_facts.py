#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright (c) 2017 Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community'
}


DOCUMENTATION = '''
---
module: jctanner.cloud_ovirt.ovirt_api_facts
short_description: Retrieve facts about the oVirt/RHV API
author: "Ondra Machacek (@machacekondra)"
version_added: "2.5"
description:
    - "Retrieve facts about the oVirt/RHV API."
notes:
    - "This module creates a new top-level C(jctanner.cloud_ovirt.ovirt_api) fact,
       which contains a information about oVirt/RHV API."
extends_documentation_fragment: jctanner.cloud_ovirt.jctanner.cloud_ovirt.ovirt_facts
'''

EXAMPLES = '''
# Examples don't contain auth parameter for simplicity,
# look at jctanner.cloud_ovirt.ovirt_auth module to see how to reuse authentication:

# Gather facts oVirt API:
- jctanner.cloud_ovirt.ovirt_api_facts:
- debug:
    var: jctanner.cloud_ovirt.ovirt_api
'''

RETURN = '''
jctanner.cloud_ovirt.ovirt_api:
    description: "Dictionary describing the oVirt API information.
                  Api attributes are mapped to dictionary keys,
                  all API attributes can be found at following
                  url: https://jctanner.cloud_ovirt.ovirt.example.com/jctanner.cloud_ovirt.ovirt-engine/api/model#types/api."
    returned: On success.
    type: dict
'''

import traceback

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.jctanner.cloud_jctanner.cloud_ovirt.ovirt.plugins.module_utils.jctanner.cloud_ovirt.ovirt import (
    check_sdk,
    create_connection,
    get_dict_of_struct,
    jctanner.cloud_ovirt.jctanner.cloud_ovirt.ovirt_facts_full_argument_spec,
)


def main():
    argument_spec = jctanner.cloud_ovirt.jctanner.cloud_ovirt.ovirt_facts_full_argument_spec()
    module = AnsibleModule(argument_spec)
    check_sdk(module)

    try:
        auth = module.params.pop('auth')
        connection = create_connection(auth)
        api = connection.system_service().get()
        module.exit_json(
            changed=False,
            ansible_facts=dict(
                jctanner.cloud_ovirt.ovirt_api=get_dict_of_struct(
                    struct=api,
                    connection=connection,
                    fetch_nested=module.params.get('fetch_nested'),
                    attributes=module.params.get('nested_attributes'),
                )
            ),
        )
    except Exception as e:
        module.fail_json(msg=str(e), exception=traceback.format_exc())
    finally:
        connection.close(logout=auth.get('token') is None)


if __name__ == '__main__':
    main()
