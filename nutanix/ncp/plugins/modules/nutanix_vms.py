#!/usr/bin/python

# Copyright: (c) 2021
# GNU General Public License v3.0+ (see COPYING or
# https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: nutanix_vms

short_description: This module allows to communicate with the resource /vms

version_added: "1.0.0"

description: This module allows to perform the following tasks on /vms

options:
    action:
        description: This is the HTTP action used to indicate the type of request
        required: true
        type: str
    credentials:
        description: Credentials needed for authenticating to the subnet
        required: true
        type: dict # (Variable from file)
    data:
        description: This acts as either the params or the body payload depending on the HTTP action
        required: false
        type: dict
    operations:
        description: This acts as the sub_url in the requested url
        required: false
        type: list
        elements: str
    ip_address:
        description: This acts as the ip_address of the subnet. It can be passed as a list in ansible using with_items
        required: True
        type: str
    port: ###
        description: This is the port
        required: true
        type: str
    wait: ###
        description: This is the wait
        required: False
        type: bool
        default: true
    wait_timeout: ###
        description: This is the port
        required: False
        type: int
        default: 300
    validate_certs: ###
        description: This is the port
        required: False
        type: bool
        default: False

author:
 - Gevorg Khachatryan (@gevorg_khachatryan)
'''

EXAMPLES = r'''
'''

RETURN = r'''
'''

from ..module_utils.prism.vms import VM
from ..module_utils.base_module import BaseModule


def run_module():
    module = BaseModule()
    VM(module)


def main():
    run_module()


if __name__ == '__main__':
    main()
