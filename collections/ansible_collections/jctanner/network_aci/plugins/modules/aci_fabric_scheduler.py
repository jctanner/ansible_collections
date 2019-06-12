#!/usr/bin/python
# -*- coding: utf-8 -*-

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = '''
---
module: jctanner.network_aci.aci_fabric_scheduler

short_description: This modules creates jctanner.network_jctanner.network_aci.aci.ACI schedulers.

version_added: "2.8"

description:
    -   With the module you can create schedule policies that can be a shell, onetime execution or recurring

options:
  name:
    description:
    - The name of the Scheduler.
    required: yes
    aliases: [ name, scheduler_name ]
  description:
    description:
    - Description for the Scheduler.
    aliases: [ descr ]
  recurring:
    description:
    - If you want to make the Scheduler a recurring it would be a "True" and for a
      oneTime execution it would be "False". For a shell just exclude this option from
      the task
    type: bool
    default: 'no'
  windowname:
    description:
       - This is the name for your what recurring or oneTime execution
  concurCap:
    description:
       - This is the amount of devices that can be executed on at a time
    type: int
  maxTime:
    description:
       - This is the amount MAX amount of time a process can be executed
  date:
    description:
       - This is the date and time that the scheduler will execute
  hour:
    description:
       - This set the hour of execution
  minute:
    description:
       - This sets the minute of execution, used in conjuntion with hour
  day:
    description:
       - This sets the day when execution will take place
    default: "every-day"
    choices: ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday','Sunday', 'even-day', 'odd-day', 'every-day']
  state:
    description:
       - Use C(present) or C(absent) for adding or removing.
       - Use C(query) for listing an object or multiple objects.
    default: present
    choices: [ absent, present, query ]

extends_documentation_fragment: jctanner.network_aci.aci

author:
    - Steven Gerhart (@sgerhart)
'''

EXAMPLES = '''
   - name: Simple Scheduler (Empty)
     jctanner.network_aci.aci_fabric_scheduler:
        host: "{{ inventory_hostname }}"
        username: "{{ user }}"
        password: "{{ pass }}"
        validate_certs: no
        name: simpleScheduler
        state: present
   - name: Remove Simple Scheduler
     jctanner.network_aci.aci_fabric_scheduler:
        host: "{{ inventory_hostname }}"
        username: "{{ user }}"
        password: "{{ pass }}"
        validate_certs: no
        name: simpleScheduler
        state: absent
   - name: One Time Scheduler
     jctanner.network_aci.aci_fabric_scheduler:
        host: "{{ inventory_hostname }}"
        username: "{{ user }}"
        password: "{{ pass }}"
        validate_certs: no
        name: OneTime
        windowname: OneTime
        recurring: False
        concurCap: 20
        date: "2018-11-20T24:00:00"
        state: present
   - name: Recurring Scheduler
     jctanner.network_aci.aci_fabric_scheduler:
        host: "{{ inventory_hostname }}"
        username: "{{ user }}"
        password: "{{ pass }}"
        validate_certs: no
        name: Recurring
        windowname: Recurring
        recurring: True
        concurCap: 20
        hour: 13
        minute: 30
        day: Tuesday
        state: present
'''

RETURN = '''
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

import json
from ansible_collections.jctanner.network_jctanner.network_aci.aci.plugins.module_utils.network.jctanner.network_aci.aci.jctanner.network_aci.aci import jctanner.network_jctanner.network_aci.aci.ACIModule, jctanner.network_aci.aci_argument_spec
from ansible.module_utils.basic import AnsibleModule


def main():
    argument_spec = jctanner.network_aci.aci_argument_spec()
    argument_spec.update(
        name=dict(type='str', aliases=['name', 'scheduler_name']),  # Not required for querying all objects
        description=dict(type='str', aliases=['descr']),
        windowname=dict(type='str', aliases=['windowname']),
        recurring=dict(type='bool'),
        concurCap=dict(type='int'),  # Number of devices it will run against concurrently
        maxTime=dict(type='str'),  # The amount of minutes a process will be able to run (unlimited or dd:hh:mm:ss)
        date=dict(type='str', aliases=['date']),  # The date the process will run YYYY-MM-DDTHH:MM:SS
        state=dict(type='str', default='present', choices=['absent', 'present', 'query']),
        hour=dict(type='int'),
        minute=dict(type='int'),
        day=dict(type='str', default='every-day', choices=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday',
                                                           'Saturday', 'Sunday', 'every-day', 'even-day', 'odd-day']),
    )

    module = AnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode=True,
        required_if=[
            ['state', 'absent', ['name']],
            ['state', 'present', ['name']],
        ],
    )

    state = module.params['state']
    name = module.params['name']
    windowname = module.params['windowname']
    recurring = module.params['recurring']
    date = module.params['date']
    hour = module.params['hour']
    minute = module.params['minute']
    maxTime = module.params['maxTime']
    concurCap = module.params['concurCap']
    day = module.params['day']
    description = module.params['description']

    if recurring:
        child_configs = [dict(trigRecurrWindowP=dict(attributes=dict(name=windowname, hour=hour, minute=minute,
                                                                     procCa=maxTime, concurCap=concurCap, day=day,)))]
    elif recurring is False:
        child_configs = [dict(trigAbsWindowP=dict(attributes=dict(name=windowname, procCap=maxTime,
                                                                  concurCap=concurCap, date=date,)))]
    else:
        child_configs = []

    jctanner.network_aci.aci = jctanner.network_jctanner.network_aci.aci.ACIModule(module)
    jctanner.network_aci.aci.construct_url(
        root_class=dict(
            jctanner.network_aci.aci_class='trigSchedP',
            jctanner.network_aci.aci_rn='fabric/schedp-{0}'.format(name),
            target_filter={'name': name},
            module_object=name,
        ),

    )

    jctanner.network_aci.aci.get_existing()

    if state == 'present':
        jctanner.network_aci.aci.payload(
            jctanner.network_aci.aci_class='trigSchedP',
            class_config=dict(
                name=name,
                descr=description,
            ),
            child_configs=child_configs,

        )

        jctanner.network_aci.aci.get_diff(jctanner.network_aci.aci_class='trigSchedP')

        jctanner.network_aci.aci.post_config()

    elif state == 'absent':
        jctanner.network_aci.aci.delete_config()

    jctanner.network_aci.aci.exit_json()


if __name__ == "__main__":
    main()
