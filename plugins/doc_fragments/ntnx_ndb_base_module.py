# -*- coding: utf-8 -*-

# Copyright: (c) 2017,  Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type


class ModuleDocFragment(object):

    # Plugin options for ntnx ndb
    DOCUMENTATION = r"""
options:
    nutanix_host:
        description:
            - ndb era server IP address
            - C(nutanix_host). If not set then the value of the C(NUTANIX_HOST), environment variable is used.
        type: str
        required: true
    nutanix_password:
        description:
            - ndb era server password
            - C(nutanix_password). If not set then the value of the C(NUTANIX_PASSWORD), environment variable is used.
        type: str
        required: true
    nutanix_username:
        description:
            - ndb era server username
            - C(nutanix_username). If not set then the value of the C(NUTANIX_USERNAME), environment variable is used.
        type: str
        required: true
    validate_certs:
        description:
            - Set value to C(False) to skip validation for self signed certificates
            - This is not recommended for production setup
            - C(validate_certs). If not set then the value of the C(VALIDATE_CERTS), environment variable is used.
        type: bool
        default: true
    timeout:
        description:
            - write
        type: int
        required: false
        default: 2100
"""
