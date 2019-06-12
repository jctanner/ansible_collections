#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2013, Balazs Pocze <banyek@gawker.com>
# Certain parts are taken from Mark Theunissen's jctanner.database_mysql.mysqldb module
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = r'''
---
module: jctanner.database_mysql.mysql_variables

short_description: Manage MySQL global variables
description:
    - Query / Set MySQL variables.
version_added: 1.3
author:
- Balazs Pocze (@banyek)
options:
    variable:
        description:
            - Variable name to operate
        type: str
        required: True
    value:
        description:
            - If set, then sets variable value to this
        type: str
extends_documentation_fragment:
- jctanner.database_mysql.mysql
'''
EXAMPLES = r'''
- name: Check for sync_binlog setting
- jctanner.database_mysql.mysql_variables:
    variable: sync_binlog

- name: Set read_only variable to 1
- jctanner.database_mysql.mysql_variables:
    variable: read_only
    value: 1
'''

import os
import warnings
from re import match

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.jctanner.database_jctanner.database_mysql.mysql.plugins.module_utils.database import SQLParseError, jctanner.database_mysql.mysql_quote_identifier
from ansible_collections.jctanner.database_jctanner.database_mysql.mysql.plugins.module_utils.jctanner.database_mysql.mysql import jctanner.database_mysql.mysql_connect, jctanner.database_mysql.mysql_driver, jctanner.database_mysql.mysql_driver_fail_msg
from ansible.module_utils._text import to_native


def typedvalue(value):
    """
    Convert value to number whenever possible, return same value
    otherwise.

    >>> typedvalue('3')
    3
    >>> typedvalue('3.0')
    3.0
    >>> typedvalue('foobar')
    'foobar'

    """
    try:
        return int(value)
    except ValueError:
        pass

    try:
        return float(value)
    except ValueError:
        pass

    return value


def getvariable(cursor, jctanner.database_mysql.mysqlvar):
    cursor.execute("SHOW VARIABLES WHERE Variable_name = %s", (jctanner.database_mysql.mysqlvar,))
    jctanner.database_mysql.mysqlvar_val = cursor.fetchall()
    if len(jctanner.database_mysql.mysqlvar_val) == 1:
        return jctanner.database_mysql.mysqlvar_val[0][1]
    else:
        return None


def setvariable(cursor, jctanner.database_mysql.mysqlvar, value):
    """ Set a global jctanner.database_mysql.mysql variable to a given value

    The DB driver will handle quoting of the given value based on its
    type, thus numeric strings like '3.0' or '8' are illegal, they
    should be passed as numeric literals.

    """
    query = "SET GLOBAL %s = " % jctanner.database_mysql.mysql_quote_identifier(jctanner.database_mysql.mysqlvar, 'vars')
    try:
        cursor.execute(query + "%s", (value,))
        cursor.fetchall()
        result = True
    except Exception as e:
        result = to_native(e)
    return result


def main():
    module = AnsibleModule(
        argument_spec=dict(
            login_user=dict(type='str'),
            login_password=dict(type='str', no_log=True),
            login_host=dict(type='str', default='localhost'),
            login_port=dict(type='int', default=3306),
            login_unix_socket=dict(type='str'),
            variable=dict(type='str'),
            value=dict(type='str'),
            client_cert=dict(type='path', aliases=['ssl_cert']),
            client_key=dict(type='path', aliases=['ssl_key']),
            ca_cert=dict(type='path', aliases=['ssl_ca']),
            connect_timeout=dict(type='int', default=30),
            config_file=dict(type='path', default='~/.my.cnf'),
        ),
    )
    user = module.params["login_user"]
    password = module.params["login_password"]
    connect_timeout = module.params['connect_timeout']
    ssl_cert = module.params["client_cert"]
    ssl_key = module.params["client_key"]
    ssl_ca = module.params["ca_cert"]
    config_file = module.params['config_file']
    db = 'jctanner.database_mysql.mysql'

    jctanner.database_mysql.mysqlvar = module.params["variable"]
    value = module.params["value"]
    if jctanner.database_mysql.mysqlvar is None:
        module.fail_json(msg="Cannot run without variable to operate with")
    if match('^[0-9a-z_]+$', jctanner.database_mysql.mysqlvar) is None:
        module.fail_json(msg="invalid variable name \"%s\"" % jctanner.database_mysql.mysqlvar)
    if jctanner.database_mysql.mysql_driver is None:
        module.fail_json(msg=jctanner.database_mysql.mysql_driver_fail_msg)
    else:
        warnings.filterwarnings('error', category=jctanner.database_mysql.mysql_driver.Warning)

    try:
        cursor = jctanner.database_mysql.mysql_connect(module, user, password, config_file, ssl_cert, ssl_key, ssl_ca, db,
                               connect_timeout=connect_timeout)
    except Exception as e:
        if os.path.exists(config_file):
            module.fail_json(msg="unable to connect to database, check login_user and login_password are correct or %s has the credentials. "
                                 "Exception message: %s" % (config_file, to_native(e)))
        else:
            module.fail_json(msg="unable to find %s. Exception message: %s" % (config_file, to_native(e)))

    jctanner.database_mysql.mysqlvar_val = getvariable(cursor, jctanner.database_mysql.mysqlvar)
    if jctanner.database_mysql.mysqlvar_val is None:
        module.fail_json(msg="Variable not available \"%s\"" % jctanner.database_mysql.mysqlvar, changed=False)
    if value is None:
        module.exit_json(msg=jctanner.database_mysql.mysqlvar_val)
    else:
        # Type values before using them
        value_wanted = typedvalue(value)
        value_actual = typedvalue(jctanner.database_mysql.mysqlvar_val)
        if value_wanted == value_actual:
            module.exit_json(msg="Variable already set to requested value", changed=False)
        try:
            result = setvariable(cursor, jctanner.database_mysql.mysqlvar, value_wanted)
        except SQLParseError as e:
            result = to_native(e)

        if result is True:
            module.exit_json(msg="Variable change succeeded prev_value=%s" % value_actual, changed=True)
        else:
            module.fail_json(msg=result, changed=False)


if __name__ == '__main__':
    main()
