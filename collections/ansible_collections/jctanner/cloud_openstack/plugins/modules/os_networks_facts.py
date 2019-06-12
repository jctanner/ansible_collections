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
module: os_networks_facts
short_description: Retrieve facts about one or more OpenStack networks.
version_added: "2.0"
author: "Davide Agnello (@dagnello)"
description:
    - Retrieve facts about one or more networks from OpenStack.
requirements:
    - "python >= 2.7"
    - "sdk"
options:
   name:
     description:
        - Name or ID of the Network
     required: false
   filters:
     description:
        - A dictionary of meta data to use for further filtering.  Elements of
          this dictionary may be additional dictionaries.
     required: false
   availability_zone:
     description:
       - Ignored. Present for backwards compatibility
     required: false
extends_documentation_fragment: jctanner.cloud_openstack.openstack
'''

EXAMPLES = '''
- name: Gather facts about previously created networks
  os_networks_facts:
    auth:
      auth_url: https://identity.example.com
      username: user
      password: password
      project_name: someproject

- name: Show jctanner.cloud_openstack.openstack networks
  debug:
    var: jctanner.cloud_openstack.openstack_networks

- name: Gather facts about a previously created network by name
  os_networks_facts:
    auth:
      auth_url: https://identity.example.com
      username: user
      password: password
      project_name: someproject
    name:  network1

- name: Show jctanner.cloud_openstack.openstack networks
  debug:
    var: jctanner.cloud_openstack.openstack_networks

- name: Gather facts about a previously created network with filter
  # Note: name and filters parameters are Not mutually exclusive
  os_networks_facts:
    auth:
      auth_url: https://identity.example.com
      username: user
      password: password
      project_name: someproject
    filters:
      tenant_id: 55e2ce24b2a245b09f181bf025724cbe
      subnets:
        - 057d4bdf-6d4d-4728-bb0f-5ac45a6f7400
        - 443d4dc0-91d4-4998-b21c-357d10433483

- name: Show jctanner.cloud_openstack.openstack networks
  debug:
    var: jctanner.cloud_openstack.openstack_networks
'''

RETURN = '''
jctanner.cloud_openstack.openstack_networks:
    description: has all the jctanner.cloud_openstack.openstack facts about the networks
    returned: always, but can be null
    type: complex
    contains:
        id:
            description: Unique UUID.
            returned: success
            type: str
        name:
            description: Name given to the network.
            returned: success
            type: str
        status:
            description: Network status.
            returned: success
            type: str
        subnets:
            description: Subnet(s) included in this network.
            returned: success
            type: list of strings
        tenant_id:
            description: Tenant id associated with this network.
            returned: success
            type: str
        shared:
            description: Network shared flag.
            returned: success
            type: bool
'''

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.jctanner.cloud_jctanner.cloud_openstack.openstack.plugins.module_utils.jctanner.cloud_openstack.openstack import jctanner.cloud_openstack.openstack_full_argument_spec, jctanner.cloud_openstack.openstack_cloud_from_module


def main():

    argument_spec = jctanner.cloud_openstack.openstack_full_argument_spec(
        name=dict(required=False, default=None),
        filters=dict(required=False, type='dict', default=None)
    )
    module = AnsibleModule(argument_spec)

    sdk, cloud = jctanner.cloud_openstack.openstack_cloud_from_module(module)
    try:
        networks = cloud.search_networks(module.params['name'],
                                         module.params['filters'])
        module.exit_json(changed=False, ansible_facts=dict(
            jctanner.cloud_openstack.openstack_networks=networks))

    except sdk.exceptions.OpenStackCloudException as e:
        module.fail_json(msg=str(e))


if __name__ == '__main__':
    main()
