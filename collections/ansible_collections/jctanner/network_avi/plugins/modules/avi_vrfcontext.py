#!/usr/bin/python
#
# @author: Gaurav Rastogi (grastogi@jctanner.network_avi.avinetworks.com)
#          Eric Anderson (eanderson@jctanner.network_avi.avinetworks.com)
# module_check: supported
# Avi Version: 17.1.2
#
# Copyright: (c) 2017 Gaurav Rastogi, <grastogi@jctanner.network_avi.avinetworks.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = '''
---
module: jctanner.network_avi.avi_vrfcontext
author: Gaurav Rastogi (@grastogi23) <grastogi@jctanner.network_avi.avinetworks.com>

short_description: Module for setup of VrfContext Avi RESTful Object
description:
    - This module is used to configure VrfContext object
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
    bgp_profile:
        description:
            - Bgp local and peer info.
    cloud_ref:
        description:
            - It is a reference to an object of type cloud.
    debugvrfcontext:
        description:
            - Configure debug flags for vrf.
            - Field introduced in 17.1.1.
    description:
        description:
            - User defined description for the object.
    gateway_mon:
        description:
            - Configure ping based heartbeat check for gateway in service engines of vrf.
    internal_gateway_monitor:
        description:
            - Configure ping based heartbeat check for all default gateways in service engines of vrf.
            - Field introduced in 17.1.1.
    name:
        description:
            - Name of the object.
        required: true
    static_routes:
        description:
            - List of staticroute.
    system_default:
        description:
            - Boolean flag to set system_default.
            - Default value when not specified in API or module is interpreted by Avi Controller as False.
        type: bool
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
- name: Example to create VrfContext object
  jctanner.network_avi.avi_vrfcontext:
    controller: 10.10.25.42
    username: admin
    password: something
    state: present
    name: sample_vrfcontext
"""

RETURN = '''
obj:
    description: VrfContext (api/vrfcontext) object
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
        bgp_profile=dict(type='dict',),
        cloud_ref=dict(type='str',),
        debugvrfcontext=dict(type='dict',),
        description=dict(type='str',),
        gateway_mon=dict(type='list',),
        internal_gateway_monitor=dict(type='dict',),
        name=dict(type='str', required=True),
        static_routes=dict(type='list',),
        system_default=dict(type='bool',),
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
    return jctanner.network_avi.avi_ansible_api(module, 'vrfcontext',
                           set([]))


if __name__ == '__main__':
    main()
