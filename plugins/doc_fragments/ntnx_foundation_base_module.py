# -*- coding: utf-8 -*-

# Copyright: (c) 2017,  Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type


class ModuleDocFragment(object):

    # Plugin options for ntnx Foundation
    DOCUMENTATION = r"""
options:
    nutanix_host:
        description:
            - Foundation VM hostname or IP address
        type: str
        required: true
    nutanix_port:
        description:
            - PC port
        type: str
        default: 8000
        required: false
    timeout:
        description:
            - timeout for polling imaging nodes & cluster creation process in seconds
        type: int
        required: false
        default: 60
"""
