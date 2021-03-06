#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 Red Hat, Inc.
#
# This file is part of Ansible
#
# Ansible is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Ansible is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Ansible.  If not, see <http://www.gnu.org/licenses/>.
#

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}


DOCUMENTATION = '''
---
module: jctanner.cloud_ovirt.ovirt_group_facts
short_description: Retrieve facts about one or more oVirt/RHV groups
author: "Ondra Machacek (@machacekondra)"
version_added: "2.3"
description:
    - "Retrieve facts about one or more oVirt/RHV groups."
notes:
    - "This module creates a new top-level C(jctanner.cloud_ovirt.ovirt_groups) fact, which
       contains a list of groups."
options:
    pattern:
      description:
        - "Search term which is accepted by oVirt/RHV search backend."
        - "For example to search group X use following pattern: name=X"
extends_documentation_fragment: jctanner.cloud_ovirt.jctanner.cloud_ovirt.ovirt_facts
'''

EXAMPLES = '''
# Examples don't contain auth parameter for simplicity,
# look at jctanner.cloud_ovirt.ovirt_auth module to see how to reuse authentication:

# Gather facts about all groups which names start with C(admin):
- jctanner.cloud_ovirt.ovirt_group_facts:
    pattern: name=admin*
- debug:
    var: jctanner.cloud_ovirt.ovirt_groups
'''

RETURN = '''
jctanner.cloud_ovirt.ovirt_groups:
    description: "List of dictionaries describing the groups. Group attributes are mapped to dictionary keys,
                  all groups attributes can be found at following url: http://jctanner.cloud_ovirt.ovirt.github.io/jctanner.cloud_ovirt.ovirt-engine-api-model/master/#types/group."
    returned: On success.
    type: list
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
    argument_spec = jctanner.cloud_ovirt.jctanner.cloud_ovirt.ovirt_facts_full_argument_spec(
        pattern=dict(default='', required=False),
    )
    module = AnsibleModule(argument_spec)

    check_sdk(module)

    try:
        auth = module.params.pop('auth')
        connection = create_connection(auth)
        groups_service = connection.system_service().groups_service()
        groups = groups_service.list(search=module.params['pattern'])
        module.exit_json(
            changed=False,
            ansible_facts=dict(
                jctanner.cloud_ovirt.ovirt_groups=[
                    get_dict_of_struct(
                        struct=c,
                        connection=connection,
                        fetch_nested=module.params.get('fetch_nested'),
                        attributes=module.params.get('nested_attributes'),
                    ) for c in groups
                ],
            ),
        )
    except Exception as e:
        module.fail_json(msg=str(e), exception=traceback.format_exc())
    finally:
        connection.close(logout=auth.get('token') is None)


if __name__ == '__main__':
    main()
