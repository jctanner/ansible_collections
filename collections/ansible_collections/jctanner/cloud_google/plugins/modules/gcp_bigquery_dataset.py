#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2017 Google
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
# ----------------------------------------------------------------------------
#
#     ***     AUTO GENERATED CODE    ***    AUTO GENERATED CODE     ***
#
# ----------------------------------------------------------------------------
#
#     This file is automatically generated by Magic Modules and manual
#     changes will be clobbered when the file is regenerated.
#
#     Please read more about how to change this file at
#     https://www.github.com/GoogleCloudPlatform/magic-modules
#
# ----------------------------------------------------------------------------

from __future__ import absolute_import, division, print_function

__metaclass__ = type

################################################################################
# Documentation
################################################################################

ANSIBLE_METADATA = {'metadata_version': '1.1', 'status': ["preview"], 'supported_by': 'community'}

DOCUMENTATION = '''
---
module: jctanner.cloud_google.gcp_bigquery_dataset
description:
- Datasets allow you to organize and control access to your tables.
short_description: Creates a GCP Dataset
version_added: 2.8
author: Google Inc. (@googlecloudplatform)
requirements:
- python >= 2.6
- requests >= 2.18.4
- google-auth >= 1.3.0
options:
  state:
    description:
    - Whether the given object should exist in GCP
    choices:
    - present
    - absent
    default: present
  name:
    description:
    - Dataset name.
    required: false
  access:
    description:
    - Access controls on the bucket.
    required: false
    suboptions:
      domain:
        description:
        - A domain to grant access to. Any users signed in with the domain specified
          will be granted the specified access .
        required: false
      group_by_email:
        description:
        - An email address of a Google Group to grant access to.
        required: false
      role:
        description:
        - Describes the rights granted to the user specified by the other member of
          the access object .
        - 'Some valid choices include: "READER", "WRITER", "OWNER"'
        required: false
      special_group:
        description:
        - A special group to grant access to.
        required: false
      user_by_email:
        description:
        - 'An email address of a user to grant access to. For example: fred@example.com
          .'
        required: false
      view:
        description:
        - A view from a different dataset to grant access to. Queries executed against
          that view will have read access to tables in this dataset. The role field
          is not required when this field is set. If that view is updated by any user,
          access to the view needs to be granted again via an update operation.
        required: false
        suboptions:
          dataset_id:
            description:
            - The ID of the dataset containing this table.
            required: true
          project_id:
            description:
            - The ID of the project containing this table.
            required: true
          table_id:
            description:
            - The ID of the table. The ID must contain only letters (a-z, A-Z), numbers
              (0-9), or underscores. The maximum length is 1,024 characters.
            required: true
  dataset_reference:
    description:
    - A reference that identifies the dataset.
    required: true
    suboptions:
      dataset_id:
        description:
        - A unique ID for this dataset, without the project name. The ID must contain
          only letters (a-z, A-Z), numbers (0-9), or underscores. The maximum length
          is 1,024 characters.
        required: true
      project_id:
        description:
        - The ID of the project containing this dataset.
        required: false
  default_table_expiration_ms:
    description:
    - The default lifetime of all tables in the dataset, in milliseconds .
    required: false
  description:
    description:
    - A user-friendly description of the dataset.
    required: false
  friendly_name:
    description:
    - A descriptive name for the dataset.
    required: false
  labels:
    description:
    - The labels associated with this dataset. You can use these to organize and group
      your datasets .
    required: false
  location:
    description:
    - The geographic location where the dataset should reside. Possible values include
      EU and US. The default value is US.
    required: false
    default: US
extends_documentation_fragment: jctanner.cloud_google.gcp
'''

EXAMPLES = '''
- name: create a dataset
  jctanner.cloud_google.gcp_bigquery_dataset:
    name: my_example_dataset
    dataset_reference:
      dataset_id: my_example_dataset
    project: test_project
    auth_kind: serviceaccount
    service_account_file: "/tmp/auth.pem"
    state: present
'''

RETURN = '''
name:
  description:
  - Dataset name.
  returned: success
  type: str
access:
  description:
  - Access controls on the bucket.
  returned: success
  type: complex
  contains:
    domain:
      description:
      - A domain to grant access to. Any users signed in with the domain specified
        will be granted the specified access .
      returned: success
      type: str
    groupByEmail:
      description:
      - An email address of a Google Group to grant access to.
      returned: success
      type: str
    role:
      description:
      - Describes the rights granted to the user specified by the other member of
        the access object .
      returned: success
      type: str
    specialGroup:
      description:
      - A special group to grant access to.
      returned: success
      type: str
    userByEmail:
      description:
      - 'An email address of a user to grant access to. For example: fred@example.com
        .'
      returned: success
      type: str
    view:
      description:
      - A view from a different dataset to grant access to. Queries executed against
        that view will have read access to tables in this dataset. The role field
        is not required when this field is set. If that view is updated by any user,
        access to the view needs to be granted again via an update operation.
      returned: success
      type: complex
      contains:
        datasetId:
          description:
          - The ID of the dataset containing this table.
          returned: success
          type: str
        projectId:
          description:
          - The ID of the project containing this table.
          returned: success
          type: str
        tableId:
          description:
          - The ID of the table. The ID must contain only letters (a-z, A-Z), numbers
            (0-9), or underscores. The maximum length is 1,024 characters.
          returned: success
          type: str
creationTime:
  description:
  - The time when this dataset was created, in milliseconds since the epoch.
  returned: success
  type: int
datasetReference:
  description:
  - A reference that identifies the dataset.
  returned: success
  type: complex
  contains:
    datasetId:
      description:
      - A unique ID for this dataset, without the project name. The ID must contain
        only letters (a-z, A-Z), numbers (0-9), or underscores. The maximum length
        is 1,024 characters.
      returned: success
      type: str
    projectId:
      description:
      - The ID of the project containing this dataset.
      returned: success
      type: str
defaultTableExpirationMs:
  description:
  - The default lifetime of all tables in the dataset, in milliseconds .
  returned: success
  type: int
description:
  description:
  - A user-friendly description of the dataset.
  returned: success
  type: str
friendlyName:
  description:
  - A descriptive name for the dataset.
  returned: success
  type: str
id:
  description:
  - The fully-qualified unique name of the dataset in the format projectId:datasetId.
    The dataset name without the project name is given in the datasetId field .
  returned: success
  type: str
labels:
  description:
  - The labels associated with this dataset. You can use these to organize and group
    your datasets .
  returned: success
  type: dict
lastModifiedTime:
  description:
  - The date when this dataset or any of its tables was last modified, in milliseconds
    since the epoch.
  returned: success
  type: int
location:
  description:
  - The geographic location where the dataset should reside. Possible values include
    EU and US. The default value is US.
  returned: success
  type: str
'''

################################################################################
# Imports
################################################################################

from ansible_collections.jctanner.cloud_google.plugins.module_utils.jctanner.cloud_google.gcp_utils import navigate_hash, GcpSession, GcpModule, GcpRequest, remove_nones_from_dict, replace_resource_dict
import json

################################################################################
# Main
################################################################################


def main():
    """Main function"""

    module = GcpModule(
        argument_spec=dict(
            state=dict(default='present', choices=['present', 'absent'], type='str'),
            name=dict(type='str'),
            access=dict(
                type='list',
                elements='dict',
                options=dict(
                    domain=dict(type='str'),
                    group_by_email=dict(type='str'),
                    role=dict(type='str'),
                    special_group=dict(type='str'),
                    user_by_email=dict(type='str'),
                    view=dict(
                        type='dict',
                        options=dict(
                            dataset_id=dict(required=True, type='str'), project_id=dict(required=True, type='str'), table_id=dict(required=True, type='str')
                        ),
                    ),
                ),
            ),
            dataset_reference=dict(required=True, type='dict', options=dict(dataset_id=dict(required=True, type='str'), project_id=dict(type='str'))),
            default_table_expiration_ms=dict(type='int'),
            description=dict(type='str'),
            friendly_name=dict(type='str'),
            labels=dict(type='dict'),
            location=dict(default='US', type='str'),
        )
    )

    if not module.params['scopes']:
        module.params['scopes'] = ['https://www.googleapis.com/auth/bigquery']

    state = module.params['state']
    kind = 'bigquery#dataset'

    fetch = fetch_resource(module, self_link(module), kind)
    changed = False

    if fetch:
        if state == 'present':
            if is_different(module, fetch):
                update(module, self_link(module), kind)
                fetch = fetch_resource(module, self_link(module), kind)
                changed = True
        else:
            delete(module, self_link(module), kind)
            fetch = {}
            changed = True
    else:
        if state == 'present':
            fetch = create(module, collection(module), kind)
            changed = True
        else:
            fetch = {}

    fetch.update({'changed': changed})

    module.exit_json(**fetch)


def create(module, link, kind):
    auth = GcpSession(module, 'bigquery')
    return return_if_object(module, auth.post(link, resource_to_request(module)), kind)


def update(module, link, kind):
    auth = GcpSession(module, 'bigquery')
    return return_if_object(module, auth.put(link, resource_to_request(module)), kind)


def delete(module, link, kind):
    auth = GcpSession(module, 'bigquery')
    return return_if_object(module, auth.delete(link), kind)


def resource_to_request(module):
    request = {
        u'kind': 'bigquery#dataset',
        u'name': module.params.get('name'),
        u'access': DatasetAccessArray(module.params.get('access', []), module).to_request(),
        u'datasetReference': DatasetDatasetreference(module.params.get('dataset_reference', {}), module).to_request(),
        u'defaultTableExpirationMs': module.params.get('default_table_expiration_ms'),
        u'description': module.params.get('description'),
        u'friendlyName': module.params.get('friendly_name'),
        u'labels': module.params.get('labels'),
        u'location': module.params.get('location'),
    }
    return_vals = {}
    for k, v in request.items():
        if v or v is False:
            return_vals[k] = v

    return return_vals


def fetch_resource(module, link, kind, allow_not_found=True):
    auth = GcpSession(module, 'bigquery')
    return return_if_object(module, auth.get(link), kind, allow_not_found)


def self_link(module):
    return "https://www.googleapis.com/bigquery/v2/projects/{project}/datasets/{name}".format(**module.params)


def collection(module):
    return "https://www.googleapis.com/bigquery/v2/projects/{project}/datasets".format(**module.params)


def return_if_object(module, response, kind, allow_not_found=False):
    # If not found, return nothing.
    if allow_not_found and response.status_code == 404:
        return None

    # If no content, return nothing.
    if response.status_code == 204:
        return None

    try:
        module.raise_for_status(response)
        result = response.json()
    except getattr(json.decoder, 'JSONDecodeError', ValueError):
        module.fail_json(msg="Invalid JSON response with error: %s" % response.text)

    if navigate_hash(result, ['error', 'errors']):
        module.fail_json(msg=navigate_hash(result, ['error', 'errors']))

    return result


def is_different(module, response):
    request = resource_to_request(module)
    response = response_to_hash(module, response)

    # Remove all output-only from response.
    response_vals = {}
    for k, v in response.items():
        if k in request:
            response_vals[k] = v

    request_vals = {}
    for k, v in request.items():
        if k in response:
            request_vals[k] = v

    return GcpRequest(request_vals) != GcpRequest(response_vals)


# Remove unnecessary properties from the response.
# This is for doing comparisons with Ansible's current parameters.
def response_to_hash(module, response):
    return {
        u'name': response.get(u'name'),
        u'access': DatasetAccessArray(response.get(u'access', []), module).from_response(),
        u'creationTime': response.get(u'creationTime'),
        u'datasetReference': DatasetDatasetreference(response.get(u'datasetReference', {}), module).from_response(),
        u'defaultTableExpirationMs': response.get(u'defaultTableExpirationMs'),
        u'description': response.get(u'description'),
        u'friendlyName': response.get(u'friendlyName'),
        u'id': response.get(u'id'),
        u'labels': response.get(u'labels'),
        u'lastModifiedTime': response.get(u'lastModifiedTime'),
        u'location': response.get(u'location'),
    }


class DatasetAccessArray(object):
    def __init__(self, request, module):
        self.module = module
        if request:
            self.request = request
        else:
            self.request = []

    def to_request(self):
        items = []
        for item in self.request:
            items.append(self._request_for_item(item))
        return items

    def from_response(self):
        items = []
        for item in self.request:
            items.append(self._response_from_item(item))
        return items

    def _request_for_item(self, item):
        return remove_nones_from_dict(
            {
                u'domain': item.get('domain'),
                u'groupByEmail': item.get('group_by_email'),
                u'role': item.get('role'),
                u'specialGroup': item.get('special_group'),
                u'userByEmail': item.get('user_by_email'),
                u'view': DatasetView(item.get('view', {}), self.module).to_request(),
            }
        )

    def _response_from_item(self, item):
        return remove_nones_from_dict(
            {
                u'domain': item.get(u'domain'),
                u'groupByEmail': item.get(u'groupByEmail'),
                u'role': item.get(u'role'),
                u'specialGroup': item.get(u'specialGroup'),
                u'userByEmail': item.get(u'userByEmail'),
                u'view': DatasetView(item.get(u'view', {}), self.module).from_response(),
            }
        )


class DatasetView(object):
    def __init__(self, request, module):
        self.module = module
        if request:
            self.request = request
        else:
            self.request = {}

    def to_request(self):
        return remove_nones_from_dict(
            {u'datasetId': self.request.get('dataset_id'), u'projectId': self.request.get('project_id'), u'tableId': self.request.get('table_id')}
        )

    def from_response(self):
        return remove_nones_from_dict(
            {u'datasetId': self.request.get(u'datasetId'), u'projectId': self.request.get(u'projectId'), u'tableId': self.request.get(u'tableId')}
        )


class DatasetDatasetreference(object):
    def __init__(self, request, module):
        self.module = module
        if request:
            self.request = request
        else:
            self.request = {}

    def to_request(self):
        return remove_nones_from_dict({u'datasetId': self.request.get('dataset_id'), u'projectId': self.request.get('project_id')})

    def from_response(self):
        return remove_nones_from_dict({u'datasetId': self.request.get(u'datasetId'), u'projectId': self.request.get(u'projectId')})


if __name__ == '__main__':
    main()
