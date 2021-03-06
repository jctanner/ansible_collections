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
module: jctanner.network_aci.aci_domain
short_description: Manage physical, virtual, bridged, routed or FC domain profiles (phys:DomP, vmm:DomP, l2ext:DomP, l3ext:DomP, fc:DomP)
description:
- Manage physical, virtual, bridged, routed or FC domain profiles on Cisco jctanner.network_jctanner.network_aci.aci.ACI fabrics.
version_added: '2.5'
options:
  domain:
    description:
    - Name of the physical, virtual, bridged routed or FC domain profile.
    type: str
    aliases: [ domain_name, domain_profile, name ]
  domain_type:
    description:
    - The type of domain profile.
    - 'C(fc): The FC domain profile is a policy pertaining to single FC Management domain'
    - 'C(l2dom): The external bridged domain profile is a policy for managing L2 bridged infrastructure bridged outside the fabric.'
    - 'C(l3dom): The external routed domain profile is a policy for managing L3 routed infrastructure outside the fabric.'
    - 'C(phys): The physical domain profile stores the physical resources and encap resources that should be used for EPGs associated with this domain.'
    - 'C(vmm): The VMM domain profile is a policy for grouping VM controllers with similar networking policy requirements.'
    type: str
    choices: [ fc, l2dom, l3dom, phys, vmm ]
    aliases: [ type ]
  dscp:
    description:
    - The target Differentiated Service (DSCP) value.
    - The APIC defaults to C(unspecified) when unset during creation.
    type: str
    choices: [ AF11, AF12, AF13, AF21, AF22, AF23, AF31, AF32, AF33, AF41, AF42, AF43, CS0, CS1, CS2, CS3, CS4, CS5, CS6, CS7, EF, VA, unspecified ]
    aliases: [ target ]
  encap_mode:
    description:
    - The layer 2 encapsulation protocol to use with the virtual switch.
    type: str
    choices: [ unknown, vlan, vxlan ]
  multicast_address:
    description:
    - The muticast IP address to use for the virtual switch.
    type: str
  state:
    description:
    - Use C(present) or C(absent) for adding or removing.
    - Use C(query) for listing an object or multiple objects.
    type: str
    choices: [ absent, present, query ]
    default: present
  vm_provider:
    description:
    - The VM platform for VMM Domains.
    - Support for Kubernetes was added in jctanner.network_jctanner.network_aci.aci.ACI v3.0.
    - Support for CloudFoundry, OpenShift and Red Hat was added in jctanner.network_jctanner.network_aci.aci.ACI v3.1.
    type: str
    choices: [ cloudfoundry, kubernetes, microsoft, openshift, openstack, redhat, vmware ]
  vswitch:
    description:
    - The virtual switch to use for vmm domains.
    - The APIC defaults to C(default) when unset during creation.
    type: str
    choices: [ avs, default, dvs, unknown ]
extends_documentation_fragment: jctanner.network_aci.aci
seealso:
- module: jctanner.network_aci.aci_aep_to_domain
- module: jctanner.network_aci.aci_domain_to_encap_pool
- module: jctanner.network_aci.aci_domain_to_vlan_pool
- name: APIC Management Information Model reference
  description: More information about the internal APIC classes B(phys:DomP),
               B(vmm:DomP), B(l2ext:DomP), B(l3ext:DomP) and B(fc:DomP)
  link: https://developer.cisco.com/docs/apic-mim-ref/
author:
- Dag Wieers (@dagwieers)
'''

EXAMPLES = r'''
- name: Add a new physical domain
  jctanner.network_aci.aci_domain:
    host: apic
    username: admin
    password: SomeSecretPassword
    domain: phys_dom
    domain_type: phys
    state: present

- name: Remove a physical domain
  jctanner.network_aci.aci_domain:
    host: apic
    username: admin
    password: SomeSecretPassword
    domain: phys_dom
    domain_type: phys
    state: absent

- name: Add a new VMM domain
  jctanner.network_aci.aci_domain:
    host: apic
    username: admin
    password: SomeSecretPassword
    domain: hyperv_dom
    domain_type: vmm
    vm_provider: microsoft
    state: present
  delegate_to: localhost

- name: Remove a VMM domain
  jctanner.network_aci.aci_domain:
    host: apic
    username: admin
    password: SomeSecretPassword
    domain: hyperv_dom
    domain_type: vmm
    vm_provider: microsoft
    state: absent
  delegate_to: localhost

- name: Query a specific physical domain
  jctanner.network_aci.aci_domain:
    host: apic
    username: admin
    password: SomeSecretPassword
    domain: phys_dom
    domain_type: phys
    state: query
  delegate_to: localhost
  register: query_result

- name: Query all domains
  jctanner.network_aci.aci_domain:
    host: apic
    username: admin
    password: SomeSecretPassword
    domain_type: phys
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

VM_PROVIDER_MAPPING = dict(
    cloudfoundry='CloudFoundry',
    kubernetes='Kubernetes',
    microsoft='Microsoft',
    openshift='OpenShift',
    openstack='OpenStack',
    redhat='Redhat',
    vmware='VMware',
)

VSWITCH_MAPPING = dict(
    avs='n1kv',
    default='default',
    dvs='default',
    unknown='unknown',
)


def main():
    argument_spec = jctanner.network_aci.aci_argument_spec()
    argument_spec.update(
        domain_type=dict(type='str', required=True, choices=['fc', 'l2dom', 'l3dom', 'phys', 'vmm'], aliases=['type']),
        domain=dict(type='str', aliases=['domain_name', 'domain_profile', 'name']),  # Not required for querying all objects
        dscp=dict(type='str',
                  choices=['AF11', 'AF12', 'AF13', 'AF21', 'AF22', 'AF23', 'AF31', 'AF32', 'AF33', 'AF41', 'AF42', 'AF43',
                           'CS0', 'CS1', 'CS2', 'CS3', 'CS4', 'CS5', 'CS6', 'CS7', 'EF', 'VA', 'unspecified'],
                  aliases=['target']),
        encap_mode=dict(type='str', choices=['unknown', 'vlan', 'vxlan']),
        multicast_address=dict(type='str'),
        state=dict(type='str', default='present', choices=['absent', 'present', 'query']),
        vm_provider=dict(type='str', choices=['cloudfoundry', 'kubernetes', 'microsoft', 'openshift', 'openstack', 'redhat', 'vmware']),
        vswitch=dict(type='str', choices=['avs', 'default', 'dvs', 'unknown']),
    )

    module = AnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode=True,
        required_if=[
            ['domain_type', 'vmm', ['vm_provider']],
            ['state', 'absent', ['domain', 'domain_type']],
            ['state', 'present', ['domain', 'domain_type']],
        ],
    )

    dscp = module.params['dscp']
    domain = module.params['domain']
    domain_type = module.params['domain_type']
    encap_mode = module.params['encap_mode']
    multicast_address = module.params['multicast_address']
    vm_provider = module.params['vm_provider']
    vswitch = module.params['vswitch']
    if vswitch is not None:
        vswitch = VSWITCH_MAPPING[vswitch]
    state = module.params['state']

    if domain_type != 'vmm':
        if vm_provider is not None:
            module.fail_json(msg="Domain type '{0}' cannot have parameter 'vm_provider'".format(domain_type))
        if encap_mode is not None:
            module.fail_json(msg="Domain type '{0}' cannot have parameter 'encap_mode'".format(domain_type))
        if multicast_address is not None:
            module.fail_json(msg="Domain type '{0}' cannot have parameter 'multicast_address'".format(domain_type))
        if vswitch is not None:
            module.fail_json(msg="Domain type '{0}' cannot have parameter 'vswitch'".format(domain_type))

    if dscp is not None and domain_type not in ['l2dom', 'l3dom']:
        module.fail_json(msg="DSCP values can only be assigned to 'l2ext and 'l3ext' domains")

    # Compile the full domain for URL building
    if domain_type == 'fc':
        domain_class = 'fcDomP'
        domain_mo = 'uni/fc-{0}'.format(domain)
        domain_rn = 'fc-{0}'.format(domain)
    elif domain_type == 'l2dom':
        domain_class = 'l2extDomP'
        domain_mo = 'uni/l2dom-{0}'.format(domain)
        domain_rn = 'l2dom-{0}'.format(domain)
    elif domain_type == 'l3dom':
        domain_class = 'l3extDomP'
        domain_mo = 'uni/l3dom-{0}'.format(domain)
        domain_rn = 'l3dom-{0}'.format(domain)
    elif domain_type == 'phys':
        domain_class = 'physDomP'
        domain_mo = 'uni/phys-{0}'.format(domain)
        domain_rn = 'phys-{0}'.format(domain)
    elif domain_type == 'vmm':
        domain_class = 'vmmDomP'
        domain_mo = 'uni/vmmp-{0}/dom-{1}'.format(VM_PROVIDER_MAPPING[vm_provider], domain)
        domain_rn = 'vmmp-{0}/dom-{1}'.format(VM_PROVIDER_MAPPING[vm_provider], domain)

    # Ensure that querying all objects works when only domain_type is provided
    if domain is None:
        domain_mo = None

    jctanner.network_aci.aci = jctanner.network_jctanner.network_aci.aci.ACIModule(module)
    jctanner.network_aci.aci.construct_url(
        root_class=dict(
            jctanner.network_aci.aci_class=domain_class,
            jctanner.network_aci.aci_rn=domain_rn,
            module_object=domain_mo,
            target_filter={'name': domain},
        ),
    )

    jctanner.network_aci.aci.get_existing()

    if state == 'present':
        jctanner.network_aci.aci.payload(
            jctanner.network_aci.aci_class=domain_class,
            class_config=dict(
                encapMode=encap_mode,
                mcastAddr=multicast_address,
                mode=vswitch,
                name=domain,
                targetDscp=dscp,
            ),
        )

        jctanner.network_aci.aci.get_diff(jctanner.network_aci.aci_class=domain_class)

        jctanner.network_aci.aci.post_config()

    elif state == 'absent':
        jctanner.network_aci.aci.delete_config()

    jctanner.network_aci.aci.exit_json()


if __name__ == "__main__":
    main()
