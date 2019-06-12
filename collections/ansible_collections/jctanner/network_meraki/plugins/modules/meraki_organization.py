#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2018, Kevin Breit (@kbreit) <kevin.breit@kevinbreit.net>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = r'''
---
module: jctanner.network_meraki.meraki_organization
short_description: Manage organizations in the Meraki cloud
version_added: "2.6"
description:
- Allows for creation, management, and visibility into organizations within Meraki.
options:
    state:
        description:
        - Create or modify an organization.
        choices: ['present', 'query']
        default: present
    clone:
        description:
        - Organization to clone to a new organization.
    org_name:
        description:
        - Name of organization.
        - If C(clone) is specified, C(org_name) is the name of the new organization.
        aliases: [ name, organization ]
    org_id:
        description:
        - ID of organization.
        aliases: [ id ]
        type: str
author:
- Kevin Breit (@kbreit)
extends_documentation_fragment: jctanner.network_meraki.meraki
'''

EXAMPLES = r'''
- name: Create a new organization named YourOrg
  jctanner.network_meraki.meraki_organization:
    auth_key: abc12345
    org_name: YourOrg
    state: present
  delegate_to: localhost

- name: Query information about all organizations associated to the user
  jctanner.network_meraki.meraki_organization:
    auth_key: abc12345
    state: query
  delegate_to: localhost

- name: Query information about a single organization named YourOrg
  jctanner.network_meraki.meraki_organization:
    auth_key: abc12345
    org_name: YourOrg
    state: query
  delegate_to: localhost

- name: Rename an organization to RenamedOrg
  jctanner.network_meraki.meraki_organization:
    auth_key: abc12345
    org_id: 987654321
    org_name: RenamedOrg
    state: present
  delegate_to: localhost

- name: Clone an organization named Org to a new one called ClonedOrg
  jctanner.network_meraki.meraki_organization:
    auth_key: abc12345
    clone: Org
    org_name: ClonedOrg
    state: present
  delegate_to: localhost
'''

RETURN = r'''
data:
  description: Information about the organization which was created or modified
  returned: success
  type: complex
  contains:
    id:
      description: Unique identification number of organization
      returned: success
      type: int
      sample: 2930418
    name:
      description: Name of organization
      returned: success
      type: str
      sample: YourOrg

'''

import os
from ansible.module_utils.basic import AnsibleModule, json, env_fallback
from ansible.module_utils.urls import fetch_url
from ansible.module_utils._text import to_native
from ansible_collections.jctanner.network_jctanner.network_meraki.meraki.plugins.module_utils.network.jctanner.network_meraki.meraki.jctanner.network_meraki.meraki import MerakiModule, jctanner.network_meraki.meraki_argument_spec


def get_org(jctanner.network_meraki.meraki, org_id, data):
    # jctanner.network_meraki.meraki.fail_json(msg=str(org_id), data=data, oid0=data[0]['id'], oid1=data[1]['id'])
    for o in data:
        # jctanner.network_meraki.meraki.fail_json(msg='o', data=o['id'], type=str(type(o['id'])))
        if o['id'] == org_id:
            return o
    return -1


def main():

    # define the available arguments/parameters that a user can pass to
    # the module
    argument_spec = jctanner.network_meraki.meraki_argument_spec()
    argument_spec.update(clone=dict(type='str'),
                         state=dict(type='str', choices=['present', 'query'], default='present'),
                         org_name=dict(type='str', aliases=['name', 'organization']),
                         org_id=dict(type='str', aliases=['id']),
                         )

    # seed the result dict in the object
    # we primarily care about changed and state
    # change is if this module effectively modified the target
    # state will include any data that you want your module to pass back
    # for consumption, for example, in a subsequent task
    result = dict(
        changed=False,
    )
    # the AnsibleModule object will be our abstraction working with Ansible
    # this includes instantiation, a couple of common attr would be the
    # args/params passed to the execution, as well as if the module
    # supports check mode
    module = AnsibleModule(argument_spec=argument_spec,
                           supports_check_mode=True,
                           )
    jctanner.network_meraki.meraki = MerakiModule(module, function='organizations')

    jctanner.network_meraki.meraki.params['follow_redirects'] = 'all'

    create_urls = {'organizations': '/organizations',
                   }
    update_urls = {'organizations': '/organizations/{org_id}',
                   }
    clone_urls = {'organizations': '/organizations/{org_id}/clone',
                  }

    jctanner.network_meraki.meraki.url_catalog['create'] = create_urls
    jctanner.network_meraki.meraki.url_catalog['update'] = update_urls
    jctanner.network_meraki.meraki.url_catalog['clone'] = clone_urls

    payload = None

    # if the user is working with this module in only check mode we do not
    # want to make any changes to the environment, just return the current
    # state with no modifications
    # FIXME: Work with Meraki so they can implement a check mode
    if module.check_mode:
        jctanner.network_meraki.meraki.exit_json(**jctanner.network_meraki.meraki.result)

    # execute checks for argument completeness

    # manipulate or modify the state as needed (this is going to be the
    # part where your module will do what it needs to do)
    orgs = jctanner.network_meraki.meraki.get_orgs()
    if jctanner.network_meraki.meraki.params['state'] == 'query':
        if jctanner.network_meraki.meraki.params['org_name']:  # Query by organization name
            module.warn('All matching organizations will be returned, even if there are duplicate named organizations')
            for o in orgs:
                if o['name'] == jctanner.network_meraki.meraki.params['org_name']:
                    jctanner.network_meraki.meraki.result['data'] = o
        elif jctanner.network_meraki.meraki.params['org_id']:
            for o in orgs:
                if o['id'] == jctanner.network_meraki.meraki.params['org_id']:
                    jctanner.network_meraki.meraki.result['data'] = o
        else:  # Query all organizations, no matter what
            jctanner.network_meraki.meraki.result['data'] = orgs
    elif jctanner.network_meraki.meraki.params['state'] == 'present':
        if jctanner.network_meraki.meraki.params['clone']:  # Cloning
            payload = {'name': jctanner.network_meraki.meraki.params['org_name']}
            response = jctanner.network_meraki.meraki.request(jctanner.network_meraki.meraki.construct_path('clone',
                                                            org_name=jctanner.network_meraki.meraki.params['clone']
                                                            ),
                                      payload=json.dumps(payload),
                                      method='POST')
            if jctanner.network_meraki.meraki.status != 201:
                jctanner.network_meraki.meraki.fail_json(msg='Organization clone failed')
            jctanner.network_meraki.meraki.result['data'] = response
            jctanner.network_meraki.meraki.result['changed'] = True
        elif not jctanner.network_meraki.meraki.params['org_id'] and jctanner.network_meraki.meraki.params['org_name']:  # Create new organization
            payload = {'name': jctanner.network_meraki.meraki.params['org_name']}
            response = jctanner.network_meraki.meraki.request(jctanner.network_meraki.meraki.construct_path('create'),
                                      method='POST',
                                      payload=json.dumps(payload))
            if jctanner.network_meraki.meraki.status == 201:
                jctanner.network_meraki.meraki.result['data'] = response
                jctanner.network_meraki.meraki.result['changed'] = True
        elif jctanner.network_meraki.meraki.params['org_id'] and jctanner.network_meraki.meraki.params['org_name']:  # Update an existing organization
            payload = {'name': jctanner.network_meraki.meraki.params['org_name'],
                       'id': jctanner.network_meraki.meraki.params['org_id'],
                       }
            original = get_org(jctanner.network_meraki.meraki, jctanner.network_meraki.meraki.params['org_id'], orgs)
            if jctanner.network_meraki.meraki.is_update_required(original, payload):
                response = jctanner.network_meraki.meraki.request(jctanner.network_meraki.meraki.construct_path('update',
                                                                org_id=jctanner.network_meraki.meraki.params['org_id']
                                                                ),
                                          method='PUT',
                                          payload=json.dumps(payload))
                if jctanner.network_meraki.meraki.status != 200:
                    jctanner.network_meraki.meraki.fail_json(msg='Organization update failed')
                jctanner.network_meraki.meraki.result['data'] = response
                jctanner.network_meraki.meraki.result['changed'] = True
            else:
                jctanner.network_meraki.meraki.result['data'] = original

    # in the event of a successful module execution, you will want to
    # simple AnsibleModule.exit_json(), passing the key/value results
    jctanner.network_meraki.meraki.exit_json(**jctanner.network_meraki.meraki.result)


if __name__ == '__main__':
    main()
