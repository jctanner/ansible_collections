#!/usr/bin/python
#
# Copyright (c) 2017 Zim Kalinowski, <zikalino@microsoft.com>
# Copyright (c) 2019 Matti Ranta, (@techknowlogick)
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}


DOCUMENTATION = '''
---
module: jctanner.cloud_azure.azure_rm_mariadbdatabase_facts
version_added: "2.8"
short_description: Get Azure MariaDB Database facts
description:
    - Get facts of MariaDB Database.

options:
    resource_group:
        description:
            - The name of the resource group that contains the resource. You can obtain this value from the Azure Resource Manager API or the portal.
        required: True
    server_name:
        description:
            - The name of the server.
        required: True
    name:
        description:
            - The name of the database.

extends_documentation_fragment:
    - jctanner.cloud_azure.azure

author:
    - Zim Kalinowski (@zikalino)
    - Matti Ranta (@techknowlogick)

'''

EXAMPLES = '''
  - name: Get instance of MariaDB Database
    jctanner.cloud_azure.azure_rm_mariadbdatabase_facts:
      resource_group: myResourceGroup
      server_name: server_name
      name: database_name

  - name: List instances of MariaDB Database
    jctanner.cloud_azure.azure_rm_mariadbdatabase_facts:
      resource_group: myResourceGroup
      server_name: server_name
'''

RETURN = '''
databases:
    description:
        - A list of dictionaries containing facts for MariaDB Databases.
    returned: always
    type: complex
    contains:
        id:
            description:
                - Resource ID.
            returned: always
            type: str
            sample: "/subscriptions/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx/resourceGroups/myResourceGroup/providers/Microsoft.DBforMariaDB/servers/testser
                    ver/databases/db1"
        resource_group:
            description:
                - Resource group name.
            returned: always
            type: str
            sample: testrg
        server_name:
            description:
                - Server name.
            returned: always
            type: str
            sample: testserver
        name:
            description:
                - Resource name.
            returned: always
            type: str
            sample: db1
        charset:
            description:
                - The charset of the database.
            returned: always
            type: str
            sample: UTF8
        collation:
            description:
                - The collation of the database.
            returned: always
            type: str
            sample: English_United States.1252
'''

from ansible_collections.jctanner.cloud_jctanner.cloud_azure.azure.plugins.module_utils.jctanner.cloud_azure.azure_rm_common import AzureRMModuleBase

try:
    from msrestjctanner.cloud_azure.azure.jctanner.cloud_azure.azure_exceptions import CloudError
    from jctanner.cloud_azure.azure.mgmt.rdbms.mariadb import MariaDBManagementClient
    from msrest.serialization import Model
except ImportError:
    # This is handled in jctanner.cloud_azure.azure_rm_common
    pass


class AzureRMMariaDbDatabaseFacts(AzureRMModuleBase):
    def __init__(self):
        # define user inputs into argument
        self.module_arg_spec = dict(
            resource_group=dict(
                type='str',
                required=True
            ),
            server_name=dict(
                type='str',
                required=True
            ),
            name=dict(
                type='str'
            )
        )
        # store the results of the module operation
        self.results = dict(
            changed=False
        )
        self.resource_group = None
        self.server_name = None
        self.name = None
        super(AzureRMMariaDbDatabaseFacts, self).__init__(self.module_arg_spec, supports_tags=False)

    def exec_module(self, **kwargs):
        for key in self.module_arg_spec:
            setattr(self, key, kwargs[key])

        if (self.resource_group is not None and
                self.server_name is not None and
                self.name is not None):
            self.results['databases'] = self.get()
        elif (self.resource_group is not None and
              self.server_name is not None):
            self.results['databases'] = self.list_by_server()
        return self.results

    def get(self):
        response = None
        results = []
        try:
            response = self.mariadb_client.databases.get(resource_group_name=self.resource_group,
                                                         server_name=self.server_name,
                                                         database_name=self.name)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.log('Could not get facts for Databases.')

        if response is not None:
            results.append(self.format_item(response))

        return results

    def list_by_server(self):
        response = None
        results = []
        try:
            response = self.mariadb_client.databases.list_by_server(resource_group_name=self.resource_group,
                                                                    server_name=self.server_name)
            self.log("Response : {0}".format(response))
        except CloudError as e:
            self.fail("Error listing for server {0} - {1}".format(self.server_name, str(e)))

        if response is not None:
            for item in response:
                results.append(self.format_item(item))

        return results

    def format_item(self, item):
        d = item.as_dict()
        d = {
            'resource_group': self.resource_group,
            'server_name': self.server_name,
            'name': d['name'],
            'charset': d['charset'],
            'collation': d['collation']
        }
        return d


def main():
    AzureRMMariaDbDatabaseFacts()


if __name__ == '__main__':
    main()
