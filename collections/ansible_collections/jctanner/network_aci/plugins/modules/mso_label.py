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
module: jctanner.network_aci.mso_label
short_description: Manage labels
description:
- Manage labels on Cisco jctanner.network_jctanner.network_aci.aci.ACI Multi-Site.
author:
- Dag Wieers (@dagwieers)
version_added: '2.8'
options:
  label:
    description:
    - The name of the label.
    type: str
    required: yes
    aliases: [ name ]
  type:
    description:
    - The type of the label.
    type: str
    choices: [ site ]
    default: site
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
- name: Add a new label
  jctanner.network_aci.mso_label:
    host: jctanner.network_aci.mso_host
    username: admin
    password: SomeSecretPassword
    label: Belgium
    type: site
    state: present
  delegate_to: localhost

- name: Remove a label
  jctanner.network_aci.mso_label:
    host: jctanner.network_aci.mso_host
    username: admin
    password: SomeSecretPassword
    label: Belgium
    state: absent
  delegate_to: localhost

- name: Query a label
  jctanner.network_aci.mso_label:
    host: jctanner.network_aci.mso_host
    username: admin
    password: SomeSecretPassword
    label: Belgium
    state: query
  delegate_to: localhost
  register: query_result

- name: Query all labels
  jctanner.network_aci.mso_label:
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
        label=dict(type='str', aliases=['name']),
        type=dict(type='str', default='site', choices=['site']),
        state=dict(type='str', default='present', choices=['absent', 'present', 'query']),
    )

    module = AnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode=True,
        required_if=[
            ['state', 'absent', ['label']],
            ['state', 'present', ['label']],
        ],
    )

    label = module.params['label']
    label_type = module.params['type']
    state = module.params['state']

    jctanner.network_aci.mso = MSOModule(module)

    label_id = None
    path = 'labels'

    # Query for existing object(s)
    if label:
        jctanner.network_aci.mso.existing = jctanner.network_aci.mso.get_obj(path, displayName=label)
        if jctanner.network_aci.mso.existing:
            label_id = jctanner.network_aci.mso.existing['id']
            # If we found an existing object, continue with it
            path = 'labels/{id}'.format(id=label_id)
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
            id=label_id,
            displayName=label,
            type=label_type,
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
