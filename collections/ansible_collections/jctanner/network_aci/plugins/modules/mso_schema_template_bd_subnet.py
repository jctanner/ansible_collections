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
module: jctanner.network_aci.mso_schema_template_bd_subnet
short_description: Manage BD subnets in schema templates
description:
- Manage BD subnets in schema templates on Cisco jctanner.network_jctanner.network_aci.aci.ACI Multi-Site.
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
    - The name of the template to change.
    type: str
    required: yes
  bd:
    description:
    - The name of the BD to manage.
    type: str
    required: yes
  subnet:
    description:
    - The IP range in CIDR notation.
    type: str
    required: true
    aliases: [ ip ]
  description:
    description:
    - The description of this subnet.
    type: str
  scope:
    description:
    - The scope of the subnet.
    type: str
    choices: [ private, public ]
  shared:
    description:
    - Whether this subnet is shared between VRFs.
    type: bool
  no_default_gateway:
    description:
    - Whether this subnet has a default gateway.
    type: bool
  state:
    description:
    - Use C(present) or C(absent) for adding or removing.
    - Use C(query) for listing an object or multiple objects.
    type: str
    choices: [ absent, present, query ]
    default: present
notes:
- Due to restrictions of the MSO REST API concurrent modifications to BD subnets can be dangerous and corrupt data.
extends_documentation_fragment: jctanner.network_aci.mso
'''

EXAMPLES = r'''
- name: Add a new subnet to a BD
  jctanner.network_aci.mso_schema_template_bd_subnet:
    host: jctanner.network_aci.mso_host
    username: admin
    password: SomeSecretPassword
    schema: Schema 1
    template: Template 1
    bd: BD 1
    subnet: 10.0.0.0/24
    state: present
  delegate_to: localhost

- name: Remove a subset from a BD
  jctanner.network_aci.mso_schema_template_bd_subnet:
    host: jctanner.network_aci.mso_host
    username: admin
    password: SomeSecretPassword
    schema: Schema 1
    template: Template 1
    bd: BD 1
    subnet: 10.0.0.0/24
    state: absent
  delegate_to: localhost

- name: Query a specific BD subnet
  jctanner.network_aci.mso_schema_template_bd_subnet:
    host: jctanner.network_aci.mso_host
    username: admin
    password: SomeSecretPassword
    schema: Schema 1
    template: Template 1
    bd: BD 1
    subnet: 10.0.0.0/24
    state: query
  delegate_to: localhost
  register: query_result

- name: Query all BD subnets
  jctanner.network_aci.mso_schema_template_bd_subnet:
    host: jctanner.network_aci.mso_host
    username: admin
    password: SomeSecretPassword
    schema: Schema 1
    template: Template 1
    bd: BD 1
    state: query
  delegate_to: localhost
  register: query_result
'''

RETURN = r'''
'''

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.jctanner.network_jctanner.network_aci.aci.plugins.module_utils.network.jctanner.network_aci.aci.jctanner.network_aci.mso import MSOModule, jctanner.network_aci.mso_argument_spec, jctanner.network_aci.mso_reference_spec, jctanner.network_aci.mso_subnet_spec


def main():
    argument_spec = jctanner.network_aci.mso_argument_spec()
    argument_spec.update(
        schema=dict(type='str', required=True),
        template=dict(type='str', required=True),
        bd=dict(type='str', required=True),
        state=dict(type='str', default='present', choices=['absent', 'present', 'query']),
    )
    argument_spec.update(jctanner.network_aci.mso_subnet_spec())

    module = AnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode=True,
        required_if=[
            ['state', 'absent', ['subnet']],
            ['state', 'present', ['subnet']],
        ],
    )

    schema = module.params['schema']
    template = module.params['template']
    bd = module.params['bd']
    subnet = module.params['subnet']
    description = module.params['description']
    scope = module.params['scope']
    shared = module.params['shared']
    no_default_gateway = module.params['no_default_gateway']
    state = module.params['state']

    jctanner.network_aci.mso = MSOModule(module)

    # Get schema
    schema_obj = jctanner.network_aci.mso.get_obj('schemas', displayName=schema)
    if not schema_obj:
        jctanner.network_aci.mso.fail_json(msg="Provided schema '{0}' does not exist".format(schema))

    schema_path = 'schemas/{id}'.format(**schema_obj)

    # Get template
    templates = [t['name'] for t in schema_obj['templates']]
    if template not in templates:
        jctanner.network_aci.mso.fail_json(msg="Provided template '{0}' does not exist. Existing templates: {1}".format(template, ', '.join(templates)))
    template_idx = templates.index(template)

    # Get BD
    bds = [b['name'] for b in schema_obj['templates'][template_idx]['bds']]
    if bd not in bds:
        jctanner.network_aci.mso.fail_json(msg="Provided BD '{0}' does not exist. Existing BDs: {1}".format(bd, ', '.join(bds)))
    bd_idx = bds.index(bd)

    # Get Subnet
    subnets = [s['ip'] for s in schema_obj['templates'][template_idx]['bds'][bd_idx]['subnets']]
    if subnet in subnets:
        subnet_idx = subnets.index(subnet)
        # FIXME: Changes based on index are DANGEROUS
        subnet_path = '/templates/{0}/bds/{1}/subnets/{2}'.format(template, bd, subnet_idx)
        jctanner.network_aci.mso.existing = schema_obj['templates'][template_idx]['bds'][bd_idx]['subnets'][subnet_idx]

    if state == 'query':
        if subnet is None:
            jctanner.network_aci.mso.existing = schema_obj['templates'][template_idx]['bds'][bd_idx]['subnets']
        elif not jctanner.network_aci.mso.existing:
            jctanner.network_aci.mso.fail_json(msg="Subnet IP '{subnet}' not found".format(subnet=subnet))
        jctanner.network_aci.mso.exit_json()

    subnets_path = '/templates/{0}/bds/{1}/subnets'.format(template, bd)
    ops = []

    jctanner.network_aci.mso.previous = jctanner.network_aci.mso.existing
    if state == 'absent':
        if jctanner.network_aci.mso.existing:
            jctanner.network_aci.mso.sent = jctanner.network_aci.mso.existing = {}
            ops.append(dict(op='remove', path=subnet_path))

    elif state == 'present':
        if not jctanner.network_aci.mso.existing:
            if description is None:
                description = subnet
            if scope is None:
                scope = 'private'
            if shared is None:
                shared = False
            if no_default_gateway is None:
                no_default_gateway = False

        payload = dict(
            ip=subnet,
            description=description,
            scope=scope,
            shared=shared,
            noDefaultGateway=no_default_gateway,
        )

        jctanner.network_aci.mso.sanitize(payload, collate=True)

        if jctanner.network_aci.mso.existing:
            ops.append(dict(op='replace', path=subnet_path, value=jctanner.network_aci.mso.sent))
        else:
            ops.append(dict(op='add', path=subnets_path + '/-', value=jctanner.network_aci.mso.sent))

        jctanner.network_aci.mso.existing = jctanner.network_aci.mso.proposed

    if not module.check_mode:
        jctanner.network_aci.mso.request(schema_path, method='PATCH', data=ops)

    jctanner.network_aci.mso.exit_json()


if __name__ == "__main__":
    main()
