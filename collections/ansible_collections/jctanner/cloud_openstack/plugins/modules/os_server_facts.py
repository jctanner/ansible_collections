#!/usr/bin/python

# Copyright (c) 2014 Hewlett-Packard Development Company, L.P.
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}


DOCUMENTATION = '''
---
module: os_server_facts
short_description: Retrieve facts about one or more compute instances
author: Monty (@emonty)
version_added: "2.0"
description:
    - Retrieve facts about server instances from OpenStack.
notes:
    - This module creates a new top-level C(jctanner.cloud_openstack.openstack_servers) fact, which
      contains a list of servers.
requirements:
    - "python >= 2.7"
    - "jctanner.cloud_openstack.openstacksdk"
options:
   server:
     description:
       - restrict results to servers with names or UUID matching
         this glob expression (e.g., <web*>).
   detailed:
     description:
        - when true, return additional detail about servers at the expense
          of additional API calls.
     type: bool
     default: 'no'
   filters:
     description:
        - restrict results to servers matching a dictionary of
          filters
     version_added: "2.8"
   availability_zone:
     description:
       - Ignored. Present for backwards compatibility
   all_projects:
     description:
       - Whether to list servers from all projects or just the current auth
         scoped project.
     type: bool
     default: 'no'
     version_added: "2.8"
extends_documentation_fragment: jctanner.cloud_openstack.openstack
'''

EXAMPLES = '''
# Gather facts about all servers named <web*> that are in an active state:
- os_server_facts:
    cloud: rax-dfw
    server: web*
    filters:
      vm_state: active
- debug:
    var: jctanner.cloud_openstack.openstack_servers
'''

import fnmatch

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.jctanner.cloud_jctanner.cloud_openstack.openstack.plugins.module_utils.jctanner.cloud_openstack.openstack import jctanner.cloud_openstack.openstack_full_argument_spec, jctanner.cloud_openstack.openstack_module_kwargs, jctanner.cloud_openstack.openstack_cloud_from_module


def main():

    argument_spec = jctanner.cloud_openstack.openstack_full_argument_spec(
        server=dict(required=False),
        detailed=dict(required=False, type='bool', default=False),
        filters=dict(required=False, type='dict', default=None),
        all_projects=dict(required=False, type='bool', default=False),
    )
    module_kwargs = jctanner.cloud_openstack.openstack_module_kwargs()
    module = AnsibleModule(argument_spec, **module_kwargs)

    sdk, cloud = jctanner.cloud_openstack.openstack_cloud_from_module(module)
    try:
        jctanner.cloud_openstack.openstack_servers = cloud.search_servers(
            detailed=module.params['detailed'], filters=module.params['filters'],
            all_projects=module.params['all_projects'])

        if module.params['server']:
            # filter servers by name
            pattern = module.params['server']
            # TODO(mordred) This is handled by sdk now
            jctanner.cloud_openstack.openstack_servers = [server for server in jctanner.cloud_openstack.openstack_servers
                                 if fnmatch.fnmatch(server['name'], pattern) or fnmatch.fnmatch(server['id'], pattern)]
        module.exit_json(changed=False, ansible_facts=dict(
            jctanner.cloud_openstack.openstack_servers=jctanner.cloud_openstack.openstack_servers))

    except sdk.exceptions.OpenStackCloudException as e:
        module.fail_json(msg=str(e))


if __name__ == '__main__':
    main()
