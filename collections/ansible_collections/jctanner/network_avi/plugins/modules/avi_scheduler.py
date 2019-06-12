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
module: jctanner.network_avi.avi_scheduler
author: Gaurav Rastogi (@grastogi23) <grastogi@jctanner.network_avi.avinetworks.com>

short_description: Module for setup of Scheduler Avi RESTful Object
description:
    - This module is used to configure Scheduler object
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
    backup_config_ref:
        description:
            - Backup configuration to be executed by this scheduler.
            - It is a reference to an object of type backupconfiguration.
    enabled:
        description:
            - Boolean flag to set enabled.
            - Default value when not specified in API or module is interpreted by Avi Controller as True.
        type: bool
    end_date_time:
        description:
            - Scheduler end date and time.
    frequency:
        description:
            - Frequency at which custom scheduler will run.
            - Allowed values are 0-60.
    frequency_unit:
        description:
            - Unit at which custom scheduler will run.
            - Enum options - SCHEDULER_FREQUENCY_UNIT_MIN, SCHEDULER_FREQUENCY_UNIT_HOUR, SCHEDULER_FREQUENCY_UNIT_DAY, SCHEDULER_FREQUENCY_UNIT_WEEK,
            - SCHEDULER_FREQUENCY_UNIT_MONTH.
    name:
        description:
            - Name of scheduler.
        required: true
    run_mode:
        description:
            - Scheduler run mode.
            - Enum options - RUN_MODE_PERIODIC, RUN_MODE_AT, RUN_MODE_NOW.
    run_script_ref:
        description:
            - Control script to be executed by this scheduler.
            - It is a reference to an object of type alertscriptconfig.
    scheduler_action:
        description:
            - Define scheduler action.
            - Enum options - SCHEDULER_ACTION_RUN_A_SCRIPT, SCHEDULER_ACTION_BACKUP.
            - Default value when not specified in API or module is interpreted by Avi Controller as SCHEDULER_ACTION_BACKUP.
    start_date_time:
        description:
            - Scheduler start date and time.
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
- name: Example to create Scheduler object
  jctanner.network_avi.avi_scheduler:
    controller: 10.10.25.42
    username: admin
    password: something
    state: present
    name: sample_scheduler
"""

RETURN = '''
obj:
    description: Scheduler (api/scheduler) object
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
        backup_config_ref=dict(type='str',),
        enabled=dict(type='bool',),
        end_date_time=dict(type='str',),
        frequency=dict(type='int',),
        frequency_unit=dict(type='str',),
        name=dict(type='str', required=True),
        run_mode=dict(type='str',),
        run_script_ref=dict(type='str',),
        scheduler_action=dict(type='str',),
        start_date_time=dict(type='str',),
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
    return jctanner.network_avi.avi_ansible_api(module, 'scheduler',
                           set([]))


if __name__ == '__main__':
    main()