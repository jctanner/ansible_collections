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
module: jctanner.network_aci.mso_user
short_description: Manage users
description:
- Manage users on Cisco jctanner.network_jctanner.network_aci.aci.ACI Multi-Site.
author:
- Dag Wieers (@dagwieers)
version_added: '2.8'
options:
  user:
    description:
    - The name of the user.
    type: str
    required: yes
    aliases: [ name ]
  user_password:
    description:
    - The password of the user.
    type: str
  first_name:
    description:
    - The first name of the user.
    - This parameter is required when creating new users.
    type: str
  last_name:
    description:
    - The last name of the user.
    - This parameter is required when creating new users.
    type: str
  email:
    description:
    - The email address of the user.
    - This parameter is required when creating new users.
    type: str
  phone:
    description:
    - The phone number of the user.
    - This parameter is required when creating new users.
    type: str
  account_status:
    description:
    - The status of the user account.
    type: str
    choices: [ active ]
  domain:
    description:
    - The domain this user belongs to.
    - When creating new users, this defaults to C(Local).
    type: str
  roles:
    description:
    - The roles for this user.
    type: list
  state:
    description:
    - Use C(present) or C(absent) for adding or removing.
    - Use C(query) for listing an object or multiple objects.
    type: str
    choices: [ absent, present, query ]
    default: present
notes:
- A default installation of jctanner.network_jctanner.network_aci.aci.ACI Multi-Site ships with admin password 'we1come!' which requires a password change on first login.
  See the examples of how to change the 'admin' password using Ansible.
extends_documentation_fragment: jctanner.network_aci.mso
'''

EXAMPLES = r'''
- name: Update initial admin password
  jctanner.network_aci.mso_user:
    host: jctanner.network_aci.mso_host
    username: admin
    password: we1come!
    user_name: admin
    user_password: SomeSecretPassword
    state: present
  delegate_to: localhost

- name: Add a new user
  jctanner.network_aci.mso_user:
    host: jctanner.network_aci.mso_host
    username: admin
    password: SomeSecretPassword
    user_name: dag
    description: Test user
    first_name: Dag
    last_name: Wieers
    email: dag@wieers.com
    phone: +32 478 436 299
    state: present
  delegate_to: localhost

- name: Remove a user
  jctanner.network_aci.mso_user:
    host: jctanner.network_aci.mso_host
    username: admin
    password: SomeSecretPassword
    user_name: dag
    state: absent
  delegate_to: localhost

- name: Query a user
  jctanner.network_aci.mso_user:
    host: jctanner.network_aci.mso_host
    username: admin
    password: SomeSecretPassword
    user_name: dag
    state: query
  delegate_to: localhost
  register: query_result

- name: Query all users
  jctanner.network_aci.mso_user:
    host: jctanner.network_aci.mso_host
    username: admin
    password: SomeSecretPassword
    state: query
  delegate_to: localhost
  register: query_result
'''

RETURN = r''' # '''

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.jctanner.network_jctanner.network_aci.aci.plugins.module_utils.network.jctanner.network_aci.aci.jctanner.network_aci.mso import MSOModule, jctanner.network_aci.mso_argument_spec, issubset


def main():
    argument_spec = jctanner.network_aci.mso_argument_spec()
    argument_spec.update(
        user=dict(type='str', aliases=['name']),
        user_password=dict(type='str', no_log=True),
        first_name=dict(type='str'),
        last_name=dict(type='str'),
        email=dict(type='str'),
        phone=dict(type='str'),
        # TODO: What possible options do we have ?
        account_status=dict(type='str', choices=['active']),
        domain=dict(type='str'),
        roles=dict(type='list'),
        state=dict(type='str', default='present', choices=['absent', 'present', 'query']),
    )

    module = AnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode=True,
        required_if=[
            ['state', 'absent', ['user']],
            ['state', 'present', ['user']],
        ],
    )

    user_name = module.params['user']
    user_password = module.params['user_password']
    first_name = module.params['first_name']
    last_name = module.params['last_name']
    email = module.params['email']
    phone = module.params['phone']
    account_status = module.params['account_status']
    state = module.params['state']

    jctanner.network_aci.mso = MSOModule(module)

    roles = jctanner.network_aci.mso.lookup_roles(module.params['roles'])
    domain = jctanner.network_aci.mso.lookup_domain(module.params['domain'])

    user_id = None
    path = 'users'

    # Query for existing object(s)
    if user_name:
        jctanner.network_aci.mso.existing = jctanner.network_aci.mso.get_obj(path, username=user_name)
        if jctanner.network_aci.mso.existing:
            user_id = jctanner.network_aci.mso.existing['id']
            # If we found an existing object, continue with it
            path = 'users/{id}'.format(id=user_id)
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
            id=user_id,
            username=user_name,
            password=user_password,
            firstName=first_name,
            lastName=last_name,
            emailAddress=email,
            phoneNumber=phone,
            accountStatus=account_status,
            domainId=domain,
            roles=roles,
            # active=True,
            # remote=True,
        )

        jctanner.network_aci.mso.sanitize(payload, collate=True)

        if jctanner.network_aci.mso.sent.get('accountStatus') is None:
            jctanner.network_aci.mso.sent['accountStatus'] = 'active'

        if jctanner.network_aci.mso.existing:
            if not issubset(jctanner.network_aci.mso.sent, jctanner.network_aci.mso.existing):
                # NOTE: Since MSO always returns '******' as password, we need to assume a change
                if 'password' in jctanner.network_aci.mso.proposed:
                    jctanner.network_aci.mso.module.warn("A password change is assumed, as the MSO REST API does not return passwords we do not know.")
                    jctanner.network_aci.mso.result['changed'] = True

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
