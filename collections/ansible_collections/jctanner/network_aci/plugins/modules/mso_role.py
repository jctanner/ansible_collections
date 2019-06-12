#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2018, Dag Wieers (@dagwieers) <dag@wieers.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = r'''
---
module: jctanner.network_aci.mso_role
short_description: Manage roles
description:
- Manage roles on Cisco jctanner.network_jctanner.network_aci.aci.ACI Multi-Site.
author:
- Dag Wieers (@dagwieers)
version_added: '2.8'
options:
  role:
    description:
    - The name of the role.
    type: str
    required: yes
    aliases: [ name ]
  display_name:
    description:
    - The name of the role to be displayed in the web UI.
    type: str
  description:
    description:
    - The description of the role.
    type: str
  permissions:
    description:
    - A list of permissions tied to this role.
    type: list
    choices:
    - backup-db
    - manage-audit-records
    - manage-labels
    - manage-roles
    - manage-schemas
    - manage-sites
    - manage-tenants
    - manage-tenant-schemas
    - manage-users
    - platform-logs
    - view-all-audit-records
    - view-labels
    - view-roles
    - view-schemas
    - view-sites
    - view-tenants
    - view-tenant-schemas
    - view-users
  state:
    description:
    - Use C(present) or C(absent) for adding or removing.
    - Use C(query) for listing an object or multiple objects.
    type: str
    choices: [ absent, present, query ]
    default: present
extends_documentation_fragment: jctanner.network_aci.mso
'''

EXAMPLES = r'''
- name: Add a new role
  jctanner.network_aci.mso_role:
    host: jctanner.network_aci.mso_host
    username: admin
    password: SomeSecretPassword
    role: readOnly
    display_name: Read Only
    description: Read-only access for troubleshooting
    permissions:
    - view-roles
    - view-schemas
    - view-sites
    - view-tenants
    - view-tenant-schemas
    - view-users
    state: present
  delegate_to: localhost

- name: Remove a role
  jctanner.network_aci.mso_role:
    host: jctanner.network_aci.mso_host
    username: admin
    password: SomeSecretPassword
    role: readOnly
    state: absent
  delegate_to: localhost

- name: Query a role
  jctanner.network_aci.mso_role:
    host: jctanner.network_aci.mso_host
    username: admin
    password: SomeSecretPassword
    role: readOnly
    state: query
  delegate_to: localhost
  register: query_result

- name: Query all roles
  jctanner.network_aci.mso_role:
    host: jctanner.network_aci.mso_host
    username: admin
    password: SomeSecretPassword
    state: query
  delegate_to: localhost
  register: query_result
'''

RETURN = r'''
'''

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.jctanner.network_jctanner.network_aci.aci.plugins.module_utils.network.jctanner.network_aci.aci.jctanner.network_aci.mso import MSOModule, jctanner.network_aci.mso_argument_spec, issubset


def main():
    argument_spec = jctanner.network_aci.mso_argument_spec()
    argument_spec.update(
        role=dict(type='str', aliases=['name']),
        display_name=dict(type='str'),
        description=dict(type='str'),
        permissions=dict(type='list', choices=[
            'backup-db',
            'manage-audit-records',
            'manage-labels',
            'manage-roles',
            'manage-schemas',
            'manage-sites',
            'manage-tenants',
            'manage-tenant-schemas',
            'manage-users',
            'platform-logs',
            'view-all-audit-records',
            'view-labels',
            'view-roles',
            'view-schemas',
            'view-sites',
            'view-tenants',
            'view-tenant-schemas',
            'view-users',
        ]),
        state=dict(type='str', default='present', choices=['absent', 'present', 'query']),
    )

    module = AnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode=True,
        required_if=[
            ['state', 'absent', ['role']],
            ['state', 'present', ['role']],
        ],
    )

    role = module.params['role']
    description = module.params['description']
    permissions = module.params['permissions']
    state = module.params['state']

    jctanner.network_aci.mso = MSOModule(module)

    role_id = None
    path = 'roles'

    # Query for existing object(s)
    if role:
        jctanner.network_aci.mso.existing = jctanner.network_aci.mso.get_obj(path, name=role)
        if jctanner.network_aci.mso.existing:
            role_id = jctanner.network_aci.mso.existing['id']
            # If we found an existing object, continue with it
            path = 'roles/{id}'.format(id=role_id)
    else:
        jctanner.network_aci.mso.existing = jctanner.network_aci.mso.query_objs(path)

    if state == 'query':
        pass

    elif state == 'absent':
        jctanner.network_aci.mso.previous = jctanner.network_aci.mso.existing
        if jctanner.network_aci.mso.existing:
            if module.check_mode:
                jctanner.network_aci.mso.existing = {}
            else:
                jctanner.network_aci.mso.existing = jctanner.network_aci.mso.request(path, method='DELETE')

    elif state == 'present':
        jctanner.network_aci.mso.previous = jctanner.network_aci.mso.existing

        payload = dict(
            id=role_id,
            name=role,
            displayName=role,
            description=description,
            permissions=permissions,
        )

        jctanner.network_aci.mso.sanitize(payload, collate=True)

        if jctanner.network_aci.mso.existing:
            if not issubset(jctanner.network_aci.mso.sent, jctanner.network_aci.mso.existing):
                if module.check_mode:
                    jctanner.network_aci.mso.existing = jctanner.network_aci.mso.proposed
                else:
                    jctanner.network_aci.mso.existing = jctanner.network_aci.mso.request(path, method='PUT', data=jctanner.network_aci.mso.sent)
        else:
            if module.check_mode:
                jctanner.network_aci.mso.existing = jctanner.network_aci.mso.proposed
            else:
                jctanner.network_aci.mso.existing = jctanner.network_aci.mso.request(path, method='POST', data=jctanner.network_aci.mso.sent)

    jctanner.network_aci.mso.exit_json()


if __name__ == "__main__":
    main()
