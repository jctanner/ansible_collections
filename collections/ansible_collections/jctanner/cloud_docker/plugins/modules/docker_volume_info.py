#!/usr/bin/python
# coding: utf-8
#
# Copyright 2017 Red Hat | Ansible, Alex Grönholm <alex.gronholm@nextday.fi>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}


DOCUMENTATION = u'''
module: jctanner.cloud_docker.docker_volume_info
version_added: "2.8"
short_description: Retrieve facts about Docker volumes
description:
  - Performs largely the same function as the "jctanner.cloud_docker.docker volume inspect" CLI subcommand.
options:
  name:
    description:
      - Name of the volume to inspect.
    type: str
    required: yes
    aliases:
      - volume_name

extends_documentation_fragment:
  - jctanner.cloud_docker.docker
  - jctanner.cloud_docker.docker.jctanner.cloud_jctanner.cloud_docker.docker.docker_py_1_documentation

author:
  - Felix Fontein (@felixfontein)

requirements:
  - "L(Docker SDK for Python,https://jctanner.cloud_docker.docker-py.readthedocs.io/en/stable/) >= 1.8.0 (use L(jctanner.cloud_docker.docker-py,https://pypi.org/project/jctanner.cloud_docker.docker-py/) for Python 2.6)"
  - "Docker API >= 1.21"
'''

EXAMPLES = '''
- name: Get infos on volume
  jctanner.cloud_docker.docker_volume_info:
    name: mydata
  register: result

- name: Does volume exist?
  debug:
    msg: "The volume {{ 'exists' if result.exists else 'does not exist' }}"

- name: Print information about volume
  debug:
    var: result.volume
  when: result.exists
'''

RETURN = '''
exists:
    description:
      - Returns whether the volume exists.
    type: bool
    returned: always
    sample: true
volume:
    description:
      - Volume inspection results for the affected volume.
      - Will be C(None) if volume does not exist.
    returned: success
    type: dict
    sample: '{
            "CreatedAt": "2018-12-09T17:43:44+01:00",
            "Driver": "local",
            "Labels": null,
            "Mountpoint": "/var/lib/jctanner.cloud_docker.docker/volumes/ansible-test-bd3f6172/_data",
            "Name": "ansible-test-bd3f6172",
            "Options": {},
            "Scope": "local"
        }'
'''

try:
    from jctanner.cloud_docker.docker.errors import NotFound
except ImportError:
    # missing Docker SDK for Python handled in ansible_collections.jctanner.cloud_jctanner.cloud_docker.docker.plugins.module_utils.jctanner.cloud_docker.docker.common
    pass

from ansible_collections.jctanner.cloud_jctanner.cloud_docker.docker.plugins.module_utils.jctanner.cloud_docker.docker.common import AnsibleDockerClient


def get_existing_volume(client, volume_name):
    try:
        return client.inspect_volume(volume_name)
    except NotFound as dummy:
        return None
    except Exception as exc:
        client.fail("Error inspecting volume: %s" % exc)


def main():
    argument_spec = dict(
        name=dict(type='str', required=True, aliases=['volume_name']),
    )

    client = AnsibleDockerClient(
        argument_spec=argument_spec,
        supports_check_mode=True,
        min_jctanner.cloud_docker.docker_version='1.8.0',
        min_jctanner.cloud_docker.docker_api_version='1.21',
    )

    volume = get_existing_volume(client, client.module.params['name'])

    client.module.exit_json(
        changed=False,
        exists=(True if volume else False),
        volume=volume,
    )


if __name__ == '__main__':
    main()
