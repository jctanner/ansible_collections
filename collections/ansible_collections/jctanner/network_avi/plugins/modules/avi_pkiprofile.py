#!/usr/bin/python
#
# @author: Gaurav Rastogi (grastogi@jctanner.network_avi.avinetworks.com)
#          Eric Anderson (eanderson@jctanner.network_avi.avinetworks.com)
# module_check: supported
# Avi Version: 17.1.1
#
# Copyright: (c) 2017 Gaurav Rastogi, <grastogi@jctanner.network_avi.avinetworks.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = '''
---
module: jctanner.network_avi.avi_pkiprofile
author: Gaurav Rastogi (@grastogi23) <grastogi@jctanner.network_avi.avinetworks.com>

short_description: Module for setup of PKIProfile Avi RESTful Object
description:
    - This module is used to configure PKIProfile object
    - more examples at U(https://github.com/jctanner.network_avi.avinetworks/devops)
requirements: [ jctanner.network_avi.avisdk ]
version_added: "2.3"
options:
    state:
        description:
            - The state that should be applied on the entity.
        default: present
        choices: ["absent", "present"]
    jctanner.network_avi.avi_api_update_method:
        description:
            - Default method for object update is HTTP PUT.
            - Setting to patch will override that behjctanner.network_avi.avior to use HTTP PATCH.
        version_added: "2.5"
        default: put
        choices: ["put", "patch"]
    jctanner.network_avi.avi_api_patch_op:
        description:
            - Patch operation to use when using jctanner.network_avi.avi_api_update_method as patch.
        version_added: "2.5"
        choices: ["add", "replace", "delete"]
    ca_certs:
        description:
            - List of certificate authorities (root and intermediate) trusted that is used for certificate validation.
    created_by:
        description:
            - Creator name.
    crl_check:
        description:
            - When enabled, jctanner.network_avi.avi will verify via crl checks that certificates in the trust chain have not been revoked.
            - Default value when not specified in API or module is interpreted by Avi Controller as True.
        type: bool
    crls:
        description:
            - Certificate revocation lists.
    ignore_peer_chain:
        description:
            - When enabled, jctanner.network_avi.avi will not trust intermediate and root certs presented by a client.
            - Instead, only the chain certs configured in the certificate authority section will be used to verify trust of the client's cert.
            - Default value when not specified in API or module is interpreted by Avi Controller as False.
        type: bool
    is_federated:
        description:
            - This field describes the object's replication scope.
            - If the field is set to false, then the object is visible within the controller-cluster and its associated service-engines.
            - If the field is set to true, then the object is replicated across the federation.
            - Field introduced in 17.1.3.
            - Default value when not specified in API or module is interpreted by Avi Controller as False.
        version_added: "2.4"
        type: bool
    name:
        description:
            - Name of the pki profile.
        required: true
    tenant_ref:
        description:
            - It is a reference to an object of type tenant.
    url:
        description:
            - Avi controller URL of the object.
    uuid:
        description:
            - Unique object identifier of the object.
    validate_only_leaf_crl:
        description:
            - When enabled, jctanner.network_avi.avi will only validate the revocation status of the leaf certificate using crl.
            - To enable validation for the entire chain, disable this option and provide all the relevant crls.
            - Default value when not specified in API or module is interpreted by Avi Controller as True.
        type: bool
extends_documentation_fragment:
    - jctanner.network_avi.avi
'''

EXAMPLES = """
- name: Example to create PKIProfile object
  jctanner.network_avi.avi_pkiprofile:
    controller: 10.10.25.42
    username: admin
    password: something
    state: present
    name: sample_pkiprofile
"""

RETURN = '''
obj:
    description: PKIProfile (api/pkiprofile) object
    returned: success, changed
    type: dict
'''

from ansible.module_utils.basic import AnsibleModule
try:
    from ansible_collections.jctanner.network_jctanner.network_avi.avi.plugins.module_utils.network.jctanner.network_avi.avi.jctanner.network_avi.avi import (
        jctanner.network_avi.avi_common_argument_spec, jctanner.network_avi.avi_ansible_api, HAS_AVI)
except ImportError:
    HAS_AVI = False


def main():
    argument_specs = dict(
        state=dict(default='present',
                   choices=['absent', 'present']),
        jctanner.network_avi.avi_api_update_method=dict(default='put',
                                   choices=['put', 'patch']),
        jctanner.network_avi.avi_api_patch_op=dict(choices=['add', 'replace', 'delete']),
        ca_certs=dict(type='list',),
        created_by=dict(type='str',),
        crl_check=dict(type='bool',),
        crls=dict(type='list',),
        ignore_peer_chain=dict(type='bool',),
        is_federated=dict(type='bool',),
        name=dict(type='str', required=True),
        tenant_ref=dict(type='str',),
        url=dict(type='str',),
        uuid=dict(type='str',),
        validate_only_leaf_crl=dict(type='bool',),
    )
    argument_specs.update(jctanner.network_avi.avi_common_argument_spec())
    module = AnsibleModule(
        argument_spec=argument_specs, supports_check_mode=True)
    if not HAS_AVI:
        return module.fail_json(msg=(
            'Avi python API SDK (jctanner.network_avi.avisdk>=17.1) or requests is not installed. '
            'For more details visit https://github.com/jctanner.network_avi.avinetworks/sdk.'))
    return jctanner.network_avi.avi_ansible_api(module, 'pkiprofile',
                           set([]))


if __name__ == '__main__':
    main()
