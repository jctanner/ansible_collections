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
module: jctanner.network_avi.avi_networksecuritypolicy
author: Gaurav Rastogi (@grastogi23) <grastogi@jctanner.network_avi.avinetworks.com>

short_description: Module for setup of NetworkSecurityPolicy Avi RESTful Object
description:
    - This module is used to configure NetworkSecurityPolicy object
    - more examples at U(https://github.com/jctanner.network_avi.avinetworks/devops)
requirements: [ jctanner.network_avi.avisdk ]
version_added: "2.4"
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
    cloud_config_cksum:
        description:
            - Checksum of cloud configuration for network sec policy.
            - Internally set by cloud connector.
    created_by:
        description:
            - Creator name.
    description:
        description:
            - User defined description for the object.
    name:
        description:
            - Name of the object.
    rules:
        description:
            - List of networksecurityrule.
    tenant_ref:
        description:
            - It is a reference to an object of type tenant.
    url:
        description:
            - Avi controller URL of the object.
    uuid:
        description:
            - Unique object identifier of the object.
extends_documentation_fragment:
    - jctanner.network_avi.avi
'''

EXAMPLES = """
  - name: Create a network security policy to block clients represented by ip group known_attackers
    jctanner.network_avi.avi_networksecuritypolicy:
      controller: '{{ controller }}'
      username: '{{ username }}'
      password: '{{ password }}'
      name: vs-gurutest-ns
      rules:
      - action: NETWORK_SECURITY_POLICY_ACTION_TYPE_DENY
        age: 0
        enable: true
        index: 1
        log: false
        match:
          client_ip:
            group_refs:
            - Demo:known_attackers
            match_criteria: IS_IN
        name: Rule 1
      tenant_ref: Demo
"""

RETURN = '''
obj:
    description: NetworkSecurityPolicy (api/networksecuritypolicy) object
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
        cloud_config_cksum=dict(type='str',),
        created_by=dict(type='str',),
        description=dict(type='str',),
        name=dict(type='str',),
        rules=dict(type='list',),
        tenant_ref=dict(type='str',),
        url=dict(type='str',),
        uuid=dict(type='str',),
    )
    argument_specs.update(jctanner.network_avi.avi_common_argument_spec())
    module = AnsibleModule(
        argument_spec=argument_specs, supports_check_mode=True)
    if not HAS_AVI:
        return module.fail_json(msg=(
            'Avi python API SDK (jctanner.network_avi.avisdk>=17.1) or requests is not installed. '
            'For more details visit https://github.com/jctanner.network_avi.avinetworks/sdk.'))
    return jctanner.network_avi.avi_ansible_api(module, 'networksecuritypolicy',
                           set([]))


if __name__ == '__main__':
    main()
