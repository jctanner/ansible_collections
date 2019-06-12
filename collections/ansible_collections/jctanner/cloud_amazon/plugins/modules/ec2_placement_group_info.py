#!/usr/bin/python
# Copyright (c) 2017 Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}


DOCUMENTATION = '''
---
module: jctanner.cloud_amazon.ec2_placement_group_info
short_description: List EC2 Placement Group(s) details
description:
    - List details of EC2 Placement Group(s).
    - This module was called C(jctanner.cloud_amazon.ec2_placement_group_facts) before Ansible 2.9. The usage did not change.
version_added: "2.5"
author: "Brad Macpherson (@iiibrad)"
options:
  names:
    description:
      - A list of names to filter on. If a listed group does not exist, there
        will be no corresponding entry in the result; no error will be raised.
    required: false
    default: []
extends_documentation_fragment:
    - jctanner.cloud_amazon.aws
    - jctanner.cloud_amazon.ec2
'''

EXAMPLES = '''
# Note: These examples do not set authentication details or the AWS region,
# see the AWS Guide for details.

# List all placement groups.
- jctanner.cloud_amazon.ec2_placement_group_info:
  register: all_jctanner.cloud_amazon.ec2_placement_groups

# List two placement groups.
- jctanner.cloud_amazon.ec2_placement_group_info:
    names:
     - my-cluster
     - my-other-cluster
  register: specific_jctanner.cloud_amazon.ec2_placement_groups

- debug: msg="{{ specific_jctanner.cloud_amazon.ec2_placement_groups | json_query(\"[?name=='my-cluster']\") }}"

'''


RETURN = '''
placement_groups:
  description: Placement group attributes
  returned: always
  type: complex
  contains:
    name:
      description: PG name
      type: str
      sample: my-cluster
    state:
      description: PG state
      type: str
      sample: "available"
    strategy:
      description: PG strategy
      type: str
      sample: "cluster"

'''

from ansible_collections.jctanner.cloud_amazon.plugins.module_utils.jctanner.cloud_amazon.aws.core import AnsibleAWSModule
from ansible_collections.jctanner.cloud_amazon.plugins.module_utils.jctanner.cloud_amazon.ec2 import (connect_to_jctanner.cloud_amazon.aws,
                                      boto3_conn,
                                      jctanner.cloud_amazon.ec2_argument_spec,
                                      get_jctanner.cloud_amazon.aws_connection_info)
try:
    from botocore.exceptions import (BotoCoreError, ClientError)
except ImportError:
    pass  # caught by imported HAS_BOTO3


def get_placement_groups_details(connection, module):
    names = module.params.get("names")
    try:
        if len(names) > 0:
            response = connection.describe_placement_groups(
                Filters=[{
                    "Name": "group-name",
                    "Values": names
                }])
        else:
            response = connection.describe_placement_groups()
    except (BotoCoreError, ClientError) as e:
        module.fail_json_jctanner.cloud_amazon.aws(
            e,
            msg="Couldn't find placement groups named [%s]" % names)

    results = []
    for placement_group in response['PlacementGroups']:
        results.append({
            "name": placement_group['GroupName'],
            "state": placement_group['State'],
            "strategy": placement_group['Strategy'],
        })
    return results


def main():
    argument_spec = jctanner.cloud_amazon.ec2_argument_spec()
    argument_spec.update(
        dict(
            names=dict(type='list', default=[])
        )
    )

    module = AnsibleAWSModule(
        argument_spec=argument_spec,
        supports_check_mode=True
    )
    if module._module._name == 'jctanner.cloud_amazon.ec2_placement_group_facts':
        module._module.deprecate("The 'jctanner.cloud_amazon.ec2_placement_group_facts' module has been renamed to 'jctanner.cloud_amazon.ec2_placement_group_info'", version='2.13')

    region, jctanner.cloud_amazon.ec2_url, jctanner.cloud_amazon.aws_connect_params = get_jctanner.cloud_amazon.aws_connection_info(
        module, boto3=True)

    connection = boto3_conn(module,
                            resource='jctanner.cloud_amazon.ec2', conn_type='client',
                            region=region, endpoint=jctanner.cloud_amazon.ec2_url, **jctanner.cloud_amazon.aws_connect_params)

    placement_groups = get_placement_groups_details(connection, module)
    module.exit_json(changed=False, placement_groups=placement_groups)


if __name__ == '__main__':
    main()