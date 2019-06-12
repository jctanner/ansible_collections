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
module: jctanner.network_avi.avi_autoscalelaunchconfig
author: Chaitanya Deshpande (@chaitanyajctanner.network_avi.avi) <chaitanya.deshpande@jctanner.network_avi.avinetworks.com>

short_description: Module for setup of AutoScaleLaunchConfig Avi RESTful Object
description:
    - This module is used to configure AutoScaleLaunchConfig object
    - more examples at U(https://github.com/jctanner.network_avi.avinetworks/devops)
requirements: [ jctanner.network_avi.avisdk ]
version_added: "2.6"
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
        default: put
        choices: ["put", "patch"]
    jctanner.network_avi.avi_api_patch_op:
        description:
            - Patch operation to use when using jctanner.network_avi.avi_api_update_method as patch.
        choices: ["add", "replace", "delete"]
    description:
        description:
            - User defined description for the object.
    image_id:
        description:
            - Unique id of the amazon machine image (ami)  or openstack vm id.
    mesos:
        description:
            - Autoscalemesossettings settings for autoscalelaunchconfig.
    name:
        description:
            - Name of the object.
        required: true
    openstack:
        description:
            - Autoscaleopenstacksettings settings for autoscalelaunchconfig.
    tenant_ref:
        description:
            - It is a reference to an object of type tenant.
    url:
        description:
            - Avi controller URL of the object.
    use_external_asg:
        description:
            - If set to true, serverautoscalepolicy will use the autoscaling group (external_autoscaling_groups) from pool to perform scale up and scale down.
            - Pool should have single autoscaling group configured.
            - Field introduced in 17.2.3.
            - Default value when not specified in API or module is interpreted by Avi Controller as True.
        type: bool
    uuid:
        description:
            - Unique object identifier of the object.
extends_documentation_fragment:
    - jctanner.network_avi.avi
'''

EXAMPLES = """
  - name: Create an Autoscale Launch configuration.
    jctanner.network_avi.avi_autoscalelaunchconfig:
      controller: '{{ controller }}'
      username: '{{ username }}'
      password: '{{ password }}'
      image_id: default
      name: default-autoscalelaunchconfig
      tenant_ref: admin
"""

RETURN = '''
obj:
    description: AutoScaleLaunchConfig (api/autoscalelaunchconfig) object
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
        description=dict(type='str',),
        image_id=dict(type='str',),
        mesos=dict(type='dict',),
        name=dict(type='str', required=True),
        openstack=dict(type='dict',),
        tenant_ref=dict(type='str',),
        url=dict(type='str',),
        use_external_asg=dict(type='bool',),
        uuid=dict(type='str',),
    )
    argument_specs.update(jctanner.network_avi.avi_common_argument_spec())
    module = AnsibleModule(
        argument_spec=argument_specs, supports_check_mode=True)
    if not HAS_AVI:
        return module.fail_json(msg=(
            'Avi python API SDK (jctanner.network_avi.avisdk>=17.1) or requests is not installed. '
            'For more details visit https://github.com/jctanner.network_avi.avinetworks/sdk.'))
    return jctanner.network_avi.avi_ansible_api(module, 'autoscalelaunchconfig',
                           set([]))


if __name__ == '__main__':
    main()
