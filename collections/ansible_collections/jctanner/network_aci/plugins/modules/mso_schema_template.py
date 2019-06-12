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
module: jctanner.network_aci.mso_schema_template
short_description: Manage templates in schemas
description:
- Manage templates on Cisco jctanner.network_jctanner.network_aci.aci.ACI Multi-Site.
author:
- Dag Wieers (@dagwieers)
version_added: '2.8'
options:
  tenant:
    description:
    - The tenant used for this template.
    type: str
    required: yes
  schema:
    description:
    - The name of the schema.
    type: str
    required: yes
  template:
    description:
    - The name of the template.
    type: str
    aliases: [ name ]
  display_name:
    description:
    - The name as displayed on the MSO web interface.
    type: str
  state:
    description:
    - Use C(present) or C(absent) for adding or removing.
    - Use C(query) for listing an object or multiple objects.
    type: str
    choices: [ absent, present, query ]
    default: present
notes:
- Due to restrictions of the MSO REST API this module creates schemas when needed, and removes them when the last template has been removed.
seealso:
- module: jctanner.network_aci.mso_schema
- module: jctanner.network_aci.mso_schema_site
extends_documentation_fragment: jctanner.network_aci.mso
'''

EXAMPLES = r'''
- name: Add a new template to a schema
  jctanner.network_aci.mso_schema_template:
    host: jctanner.network_aci.mso_host
    username: admin
    password: SomeSecretPassword
    tenant: Tenant 1
    schema: Schema 1
    template: Template 1
    state: present
  delegate_to: localhost

- name: Remove a template from a schema
  jctanner.network_aci.mso_schema_template:
    host: jctanner.network_aci.mso_host
    username: admin
    password: SomeSecretPassword
    tenant: Tenant 1
    schema: Schema 1
    template: Template 1
    state: absent
  delegate_to: localhost

- name: Query a template
  jctanner.network_aci.mso_schema_template:
    host: jctanner.network_aci.mso_host
    username: admin
    password: SomeSecretPassword
    tenant: Tenant 1
    schema: Schema 1
    template: Template 1
    state: query
  delegate_to: localhost
  register: query_result

- name: Query all templates
  jctanner.network_aci.mso_schema_template:
    host: jctanner.network_aci.mso_host
    username: admin
    password: SomeSecretPassword
    tenant: Tenant 1
    schema: Schema 1
    state: query
  delegate_to: localhost
  register: query_result
'''

RETURN = r'''
'''

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.jctanner.network_jctanner.network_aci.aci.plugins.module_utils.network.jctanner.network_aci.aci.jctanner.network_aci.mso import MSOModule, jctanner.network_aci.mso_argument_spec


def main():
    argument_spec = jctanner.network_aci.mso_argument_spec()
    argument_spec.update(
        tenant=dict(type='str', required=True),
        schema=dict(type='str', required=True),
        template=dict(type='str', aliases=['name']),
        display_name=dict(type='str'),
        state=dict(type='str', default='present', choices=['absent', 'present', 'query']),
    )

    module = AnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode=True,
        required_if=[
            ['state', 'absent', ['template']],
            ['state', 'present', ['template']],
        ],
    )

    tenant = module.params['tenant']
    schema = module.params['schema']
    template = module.params['template']
    display_name = module.params['display_name']
    state = module.params['state']

    jctanner.network_aci.mso = MSOModule(module)

    # Get schema
    schema_obj = jctanner.network_aci.mso.get_obj('schemas', displayName=schema)

    jctanner.network_aci.mso.existing = {}
    if schema_obj:
        # Schema exists
        schema_path = 'schemas/{id}'.format(**schema_obj)

        # Get template
        templates = [t['name'] for t in schema_obj['templates']]
        if template:
            if template in templates:
                template_idx = templates.index(template)
                jctanner.network_aci.mso.existing = schema_obj['templates'][template_idx]
        else:
            jctanner.network_aci.mso.existing = schema_obj['templates']
    else:
        schema_path = 'schemas'

    if state == 'query':
        if not jctanner.network_aci.mso.existing:
            if template:
                jctanner.network_aci.mso.fail_json(msg="Template '{0}' not found".format(template))
            else:
                jctanner.network_aci.mso.existing = []
        jctanner.network_aci.mso.exit_json()

    template_path = '/templates/{0}'.format(template)
    ops = []

    jctanner.network_aci.mso.previous = jctanner.network_aci.mso.existing
    if state == 'absent':
        jctanner.network_aci.mso.proposed = jctanner.network_aci.mso.sent = {}

        if not schema_obj:
            # There was no schema to begin with
            pass
        elif len(templates) == 1:
            # There is only one tenant, remove schema
            jctanner.network_aci.mso.existing = {}
            if not module.check_mode:
                jctanner.network_aci.mso.request(schema_path, method='DELETE')
        elif jctanner.network_aci.mso.existing:
            # Remove existing template
            jctanner.network_aci.mso.existing = {}
            ops.append(dict(op='remove', path=template_path))
        else:
            # There was no template to begin with
            pass

    elif state == 'present':
        tenant_id = jctanner.network_aci.mso.lookup_tenant(tenant)

        if display_name is None:
            display_name = jctanner.network_aci.mso.existing.get('displayName', template)

        if not schema_obj:
            # Schema does not exist, so we have to create it
            payload = dict(
                displayName=schema,
                templates=[dict(
                    name=template,
                    displayName=display_name,
                    tenantId=tenant_id,
                )],
                sites=[],
            )

            jctanner.network_aci.mso.existing = payload['templates'][0]

            if not module.check_mode:
                jctanner.network_aci.mso.request(schema_path, method='POST', data=payload)

        elif jctanner.network_aci.mso.existing:
            # Template exists, so we have to update it
            payload = dict(
                name=template,
                displayName=display_name,
                tenantId=tenant_id,
            )

            jctanner.network_aci.mso.sanitize(payload, collate=True)

            ops.append(dict(op='replace', path=template_path + '/displayName', value=display_name))
            ops.append(dict(op='replace', path=template_path + '/tenantId', value=tenant_id))

            jctanner.network_aci.mso.existing = jctanner.network_aci.mso.proposed
        else:
            # Template does not exist, so we have to add it
            payload = dict(
                name=template,
                displayName=display_name,
                tenantId=tenant_id,
            )

            jctanner.network_aci.mso.sanitize(payload, collate=True)

            ops.append(dict(op='add', path='/templates/-', value=payload))

            jctanner.network_aci.mso.existing = jctanner.network_aci.mso.proposed

    if not module.check_mode:
        jctanner.network_aci.mso.request(schema_path, method='PATCH', data=ops)

    jctanner.network_aci.mso.exit_json()


if __name__ == "__main__":
    main()
