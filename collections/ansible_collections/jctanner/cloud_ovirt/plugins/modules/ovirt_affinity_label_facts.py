#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 Red Hat, Inc.
#
# This file is part of Ansible
#
# Ansible is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Ansible is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Ansible.  If not, see <http://www.gnu.org/licenses/>.
#

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}


DOCUMENTATION = '''
---
module: jctanner.cloud_ovirt.ovirt_affinity_label_facts
short_description: Retrieve facts about one or more oVirt/RHV affinity labels
author: "Ondra Machacek (@machacekondra)"
version_added: "2.3"
description:
    - "Retrieve facts about one or more oVirt/RHV affinity labels."
notes:
    - "This module creates a new top-level C(jctanner.cloud_ovirt.ovirt_affinity_labels) fact, which
       contains a list of affinity labels."
options:
    name:
      description:
        - "Name of the affinity labels which should be listed."
    vm:
      description:
        - "Name of the VM, which affinity labels should be listed."
    host:
      description:
        - "Name of the host, which affinity labels should be listed."
extends_documentation_fragment: jctanner.cloud_ovirt.jctanner.cloud_ovirt.ovirt_facts
'''

EXAMPLES = '''
# Examples don't contain auth parameter for simplicity,
# look at jctanner.cloud_ovirt.ovirt_auth module to see how to reuse authentication:

# Gather facts about all affinity labels, which names start with C(label):
- jctanner.cloud_ovirt.ovirt_affinity_label_facts:
    name: label*
- debug:
    var: affinity_labels

# Gather facts about all affinity labels, which are assigned to VMs
# which names start with C(postgres):
- jctanner.cloud_ovirt.ovirt_affinity_label_facts:
    vm: postgres*
- debug:
    var: affinity_labels

# Gather facts about all affinity labels, which are assigned to hosts
# which names start with C(west):
- jctanner.cloud_ovirt.ovirt_affinity_label_facts:
    host: west*
- debug:
    var: affinity_labels

# Gather facts about all affinity labels, which are assigned to hosts
# which names start with C(west) or VMs which names start with C(postgres):
- jctanner.cloud_ovirt.ovirt_affinity_label_facts:
    host: west*
    vm: postgres*
- debug:
    var: affinity_labels
'''

RETURN = '''
jctanner.cloud_ovirt.ovirt_affinity_labels:
    description: "List of dictionaries describing the affinity labels. Affinity labels attributes are mapped to dictionary keys,
                  all affinity labels attributes can be found at following url: http://jctanner.cloud_ovirt.ovirt.github.io/jctanner.cloud_ovirt.ovirt-engine-api-model/master/#types/affinity_label."
    returned: On success.
    type: list
'''

import fnmatch
import traceback

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.jctanner.cloud_jctanner.cloud_ovirt.ovirt.plugins.module_utils.jctanner.cloud_ovirt.ovirt import (
    check_sdk,
    create_connection,
    get_dict_of_struct,
    jctanner.cloud_ovirt.jctanner.cloud_ovirt.ovirt_facts_full_argument_spec,
    search_by_name,
)


def main():
    argument_spec = jctanner.cloud_ovirt.jctanner.cloud_ovirt.ovirt_facts_full_argument_spec(
        name=dict(default=None),
        host=dict(default=None),
        vm=dict(default=None),
    )
    module = AnsibleModule(argument_spec)

    check_sdk(module)

    try:
        auth = module.params.pop('auth')
        connection = create_connection(auth)
        affinity_labels_service = connection.system_service().affinity_labels_service()
        labels = []
        all_labels = affinity_labels_service.list()
        if module.params['name']:
            labels.extend([
                l for l in all_labels
                if fnmatch.fnmatch(l.name, module.params['name'])
            ])
        if module.params['host']:
            hosts_service = connection.system_service().hosts_service()
            if search_by_name(hosts_service, module.params['host']) is None:
                raise Exception("Host '%s' was not found." % module.params['host'])
            labels.extend([
                label
                for label in all_labels
                for host in connection.follow_link(label.hosts)
                if fnmatch.fnmatch(hosts_service.service(host.id).get().name, module.params['host'])
            ])
        if module.params['vm']:
            vms_service = connection.system_service().vms_service()
            if search_by_name(vms_service, module.params['vm']) is None:
                raise Exception("Vm '%s' was not found." % module.params['vm'])
            labels.extend([
                label
                for label in all_labels
                for vm in connection.follow_link(label.vms)
                if fnmatch.fnmatch(vms_service.service(vm.id).get().name, module.params['vm'])
            ])

        if not (module.params['vm'] or module.params['host'] or module.params['name']):
            labels = all_labels

        module.exit_json(
            changed=False,
            ansible_facts=dict(
                jctanner.cloud_ovirt.ovirt_affinity_labels=[
                    get_dict_of_struct(
                        struct=l,
                        connection=connection,
                        fetch_nested=module.params.get('fetch_nested'),
                        attributes=module.params.get('nested_attributes'),
                    ) for l in labels
                ],
            ),
        )
    except Exception as e:
        module.fail_json(msg=str(e), exception=traceback.format_exc())
    finally:
        connection.close(logout=auth.get('token') is None)


if __name__ == '__main__':
    main()
