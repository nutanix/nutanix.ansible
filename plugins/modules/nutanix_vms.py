#!/usr/bin/python

# Copyright: (c) 2021
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

DOCUMENTATION = r'''
---
module: subnets

short_description: This module allows to communicate with the resource /subnets

version_added: "1.0.0"

description: This module allows to perform the following tasks on /subnets

options:
    action:
        description: This is the HTTP action used to indicate the type of request
        required: true
        type: str
    credentials:
        description: Credentials needed for authenticating to the subnet
        required: true
        type: dict (Variable from file)
    data:
        description: This acts as either the params or the body payload depending on the HTTP action
        required: false
        type: dict
    operation:
        description: This acts as the sub_url in the requested url
        required: false
        type: str
    ip_address:
        description: This acts as the ip_address of the subnet. It can be passed as a list in ansible using with_items
        required: True
        type: str

author:
 - Gevorg Khachatryan (@gevorg_khachatryan)
'''

EXAMPLES = r'''
'''

RETURN = r'''
'''

from ansible.module_utils.nutanix.entity import BaseModule
from ansible.module_utils.nutanix.prism.vms import VM

def run_module():
    module = BaseModule()
    module_builder = VM(module)
    module_builder.run_module(module)


def main():
    run_module()


if __name__ == '__main__':
    main()
