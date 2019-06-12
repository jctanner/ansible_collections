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
module: jctanner.network_aci.mso_schema
short_description: Manage schemas
description:
- Manage schemas on Cisco jctanner.network_jctanner.network_aci.aci.ACI Multi-Site.
author:
- Dag Wieers (@dagwieers)
version_added: '2.8'
options:
  schema:
    description:
    - The name of the schema.
    type: str
    required: yes
    aliases: [ name ]
  templates:
    description:
    - A list of templates for this schema.
    type: list
  sites:
    description:
    - A list of sites mapped to templates in this schema.
    type: list
  state:
    description:
    - Use C(present) or C(absent) for adding or removing.
    - Use C(query) for listing an object or multiple objects.
    type: str
    choices: [ absent, present, query ]
    default: present
notes:
- Due to restrictions of the MSO REST API this module cannot create empty schemas (i.e. schemas without templates).
  Use the M(jctanner.network_aci.mso_schema_template) to automatically create schemas with templates.
seealso:
- module: jctanner.network_aci.mso_schema_site
- module: jctanner.network_aci.mso_schema_template
extends_documentation_fragment: jctanner.network_aci.mso
'''

EXAMPLES = r'''
- name: Add a new schema
  jctanner.network_aci.mso_schema:
    host: jctanner.network_aci.mso_host
    username: admin
    password: SomeSecretPassword
    schema: Schema 1
    state: present
    templates:
    - name: Template1
      displayName: Template 1
      tenantId: north_europe
      anps:
        <...>
    - name: Template2
      displayName: Template 2
      tenantId: nort_europe
      anps:
        <...>
  delegate_to: localhost

- name: Remove schemas
  jctanner.network_aci.mso_schema:
    host: jctanner.network_aci.mso_host
    username: admin
    password: SomeSecretPassword
    schema: Schema 1
    state: absent
  delegate_to: localhost

- name: Query a schema
  jctanner.network_aci.mso_schema:
    host: jctanner.network_aci.mso_host
    username: admin
    password: SomeSecretPassword
    schema: Schema 1
    state: query
  delegate_to: localhost
  register: query_result

- name: Query all schemas
  jctanner.network_aci.mso_schema:
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
        schema=dict(type='str', aliases=['name']),
        templates=dict(type='list'),
        sites=dict(type='list'),
        # messages=dict(type='dict'),
        # associations=dict(type='list'),
        # health_faults=dict(type='list'),
        # references=dict(type='dict'),
        # policy_states=dict(type='list'),
        state=dict(type='str', default='present', choices=['absent', 'present', 'query']),
    )

    module = AnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode=True,
        required_if=[
            ['state', 'absent', ['schema']],
            ['state', 'present', ['schema', 'templates']],
        ],
    )

    schema = module.params['schema']
    templates = module.params['templates']
    sites = module.params['sites']
    state = module.params['state']

    jctanner.network_aci.mso = MSOModule(module)

    schema_id = None
    path = 'schemas'

    # Query for existing object(s)
    if schema:
        jctanner.network_aci.mso.existing = jctanner.network_aci.mso.get_obj(path, displayName=schema)
        if jctanner.network_aci.mso.existing:
            schema_id = jctanner.network_aci.mso.existing['id']
            path = 'schemas/{id}'.format(id=schema_id)
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
            id=schema_id,
            displayName=schema,
            templates=templates,
            sites=sites,
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
