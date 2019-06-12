#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2019, Dag Wieers (@dagwieers) <dag@wieers.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = r'''
---
module: jctanner.network_aci.mso_schema_site_anp
short_description: Manage site-local Application Network Profiles (ANPs) in schema template
description:
- Manage site-local ANPs in schema template on Cisco jctanner.network_jctanner.network_aci.aci.ACI Multi-Site.
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
    - The name of the site.
    type: str
    required: yes
  template:
    description:
    - The name of the template.
    type: str
    required: yes
  anp:
    description:
    - The name of the ANP to manage.
    type: str
    aliases: [ name ]
  state:
    description:
    - Use C(present) or C(absent) for adding or removing.
    - Use C(query) for listing an object or multiple objects.
    type: str
    choices: [ absent, present, query ]
    default: present
seealso:
- module: jctanner.network_aci.mso_schema_site
- module: jctanner.network_aci.mso_schema_site_anp_epg
- module: jctanner.network_aci.mso_schema_template_anp
extends_documentation_fragment: jctanner.network_aci.mso
'''

EXAMPLES = r'''
- name: Add a new site ANP
  jctanner.network_aci.mso_schema_site_anp:
    host: jctanner.network_aci.mso_host
    username: admin
    password: SomeSecretPassword
    schema: Schema1
    site: Site1
    template: Template1
    anp: ANP1
    state: present
  delegate_to: localhost

- name: Remove a site ANP
  jctanner.network_aci.mso_schema_site_anp:
    host: jctanner.network_aci.mso_host
    username: admin
    password: SomeSecretPassword
    schema: Schema1
    site: Site1
    template: Template1
    anp: ANP1
    state: absent
  delegate_to: localhost

- name: Query a specific site ANPs
  jctanner.network_aci.mso_schema_site_anp:
    host: jctanner.network_aci.mso_host
    username: admin
    password: SomeSecretPassword
    schema: Schema1
    site: Site1
    template: Template1
    state: query
  delegate_to: localhost
  register: query_result

- name: Query all site ANPs
  jctanner.network_aci.mso_schema_site_anp:
    host: jctanner.network_aci.mso_host
    username: admin
    password: SomeSecretPassword
    schema: Schema1
    site: Site1
    template: Template1
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
        schema=dict(type='str', required=True),
        site=dict(type='str', required=True),
        template=dict(type='str', required=True),
        anp=dict(type='str', aliases=['name']),  # This parameter is not required for querying all objects
        state=dict(type='str', default='present', choices=['absent', 'present', 'query']),
    )

    module = AnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode=True,
        required_if=[
            ['state', 'absent', ['anp']],
            ['state', 'present', ['anp']],
        ],
    )

    schema = module.params['schema']
    site = module.params['site']
    template = module.params['template']
    anp = module.params['anp']
    state = module.params['state']

    jctanner.network_aci.mso = MSOModule(module)

    # Get schema_id
    schema_obj = jctanner.network_aci.mso.get_obj('schemas', displayName=schema)
    if not schema_obj:
        jctanner.network_aci.mso.fail_json(msg="Provided schema '{0}' does not exist".format(schema))

    schema_path = 'schemas/{id}'.format(**schema_obj)
    schema_id = schema_obj['id']

    # Get site
    site_id = jctanner.network_aci.mso.lookup_site(site)

    # Get site_idx
    sites = [(s['siteId'], s['templateName']) for s in schema_obj['sites']]
    if (site_id, template) not in sites:
        jctanner.network_aci.mso.fail_json(msg="Provided site/template '{0}-{1}' does not exist. Existing sites/templates: {2}".format(site, template, ', '.join(sites)))

    # Schema-access uses indexes
    site_idx = sites.index((site_id, template))
    # Path-based access uses site_id-template
    site_template = '{0}-{1}'.format(site_id, template)

    # Get ANP
    anp_ref = jctanner.network_aci.mso.anp_ref(schema_id=schema_id, template=template, anp=anp)
    anps = [a['anpRef'] for a in schema_obj['sites'][site_idx]['anps']]

    if anp is not None and anp_ref in anps:
        anp_idx = anps.index(anp_ref)
        anp_path = '/sites/{0}/anps/{1}'.format(site_template, anp)
        jctanner.network_aci.mso.existing = schema_obj['sites'][site_idx]['anps'][anp_idx]

    if state == 'query':
        if anp is None:
            jctanner.network_aci.mso.existing = schema_obj['sites'][site_idx]['anps']
        elif not jctanner.network_aci.mso.existing:
            jctanner.network_aci.mso.fail_json(msg="ANP '{anp}' not found".format(anp=anp))
        jctanner.network_aci.mso.exit_json()

    anps_path = '/sites/{0}/anps'.format(site_template)
    ops = []

    jctanner.network_aci.mso.previous = jctanner.network_aci.mso.existing
    if state == 'absent':
        if jctanner.network_aci.mso.existing:
            jctanner.network_aci.mso.sent = jctanner.network_aci.mso.existing = {}
            ops.append(dict(op='remove', path=anp_path))

    elif state == 'present':

        payload = dict(
            anpRef=dict(
                schemaId=schema_id,
                templateName=template,
                anpName=anp,
            ),
        )

        jctanner.network_aci.mso.sanitize(payload, collate=True)

        if not jctanner.network_aci.mso.existing:
            ops.append(dict(op='add', path=anps_path + '/-', value=jctanner.network_aci.mso.sent))

        jctanner.network_aci.mso.existing = jctanner.network_aci.mso.proposed

    if not module.check_mode:
        jctanner.network_aci.mso.request(schema_path, method='PATCH', data=ops)

    jctanner.network_aci.mso.exit_json()


if __name__ == "__main__":
    main()
