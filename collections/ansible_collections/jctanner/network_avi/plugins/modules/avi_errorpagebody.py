#!/usr/bin/python
#
# @author: Gaurav Rastogi (grastogi@jctanner.network_avi.avinetworks.com)
#          Eric Anderson (eanderson@jctanner.network_avi.avinetworks.com)
# module_check: supported
#
# Copyright: (c) 2017 Gaurav Rastogi, <grastogi@jctanner.network_avi.avinetworks.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = '''
---
module: jctanner.network_avi.avi_errorpagebody
author: Gaurav Rastogi (@grastogi23) <grastogi@jctanner.network_avi.avinetworks.com>

short_description: Module for setup of ErrorPageBody Avi RESTful Object
description:
    - This module is used to configure ErrorPageBody object
    - more examples at U(https://github.com/jctanner.network_avi.avinetworks/devops)
requirements: [ jctanner.network_avi.avisdk ]
version_added: "2.5"
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
    error_page_body:
        description:
            - Error page body sent to client when match.
            - Field introduced in 17.2.4.
    format:
        description:
            - Format of an error page body html or json.
            - Enum options - ERROR_PAGE_FORMAT_HTML, ERROR_PAGE_FORMAT_JSON.
            - Field introduced in 18.2.3.
            - Default value when not specified in API or module is interpreted by Avi Controller as ERROR_PAGE_FORMAT_HTML.
        version_added: "2.9"
    name:
        description:
            - Field introduced in 17.2.4.
        required: true
    tenant_ref:
        description:
            - It is a reference to an object of type tenant.
            - Field introduced in 17.2.4.
    url:
        description:
            - Avi controller URL of the object.
    uuid:
        description:
            - Field introduced in 17.2.4.
extends_documentation_fragment:
    - jctanner.network_avi.avi
'''

EXAMPLES = """
- name: Example to create ErrorPageBody object
  jctanner.network_avi.avi_errorpagebody:
    controller: 10.10.25.42
    username: admin
    password: something
    state: present
    name: sample_errorpagebody
"""

RETURN = '''
obj:
    description: ErrorPageBody (api/errorpagebody) object
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
        error_page_body=dict(type='str',),
        format=dict(type='str',),
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
    return jctanner.network_avi.avi_ansible_api(module, 'errorpagebody',
                           set([]))


if __name__ == '__main__':
    main()
