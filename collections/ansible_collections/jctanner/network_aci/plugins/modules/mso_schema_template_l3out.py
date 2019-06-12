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
module: jctanner.network_aci.mso_schema_template_l3out
short_description: Manage l3outs in schema templates
description:
- Manage l3outs in schema templates on Cisco jctanner.network_jctanner.network_aci.aci.ACI Multi-Site.
author:
- Dag Wieers (@dagwieers)
version_added: '2.8'
options:
  schema:
    description:
    - The name of the schema.
    type: str
    required: yes
  template:
    description:
    - The name of the template.
    type: str
    required: yes
  l3out:
    description:
    - The name of the l3out to manage.
    type: str
    aliases: [ name ]
  display_name:
    description:
    - The name as displayed on the MSO web interface.
    type: str
  vrf:
    description:
    - The VRF associated to this L3out.
    type: dict
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
- name: Add a new L3out
  jctanner.network_aci.mso_schema_template_l3out:
    host: jctanner.network_aci.mso_host
    username: admin
    password: SomeSecretPassword
    schema: Schema 1
    template: Template 1
    l3out: L3out 1
    state: present
  delegate_to: localhost

- name: Remove an L3out
  jctanner.network_aci.mso_schema_template_l3out:
    host: jctanner.network_aci.mso_host
    username: admin
    password: SomeSecretPassword
    schema: Schema 1
    template: Template 1
    l3out: L3out 1
    state: absent
  delegate_to: localhost

- name: Query a specific L3outs
  jctanner.network_aci.mso_schema_template_l3out:
    host: jctanner.network_aci.mso_host
    username: admin
    password: SomeSecretPassword
    schema: Schema 1
    template: Template 1
    l3out: L3out 1
    state: query
  delegate_to: localhost
  register: query_result

- name: Query all L3outs
  jctanner.network_aci.mso_schema_template_l3out:
    host: jctanner.network_aci.mso_host
    username: admin
    password: SomeSecretPassword
    schema: Schema 1
    template: Template 1
    state: query
  delegate_to: localhost
  register: query_result
'''

RETURN = r'''
'''

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.jctanner.network_jctanner.network_aci.aci.plugins.module_utils.network.jctanner.network_aci.aci.jctanner.network_aci.mso import MSOModule, jctanner.network_aci.mso_argument_spec, jctanner.network_aci.mso_reference_spec, issubset


def main():
    argument_spec = jctanner.network_aci.mso_argument_spec()
    argument_spec.update(
        schema=dict(type='str', required=True),
        template=dict(type='str', required=True),
        l3out=dict(type='str', aliases=['name']),  # This parameter is not required for querying all objects
        display_name=dict(type='str'),
        vrf=dict(type='dict', options=jctanner.network_aci.mso_reference_spec()),
        state=dict(type='str', default='present', choices=['absent', 'present', 'query']),
    )

    module = AnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode=True,
        required_if=[
            ['state', 'absent', ['l3out']],
            ['state', 'present', ['l3out', 'vrf']],
        ],
    )

    schema = module.params['schema']
    template = module.params['template']
    l3out = module.params['l3out']
    display_name = module.params['display_name']
    vrf = module.params['vrf']
    state = module.params['state']

    jctanner.network_aci.mso = MSOModule(module)

    # Get schema_id
    schema_obj = jctanner.network_aci.mso.get_obj('schemas', displayName=schema)
    if schema_obj:
        schema_id = schema_obj['id']
    else:
        jctanner.network_aci.mso.fail_json(msg="Provided schema '{0}' does not exist".format(schema))

    schema_path = 'schemas/{id}'.format(**schema_obj)

    # Get template
    templates = [t['name'] for t in schema_obj['templates']]
    if template not in templates:
        jctanner.network_aci.mso.fail_json(msg="Provided template '{0}' does not exist. Existing templates: {1}".format(template, ', '.join(templates)))
    template_idx = templates.index(template)

    # Get L3out
    l3outs = [l['name'] for l in schema_obj['templates'][template_idx]['intersiteL3outs']]

    if l3out is not None and l3out in l3outs:
        l3out_idx = l3outs.index(l3out)
        jctanner.network_aci.mso.existing = schema_obj['templates'][template_idx]['intersiteL3outs'][l3out_idx]

    if state == 'query':
        if l3out is None:
            jctanner.network_aci.mso.existing = schema_obj['templates'][template_idx]['intersiteL3outs']
        elif not jctanner.network_aci.mso.existing:
            jctanner.network_aci.mso.fail_json(msg="L3out '{l3out}' not found".format(l3out=l3out))
        jctanner.network_aci.mso.exit_json()

    l3outs_path = '/templates/{0}/intersiteL3outs'.format(template)
    l3out_path = '/templates/{0}/intersiteL3outs/{1}'.format(template, l3out)
    ops = []

    jctanner.network_aci.mso.previous = jctanner.network_aci.mso.existing
    if state == 'absent':
        if jctanner.network_aci.mso.existing:
            jctanner.network_aci.mso.sent = jctanner.network_aci.mso.existing = {}
            ops.append(dict(op='remove', path=l3out_path))

    elif state == 'present':
        vrf_ref = jctanner.network_aci.mso.make_reference(vrf, 'vrf', schema_id, template)

        if display_name is None and not jctanner.network_aci.mso.existing:
            display_name = l3out

        payload = dict(
            name=l3out,
            displayName=display_name,
            vrfRef=vrf_ref,
        )

        jctanner.network_aci.mso.sanitize(payload, collate=True)

        if jctanner.network_aci.mso.existing:
            ops.append(dict(op='replace', path=l3out_path, value=jctanner.network_aci.mso.sent))
        else:
            ops.append(dict(op='add', path=l3outs_path + '/-', value=jctanner.network_aci.mso.sent))

        jctanner.network_aci.mso.existing = jctanner.network_aci.mso.proposed

    if not module.check_mode:
        jctanner.network_aci.mso.request(schema_path, method='PATCH', data=ops)

    jctanner.network_aci.mso.exit_json()


if __name__ == "__main__":
    main()
