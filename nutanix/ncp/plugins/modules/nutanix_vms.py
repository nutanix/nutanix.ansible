#!/usr/bin/python

# Copyright: (c) 2021
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
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

from ..module_utils.base_module import BaseModule
from ..module_utils.prism.vms import VM

def run_module():
    BaseModule.argument_spec.update(dict(
        spec__name=dict(type='str', required=True, aliases=['name']),
        uuid=dict(type='str', required=False),
        cpu_properties=dict(type="dict", required=False, options=dict(
            spec__resources__num_sockets=dict(type='int', default=1, alises=['core_count']),
            spec__resources__num_threads_per_core=dict(type='int', default=1, choices=[1, 2],
                                                       alises=['threads_per_core'])
        )),
        spec__resources__nic_list__is_connected=dict(type='bool', aliases=['is_connected'], default=True),
        spec__cluster_reference__uuid=dict(type='str', aliases=['cluster_uuid']),
        spec__cluster_reference__name=dict(type='str', aliases=['cluster_name'], required=False),
        spec__cluster_reference__kind=dict(type='str', aliases=['cluster_kind'], required=False, default='cluster'),
        spec__resources__nic_list__subnet_reference__uuid=dict(type='str', aliases=['subnet_uuid']),
        spec__resources__nic_list__subnet_reference__name=dict(type='str',
                                                               aliases=['subnet_name'],
                                                               required=False),
        spec__resources__nic_list__subnet_reference__kind=dict(type='str',
                                                               aliases=['subnet_kind'],
                                                               required=False,
                                                               default='subnet'),
    ))
    module = BaseModule()
    VM(module)


def main():
    run_module()


if __name__ == '__main__':
    main()
