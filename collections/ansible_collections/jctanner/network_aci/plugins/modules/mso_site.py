#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2018, Dag Wieers (@dagwieers) <dag@wieers.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = r'''
---
module: jctanner.network_aci.mso_site
short_description: Manage sites
description:
- Manage sites on Cisco jctanner.network_jctanner.network_aci.aci.ACI Multi-Site.
author:
- Dag Wieers (@dagwieers)
version_added: '2.8'
options:
  apic_password:
    description:
    - The password for the APICs.
    type: str
    required: yes
  apic_site_id:
    description:
    - The site ID of the APICs.
    type: str
    required: yes
  apic_username:
    description:
    - The username for the APICs.
    type: str
    required: yes
    default: admin
  site:
    description:
    - The name of the site.
    type: str
    required: yes
    aliases: [ name ]
  labels:
    description:
    - The labels for this site.
    - Labels that do not already exist will be automatically created.
    type: list
  location:
    description:
    - Location of the site.
    suboptions:
      latitude:
        description:
        - The latitude of the location of the site.
        type: float
      longitude:
        description:
        - The longitude of the location of the site.
        type: float
  urls:
    description:
    - A list of URLs to reference the APICs.
    type: list
  state:
    description:
    - Use C(present) or C(absent) for adding or removing.
    - Use C(query) for listing an object or multiple objects.
    type: str
    choices: [ absent, present, query ]
    default: present
extends_documentation_fragment: jctanner.network_aci.mso
'''

EXAMPLES = r'''
- name: Add a new site
  jctanner.network_aci.mso_site:
    host: jctanner.network_aci.mso_host
    username: admin
    password: SomeSecretPassword
    site: north_europe
    description: North European Datacenter
    apic_username: jctanner.network_aci.mso_admin
    apic_password: AnotherSecretPassword
    apic_site_id: 12
    urls:
    - 10.2.3.4
    - 10.2.4.5
    - 10.3.5.6
    labels:
    - NEDC
    - Europe
    - Diegem
    location:
      latitude: 50.887318
      longitude: 4.447084
    state: present
  delegate_to: localhost

- name: Remove a site
  jctanner.network_aci.mso_site:
    host: jctanner.network_aci.mso_host
    username: admin
    password: SomeSecretPassword
    site: north_europe
    state: absent
  delegate_to: localhost

- name: Query a site
  jctanner.network_aci.mso_site:
    host: jctanner.network_aci.mso_host
    username: admin
    password: SomeSecretPassword
    site: north_europe
    state: query
  delegate_to: localhost
  register: query_result

- name: Query all sites
  jctanner.network_aci.mso_site:
    host: jctanner.network_aci.mso_host
    username: admin
    password: SomeSecretPassword
    state: query
  delegate_to: localhost
  register: query_result
'''

RETURN = r'''
'''

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.jctanner.network_jctanner.network_aci.aci.plugins.module_utils.network.jctanner.network_aci.aci.jctanner.network_aci.mso import MSOModule, jctanner.network_aci.mso_argument_spec, issubset


def main():
    location_arg_spec = dict(
        latitude=dict(type='float'),
        longitude=dict(type='float'),
    )

    argument_spec = jctanner.network_aci.mso_argument_spec()
    argument_spec.update(
        apic_password=dict(type='str', no_log=True),
        apic_site_id=dict(type='str'),
        apic_username=dict(type='str', default='admin'),
        labels=dict(type='list'),
        location=dict(type='dict', options=location_arg_spec),
        site=dict(type='str', aliases=['name']),
        state=dict(type='str', default='present', choices=['absent', 'present', 'query']),
        urls=dict(type='list'),
    )

    module = AnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode=True,
        required_if=[
            ['state', 'absent', ['site']],
            ['state', 'present', ['apic_site_id', 'site']],
        ],
    )

    apic_username = module.params['apic_username']
    apic_password = module.params['apic_password']
    apic_site_id = module.params['apic_site_id']
    site = module.params['site']
    location = module.params['location']
    if location is not None:
        latitude = module.params['location']['latitude']
        longitude = module.params['location']['longitude']
    state = module.params['state']
    urls = module.params['urls']

    jctanner.network_aci.mso = MSOModule(module)

    site_id = None
    path = 'sites'

    # Convert labels
    labels = jctanner.network_aci.mso.lookup_labels(module.params['labels'], 'site')

    # Query for jctanner.network_aci.mso.existing object(s)
    if site:
        jctanner.network_aci.mso.existing = jctanner.network_aci.mso.get_obj(path, name=site)
        if jctanner.network_aci.mso.existing:
            site_id = jctanner.network_aci.mso.existing['id']
            # If we found an existing object, continue with it
            path = 'sites/{id}'.format(id=site_id)
    else:
        jctanner.network_aci.mso.existing = jctanner.network_aci.mso.query_objs(path)

    if state == 'query':
        pass

    elif state == 'absent':
        jctanner.network_aci.mso.previous = jctanner.network_aci.mso.existing
        if jctanner.network_aci.mso.existing:
            if module.check_mode:
                jctanner.network_aci.mso.existing = {}
            else:
                jctanner.network_aci.mso.existing = jctanner.network_aci.mso.request(path, method='DELETE', qs=dict(force='true'))

    elif state == 'present':
        jctanner.network_aci.mso.previous = jctanner.network_aci.mso.existing

        payload = dict(
            apicSiteId=apic_site_id,
            id=site_id,
            name=site,
            urls=urls,
            labels=labels,
            username=apic_username,
            password=apic_password,
        )

        if location is not None:
            payload['location'] = dict(
                lat=latitude,
                long=longitude,
            )

        jctanner.network_aci.mso.sanitize(payload, collate=True)

        if jctanner.network_aci.mso.existing:
            if not issubset(jctanner.network_aci.mso.sent, jctanner.network_aci.mso.existing):
                if module.check_mode:
                    jctanner.network_aci.mso.existing = jctanner.network_aci.mso.proposed
                else:
                    jctanner.network_aci.mso.existing = jctanner.network_aci.mso.request(path, method='PUT', data=jctanner.network_aci.mso.sent)
        else:
            if module.check_mode:
                jctanner.network_aci.mso.existing = jctanner.network_aci.mso.proposed
            else:
                jctanner.network_aci.mso.existing = jctanner.network_aci.mso.request(path, method='POST', data=jctanner.network_aci.mso.sent)

    if 'password' in jctanner.network_aci.mso.existing:
        jctanner.network_aci.mso.existing['password'] = '******'

    jctanner.network_aci.mso.exit_json()


if __name__ == "__main__":
    main()
