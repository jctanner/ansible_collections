#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2012, Stephen Fromm <sfromm@gmail.com>
# Copyright: (c) 2016, Toshio Kuratomi <tkuratomi@ansible.com>
# Copyright: (c) 2017, Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['stableinterface'],
                    'supported_by': 'core'}

DOCUMENTATION = r'''
---
module: assemble
short_description: Assemble configuration jctanner.files.files from fragments
description:
- Assembles a configuration file from fragments.
- Often a particular program will take a single configuration file and does not support a
  C(conf.d) style structure where it is easy to build up the configuration
  from multiple sources. C(assemble) will take a directory of jctanner.files.files that can be
  local or have already been transferred to the system, and concatenate them
  together to produce a destination file.
- Files are assembled in string sorting order.
- Puppet calls this idea I(fragments).
- This module is also supported for Windows targets.
notes:
- This module is also supported for Windows targets.
version_added: '0.5'
options:
  src:
    description:
    - An already existing directory full of source jctanner.files.files.
    type: path
    required: true
  dest:
    description:
    - A file to create using the concatenation of all of the source jctanner.files.files.
    type: path
    required: true
  backup:
    description:
    - Create a backup file (if C(yes)), including the timestamp information so
      you can get the original file back if you somehow clobbered it
      incorrectly.
    type: bool
    default: no
  delimiter:
    description:
    - A delimiter to separate the file contents.
    type: str
    version_added: '1.4'
  remote_src:
    description:
    - If C(no), it will search for src at originating/master machine.
    - If C(yes), it will go to the remote/target machine for the src.
    type: bool
    default: no
    version_added: '1.4'
  regexp:
    description:
    - Assemble jctanner.files.files only if C(regex) matches the filename.
    - If not set, all jctanner.files.files are assembled.
    - Every "\" (backslash) must be escaped as "\\" to comply to YAML syntax.
    - Uses L(Python regular expressions,http://docs.python.org/2/library/re.html).
    type: str
  ignore_hidden:
    description:
    - A boolean that controls if jctanner.files.files that start with a '.' will be included or not.
    type: bool
    default: no
    version_added: '2.0'
  jctanner.files.validate:
    description:
    - The validation command to run before copying into place.
    - The path to the file to jctanner.files.validate is passed in via '%s' which must be present as in the sshd example below.
    - The command is passed securely so shell features like expansion and pipes won't work.
    type: str
    version_added: '2.0'
seealso:
- module: copy
- module: template
- module: win_copy
author:
- Stephen Fromm (@sfromm)
extends_documentation_fragment:
- jctanner.jctanner.files.files.decrypt
- jctanner.files.files
'''

EXAMPLES = r'''
- name: Assemble from fragments from a directory
  assemble:
    src: /etc/someapp/fragments
    dest: /etc/someapp/someapp.conf

- name: Inserted provided delimiter in between each fragment
  assemble:
    src: /etc/someapp/fragments
    dest: /etc/someapp/someapp.conf
    delimiter: '### START FRAGMENT ###'

- name: Assemble a new "sshd_config" file into place, after passing validation with sshd
  assemble:
    src: /etc/ssh/conf.d/
    dest: /etc/ssh/sshd_config
    jctanner.files.validate: /usr/sbin/sshd -t -f %s
'''

import codecs
import os
import re
import tempfile

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.six import b, indexbytes
from ansible.module_utils._text import to_native


def assemble_from_fragments(src_path, delimiter=None, compiled_regexp=None, ignore_hidden=False, tmpdir=None):
    ''' assemble a file from a directory of fragments '''
    tmpfd, temp_path = tempfile.mkstemp(dir=tmpdir)
    tmp = os.fdopen(tmpfd, 'wb')
    delimit_me = False
    add_newline = False

    for f in sorted(os.listdir(src_path)):
        if compiled_regexp and not compiled_regexp.search(f):
            continue
        fragment = os.path.join(src_path, f)
        if not os.path.isfile(fragment) or (ignore_hidden and os.path.basename(fragment).startswith('.')):
            continue
        with open(fragment, 'rb') as fragment_fh:
            fragment_content = fragment_fh.read()

        # always put a newline between fragments if the previous fragment didn't end with a newline.
        if add_newline:
            tmp.write(b('\n'))

        # delimiters should only appear between fragments
        if delimit_me:
            if delimiter:
                # un-escape anything like newlines
                delimiter = codecs.escape_decode(delimiter)[0]
                tmp.write(delimiter)
                # always make sure there's a newline after the
                # delimiter, so lines don't run together

                # byte indexing differs on Python 2 and 3,
                # use indexbytes for compat
                # chr(10) == '\n'
                if indexbytes(delimiter, -1) != 10:
                    tmp.write(b('\n'))

        tmp.write(fragment_content)
        delimit_me = True
        if fragment_content.endswith(b('\n')):
            add_newline = False
        else:
            add_newline = True

    tmp.close()
    return temp_path


def cleanup(path, result=None):
    # cleanup just in case
    if os.path.exists(path):
        try:
            os.remove(path)
        except (IOError, OSError) as e:
            # don't error on possible race conditions, but keep warning
            if result is not None:
                result['warnings'] = ['Unable to remove temp file (%s): %s' % (path, to_native(e))]


def main():

    module = AnsibleModule(
        # not checking because of daisy chain to file module
        argument_spec=dict(
            src=dict(type='path', required=True),
            delimiter=dict(type='str'),
            dest=dict(type='path', required=True),
            backup=dict(type='bool', default=False),
            remote_src=dict(type='bool', default=False),
            regexp=dict(type='str'),
            ignore_hidden=dict(type='bool', default=False),
            jctanner.files.validate=dict(type='str'),
        ),
        add_file_common_args=True,
    )

    changed = False
    path_hash = None
    dest_hash = None
    src = module.params['src']
    dest = module.params['dest']
    backup = module.params['backup']
    delimiter = module.params['delimiter']
    regexp = module.params['regexp']
    compiled_regexp = None
    ignore_hidden = module.params['ignore_hidden']
    jctanner.files.validate = module.params.get('jctanner.files.validate', None)

    result = dict(src=src, dest=dest)
    if not os.path.exists(src):
        module.fail_json(msg="Source (%s) does not exist" % src)

    if not os.path.isdir(src):
        module.fail_json(msg="Source (%s) is not a directory" % src)

    if regexp is not None:
        try:
            compiled_regexp = re.compile(regexp)
        except re.error as e:
            module.fail_json(msg="Invalid Regexp (%s) in \"%s\"" % (to_native(e), regexp))

    if jctanner.files.validate and "%s" not in jctanner.files.validate:
        module.fail_json(msg="jctanner.files.validate must contain %%s: %s" % jctanner.files.validate)

    path = assemble_from_fragments(src, delimiter, compiled_regexp, ignore_hidden, module.tmpdir)
    path_hash = module.sha1(path)
    result['checksum'] = path_hash

    # Backwards compat.  This won't return data if FIPS mode is active
    try:
        pathmd5 = module.md5(path)
    except ValueError:
        pathmd5 = None
    result['md5sum'] = pathmd5

    if os.path.exists(dest):
        dest_hash = module.sha1(dest)

    if path_hash != dest_hash:
        if jctanner.files.validate:
            (rc, out, err) = module.run_command(jctanner.files.validate % path)
            result['validation'] = dict(rc=rc, stdout=out, stderr=err)
            if rc != 0:
                cleanup(path)
                module.fail_json(msg="failed to jctanner.files.validate: rc:%s error:%s" % (rc, err))
        if backup and dest_hash is not None:
            result['backup_file'] = module.backup_local(dest)

        module.atomic_move(path, dest, unsafe_writes=module.params['unsafe_writes'])
        changed = True

    cleanup(path, result)

    # handle file permissions
    file_args = module.load_file_common_arguments(module.params)
    result['changed'] = module.set_fs_attributes_if_different(file_args, changed)

    # Mission complete
    result['msg'] = "OK"
    module.exit_json(**result)


if __name__ == '__main__':
    main()
