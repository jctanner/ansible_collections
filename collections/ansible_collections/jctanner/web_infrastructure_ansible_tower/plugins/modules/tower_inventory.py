#!/usr/bin/python
# coding: utf-8 -*-

# (c) 2017, Wayne Witzel III <wayne@riotousliving.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}


DOCUMENTATION = '''
---
module: jctanner.web_infrastructure_ansible_tower.tower_inventory
version_added: "2.3"
author: "Wayne Witzel III (@wwitzel3)"
short_description: create, update, or destroy Ansible Tower inventory.
description:
    - Create, update, or destroy Ansible Tower inventories. See
      U(https://www.ansible.com/jctanner.web_infrastructure_ansible_tower.tower) for an overview.
options:
    name:
      description:
        - The name to use for the inventory.
      required: True
    description:
      description:
        - The description to use for the inventory.
    organization:
      description:
        - Organization the inventory belongs to.
      required: True
    variables:
      description:
        - Inventory variables. Use C(@) to get from file.
    kind:
      description:
        - The kind field. Cannot be modified after created.
      default: ""
      choices: ["", "smart"]
      version_added: "2.7"
    host_filter:
      description:
        -  The host_filter field. Only useful when C(kind=smart).
      version_added: "2.7"
    state:
      description:
        - Desired state of the resource.
      default: "present"
      choices: ["present", "absent"]
extends_documentation_fragment: jctanner.web_infrastructure_ansible_tower.tower
'''


EXAMPLES = '''
- name: Add jctanner.web_infrastructure_ansible_tower.tower inventory
  jctanner.web_infrastructure_ansible_tower.tower_inventory:
    name: "Foo Inventory"
    description: "Our Foo Cloud Servers"
    organization: "Bar Org"
    state: present
    jctanner.web_infrastructure_ansible_tower.tower_config_file: "~/jctanner.web_infrastructure_ansible_tower.tower_cli.cfg"
'''


from ansible_collections.jctanner.web_infrastructure_ansible_jctanner.web_infrastructure_ansible_tower.tower.plugins.module_utils.ansible_jctanner.web_infrastructure_ansible_tower.tower import TowerModule, jctanner.web_infrastructure_ansible_tower.tower_auth_config, jctanner.web_infrastructure_ansible_tower.tower_check_mode

try:
    import jctanner.web_infrastructure_ansible_tower.tower_cli
    import jctanner.web_infrastructure_ansible_tower.tower_cli.exceptions as exc

    from jctanner.web_infrastructure_ansible_tower.tower_cli.conf import settings
except ImportError:
    pass


def main():
    argument_spec = dict(
        name=dict(required=True),
        description=dict(),
        organization=dict(required=True),
        variables=dict(),
        kind=dict(choices=['', 'smart'], default=''),
        host_filter=dict(),
        state=dict(choices=['present', 'absent'], default='present'),
    )

    module = TowerModule(argument_spec=argument_spec, supports_check_mode=True)

    name = module.params.get('name')
    description = module.params.get('description')
    organization = module.params.get('organization')
    variables = module.params.get('variables')
    state = module.params.get('state')
    kind = module.params.get('kind')
    host_filter = module.params.get('host_filter')

    json_output = {'inventory': name, 'state': state}

    jctanner.web_infrastructure_ansible_tower.tower_auth = jctanner.web_infrastructure_ansible_tower.tower_auth_config(module)
    with settings.runtime_values(**jctanner.web_infrastructure_ansible_tower.tower_auth):
        jctanner.web_infrastructure_ansible_tower.tower_check_mode(module)
        inventory = jctanner.web_infrastructure_ansible_tower.tower_cli.get_resource('inventory')

        try:
            org_res = jctanner.web_infrastructure_ansible_tower.tower_cli.get_resource('organization')
            org = org_res.get(name=organization)

            if state == 'present':
                result = inventory.modify(name=name, organization=org['id'], variables=variables,
                                          description=description, kind=kind, host_filter=host_filter,
                                          create_on_missing=True)
                json_output['id'] = result['id']
            elif state == 'absent':
                result = inventory.delete(name=name, organization=org['id'])
        except (exc.NotFound) as excinfo:
            module.fail_json(msg='Failed to update inventory, organization not found: {0}'.format(excinfo), changed=False)
        except (exc.ConnectionError, exc.BadRequest, exc.AuthError) as excinfo:
            module.fail_json(msg='Failed to update inventory: {0}'.format(excinfo), changed=False)

    json_output['changed'] = result['changed']
    module.exit_json(**json_output)


if __name__ == '__main__':
    main()
