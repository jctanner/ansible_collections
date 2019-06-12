#!/usr/bin/python
# Copyright: Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}


DOCUMENTATION = '''
module: jctanner.cloud_amazon.ec2_vpc_nat_gateway_info
short_description: Retrieves AWS VPC Managed Nat Gateway details using AWS methods.
description:
  - Gets various details related to AWS VPC Managed Nat Gateways
  - This module was called C(jctanner.cloud_amazon.ec2_vpc_nat_gateway_facts) before Ansible 2.9. The usage did not change.
version_added: "2.3"
requirements: [ boto3 ]
options:
  nat_gateway_ids:
    description:
      - Get details of specific nat gateway IDs
  filters:
    description:
      - A dict of filters to apply. Each dict item consists of a filter key and a filter value.
        See U(https://docs.jctanner.cloud_amazon.aws.amazon.com/AWSEC2/latest/APIReference/API_DescribeNatGateways.html)
        for possible filters.
author: Karen Cheng (@Etherdaemon)
extends_documentation_fragment:
  - jctanner.cloud_amazon.aws
  - jctanner.cloud_amazon.ec2
'''

EXAMPLES = '''
# Simple example of listing all nat gateways
- name: List all managed nat gateways in ap-southeast-2
  jctanner.cloud_amazon.ec2_vpc_nat_gateway_info:
    region: ap-southeast-2
  register: all_ngws

- name: Debugging the result
  debug:
    msg: "{{ all_ngws.result }}"

- name: Get details on specific nat gateways
  jctanner.cloud_amazon.ec2_vpc_nat_gateway_info:
    nat_gateway_ids:
      - nat-1234567891234567
      - nat-7654321987654321
    region: ap-southeast-2
  register: specific_ngws

- name: Get all nat gateways with specific filters
  jctanner.cloud_amazon.ec2_vpc_nat_gateway_info:
    region: ap-southeast-2
    filters:
      state: ['pending']
  register: pending_ngws

- name: Get nat gateways with specific filter
  jctanner.cloud_amazon.ec2_vpc_nat_gateway_info:
    region: ap-southeast-2
    filters:
      subnet-id: subnet-12345678
      state: ['available']
  register: existing_nat_gateways
'''

RETURN = '''
result:
  description: The result of the describe, converted to ansible snake case style.
    See http://boto3.readthedocs.io/en/latest/reference/services/jctanner.cloud_amazon.ec2.html#EC2.Client.describe_nat_gateways for the response.
  returned: success
  type: list
'''

import json

try:
    import botocore
except ImportError:
    pass  # will be detected by imported HAS_BOTO3

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.jctanner.cloud_amazon.plugins.module_utils.jctanner.cloud_amazon.ec2 import (jctanner.cloud_amazon.ec2_argument_spec, get_jctanner.cloud_amazon.aws_connection_info, boto3_conn,
                                      camel_dict_to_snake_dict, ansible_dict_to_boto3_filter_list, boto3_tag_list_to_ansible_dict, HAS_BOTO3)


def date_handler(obj):
    return obj.isoformat() if hasattr(obj, 'isoformat') else obj


def get_nat_gateways(client, module, nat_gateway_id=None):
    params = dict()
    nat_gateways = list()

    params['Filter'] = ansible_dict_to_boto3_filter_list(module.params.get('filters'))
    params['NatGatewayIds'] = module.params.get('nat_gateway_ids')

    try:
        result = json.loads(json.dumps(client.describe_nat_gateways(**params), default=date_handler))
    except Exception as e:
        module.fail_json(msg=str(e.message))

    for gateway in result['NatGateways']:
        # Turn the boto3 result into ansible_friendly_snaked_names
        converted_gateway = camel_dict_to_snake_dict(gateway)
        if 'tags' in converted_gateway:
            # Turn the boto3 result into ansible friendly tag dictionary
            converted_gateway['tags'] = boto3_tag_list_to_ansible_dict(converted_gateway['tags'])

        nat_gateways.append(converted_gateway)

    return nat_gateways


def main():
    argument_spec = jctanner.cloud_amazon.ec2_argument_spec()
    argument_spec.update(
        dict(
            filters=dict(default={}, type='dict'),
            nat_gateway_ids=dict(default=[], type='list'),
        )
    )

    module = AnsibleModule(argument_spec=argument_spec,
                           supports_check_mode=True)
    if module._name == 'jctanner.cloud_amazon.ec2_vpc_nat_gateway_facts':
        module.deprecate("The 'jctanner.cloud_amazon.ec2_vpc_nat_gateway_facts' module has been renamed to 'jctanner.cloud_amazon.ec2_vpc_nat_gateway_info'", version='2.13')

    # Validate Requirements
    if not HAS_BOTO3:
        module.fail_json(msg='botocore/boto3 is required.')

    try:
        region, jctanner.cloud_amazon.ec2_url, jctanner.cloud_amazon.aws_connect_params = get_jctanner.cloud_amazon.aws_connection_info(module, boto3=True)
        if region:
            connection = boto3_conn(module, conn_type='client', resource='jctanner.cloud_amazon.ec2', region=region, endpoint=jctanner.cloud_amazon.ec2_url, **jctanner.cloud_amazon.aws_connect_params)
        else:
            module.fail_json(msg="region must be specified")
    except botocore.exceptions.NoCredentialsError as e:
        module.fail_json(msg=str(e))

    results = get_nat_gateways(connection, module)

    module.exit_json(result=results)


if __name__ == '__main__':
    main()
