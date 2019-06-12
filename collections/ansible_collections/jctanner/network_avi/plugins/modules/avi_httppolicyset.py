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
module: jctanner.network_avi.avi_httppolicyset
author: Gaurav Rastogi (@grastogi23) <grastogi@jctanner.network_avi.avinetworks.com>

short_description: Module for setup of HTTPPolicySet Avi RESTful Object
description:
    - This module is used to configure HTTPPolicySet object
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
            - Checksum of cloud configuration for pool.
            - Internally set by cloud connector.
    created_by:
        description:
            - Creator name.
    description:
        description:
            - User defined description for the object.
    http_request_policy:
        description:
            - Http request policy for the virtual service.
    http_response_policy:
        description:
            - Http response policy for the virtual service.
    http_security_policy:
        description:
            - Http security policy for the virtual service.
    is_internal_policy:
        description:
            - Boolean flag to set is_internal_policy.
            - Default value when not specified in API or module is interpreted by Avi Controller as False.
        type: bool
    name:
        description:
            - Name of the http policy set.
        required: true
    tenant_ref:
        description:
            - It is a reference to an object of type tenant.
    url:
        description:
            - Avi controller URL of the object.
    uuid:
        description:
            - Uuid of the http policy set.
extends_documentation_fragment:
    - jctanner.network_avi.avi
'''

EXAMPLES = """
- name: Create a HTTP Policy set two switch between testpool1 and testpool2
  jctanner.network_avi.avi_httppolicyset:
    controller: 10.10.27.90
    username: admin
    password: AviNetworks123!
    name: test-HTTP-Policy-Set
    tenant_ref: admin
    http_request_policy:
    rules:
      - index: 1
        enable: true
        name: test-test1
        match:
          path:
            match_case: INSENSITIVE
            match_str:
              - /test1
            match_criteria: EQUALS
        switching_action:
          action: HTTP_SWITCHING_SELECT_POOL
          status_code: HTTP_LOCAL_RESPONSE_STATUS_CODE_200
          pool_ref: "/api/pool?name=testpool1"
      - index: 2
        enable: true
        name: test-test2
        match:
          path:
            match_case: INSENSITIVE
            match_str:
              - /test2
            match_criteria: CONTAINS
        switching_action:
          action: HTTP_SWITCHING_SELECT_POOL
          status_code: HTTP_LOCAL_RESPONSE_STATUS_CODE_200
          pool_ref: "/api/pool?name=testpool2"
    is_internal_policy: false
"""

RETURN = '''
obj:
    description: HTTPPolicySet (api/httppolicyset) object
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
        http_request_policy=dict(type='dict',),
        http_response_policy=dict(type='dict',),
        http_security_policy=dict(type='dict',),
        is_internal_policy=dict(type='bool',),
        name=dict(type='str', required=True),
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
    return jctanner.network_avi.avi_ansible_api(module, 'httppolicyset',
                           set([]))


if __name__ == '__main__':
    main()
