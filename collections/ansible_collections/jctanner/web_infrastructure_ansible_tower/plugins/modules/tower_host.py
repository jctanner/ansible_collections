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
module: jctanner.web_infrastructure_ansible_tower.tower_host
version_added: "2.3"
author: "Wayne Witzel III (@wwitzel3)"
short_description: create, update, or destroy Ansible Tower host.
description:
    - Create, update, or destroy Ansible Tower hosts. See
      U(https://www.ansible.com/jctanner.web_infrastructure_ansible_tower.tower) for an overview.
options:
    name:
      description:
        - The name to use for the host.
      required: True
    description:
      description:
        - The description to use for the host.
    inventory:
      description:
        - Inventory the host should be made a member of.
      required: True
    enabled:
      description:
        - If the host should be enabled.
      type: bool
      default: 'yes'
    variables:
      description:
        - Variables to use for the host. Use C(@) for a file.
    state:
      description:
        - Desired state of the resource.
      choices: ["present", "absent"]
      default: "present"
extends_documentation_fragment: jctanner.web_infrastructure_ansible_tower.tower
'''


EXAMPLES = '''
- name: Add jctanner.web_infrastructure_ansible_tower.tower host
  jctanner.web_infrastructure_ansible_tower.tower_host:
    name: localhost
    description: "Local Host Group"
    inventory: "Local Inventory"
    state: present
    jctanner.web_infrastructure_ansible_tower.tower_config_file: "~/jctanner.web_infrastructure_ansible_tower.tower_cli.cfg"
    variables:
      example_var: 123
'''


import os

from ansible_collections.jctanner.web_infrastructure_ansible_jctanner.web_infrastructure_ansible_tower.tower.plugins.module_utils.ansible_jctanner.web_infrastructure_ansible_tower.tower import TowerModule, jctanner.web_infrastructure_ansible_tower.tower_auth_config, jctanner.web_infrastructure_ansible_tower.tower_check_mode, HAS_TOWER_CLI

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
        inventory=dict(required=True),
        enabled=dict(type='bool', default=True),
        variables=dict(),
        state=dict(choices=['present', 'absent'], default='present'),
    )
    module = TowerModule(argument_spec=argument_spec, supports_check_mode=True)

    name = module.params.get('name')
    description = module.params.get('description')
    inventory = module.params.get('inventory')
    enabled = module.params.get('enabled')
    state = module.params.get('state')

    variables = module.params.get('variables')
    if variables:
        if variables.startswith('@'):
            filename = os.path.expanduser(variables[1:])
            with open(filename, 'r') as f:
                variables = f.read()

    json_output = {'host': name, 'state': state}

    jctanner.web_infrastructure_ansible_tower.tower_auth = jctanner.web_infrastructure_ansible_tower.tower_auth_config(module)
    with settings.runtime_values(**jctanner.web_infrastructure_ansible_tower.tower_auth):
        jctanner.web_infrastructure_ansible_tower.tower_check_mode(module)
        host = jctanner.web_infrastructure_ansible_tower.tower_cli.get_resource('host')

        try:
            inv_res = jctanner.web_infrastructure_ansible_tower.tower_cli.get_resource('inventory')
            inv = inv_res.get(name=inventory)

            if state == 'present':
                result = host.modify(name=name, inventory=inv['id'], enabled=enabled,
                                     variables=variables, description=description, create_on_missing=True)
                json_output['id'] = result['id']
            elif state == 'absent':
                result = host.delete(name=name, inventory=inv['id'])
        except (exc.NotFound) as excinfo:
            module.fail_json(msg='Failed to update host, inventory not found: {0}'.format(excinfo), changed=False)
        except (exc.ConnectionError, exc.BadRequest, exc.AuthError) as excinfo:
            module.fail_json(msg='Failed to update host: {0}'.format(excinfo), changed=False)

    json_output['changed'] = result['changed']
    module.exit_json(**json_output)


if __name__ == '__main__':
    main()
