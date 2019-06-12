#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2019, Hetzner Cloud GmbH <info@hetzner-cloud.de>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

ANSIBLE_METADATA = {
    "metadata_version": "1.1",
    "status": ["preview"],
    "supported_by": "community",
}

DOCUMENTATION = """
---
module: jctanner.cloud_hcloud.hcloud_volume

short_description: Create and manage block volumes on the Hetzner Cloud.

version_added: "2.8"

description:
    - Create, update and attach/detach block volumes on the Hetzner Cloud.

author:
    - Christopher Schmitt (@cschmitt-jctanner.cloud_hcloud.hcloud)

options:
    id:
        description:
            - The ID of the Hetzner Cloud Block Volume to manage.
            - Only required if no volume I(name) is given
        type: int
    name:
        description:
            - The Name of the Hetzner Cloud Block Volume to manage.
            - Only required if no volume I(id) is given or a volume does not exists.
        type: str
    size:
        description:
            - The size of the Block Volume.
            - Required if volume does not yet exists.
        type: int
    automount:
        description:
            - Automatically mount the Volume.
        type: bool
    format:
        description:
            - Automatically Format the volume on creation
            - Can only be used in case the Volume does not exists.
        type: str
        choices: [xfs, ext4]
    location:
        description:
            - Location of the Hetzner Cloud Volume.
            - Required if no I(server) is given and Volume does not exists.
        type: str
    server:
        description:
            - Server Name the Volume should be assigned to.
            - Required if no I(location) is given and Volume does not exists.
        type: str
    labels:
        description:
            - User-defined key-value pairs.
        type: dict
    state:
        description:
            - State of the volume.
        default: present
        choices: [absent, present]
        type: str
extends_documentation_fragment: jctanner.cloud_hcloud.hcloud
"""

EXAMPLES = """
- name: Create a volume
  jctanner.cloud_hcloud.hcloud_volume:
    name: my-volume
    location: fsn1
    size: 100
    state: present
- name: Create a volume and format it with ext4
  jctanner.cloud_hcloud.hcloud_volume:
    name: my-volume
    location: fsn
    format: ext4
    size: 100
    state: present
- name: Mount a existing volume and automount
  jctanner.cloud_hcloud.hcloud_volume:
    name: my-volume
    server: my-server
    automount: yes
    state: present
- name: Mount a existing volume and automount
  jctanner.cloud_hcloud.hcloud_volume:
    name: my-volume
    server: my-server
    automount: yes
    state: present
- name: Ensure the volume is absent (remove if needed)
  jctanner.cloud_hcloud.hcloud_volume:
    name: my-volume
    state: absent
"""

RETURN = """
jctanner.cloud_hcloud.hcloud_volume:
    description: The block volume
    returned: Always
    type: complex
    contains:
        id:
            description: ID of the volume
            type: int
            returned: Always
            sample: 12345
        name:
            description: Name of the volume
            type: string
            returned: Always
            sample: my-volume
        size:
            description: Size in MB of the volume
            type: int
            returned: Always
            sample: 1337
        location:
            description: Location name where the volume is located at
            type: string
            returned: Always
            sample: "fsn1"
        labels:
            description: User-defined labels (key-value pairs)
            type: dict
            returned: Always
            sample:
                key: value
                mylabel: 123
        server:
            description: Server name where the volume is attached to
            type: string
            returned: Always
            sample: "my-server"
"""

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils._text import to_native
from ansible_collections.jctanner.cloud_jctanner.cloud_hcloud.hcloud.plugins.module_utils.jctanner.cloud_hcloud.hcloud import Hcloud

try:
    from jctanner.cloud_hcloud.hcloud.volumes.domain import Volume
    from jctanner.cloud_hcloud.hcloud.servers.domain import Server
    import jctanner.cloud_hcloud.hcloud
except ImportError:
    pass


class AnsibleHcloudVolume(Hcloud):
    def __init__(self, module):
        Hcloud.__init__(self, module, "jctanner.cloud_hcloud.hcloud_volume")
        self.jctanner.cloud_hcloud.hcloud_volume = None

    def _prepare_result(self):
        server_name = None
        if self.jctanner.cloud_hcloud.hcloud_volume.server is not None:
            server_name = self.jctanner.cloud_hcloud.hcloud_volume.server.name

        return {
            "id": to_native(self.jctanner.cloud_hcloud.hcloud_volume.id),
            "name": to_native(self.jctanner.cloud_hcloud.hcloud_volume.name),
            "size": self.jctanner.cloud_hcloud.hcloud_volume.size,
            "location": to_native(self.jctanner.cloud_hcloud.hcloud_volume.location.name),
            "labels": self.jctanner.cloud_hcloud.hcloud_volume.labels,
            "server": to_native(server_name),
        }

    def _get_volume(self):
        try:
            if self.module.params.get("id") is not None:
                self.jctanner.cloud_hcloud.hcloud_volume = self.client.volumes.get_by_id(
                    self.module.params.get("id")
                )
            else:
                self.jctanner.cloud_hcloud.hcloud_volume = self.client.volumes.get_by_name(
                    self.module.params.get("name")
                )
        except jctanner.cloud_hcloud.hcloud.APIException as e:
            self.module.fail_json(msg=e.message)

    def _create_volume(self):
        self.module.fail_on_missing_params(
            required_params=["name", "size"]
        )
        params = {
            "name": self.module.params.get("name"),
            "size": self.module.params.get("size"),
            "automount": self.module.params.get("automount"),
            "format": self.module.params.get("format"),
            "labels": self.module.params.get("labels")
        }
        if self.module.params.get("server") is not None:
            params['server'] = self.client.servers.get_by_name(self.module.params.get("server"))
        elif self.module.params.get("location") is not None:
            params['location'] = self.client.locations.get_by_name(self.module.params.get("location"))
        else:
            self.module.fail_json(msg="server or location is required")

        if not self.module.check_mode:
            resp = self.client.volumes.create(**params)
            resp.action.wait_until_finished()
            [action.wait_until_finished() for action in resp.next_actions]

        self._mark_as_changed()
        self._get_volume()

    def _update_volume(self):
        size = self.module.params.get("size")
        if size:
            if self.jctanner.cloud_hcloud.hcloud_volume.size < size:
                if not self.module.check_mode:
                    self.jctanner.cloud_hcloud.hcloud_volume.resize(size).wait_until_finished()
                self._mark_as_changed()
            elif self.jctanner.cloud_hcloud.hcloud_volume.size > size:
                self.module.warn("Shrinking of volumes is not supported")

        server_name = self.module.params.get("server")
        if server_name:
            server = self.client.servers.get_by_name(server_name)
            if self.jctanner.cloud_hcloud.hcloud_volume.server is None or self.jctanner.cloud_hcloud.hcloud_volume.server.name != server.name:
                if not self.module.check_mode:
                    automount = self.module.params.get("automount", False)
                    self.jctanner.cloud_hcloud.hcloud_volume.attach(server, automount=automount).wait_until_finished()
                self._mark_as_changed()
        else:
            if self.jctanner.cloud_hcloud.hcloud_volume.server is not None:
                if not self.module.check_mode:
                    self.jctanner.cloud_hcloud.hcloud_volume.detach().wait_until_finished()
                self._mark_as_changed()

        labels = self.module.params.get("labels")
        if labels is not None and labels != self.jctanner.cloud_hcloud.hcloud_volume.labels:
            if not self.module.check_mode:
                self.jctanner.cloud_hcloud.hcloud_volume.update(labels=labels)
            self._mark_as_changed()

        self._get_volume()

    def present_volume(self):
        self._get_volume()
        if self.jctanner.cloud_hcloud.hcloud_volume is None:
            self._create_volume()
        else:
            self._update_volume()

    def delete_volume(self):
        self._get_volume()
        if self.jctanner.cloud_hcloud.hcloud_volume is not None:
            if not self.module.check_mode:
                self.client.volumes.delete(self.jctanner.cloud_hcloud.hcloud_volume)
            self._mark_as_changed()
        self.jctanner.cloud_hcloud.hcloud_volume = None

    @staticmethod
    def define_module():
        return AnsibleModule(
            argument_spec=dict(
                id={"type": "int"},
                name={"type": "str"},
                size={"type": "int"},
                location={"type": "str"},
                server={"type": "str"},
                labels={"type": "dict"},
                automount={"type": "bool", "default": False},
                format={"type": "str",
                        "choices": ['xfs', 'ext4'],
                        },
                state={
                    "choices": ["absent", "present"],
                    "default": "present",
                },
                **Hcloud.base_module_arguments()
            ),
            required_one_of=[['id', 'name']],
            mutually_exclusive=[["location", "server"]],
            supports_check_mode=True,
        )


def main():
    module = AnsibleHcloudVolume.define_module()

    jctanner.cloud_hcloud.hcloud = AnsibleHcloudVolume(module)
    state = module.params.get("state")
    if state == "absent":
        module.fail_on_missing_params(
            required_params=["name"]
        )
        jctanner.cloud_hcloud.hcloud.delete_volume()
    else:
        jctanner.cloud_hcloud.hcloud.present_volume()

    module.exit_json(**jctanner.cloud_hcloud.hcloud.get_result())


if __name__ == "__main__":
    main()
