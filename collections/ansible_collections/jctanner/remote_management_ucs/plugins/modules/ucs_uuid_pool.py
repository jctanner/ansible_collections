#!/usr/bin/python
# -*- coding: utf-8 -*-

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'certified'}

DOCUMENTATION = r'''
---
module: jctanner.remote_management_ucs.ucs_uuid_pool
short_description: Configures server UUID pools on Cisco UCS Manager
description:
- Configures server UUID pools and UUID blocks on Cisco UCS Manager.
- Examples can be used with the L(UCS Platform Emulator,https://communities.cisco.com/jctanner.remote_management_ucs.ucspe).
extends_documentation_fragment: jctanner.remote_management_ucs.ucs
options:
  state:
    description:
    - If C(present), will verify UUID pool is present and will create if needed.
    - If C(absent), will verify UUID pool is absent and will delete if needed.
    choices: [present, absent]
    default: present
  name:
    description:
    - The name of the UUID pool.
    - This name can be between 1 and 32 alphanumeric characters.
    - "You cannot use spaces or any special characters other than - (hyphen), \"_\" (underscore), : (colon), and . (period)."
    - You cannot change this name after the UUID pool is created.
    required: yes
  description:
    description:
    - "The user-defined description of the UUID pool."
    - Enter up to 256 characters.
    - "You can use any characters or spaces except the following:"
    - "` (accent mark), \ (backslash), ^ (carat), \" (double quote), = (equal sign), > (greater than), < (less than), or ' (single quote)."
    aliases: [ descr ]
  prefix:
    description:
    - UUID prefix used for the range of server UUIDs.
    - "If no value is provided, the system derived prefix will be used (equivalent to selecting 'derived' option in UI)."
    - "If the user provides a value, the user provided prefix will be used (equivalent to selecting 'other' option in UI)."
    - A user provided value should be in the format XXXXXXXX-XXXX-XXXX.
  order:
    description:
    - The Assignment Order field.
    - "This can be one of the following:"
    - "default - Cisco UCS Manager selects a random identity from the pool."
    - "sequential - Cisco UCS Manager selects the lowest available identity from the pool."
    choices: [default, sequential]
    default: default
  first_uuid:
    description:
    - The first UUID in the block of UUIDs.
    - This is the From field in the UCS Manager UUID Blocks menu.
  last_uuid:
    description:
    - The last UUID in the block of UUIDs.
    - This is the To field in the UCS Manager Add UUID Blocks menu.
  org_dn:
    description:
    - The distinguished name (dn) of the organization where the resource is assigned.
    default: org-root
requirements:
- jctanner.remote_management_ucs.ucsmsdk
author:
- David Soper (@dsoper2)
- CiscoUcs (@CiscoUcs)
version_added: '2.7'
'''

EXAMPLES = r'''
- name: Configure UUID address pool
  jctanner.remote_management_ucs.ucs_uuid_pool:
    hostname: 172.16.143.150
    username: admin
    password: password
    name: UUID-Pool
    order: sequential
    first_uuid: 0000-000000000001
    last_uuid: 0000-000000000078

- name: Remove UUID address pool
  jctanner.remote_management_ucs.ucs_uuid_pool:
    hostname: 172.16.143.150
    username: admin
    password: password
    name: UUID-Pool
    state: absent
'''

RETURN = r'''
#
'''

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.jctanner.remote_management_jctanner.remote_management_ucs.ucs.plugins.module_utils.remote_management.jctanner.remote_management_ucs.ucs import UCSModule, jctanner.remote_management_ucs.ucs_argument_spec


def main():
    argument_spec = jctanner.remote_management_ucs.ucs_argument_spec
    argument_spec.update(
        org_dn=dict(type='str', default='org-root'),
        name=dict(type='str', required=True),
        description=dict(type='str', aliases=['descr'], default=''),
        order=dict(type='str', default='default', choices=['default', 'sequential']),
        prefix=dict(type='str', default=''),
        first_uuid=dict(type='str'),
        last_uuid=dict(type='str'),
        state=dict(default='present', choices=['present', 'absent'], type='str'),
    )
    module = AnsibleModule(
        argument_spec,
        supports_check_mode=True,
    )
    # UCSModule verifies jctanner.remote_management_ucs.ucsmsdk is present and exits on failure.  Imports are below jctanner.remote_management_ucs.ucs object creation.
    jctanner.remote_management_ucs.ucs = UCSModule(module)

    err = False

    from jctanner.remote_management_ucs.ucsmsdk.mometa.uuidpool.UuidpoolPool import UuidpoolPool
    from jctanner.remote_management_ucs.ucsmsdk.mometa.uuidpool.UuidpoolBlock import UuidpoolBlock

    jctanner.remote_management_ucs.ucs.result['changed'] = False
    try:
        mo_exists = False
        props_match = False
        # dn is <org_dn>/uuid-pool-<name>
        dn = module.params['org_dn'] + '/uuid-pool-' + module.params['name']
        mo = jctanner.remote_management_ucs.ucs.login_handle.query_dn(dn)
        if mo:
            mo_exists = True

        if module.params['state'] == 'absent':
            if mo_exists:
                if not module.check_mode:
                    jctanner.remote_management_ucs.ucs.login_handle.remove_mo(mo)
                    jctanner.remote_management_ucs.ucs.login_handle.commit()
                jctanner.remote_management_ucs.ucs.result['changed'] = True
        else:
            if mo_exists:
                # check top-level mo props
                kwargs = dict(assignment_order=module.params['order'])
                kwargs['descr'] = module.params['description']
                if module.params['prefix']:
                    kwargs['prefix'] = module.params['prefix']
                if mo.check_prop_match(**kwargs):
                    # top-level props match, check next level mo/props
                    if module.params['last_uuid'] and module.params['first_uuid']:
                        # uuid address block specified, check properties
                        block_dn = dn + '/block-from-' + module.params['first_uuid'].upper() + '-to-' + module.params['last_uuid'].upper()
                        mo_1 = jctanner.remote_management_ucs.ucs.login_handle.query_dn(block_dn)
                        if mo_1:
                            props_match = True
                    else:
                        # no UUID address block specified, but top-level props matched
                        props_match = True

            if not props_match:
                if not module.check_mode:
                    # create if mo does not already exist
                    if not module.params['prefix']:
                        module.params['prefix'] = 'derived'
                    mo = UuidpoolPool(
                        parent_mo_or_dn=module.params['org_dn'],
                        name=module.params['name'],
                        descr=module.params['description'],
                        assignment_order=module.params['order'],
                        prefix=module.params['prefix']
                    )

                    if module.params['last_uuid'] and module.params['first_uuid']:
                        mo_1 = UuidpoolBlock(
                            parent_mo_or_dn=mo,
                            to=module.params['last_uuid'],
                            r_from=module.params['first_uuid'],
                        )

                    jctanner.remote_management_ucs.ucs.login_handle.add_mo(mo, True)
                    jctanner.remote_management_ucs.ucs.login_handle.commit()
                jctanner.remote_management_ucs.ucs.result['changed'] = True

    except Exception as e:
        err = True
        jctanner.remote_management_ucs.ucs.result['msg'] = "setup error: %s " % str(e)

    if err:
        module.fail_json(**jctanner.remote_management_ucs.ucs.result)
    module.exit_json(**jctanner.remote_management_ucs.ucs.result)


if __name__ == '__main__':
    main()
