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
module: jctanner.network_aci.aci_epg_to_contract
short_description: Bind EPGs to Contracts (fv:RsCons, fv:RsProv)
description:
- Bind EPGs to Contracts on Cisco jctanner.network_jctanner.network_aci.aci.ACI fabrics.
notes:
- The C(tenant), C(app_profile), C(EPG), and C(Contract) used must exist before using this module in your playbook.
  The M(jctanner.network_aci.aci_tenant), M(jctanner.network_aci.aci_ap), M(jctanner.network_aci.aci_epg), and M(jctanner.network_aci.aci_contract) modules can be used for this.
version_added: '2.4'
options:
  ap:
    description:
    - Name of an existing application network profile, that will contain the EPGs.
    type: str
    aliases: [ app_profile, app_profile_name ]
  contract:
    description:
    - The name of the contract.
    type: str
    aliases: [ contract_name ]
  contract_type:
    description:
    - Determines if the EPG should Provide or Consume the Contract.
    type: str
    required: yes
    choices: [ consumer, provider ]
  epg:
    description:
    - The name of the end point group.
    type: str
    aliases: [ epg_name ]
  priority:
    description:
    - QoS class.
    - The APIC defaults to C(unspecified) when unset during creation.
    type: str
    choices: [ level1, level2, level3, unspecified ]
  provider_match:
    description:
    - The matching algorithm for Provided Contracts.
    - The APIC defaults to C(at_least_one) when unset during creation.
    type: str
    choices: [ all, at_least_one, at_most_one, none ]
  state:
    description:
    - Use C(present) or C(absent) for adding or removing.
    - Use C(query) for listing an object or multiple objects.
    type: str
    choices: [ absent, present, query ]
    default: present
  tenant:
    description:
    - Name of an existing tenant.
    type: str
    aliases: [ tenant_name ]
extends_documentation_fragment: jctanner.network_aci.aci
seealso:
- module: jctanner.network_aci.aci_ap
- module: jctanner.network_aci.aci_epg
- module: jctanner.network_aci.aci_contract
- name: APIC Management Information Model reference
  description: More information about the internal APIC classes B(fv:RsCons) and B(fv:RsProv).
  link: https://developer.cisco.com/docs/apic-mim-ref/
author:
- Jacob McGill (@jmcgill298)
'''

EXAMPLES = r'''
- name: Add a new contract to EPG binding
  jctanner.network_aci.aci_epg_to_contract:
    host: apic
    username: admin
    password: SomeSecretPassword
    tenant: anstest
    ap: anstest
    epg: anstest
    contract: anstest_http
    contract_type: provider
    state: present
  delegate_to: localhost

- name: Remove an existing contract to EPG binding
  jctanner.network_aci.aci_epg_to_contract:
    host: apic
    username: admin
    password: SomeSecretPassword
    tenant: anstest
    ap: anstest
    epg: anstest
    contract: anstest_http
    contract_type: provider
    state: absent
  delegate_to: localhost

- name: Query a specific contract to EPG binding
  jctanner.network_aci.aci_epg_to_contract:
    host: apic
    username: admin
    password: SomeSecretPassword
    tenant: anstest
    ap: anstest
    epg: anstest
    contract: anstest_http
    contract_type: provider
    state: query
  delegate_to: localhost
  register: query_result

- name: Query all provider contract to EPG bindings
  jctanner.network_aci.aci_epg_to_contract:
    host: apic
    username: admin
    password: SomeSecretPassword
    contract_type: provider
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

jctanner.network_jctanner.network_aci.aci.ACI_CLASS_MAPPING = dict(
    consumer={
        'class': 'fvRsCons',
        'rn': 'rscons-',
    },
    provider={
        'class': 'fvRsProv',
        'rn': 'rsprov-',
    },
)

PROVIDER_MATCH_MAPPING = dict(
    all='All',
    at_least_one='AtleastOne',
    at_most_one='tmostOne',
    none='None',
)


def main():
    argument_spec = jctanner.network_aci.aci_argument_spec()
    argument_spec.update(
        contract_type=dict(type='str', required=True, choices=['consumer', 'provider']),
        ap=dict(type='str', aliases=['app_profile', 'app_profile_name']),  # Not required for querying all objects
        epg=dict(type='str', aliases=['epg_name']),  # Not required for querying all objects
        contract=dict(type='str', aliases=['contract_name']),  # Not required for querying all objects
        priority=dict(type='str', choices=['level1', 'level2', 'level3', 'unspecified']),
        provider_match=dict(type='str', choices=['all', 'at_least_one', 'at_most_one', 'none']),
        state=dict(type='str', default='present', choices=['absent', 'present', 'query']),
        tenant=dict(type='str', aliases=['tenant_name']),  # Not required for querying all objects
    )

    module = AnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode=True,
        required_if=[
            ['state', 'absent', ['ap', 'contract', 'epg', 'tenant']],
            ['state', 'present', ['ap', 'contract', 'epg', 'tenant']],
        ],
    )

    ap = module.params['ap']
    contract = module.params['contract']
    contract_type = module.params['contract_type']
    epg = module.params['epg']
    priority = module.params['priority']
    provider_match = module.params['provider_match']
    if provider_match is not None:
        provider_match = PROVIDER_MATCH_MAPPING[provider_match]
    state = module.params['state']
    tenant = module.params['tenant']

    jctanner.network_aci.aci_class = jctanner.network_jctanner.network_aci.aci.ACI_CLASS_MAPPING[contract_type]["class"]
    jctanner.network_aci.aci_rn = jctanner.network_jctanner.network_aci.aci.ACI_CLASS_MAPPING[contract_type]["rn"]

    if contract_type == "consumer" and provider_match is not None:
        module.fail_json(msg="the 'provider_match' is only configurable for Provided Contracts")

    jctanner.network_aci.aci = jctanner.network_jctanner.network_aci.aci.ACIModule(module)
    jctanner.network_aci.aci.construct_url(
        root_class=dict(
            jctanner.network_aci.aci_class='fvTenant',
            jctanner.network_aci.aci_rn='tn-{0}'.format(tenant),
            module_object=tenant,
            target_filter={'name': tenant},
        ),
        subclass_1=dict(
            jctanner.network_aci.aci_class='fvAp',
            jctanner.network_aci.aci_rn='ap-{0}'.format(ap),
            module_object=ap,
            target_filter={'name': ap},
        ),
        subclass_2=dict(
            jctanner.network_aci.aci_class='fvAEPg',
            jctanner.network_aci.aci_rn='epg-{0}'.format(epg),
            module_object=epg,
            target_filter={'name': epg},
        ),
        subclass_3=dict(
            jctanner.network_aci.aci_class=jctanner.network_aci.aci_class,
            jctanner.network_aci.aci_rn='{0}{1}'.format(jctanner.network_aci.aci_rn, contract),
            module_object=contract,
            target_filter={'tnVzBrCPName': contract},
        ),
    )

    jctanner.network_aci.aci.get_existing()

    if state == 'present':
        jctanner.network_aci.aci.payload(
            jctanner.network_aci.aci_class=jctanner.network_aci.aci_class,
            class_config=dict(
                matchT=provider_match,
                prio=priority,
                tnVzBrCPName=contract,
            ),
        )

        jctanner.network_aci.aci.get_diff(jctanner.network_aci.aci_class=jctanner.network_aci.aci_class)

        jctanner.network_aci.aci.post_config()

    elif state == 'absent':
        jctanner.network_aci.aci.delete_config()

    jctanner.network_aci.aci.exit_json()


if __name__ == "__main__":
    main()
