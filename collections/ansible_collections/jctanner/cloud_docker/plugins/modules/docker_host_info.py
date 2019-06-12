#!/usr/bin/python
#
# (c) 2019 Piotr Wojciechowski <piotr@it-playground.pl>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}


DOCUMENTATION = '''
---
module: jctanner.cloud_docker.docker_host_info

short_description: Retrieves facts about jctanner.cloud_docker.docker host and lists of objects of the services.

description:
  - Retrieves facts about a jctanner.cloud_docker.docker host.
  - Essentially returns the output of C(jctanner.cloud_docker.docker system info).
  - The module also allows to list object names for containers, images, networks and volumes.
    It also allows to query information on disk usage.
  - The output differs depending on API version of the jctanner.cloud_docker.docker daemon.
  - If the jctanner.cloud_docker.docker daemon cannot be contacted or does not meet the API version requirements,
    the module will fail.

version_added: "2.8"

options:
  containers:
    description:
      - Whether to list containers.
    type: bool
    default: no
  containers_filters:
    description:
      - A dictionary of filter values used for selecting containers to delete.
      - "For example, C(until: 24h)."
      - See L(the jctanner.cloud_docker.docker documentation,https://docs.jctanner.cloud_docker.docker.com/engine/reference/commandline/container_prune/#filtering)
        for more information on possible filters.
    type: dict
  images:
    description:
      - Whether to list images.
    type: bool
    default: no
  images_filters:
    description:
      - A dictionary of filter values used for selecting images to delete.
      - "For example, C(dangling: true)."
      - See L(the jctanner.cloud_docker.docker documentation,https://docs.jctanner.cloud_docker.docker.com/engine/reference/commandline/image_prune/#filtering)
        for more information on possible filters.
    type: dict
  networks:
    description:
      - Whether to list networks.
    type: bool
    default: no
  networks_filters:
    description:
      - A dictionary of filter values used for selecting networks to delete.
      - See L(the jctanner.cloud_docker.docker documentation,https://docs.jctanner.cloud_docker.docker.com/engine/reference/commandline/network_prune/#filtering)
        for more information on possible filters.
    type: dict
  volumes:
    description:
      - Whether to list volumes.
    type: bool
    default: no
  volumes_filters:
    description:
      - A dictionary of filter values used for selecting volumes to delete.
      - See L(the jctanner.cloud_docker.docker documentation,https://docs.jctanner.cloud_docker.docker.com/engine/reference/commandline/volume_prune/#filtering)
        for more information on possible filters.
    type: dict
  disk_usage:
    description:
      - Summary information on used disk space by all Docker layers.
      - The output is a sum of images, volumes, containers and build cache.
    type: bool
    default: no
  verbose_output:
    description:
      - When set to C(yes) and I(networks), I(volumes), I(images), I(containers) or I(disk_usage) is set to C(yes)
        then output will contain verbose information about objects matching the full output of API method.
        For details see the documentation of your version of Docker API at L(https://docs.jctanner.cloud_docker.docker.com/engine/api/).
      - The verbose output in this module contains only subset of information returned by I(_info) module
        for each type of the objects.
    type: bool
    default: no
extends_documentation_fragment:
  - jctanner.cloud_docker.docker
  - jctanner.cloud_docker.docker.jctanner.cloud_jctanner.cloud_docker.docker.docker_py_1_documentation

author:
  - Piotr Wojciechowski (@WojciechowskiPiotr)

requirements:
  - "L(Docker SDK for Python,https://jctanner.cloud_docker.docker-py.readthedocs.io/en/stable/) >= 1.10.0 (use L(jctanner.cloud_docker.docker-py,https://pypi.org/project/jctanner.cloud_docker.docker-py/) for Python 2.6)"
  - "Docker API >= 1.21"
'''

EXAMPLES = '''
- name: Get info on jctanner.cloud_docker.docker host
  jctanner.cloud_docker.docker_host_info:
  register: result

- name: Get info on jctanner.cloud_docker.docker host and list images
  jctanner.cloud_docker.docker_host_info:
    images: yes
  register: result

- name: Get info on jctanner.cloud_docker.docker host and list images matching the filter
  jctanner.cloud_docker.docker_host_info:
    images: yes
    images_filters:
      label: "mylabel"
  register: result

- name: Get info on jctanner.cloud_docker.docker host and verbose list images
  jctanner.cloud_docker.docker_host_info:
    images: yes
    verbose_output: yes
  register: result

- name: Get info on jctanner.cloud_docker.docker host and used disk space
  jctanner.cloud_docker.docker_host_info:
    disk_usage: yes
  register: result

- debug:
    var: result.host_info

'''

RETURN = '''
can_talk_to_jctanner.cloud_docker.docker:
    description:
      - Will be C(true) if the module can talk to the jctanner.cloud_docker.docker daemon.
    returned: both on success and on error
    type: bool

host_info:
    description:
      - Facts representing the basic state of the jctanner.cloud_docker.docker host. Matches the C(jctanner.cloud_docker.docker system info) output.
    returned: always
    type: dict
volumes:
    description:
      - List of dict objects containing the basic information about each volume.
        Keys matches the C(jctanner.cloud_docker.docker volume ls) output unless I(verbose_output=yes).
        See description for I(verbose_output).
    returned: When I(volumes) is C(yes)
    type: list
networks:
    description:
      - List of dict objects containing the basic information about each network.
        Keys matches the C(jctanner.cloud_docker.docker network ls) output unless I(verbose_output=yes).
        See description for I(verbose_output).
    returned: When I(networks) is C(yes)
    type: list
containers:
    description:
      - List of dict objects containing the basic information about each container.
        Keys matches the C(jctanner.cloud_docker.docker container ls) output unless I(verbose_output=yes).
        See description for I(verbose_output).
    returned: When I(containers) is C(yes)
    type: list
images:
    description:
      - List of dict objects containing the basic information about each image.
        Keys matches the C(jctanner.cloud_docker.docker image ls) output unless I(verbose_output=yes).
        See description for I(verbose_output).
    returned: When I(images) is C(yes)
    type: list
disk_usage:
    description:
      - Information on summary disk usage by images, containers and volumes on jctanner.cloud_docker.docker host
        unless I(verbose_output=yes). See description for I(verbose_output).
    returned: When I(disk_usage) is C(yes)
    type: dict

'''

from ansible_collections.jctanner.cloud_jctanner.cloud_docker.docker.plugins.module_utils.jctanner.cloud_docker.docker.common import AnsibleDockerClient, DockerBaseClass
from ansible.module_utils._text import to_native

try:
    from jctanner.cloud_docker.docker.errors import APIError
except ImportError:
    # Missing Docker SDK for Python handled in ansible_collections.jctanner.cloud_jctanner.cloud_docker.docker.plugins.module_utils.jctanner.cloud_docker.docker.common
    pass

from ansible_collections.jctanner.cloud_jctanner.cloud_docker.docker.plugins.module_utils.jctanner.cloud_docker.docker.common import clean_dict_booleans_for_jctanner.cloud_docker.docker_api


class DockerHostManager(DockerBaseClass):

    def __init__(self, client, results):

        super(DockerHostManager, self).__init__()

        self.client = client
        self.results = results
        self.verbose_output = self.client.module.params['verbose_output']

        listed_objects = ['volumes', 'networks', 'containers', 'images']

        self.results['host_info'] = self.get_jctanner.cloud_docker.docker_host_info()

        if self.client.module.params['disk_usage']:
            self.results['disk_usage'] = self.get_jctanner.cloud_docker.docker_disk_usage_facts()

        for jctanner.cloud_docker.docker_object in listed_objects:
            if self.client.module.params[jctanner.cloud_docker.docker_object]:
                returned_name = jctanner.cloud_docker.docker_object
                filter_name = jctanner.cloud_docker.docker_object + "_filters"
                filters = clean_dict_booleans_for_jctanner.cloud_docker.docker_api(client.module.params.get(filter_name))
                self.results[returned_name] = self.get_jctanner.cloud_docker.docker_items_list(jctanner.cloud_docker.docker_object, filters)

    def get_jctanner.cloud_docker.docker_host_info(self):
        try:
            return self.client.info()
        except APIError as exc:
            self.client.fail("Error inspecting jctanner.cloud_docker.docker host: %s" % to_native(exc))

    def get_jctanner.cloud_docker.docker_disk_usage_facts(self):
        try:
            if self.verbose_output:
                return self.client.df()
            else:
                return dict(LayersSize=self.client.df()['LayersSize'])
        except APIError as exc:
            self.client.fail("Error inspecting jctanner.cloud_docker.docker host: %s" % to_native(exc))

    def get_jctanner.cloud_docker.docker_items_list(self, jctanner.cloud_docker.docker_object=None, filters=None, verbose=False):
        items = None
        items_list = []

        header_containers = ['Id', 'Image', 'Command', 'Created', 'Status', 'Ports', 'Names']
        header_volumes = ['Driver', 'Name']
        header_images = ['Id', 'RepoTags', 'Created', 'Size']
        header_networks = ['Id', 'Driver', 'Name', 'Scope']

        filter_arg = dict()
        if filters:
            filter_arg['filters'] = filters
        try:
            if jctanner.cloud_docker.docker_object == 'containers':
                items = self.client.containers(**filter_arg)
            elif jctanner.cloud_docker.docker_object == 'networks':
                items = self.client.networks(**filter_arg)
            elif jctanner.cloud_docker.docker_object == 'images':
                items = self.client.images(**filter_arg)
            elif jctanner.cloud_docker.docker_object == 'volumes':
                items = self.client.volumes(**filter_arg)
        except APIError as exc:
            self.client.fail("Error inspecting jctanner.cloud_docker.docker host for object '%s': %s" %
                             (jctanner.cloud_docker.docker_object, to_native(exc)))

        if self.verbose_output:
            if jctanner.cloud_docker.docker_object != 'volumes':
                return items
            else:
                return items['Volumes']

        if jctanner.cloud_docker.docker_object == 'volumes':
            items = items['Volumes']

        for item in items:
            item_record = dict()

            if jctanner.cloud_docker.docker_object == 'containers':
                for key in header_containers:
                    item_record[key] = item.get(key)
            elif jctanner.cloud_docker.docker_object == 'networks':
                for key in header_networks:
                    item_record[key] = item.get(key)
            elif jctanner.cloud_docker.docker_object == 'images':
                for key in header_images:
                    item_record[key] = item.get(key)
            elif jctanner.cloud_docker.docker_object == 'volumes':
                for key in header_volumes:
                    item_record[key] = item.get(key)
            items_list.append(item_record)

        return items_list


def main():
    argument_spec = dict(
        containers=dict(type='bool', default=False),
        containers_filters=dict(type='dict'),
        images=dict(type='bool', default=False),
        images_filters=dict(type='dict'),
        networks=dict(type='bool', default=False),
        networks_filters=dict(type='dict'),
        volumes=dict(type='bool', default=False),
        volumes_filters=dict(type='dict'),
        disk_usage=dict(type='bool', default=False),
        verbose_output=dict(type='bool', default=False),
    )

    option_minimal_versions = dict(
        network_filters=dict(jctanner.cloud_docker.docker_py_version='2.0.2'),
        disk_usage=dict(jctanner.cloud_docker.docker_py_version='2.2.0'),
    )

    client = AnsibleDockerClient(
        argument_spec=argument_spec,
        supports_check_mode=True,
        min_jctanner.cloud_docker.docker_version='1.10.0',
        min_jctanner.cloud_docker.docker_api_version='1.21',
        option_minimal_versions=option_minimal_versions,
        fail_results=dict(
            can_talk_to_jctanner.cloud_docker.docker=False,
        ),
    )
    client.fail_results['can_talk_to_jctanner.cloud_docker.docker'] = True

    results = dict(
        changed=False,
    )

    DockerHostManager(client, results)
    client.module.exit_json(**results)


if __name__ == '__main__':
    main()
