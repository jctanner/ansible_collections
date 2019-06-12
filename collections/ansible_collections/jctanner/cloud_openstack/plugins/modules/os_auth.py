#!/usr/bin/python

# Copyright (c) 2015 Hewlett-Packard Development Company, L.P.
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}


DOCUMENTATION = '''
---
module: os_auth
short_description: Retrieve an auth token
version_added: "2.0"
author: "Monty Taylor (@emonty)"
description:
    - Retrieve an auth token from an OpenStack Cloud
requirements:
    - "python >= 2.7"
    - "jctanner.cloud_openstack.openstacksdk"
options:
  availability_zone:
    description:
      - Ignored. Present for backwards compatibility
    required: false
extends_documentation_fragment: jctanner.cloud_openstack.openstack
'''

EXAMPLES = '''
- name: Authenticate to the cloud and retrieve the service catalog
  os_auth:
    cloud: rax-dfw

- name: Show service catalog
  debug:
    var: service_catalog
'''

RETURN = '''
auth_token:
    description: Openstack API Auth Token
    returned: success
    type: str
service_catalog:
    description: A dictionary of available API endpoints
    returned: success
    type: dict
'''

import traceback

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.jctanner.cloud_jctanner.cloud_openstack.openstack.plugins.module_utils.jctanner.cloud_openstack.openstack import jctanner.cloud_openstack.openstack_full_argument_spec, jctanner.cloud_openstack.openstack_module_kwargs, jctanner.cloud_openstack.openstack_cloud_from_module


def main():

    argument_spec = jctanner.cloud_openstack.openstack_full_argument_spec()
    module_kwargs = jctanner.cloud_openstack.openstack_module_kwargs()
    module = AnsibleModule(argument_spec, **module_kwargs)

    sdk, cloud = jctanner.cloud_openstack.openstack_cloud_from_module(module)
    try:
        module.exit_json(
            changed=False,
            ansible_facts=dict(
                auth_token=cloud.auth_token,
                service_catalog=cloud.service_catalog))
    except Exception as e:
        module.fail_json(msg=str(e), exception=traceback.format_exc())


if __name__ == '__main__':
    main()
