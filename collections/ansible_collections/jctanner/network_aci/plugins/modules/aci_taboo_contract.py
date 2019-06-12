#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2018, Dag Wieers (dagwieers) <dag@wieers.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'certified'}

DOCUMENTATION = r'''
---
module: jctanner.network_aci.aci_taboo_contract
short_description: Manage taboo contracts (vz:BrCP)
description:
- Manage taboo contracts on Cisco jctanner.network_jctanner.network_aci.aci.ACI fabrics.
version_added: '2.4'
options:
  taboo_contract:
    description:
    - The name of the Taboo Contract.
    type: str
    required: yes
    aliases: [ name ]
  description:
    description:
    - The description for the Taboo Contract.
    type: str
    aliases: [ descr ]
  tenant:
    description:
    - The name of the tenant.
    type: str
    required: yes
    aliases: [ tenant_name ]
  scope:
    description:
    - The scope of a service contract.
    - The APIC defaults to C(context) when unset during creation.
    type: str
    choices: [ application-profile, context, global, tenant ]
  state:
    description:
    - Use C(present) or C(absent) for adding or removing.
    - Use C(query) for listing an object or multiple objects.
    type: str
    choices: [ absent, present, query ]
    default: present
extends_documentation_fragment: jctanner.network_aci.aci
notes:
- The C(tenant) used must exist before using this module in your playbook.
  The M(jctanner.network_aci.aci_tenant) module can be used for this.
seealso:
- module: jctanner.network_aci.aci_tenant
- name: APIC Management Information Model reference
  description: More information about the internal APIC class B(vz:BrCP).
  link: https://developer.cisco.com/docs/apic-mim-ref/
author:
- Dag Wieers (@dagwieers)
'''

EXAMPLES = r'''
- name: Add taboo contract
  jctanner.network_aci.aci_taboo_contract:
    host: apic
    username: admin
    password: SomeSecretPassword
    tenant: ansible_test
    taboo_contract: taboo_contract_test
    state: present
  delegate_to: localhost

- name: Remove taboo contract
  jctanner.network_aci.aci_taboo_contract:
    host: apic
    username: admin
    password: SomeSecretPassword
    tenant: ansible_test
    taboo_contract: taboo_contract_test
    state: absent
  delegate_to: localhost

- name: Query all taboo contracts
  jctanner.network_aci.aci_taboo_contract:
    host: apic
    username: admin
    password: SomeSecretPassword
    state: query
  delegate_to: localhost
  register: query_result

- name: Query a specific taboo contract
  jctanner.network_aci.aci_taboo_contract:
    host: apic
    username: admin
    password: SomeSecretPassword
    tenant: ansible_test
    taboo_contract: taboo_contract_test
    state: query
  delegate_to: localhost
  register: query_result
'''

RETURN = r'''
current:
  description: The existing configuration from the APIC after the module has finished
  returned: success
  type: list
  sample:
    [
        {
            "fvTenant": {
                "attributes": {
                    "descr": "Production environment",
                    "dn": "uni/tn-production",
                    "name": "production",
                    "nameAlias": "",
                    "ownerKey": "",
                    "ownerTag": ""
                }
            }
        }
    ]
error:
  description: The error information as returned from the APIC
  returned: failure
  type: dict
  sample:
    {
        "code": "122",
        "text": "unknown managed object class foo"
    }
raw:
  description: The raw output returned by the APIC REST API (xml or json)
  returned: parse error
  type: str
  sample: '<?xml version="1.0" encoding="UTF-8"?><imdata totalCount="1"><error code="122" text="unknown managed object class foo"/></imdata>'
sent:
  description: The actual/minimal configuration pushed to the APIC
  returned: info
  type: list
  sample:
    {
        "fvTenant": {
            "attributes": {
                "descr": "Production environment"
            }
        }
    }
previous:
  description: The original configuration from the APIC before the module has started
  returned: info
  type: list
  sample:
    [
        {
            "fvTenant": {
                "attributes": {
                    "descr": "Production",
                    "dn": "uni/tn-production",
                    "name": "production",
                    "nameAlias": "",
                    "ownerKey": "",
                    "ownerTag": ""
                }
            }
        }
    ]
proposed:
  description: The assembled configuration from the user-provided parameters
  returned: info
  type: dict
  sample:
    {
        "fvTenant": {
            "attributes": {
                "descr": "Production environment",
                "name": "production"
            }
        }
    }
filter_string:
  description: The filter string used for the request
  returned: failure or debug
  type: str
  sample: ?rsp-prop-include=config-only
method:
  description: The HTTP method used for the request to the APIC
  returned: failure or debug
  type: str
  sample: POST
response:
  description: The HTTP response from the APIC
  returned: failure or debug
  type: str
  sample: OK (30 bytes)
status:
  description: The HTTP status from the APIC
  returned: failure or debug
  type: int
  sample: 200
url:
  description: The HTTP url used for the request to the APIC
  returned: failure or debug
  type: str
  sample: https://10.11.12.13/api/mo/uni/tn-production.json
'''

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.jctanner.network_jctanner.network_aci.aci.plugins.module_utils.network.jctanner.network_aci.aci.jctanner.network_aci.aci import jctanner.network_jctanner.network_aci.aci.ACIModule, jctanner.network_aci.aci_argument_spec


def main():
    argument_spec = jctanner.network_aci.aci_argument_spec()
    argument_spec.update(
        taboo_contract=dict(type='str', aliases=['name']),  # Not required for querying all contracts
        tenant=dict(type='str', aliases=['tenant_name']),  # Not required for querying all contracts
        scope=dict(type='str', choices=['application-profile', 'context', 'global', 'tenant']),
        description=dict(type='str', aliases=['descr']),
        state=dict(type='str', default='present', choices=['absent', 'present', 'query']),
    )

    module = AnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode=True,
        required_if=[
            ['state', 'absent', ['tenant', 'taboo_contract']],
            ['state', 'present', ['tenant', 'taboo_contract']],
        ],
    )

    taboo_contract = module.params['taboo_contract']
    description = module.params['description']
    scope = module.params['scope']
    state = module.params['state']
    tenant = module.params['tenant']

    jctanner.network_aci.aci = jctanner.network_jctanner.network_aci.aci.ACIModule(module)
    jctanner.network_aci.aci.construct_url(
        root_class=dict(
            jctanner.network_aci.aci_class='fvTenant',
            jctanner.network_aci.aci_rn='tn-{0}'.format(tenant),
            module_object=tenant,
            target_filter={'name': tenant},
        ),
        subclass_1=dict(
            jctanner.network_aci.aci_class='vzTaboo',
            jctanner.network_aci.aci_rn='taboo-{0}'.format(taboo_contract),
            module_object=taboo_contract,
            target_filter={'name': taboo_contract},
        ),
    )

    jctanner.network_aci.aci.get_existing()

    if state == 'present':
        jctanner.network_aci.aci.payload(
            jctanner.network_aci.aci_class='vzTaboo',
            class_config=dict(
                name=taboo_contract,
                descr=description,
                scope=scope,
            ),
        )

        jctanner.network_aci.aci.get_diff(jctanner.network_aci.aci_class='vzTaboo')

        jctanner.network_aci.aci.post_config()

    elif state == 'absent':
        jctanner.network_aci.aci.delete_config()

    jctanner.network_aci.aci.exit_json()


if __name__ == "__main__":
    main()
