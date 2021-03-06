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
module: jctanner.network_aci.mso_schema_template_vrf
short_description: Manage VRFs in schema templates
description:
- Manage VRFs in schema templates on Cisco jctanner.network_jctanner.network_aci.aci.ACI Multi-Site.
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
  vrf:
    description:
    - The name of the VRF to manage.
    type: str
    aliases: [ name ]
  display_name:
    description:
    - The name as displayed on the MSO web interface.
    type: str
  layer3_multicast:
    description:
    - Whether to enable L3 multicast.
    type: bool
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
- name: Add a new VRF
  jctanner.network_aci.mso_schema_template_vrf:
    host: jctanner.network_aci.mso_host
    username: admin
    password: SomeSecretPassword
    schema: Schema 1
    template: Template 1
    vrf: VRF 1
    state: present
  delegate_to: localhost

- name: Remove an VRF
  jctanner.network_aci.mso_schema_template_vrf:
    host: jctanner.network_aci.mso_host
    username: admin
    password: SomeSecretPassword
    schema: Schema 1
    template: Template 1
    vrf: VRF1
    state: absent
  delegate_to: localhost

- name: Query a specific VRFs
  jctanner.network_aci.mso_schema_template_vrf:
    host: jctanner.network_aci.mso_host
    username: admin
    password: SomeSecretPassword
    schema: Schema 1
    template: Template 1
    vrf: VRF1
    state: query
  delegate_to: localhost
  register: query_result

- name: Query all VRFs
  jctanner.network_aci.mso_schema_template_vrf:
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
        vrf=dict(type='str', aliases=['name']),  # This parameter is not required for querying all objects
        display_name=dict(type='str'),
        layer3_multicast=dict(type='bool'),
        state=dict(type='str', default='present', choices=['absent', 'present', 'query']),
    )

    module = AnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode=True,
        required_if=[
            ['state', 'absent', ['vrf']],
            ['state', 'present', ['vrf']],
        ],
    )

    schema = module.params['schema']
    template = module.params['template']
    vrf = module.params['vrf']
    display_name = module.params['display_name']
    layer3_multicast = module.params['layer3_multicast']
    state = module.params['state']

    jctanner.network_aci.mso = MSOModule(module)

    # Get schema_id
    schema_obj = jctanner.network_aci.mso.get_obj('schemas', displayName=schema)
    if not schema_obj:
        jctanner.network_aci.mso.fail_json(msg="Provided schema '{0}' does not exist".format(schema))

    schema_path = 'schemas/{id}'.format(**schema_obj)

    # Get template
    templates = [t['name'] for t in schema_obj['templates']]
    if template not in templates:
        jctanner.network_aci.mso.fail_json(msg="Provided template '{0}' does not exist. Existing templates: {1}".format(template, ', '.join(templates)))
    template_idx = templates.index(template)

    # Get ANP
    vrfs = [v['name'] for v in schema_obj['templates'][template_idx]['vrfs']]

    if vrf is not None and vrf in vrfs:
        vrf_idx = vrfs.index(vrf)
        jctanner.network_aci.mso.existing = schema_obj['templates'][template_idx]['vrfs'][vrf_idx]

    if state == 'query':
        if vrf is None:
            jctanner.network_aci.mso.existing = schema_obj['templates'][template_idx]['vrfs']
        elif not jctanner.network_aci.mso.existing:
            jctanner.network_aci.mso.fail_json(msg="VRF '{vrf}' not found".format(vrf=vrf))
        jctanner.network_aci.mso.exit_json()

    vrfs_path = '/templates/{0}/vrfs'.format(template)
    vrf_path = '/templates/{0}/vrfs/{1}'.format(template, vrf)
    ops = []

    jctanner.network_aci.mso.previous = jctanner.network_aci.mso.existing
    if state == 'absent':
        if jctanner.network_aci.mso.existing:
            jctanner.network_aci.mso.sent = jctanner.network_aci.mso.existing = {}
            ops.append(dict(op='remove', path=vrf_path))

    elif state == 'present':
        if display_name is None and not jctanner.network_aci.mso.existing:
            display_name = vrf

        payload = dict(
            name=vrf,
            displayName=display_name,
            l3MCast=layer3_multicast,
            # FIXME
            regions=[],
        )

        jctanner.network_aci.mso.sanitize(payload, collate=True)

        if jctanner.network_aci.mso.existing:
            ops.append(dict(op='replace', path=vrf_path, value=jctanner.network_aci.mso.sent))
        else:
            ops.append(dict(op='add', path=vrfs_path + '/-', value=jctanner.network_aci.mso.sent))

        jctanner.network_aci.mso.existing = jctanner.network_aci.mso.proposed

    if not module.check_mode:
        jctanner.network_aci.mso.request(schema_path, method='PATCH', data=ops)

    jctanner.network_aci.mso.exit_json()


if __name__ == "__main__":
    main()
