#!/usr/bin/python
# coding: utf-8 -*-

# (c) 2017, John Westcott IV <john.westcott.iv@redhat.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}


DOCUMENTATION = '''
---
module: jctanner.web_infrastructure_ansible_tower.tower_send
author: "John Westcott IV (@john-westcott-iv)"
version_added: "2.8"
short_description: Send assets to Ansible Tower.
description:
    - Send assets to Ansible Tower. See
      U(https://www.ansible.com/jctanner.web_infrastructure_ansible_tower.tower) for an overview.
options:
    assets:
      description:
        - The assets to import.
        - This can be the output of jctanner.web_infrastructure_ansible_tower.tower_receive or loaded from a file
      required: False
    files:
      description:
        - List of files to import.
      required: False
      default: []
    prevent:
      description:
        - A list of asset types to prevent import for
      required: false
      default: []
    password_management:
      description:
        - The password management option to use.
        - The prompt option is not supported.
      required: false
      default: 'default'
      choices: ["default", "random"]

notes:
  - One of assets or files needs to be passed in

requirements:
  - "ansible-jctanner.web_infrastructure_ansible_tower.tower-cli >= 3.3.0"
  - six.moves.StringIO
  - sys

extends_documentation_fragment: jctanner.web_infrastructure_ansible_tower.tower
'''

EXAMPLES = '''
- name: Import all jctanner.web_infrastructure_ansible_tower.tower assets
  jctanner.web_infrastructure_ansible_tower.tower_send:
    assets: "{{ export_output.assets }}"
    jctanner.web_infrastructure_ansible_tower.tower_config_file: "~/jctanner.web_infrastructure_ansible_tower.tower_cli.cfg"
'''

RETURN = '''
output:
    description: The import messages
    returned: success, fail
    type: list
    sample: [ 'Message 1', 'Messag 2' ]
'''

import os
import sys

from ansible.module_utils.six.moves import StringIO
from ansible_collections.jctanner.web_infrastructure_ansible_jctanner.web_infrastructure_ansible_tower.tower.plugins.module_utils.ansible_jctanner.web_infrastructure_ansible_tower.tower import TowerModule, jctanner.web_infrastructure_ansible_tower.tower_auth_config, HAS_TOWER_CLI

from tempfile import mkstemp

try:
    from jctanner.web_infrastructure_ansible_tower.tower_cli.cli.transfer.send import Sender
    from jctanner.web_infrastructure_ansible_tower.tower_cli.utils.exceptions import TowerCLIError

    from jctanner.web_infrastructure_ansible_tower.tower_cli.conf import settings
    TOWER_CLI_HAS_EXPORT = True
except ImportError:
    TOWER_CLI_HAS_EXPORT = False


def main():
    argument_spec = dict(
        assets=dict(required=False),
        files=dict(required=False, default=[], type='list'),
        prevent=dict(required=False, default=[], type='list'),
        password_management=dict(required=False, default='default', choices=['default', 'random']),
    )

    module = TowerModule(argument_spec=argument_spec, supports_check_mode=False)

    if not HAS_TOWER_CLI:
        module.fail_json(msg='ansible-jctanner.web_infrastructure_ansible_tower.tower-cli required for this module')

    if not TOWER_CLI_HAS_EXPORT:
        module.fail_json(msg='ansible-jctanner.web_infrastructure_ansible_tower.tower-cli version does not support export')

    assets = module.params.get('assets')
    prevent = module.params.get('prevent')
    password_management = module.params.get('password_management')
    files = module.params.get('files')

    result = dict(
        changed=False,
        msg='',
        output='',
    )

    if not assets and not files:
        result['msg'] = "Assets or files must be specified"
        module.fail_json(**result)

    path = None
    if assets:
        # We got assets so we need to dump this out to a temp file and append that to files
        handle, path = mkstemp(prefix='', suffix='', dir='')
        with open(path, 'w') as f:
            f.write(assets)
        files.append(path)

    jctanner.web_infrastructure_ansible_tower.tower_auth = jctanner.web_infrastructure_ansible_tower.tower_auth_config(module)
    failed = False
    with settings.runtime_values(**jctanner.web_infrastructure_ansible_tower.tower_auth):
        try:
            sender = Sender(no_color=False)
            old_stdout = sys.stdout
            sys.stdout = captured_stdout = StringIO()
            try:
                sender.send(files, prevent, password_management)
            except TypeError as e:
                # Newer versions of TowerCLI require 4 parameters
                sender.send(files, prevent, [], password_management)

            if sender.error_messages > 0:
                failed = True
                result['msg'] = "Transfer Failed with %d errors" % sender.error_messages
            if sender.changed_messages > 0:
                result['changed'] = True
        except TowerCLIError as e:
            result['msg'] = e.message
            failed = True
        finally:
            if path is not None:
                os.remove(path)
            result['output'] = captured_stdout.getvalue().split("\n")
            sys.stdout = old_stdout

    # Return stdout so that module returns will work
    if failed:
        module.fail_json(**result)
    else:
        module.exit_json(**result)


if __name__ == '__main__':
    main()
