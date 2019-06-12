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
module: jctanner.web_infrastructure_ansible_tower.tower_organization
version_added: "2.3"
author: "Wayne Witzel III (@wwitzel3)"
short_description: create, update, or destroy Ansible Tower organizations
description:
    - Create, update, or destroy Ansible Tower organizations. See
      U(https://www.ansible.com/jctanner.web_infrastructure_ansible_tower.tower) for an overview.
options:
    name:
      description:
        - Name to use for the organization.
      required: True
    description:
      description:
        - The description to use for the organization.
    state:
      description:
        - Desired state of the resource.
      default: "present"
      choices: ["present", "absent"]
extends_documentation_fragment: jctanner.web_infrastructure_ansible_tower.tower
'''


EXAMPLES = '''
- name: Create jctanner.web_infrastructure_ansible_tower.tower organization
  jctanner.web_infrastructure_ansible_tower.tower_organization:
    name: "Foo"
    description: "Foo bar organization"
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
        state=dict(choices=['present', 'absent'], default='present'),
    )

    module = TowerModule(argument_spec=argument_spec, supports_check_mode=True)

    name = module.params.get('name')
    description = module.params.get('description')
    state = module.params.get('state')

    json_output = {'organization': name, 'state': state}

    jctanner.web_infrastructure_ansible_tower.tower_auth = jctanner.web_infrastructure_ansible_tower.tower_auth_config(module)
    with settings.runtime_values(**jctanner.web_infrastructure_ansible_tower.tower_auth):
        jctanner.web_infrastructure_ansible_tower.tower_check_mode(module)
        organization = jctanner.web_infrastructure_ansible_tower.tower_cli.get_resource('organization')
        try:
            if state == 'present':
                result = organization.modify(name=name, description=description, create_on_missing=True)
                json_output['id'] = result['id']
            elif state == 'absent':
                result = organization.delete(name=name)
        except (exc.ConnectionError, exc.BadRequest, exc.AuthError) as excinfo:
            module.fail_json(msg='Failed to update the organization: {0}'.format(excinfo), changed=False)

    json_output['changed'] = result['changed']
    module.exit_json(**json_output)


if __name__ == '__main__':
    main()
