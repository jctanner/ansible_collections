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
module: jctanner.network_aci.aci_interface_policy_l2
short_description: Manage Layer 2 interface policies (l2:IfPol)
description:
- Manage Layer 2 interface policies on Cisco jctanner.network_jctanner.network_aci.aci.ACI fabrics.
version_added: '2.4'
options:
  l2_policy:
    description:
    - The name of the Layer 2 interface policy.
    type: str
    required: yes
    aliases: [ name ]
  description:
    description:
    - The description of the Layer 2 interface policy.
    type: str
    aliases: [ descr ]
  qinq:
    description:
    - Determines if QinQ is disabled or if the port should be considered a core or edge port.
    - The APIC defaults to C(disabled) when unset during creation.
    type: str
    choices: [ core, disabled, edge ]
  vepa:
    description:
    - Determines if Virtual Ethernet Port Aggregator is disabled or enabled.
    - The APIC defaults to C(no) when unset during creation.
    type: bool
  vlan_scope:
    description:
    - The scope of the VLAN.
    - The APIC defaults to C(global) when unset during creation.
    type: str
    choices: [ global, portlocal ]
  state:
    description:
    - Use C(present) or C(absent) for adding or removing.
    - Use C(query) for listing an object or multiple objects.
    type: str
    choices: [ absent, present, query ]
    default: present
extends_documentation_fragment: jctanner.network_aci.aci
seealso:
- name: APIC Management Information Model reference
  description: More information about the internal APIC class B(l2:IfPol).
  link: https://developer.cisco.com/docs/apic-mim-ref/
author:
- Dag Wieers (@dagwieers)
'''

EXAMPLES = r'''
- jctanner.network_aci.aci_interface_policy_l2:
    host: '{{ hostname }}'
    username: '{{ username }}'
    password: '{{ password }}'
    l2_policy: '{{ l2_policy }}'
    vlan_scope: '{{ vlan_policy }}'
    description: '{{ description }}'
  delegate_to: localhost
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

# Mapping dicts are used to normalize the proposed data to what the APIC expects, which will keep diffs accurate
QINQ_MAPPING = dict(
    core='corePort',
    disabled='disabled',
    edge='edgePort',
)


def main():
    argument_spec = jctanner.network_aci.aci_argument_spec()
    argument_spec.update(
        l2_policy=dict(type='str', aliases=['name']),  # Not required for querying all policies
        description=dict(type='str', aliases=['descr']),
        vlan_scope=dict(type='str', choices=['global', 'portlocal']),  # No default provided on purpose
        qinq=dict(type='str', choices=['core', 'disabled', 'edge']),
        vepa=dict(type='bool'),
        state=dict(type='str', default='present', choices=['absent', 'present', 'query']),
    )

    module = AnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode=True,
        required_if=[
            ['state', 'absent', ['l2_policy']],
            ['state', 'present', ['l2_policy']],
        ],
    )

    jctanner.network_aci.aci = jctanner.network_jctanner.network_aci.aci.ACIModule(module)

    l2_policy = module.params['l2_policy']
    vlan_scope = module.params['vlan_scope']
    qinq = module.params['qinq']
    if qinq is not None:
        qinq = QINQ_MAPPING[qinq]
    vepa = jctanner.network_aci.aci.boolean(module.params['vepa'], 'enabled', 'disabled')
    description = module.params['description']
    state = module.params['state']

    jctanner.network_aci.aci.construct_url(
        root_class=dict(
            jctanner.network_aci.aci_class='l2IfPol',
            jctanner.network_aci.aci_rn='infra/l2IfP-{0}'.format(l2_policy),
            module_object=l2_policy,
            target_filter={'name': l2_policy},
        ),
    )

    jctanner.network_aci.aci.get_existing()

    if state == 'present':
        jctanner.network_aci.aci.payload(
            jctanner.network_aci.aci_class='l2IfPol',
            class_config=dict(
                name=l2_policy,
                descr=description,
                vlanScope=vlan_scope,
                qinq=qinq, vepa=vepa,
            ),
        )

        jctanner.network_aci.aci.get_diff(jctanner.network_aci.aci_class='l2IfPol')

        jctanner.network_aci.aci.post_config()

    elif state == 'absent':
        jctanner.network_aci.aci.delete_config()

    jctanner.network_aci.aci.exit_json()


if __name__ == "__main__":
    main()
