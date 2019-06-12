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
module: jctanner.network_aci.aci_contract
short_description: Manage contract resources (vz:BrCP)
description:
- Manage Contract resources on Cisco jctanner.network_jctanner.network_aci.aci.ACI fabrics.
version_added: '2.4'
options:
  contract:
    description:
    - The name of the contract.
    type: str
    required: yes
    aliases: [ contract_name, name ]
  description:
    description:
    - Description for the contract.
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
  priority:
    description:
    - The desired QoS class to be used.
    - The APIC defaults to C(unspecified) when unset during creation.
    type: str
    choices: [ level1, level2, level3, unspecified ]
  dscp:
    description:
    - The target Differentiated Service (DSCP) value.
    - The APIC defaults to C(unspecified) when unset during creation.
    type: str
    choices: [ AF11, AF12, AF13, AF21, AF22, AF23, AF31, AF32, AF33, AF41, AF42, AF43, CS0, CS1, CS2, CS3, CS4, CS5, CS6, CS7, EF, VA, unspecified ]
    aliases: [ target ]
  state:
    description:
    - Use C(present) or C(absent) for adding or removing.
    - Use C(query) for listing an object or multiple objects.
    type: str
    choices: [ absent, present, query ]
    default: present
extends_documentation_fragment: jctanner.network_aci.aci
notes:
- This module does not manage Contract Subjects, see M(jctanner.network_aci.aci_contract_subject) to do this.
  Contract Subjects can still be removed using this module.
- The C(tenant) used must exist before using this module in your playbook.
  The M(jctanner.network_aci.aci_tenant) module can be used for this.
seealso:
- module: jctanner.network_aci.aci_contract_subject
- module: jctanner.network_aci.aci_tenant
- name: APIC Management Information Model reference
  description: More information about the internal APIC class B(vz:BrCP).
  link: https://developer.cisco.com/docs/apic-mim-ref/
author:
- Dag Wieers (@dagwieers)
'''

EXAMPLES = r'''
- name: Add a new contract
  jctanner.network_aci.aci_contract:
    host: apic
    username: admin
    password: SomeSecretPassword
    tenant: production
    contract: web_to_db
    description: Communication between web-servers and database
    scope: application-profile
    state: present
  delegate_to: localhost

- name: Remove an existing contract
  jctanner.network_aci.aci_contract:
    host: apic
    username: admin
    password: SomeSecretPassword
    tenant: production
    contract: web_to_db
    state: absent
  delegate_to: localhost

- name: Query a specific contract
  jctanner.network_aci.aci_contract:
    host: apic
    username: admin
    password: SomeSecretPassword
    tenant: production
    contract: web_to_db
    state: query
  delegate_to: localhost
  register: query_result

- name: Query all contracts
  jctanner.network_aci.aci_contract:
    host: apic
    username: admin
    password: SomeSecretPassword
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
        contract=dict(type='str', aliases=['contract_name', 'name']),  # Not required for querying all objects
        tenant=dict(type='str', aliases=['tenant_name']),  # Not required for querying all objects
        description=dict(type='str', aliases=['descr']),
        scope=dict(type='str', choices=['application-profile', 'context', 'global', 'tenant']),
        priority=dict(type='str', choices=['level1', 'level2', 'level3', 'unspecified']),  # No default provided on purpose
        dscp=dict(type='str',
                  choices=['AF11', 'AF12', 'AF13', 'AF21', 'AF22', 'AF23', 'AF31', 'AF32', 'AF33', 'AF41', 'AF42', 'AF43',
                           'CS0', 'CS1', 'CS2', 'CS3', 'CS4', 'CS5', 'CS6', 'CS7', 'EF', 'VA', 'unspecified'],
                  aliases=['target']),  # No default provided on purpose
        state=dict(type='str', default='present', choices=['absent', 'present', 'query']),
    )

    module = AnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode=True,
        required_if=[
            ['state', 'absent', ['contract', 'tenant']],
            ['state', 'present', ['contract', 'tenant']],
        ],
    )

    contract = module.params['contract']
    description = module.params['description']
    scope = module.params['scope']
    priority = module.params['priority']
    dscp = module.params['dscp']
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
            jctanner.network_aci.aci_class='vzBrCP',
            jctanner.network_aci.aci_rn='brc-{0}'.format(contract),
            module_object=contract,
            target_filter={'name': contract},
        ),
    )

    jctanner.network_aci.aci.get_existing()

    if state == 'present':
        jctanner.network_aci.aci.payload(
            jctanner.network_aci.aci_class='vzBrCP',
            class_config=dict(
                name=contract,
                descr=description,
                scope=scope,
                prio=priority,
                targetDscp=dscp,
            ),
        )

        jctanner.network_aci.aci.get_diff(jctanner.network_aci.aci_class='vzBrCP')

        jctanner.network_aci.aci.post_config()

    elif state == 'absent':
        jctanner.network_aci.aci.delete_config()

    jctanner.network_aci.aci.exit_json()


if __name__ == "__main__":
    main()
