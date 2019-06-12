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
module: jctanner.network_aci.mso_schema_site
short_description: Manage sites in schemas
description:
- Manage sites on Cisco jctanner.network_jctanner.network_aci.aci.ACI Multi-Site.
author:
- Dag Wieers (@dagwieers)
version_added: '2.8'
options:
  schema:
    description:
    - The name of the schema.
    type: str
    required: yes
  site:
    description:
    - The name of the site to manage.
    type: str
    required: yes
  template:
    description:
    - The name of the template.
    type: str
    required: yes
    aliases: [ name ]
  state:
    description:
    - Use C(present) or C(absent) for adding or removing.
    - Use C(query) for listing an object or multiple objects.
    type: str
    choices: [ absent, present, query ]
    default: present
seealso:
- module: jctanner.network_aci.mso_schema_template
- module: jctanner.network_aci.mso_site
extends_documentation_fragment: jctanner.network_aci.mso
'''

EXAMPLES = r'''
- name: Add a new site to a schema
  jctanner.network_aci.mso_schema_site:
    host: jctanner.network_aci.mso_host
    username: admin
    password: SomeSecretPassword
    schema: Schema 1
    site: bdsol-pod51
    template: Template 1
    state: present
  delegate_to: localhost

- name: Remove a site from a schema
  jctanner.network_aci.mso_schema:
    host: jctanner.network_aci.mso_host
    username: admin
    password: SomeSecretPassword
    schema: Schema 1
    site: bdsol-pod51
    template: Template 1
    state: absent
  delegate_to: localhost

- name: Query a schema site
  jctanner.network_aci.mso_schema:
    host: jctanner.network_aci.mso_host
    username: admin
    password: SomeSecretPassword
    schema: Schema 1
    site: bdsol-pod51
    template: Template 1
    state: query
  delegate_to: localhost
  register: query_result

- name: Query all schema sites
  jctanner.network_aci.mso_schema:
    host: jctanner.network_aci.mso_host
    username: admin
    password: SomeSecretPassword
    schema: Schema 1
    site: bdsol-pod51
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
        schema=dict(type='str', required=True),
        site=dict(type='str', aliases=['name']),
        template=dict(type='str'),
        state=dict(type='str', default='present', choices=['absent', 'present', 'query']),
    )

    module = AnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode=True,
        required_if=[
            ['state', 'absent', ['site', 'template']],
            ['state', 'present', ['site', 'template']],
        ],
    )

    schema = module.params['schema']
    site = module.params['site']
    template = module.params['template']
    state = module.params['state']

    jctanner.network_aci.mso = MSOModule(module)

    # Get schema
    schema_obj = jctanner.network_aci.mso.get_obj('schemas', displayName=schema)
    if not schema_obj:
        jctanner.network_aci.mso.fail_json(msg="Provided schema '{0}' does not exist".format(schema))

    # Schema exists
    schema_path = 'schemas/{id}'.format(**schema_obj)

    # Get site
    site_id = jctanner.network_aci.mso.lookup_site(site)

    jctanner.network_aci.mso.existing = {}
    if 'sites' in schema_obj:
        sites = [(s['siteId'], s['templateName']) for s in schema_obj['sites']]
        if template:
            if (site_id, template) in sites:
                site_idx = sites.index((site_id, template))
                jctanner.network_aci.mso.existing = schema_obj['sites'][site_idx]
        else:
            jctanner.network_aci.mso.existing = schema_obj['sites']

    if state == 'query':
        if not jctanner.network_aci.mso.existing:
            if template:
                jctanner.network_aci.mso.fail_json(msg="Template '{0}' not found".format(template))
            else:
                jctanner.network_aci.mso.existing = []
        jctanner.network_aci.mso.exit_json()

    sites_path = '/sites'
    site_path = '/sites/{0}'.format(site)
    ops = []

    jctanner.network_aci.mso.previous = jctanner.network_aci.mso.existing
    if state == 'absent':
        if jctanner.network_aci.mso.existing:
            # Remove existing site
            jctanner.network_aci.mso.sent = jctanner.network_aci.mso.existing = {}
            ops.append(dict(op='remove', path=site_path))

    elif state == 'present':
        if not jctanner.network_aci.mso.existing:
            # Add new site
            payload = dict(
                siteId=site_id,
                templateName=template,
                anps=[],
                bds=[],
                contracts=[],
                externalEpgs=[],
                intersiteL3outs=[],
                serviceGraphs=[],
                vrfs=[],
            )

            jctanner.network_aci.mso.sanitize(payload, collate=True)

            ops.append(dict(op='add', path=sites_path + '/-', value=jctanner.network_aci.mso.sent))

            jctanner.network_aci.mso.existing = jctanner.network_aci.mso.proposed

    if not module.check_mode:
        jctanner.network_aci.mso.request(schema_path, method='PATCH', data=ops)

    jctanner.network_aci.mso.exit_json()


if __name__ == "__main__":
    main()
