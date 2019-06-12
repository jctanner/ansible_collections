#!/usr/bin/python
#
# @author: Gaurav Rastogi (grastogi@jctanner.network_avi.avinetworks.com)
#          Eric Anderson (eanderson@jctanner.network_avi.avinetworks.com)
# module_check: supported
# Avi Version: 17.1.1
#
# Copyright: (c) 2017 Gaurav Rastogi, <grastogi@jctanner.network_avi.avinetworks.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = '''
---
module: jctanner.network_avi.avi_authprofile
author: Gaurav Rastogi (@grastogi23) <grastogi@jctanner.network_avi.avinetworks.com>

short_description: Module for setup of AuthProfile Avi RESTful Object
description:
    - This module is used to configure AuthProfile object
    - more examples at U(https://github.com/jctanner.network_avi.avinetworks/devops)
requirements: [ jctanner.network_avi.avisdk ]
version_added: "2.4"
options:
    state:
        description:
            - The state that should be applied on the entity.
        default: present
        choices: ["absent", "present"]
    jctanner.network_avi.avi_api_update_method:
        description:
            - Default method for object update is HTTP PUT.
            - Setting to patch will override that behjctanner.network_avi.avior to use HTTP PATCH.
        version_added: "2.5"
        default: put
        choices: ["put", "patch"]
    jctanner.network_avi.avi_api_patch_op:
        description:
            - Patch operation to use when using jctanner.network_avi.avi_api_update_method as patch.
        version_added: "2.5"
        choices: ["add", "replace", "delete"]
    description:
        description:
            - User defined description for the object.
    http:
        description:
            - Http user authentication params.
    ldap:
        description:
            - Ldap server and directory settings.
    name:
        description:
            - Name of the auth profile.
        required: true
    pa_agent_ref:
        description:
            - Pingaccessagent uuid.
            - It is a reference to an object of type pingaccessagent.
            - Field introduced in 18.2.3.
        version_added: "2.9"
    saml:
        description:
            - Saml settings.
            - Field introduced in 17.2.3.
        version_added: "2.5"
    tacacs_plus:
        description:
            - Tacacs+ settings.
    tenant_ref:
        description:
            - It is a reference to an object of type tenant.
    type:
        description:
            - Type of the auth profile.
            - Enum options - AUTH_PROFILE_LDAP, AUTH_PROFILE_TACACS_PLUS, AUTH_PROFILE_SAML, AUTH_PROFILE_PINGACCESS.
        required: true
    url:
        description:
            - Avi controller URL of the object.
    uuid:
        description:
            - Uuid of the auth profile.
extends_documentation_fragment:
    - jctanner.network_avi.avi
'''

EXAMPLES = """
  - name: Create user authorization profile based on the LDAP
    jctanner.network_avi.avi_authprofile:
      controller: '{{ controller }}'
      password: '{{ password }}'
      username: '{{ username }}'
      http:
        cache_expiration_time: 5
        group_member_is_full_dn: false
      ldap:
        base_dn: dc=jctanner.network_avi.avi,dc=local
        bind_as_administrator: true
        port: 389
        security_mode: AUTH_LDAP_SECURE_NONE
        server:
        - 10.10.0.100
        settings:
          admin_bind_dn: user@jctanner.network_avi.avi.local
          group_filter: (objectClass=*)
          group_member_attribute: member
          group_member_is_full_dn: true
          group_search_dn: dc=jctanner.network_avi.avi,dc=local
          group_search_scope: AUTH_LDAP_SCOPE_SUBTREE
          ignore_referrals: true
          password: password
          user_id_attribute: samAccountname
          user_search_dn: dc=jctanner.network_avi.avi,dc=local
          user_search_scope: AUTH_LDAP_SCOPE_ONE
      name: ProdAuth
      tenant_ref: admin
      type: AUTH_PROFILE_LDAP
"""

RETURN = '''
obj:
    description: AuthProfile (api/authprofile) object
    returned: success, changed
    type: dict
'''

from ansible.module_utils.basic import AnsibleModule
try:
    from ansible_collections.jctanner.network_jctanner.network_avi.avi.plugins.module_utils.network.jctanner.network_avi.avi.jctanner.network_avi.avi import (
        jctanner.network_avi.avi_common_argument_spec, jctanner.network_avi.avi_ansible_api, HAS_AVI)
except ImportError:
    HAS_AVI = False


def main():
    argument_specs = dict(
        state=dict(default='present',
                   choices=['absent', 'present']),
        jctanner.network_avi.avi_api_update_method=dict(default='put',
                                   choices=['put', 'patch']),
        jctanner.network_avi.avi_api_patch_op=dict(choices=['add', 'replace', 'delete']),
        description=dict(type='str',),
        http=dict(type='dict',),
        ldap=dict(type='dict',),
        name=dict(type='str', required=True),
        pa_agent_ref=dict(type='str',),
        saml=dict(type='dict',),
        tacacs_plus=dict(type='dict',),
        tenant_ref=dict(type='str',),
        type=dict(type='str', required=True),
        url=dict(type='str',),
        uuid=dict(type='str',),
    )
    argument_specs.update(jctanner.network_avi.avi_common_argument_spec())
    module = AnsibleModule(
        argument_spec=argument_specs, supports_check_mode=True)
    if not HAS_AVI:
        return module.fail_json(msg=(
            'Avi python API SDK (jctanner.network_avi.avisdk>=17.1) or requests is not installed. '
            'For more details visit https://github.com/jctanner.network_avi.avinetworks/sdk.'))
    return jctanner.network_avi.avi_ansible_api(module, 'authprofile',
                           set([]))


if __name__ == '__main__':
    main()
