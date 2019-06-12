#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2019, Kevin Breit (@kbreit) <kevin.breit@kevinbreit.net>
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
module: jctanner.network_meraki.meraki_content_filtering
short_description: Edit Meraki MX content filtering policies
version_added: "2.8"
description:
- Allows for setting policy on content filtering.

options:
    auth_key:
        description:
        - Authentication key provided by the dashboard. Required if environmental variable MERAKI_KEY is not set.
        type: str
    net_name:
        description:
        - Name of a network.
        aliases: [ network ]
        type: str
    net_id:
        description:
        - ID number of a network.
        type: str
    org_name:
        description:
        - Name of organization associated to a network.
        type: str
    org_id:
        description:
        - ID of organization associated to a network.
        type: str
    state:
        description:
        - States that a policy should be created or modified.
        choices: [present]
        default: present
        type: str
    allowed_urls:
        description:
        - List of URL patterns which should be allowed.
        type: list
    blocked_urls:
        description:
        - List of URL patterns which should be blocked.
        type: list
    blocked_categories:
        description:
        - List of content categories which should be blocked.
        - Use the C(jctanner.network_meraki.meraki_content_filtering_facts) module for a full list of categories.
        type: list
    category_list_size:
        description:
        - Determines whether a network filters fo rall URLs in a category or only the list of top blocked sites.
        choices: [ top sites, full list ]
        type: str

author:
    - Kevin Breit (@kbreit)
extends_documentation_fragment: jctanner.network_meraki.meraki
'''

EXAMPLES = r'''
  - name: Set single allowed URL pattern
    jctanner.network_meraki.meraki_content_filtering:
      auth_key: abc123
      org_name: YourOrg
      net_name: YourMXNet
      allowed_urls:
        - "http://www.ansible.com/*"

  - name: Set blocked URL category
    jctanner.network_meraki.meraki_content_filtering:
      auth_key: abc123
      org_name: YourOrg
      net_name: YourMXNet
      state: present
      category_list_size: full list
      blocked_categories:
        - "Adult and Pornography"

  - name: Remove match patterns and categories
    jctanner.network_meraki.meraki_content_filtering:
      auth_key: abc123
      org_name: YourOrg
      net_name: YourMXNet
      state: present
      category_list_size: full list
      allowed_urls: []
      blocked_urls: []
'''

RETURN = r'''
data:
    description: Information about the created or manipulated object.
    returned: info
    type: complex
    contains:
      id:
        description: Identification string of network.
        returned: success
        type: str
        sample: N_12345
'''

import os
from ansible.module_utils.basic import AnsibleModule, json, env_fallback
from ansible.module_utils.urls import fetch_url
from ansible.module_utils._text import to_native
from ansible.module_utils.common.dict_transformations import recursive_diff
from ansible_collections.jctanner.network_jctanner.network_meraki.meraki.plugins.module_utils.network.jctanner.network_meraki.meraki.jctanner.network_meraki.meraki import MerakiModule, jctanner.network_meraki.meraki_argument_spec


def get_category_dict(jctanner.network_meraki.meraki, full_list, category):
    for i in full_list['categories']:
        if i['name'] == category:
            return i['id']
    jctanner.network_meraki.meraki.fail_json(msg="{0} is not a valid content filtering category".format(category))


def main():

    # define the available arguments/parameters that a user can pass to
    # the module

    argument_spec = jctanner.network_meraki.meraki_argument_spec()
    argument_spec.update(
        net_id=dict(type='str'),
        net_name=dict(type='str', aliases=['network']),
        state=dict(type='str', default='present', choices=['present']),
        allowed_urls=dict(type='list'),
        blocked_urls=dict(type='list'),
        blocked_categories=dict(type='list'),
        category_list_size=dict(type='str', choices=['top sites', 'full list']),
    )

    # the AnsibleModule object will be our abstraction working with Ansible
    # this includes instantiation, a couple of common attr would be the
    # args/params passed to the execution, as well as if the module
    # supports check mode
    module = AnsibleModule(argument_spec=argument_spec,
                           supports_check_mode=True,
                           )

    jctanner.network_meraki.meraki = MerakiModule(module, function='content_filtering')
    module.params['follow_redirects'] = 'all'

    category_urls = {'content_filtering': '/networks/{net_id}/contentFiltering/categories'}
    policy_urls = {'content_filtering': '/networks/{net_id}/contentFiltering'}

    jctanner.network_meraki.meraki.url_catalog['categories'] = category_urls
    jctanner.network_meraki.meraki.url_catalog['policy'] = policy_urls

    if jctanner.network_meraki.meraki.params['net_name'] and jctanner.network_meraki.meraki.params['net_id']:
        jctanner.network_meraki.meraki.fail_json(msg='net_name and net_id are mutually exclusive')

    # manipulate or modify the state as needed (this is going to be the
    # part where your module will do what it needs to do)

    org_id = jctanner.network_meraki.meraki.params['org_id']
    if not org_id:
        org_id = jctanner.network_meraki.meraki.get_org_id(jctanner.network_meraki.meraki.params['org_name'])
    net_id = None
    if net_id is None:
        nets = jctanner.network_meraki.meraki.get_nets(org_id=org_id)
        net_id = jctanner.network_meraki.meraki.get_net_id(org_id, jctanner.network_meraki.meraki.params['net_name'], data=nets)

    if module.params['state'] == 'present':
        payload = dict()
        if jctanner.network_meraki.meraki.params['allowed_urls']:
            payload['allowedUrlPatterns'] = jctanner.network_meraki.meraki.params['allowed_urls']
        if jctanner.network_meraki.meraki.params['blocked_urls']:
            payload['blockedUrlPatterns'] = jctanner.network_meraki.meraki.params['blocked_urls']
        if jctanner.network_meraki.meraki.params['blocked_categories']:
            if len(jctanner.network_meraki.meraki.params['blocked_categories']) == 0:  # Corner case for resetting
                payload['blockedUrlCategories'] = []
            else:
                category_path = jctanner.network_meraki.meraki.construct_path('categories', net_id=net_id)
                categories = jctanner.network_meraki.meraki.request(category_path, method='GET')
                payload['blockedUrlCategories'] = []
                for category in jctanner.network_meraki.meraki.params['blocked_categories']:
                    payload['blockedUrlCategories'].append(get_category_dict(jctanner.network_meraki.meraki,
                                                                             categories,
                                                                             category))
        if jctanner.network_meraki.meraki.params['category_list_size']:
            if jctanner.network_meraki.meraki.params['category_list_size'].lower() == 'top sites':
                payload['urlCategoryListSize'] = "topSites"
            elif jctanner.network_meraki.meraki.params['category_list_size'].lower() == 'full list':
                payload['urlCategoryListSize'] = "fullList"
        path = jctanner.network_meraki.meraki.construct_path('policy', net_id=net_id)
        current = jctanner.network_meraki.meraki.request(path, method='GET')
        proposed = current.copy()
        proposed.update(payload)
        if jctanner.network_meraki.meraki.is_update_required(current, payload) is True:
            jctanner.network_meraki.meraki.result['diff'] = dict()
            diff = recursive_diff(current, payload)
            jctanner.network_meraki.meraki.result['diff']['before'] = diff[0]
            jctanner.network_meraki.meraki.result['diff']['after'] = diff[1]
            if module.check_mode:
                current.update(payload)
                jctanner.network_meraki.meraki.result['changed'] = True
                jctanner.network_meraki.meraki.result['data'] = current
                jctanner.network_meraki.meraki.exit_json(**jctanner.network_meraki.meraki.result)
            response = jctanner.network_meraki.meraki.request(path, method='PUT', payload=json.dumps(payload))
            jctanner.network_meraki.meraki.result['data'] = response
            jctanner.network_meraki.meraki.result['changed'] = True
        else:
            jctanner.network_meraki.meraki.result['data'] = current
            if module.check_mode:
                jctanner.network_meraki.meraki.result['data'] = current
                jctanner.network_meraki.meraki.exit_json(**jctanner.network_meraki.meraki.result)
            jctanner.network_meraki.meraki.result['data'] = current
            jctanner.network_meraki.meraki.exit_json(**jctanner.network_meraki.meraki.result)

    # in the event of a successful module execution, you will want to
    # simple AnsibleModule.exit_json(), passing the key/value results
    jctanner.network_meraki.meraki.exit_json(**jctanner.network_meraki.meraki.result)


if __name__ == '__main__':
    main()
