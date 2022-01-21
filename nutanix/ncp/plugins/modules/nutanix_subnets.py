#!/usr/bin/python

# Copyright: (c) 2021
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

from ..module_utils.base_module import BaseModule
from ..module_utils.prism.subnets import Subnet

__metaclass__ = type


DOCUMENTATION = r"""
---
module: nutanix_subnets

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
        type: str (Variable from file)
    port:
        description: This acts as the port of the subnet. It can be passed as a list in ansible using with_items
        required: True
        type: str (Variable from file)

author:
 - Gevorg Khachatryan (@gevorg_khachatryan-97)
"""

EXAMPLES = r"""

#CREATE action, request to /subnets
- hosts: [hosts_group]
  tasks:
  - nutanix_subnets:
     action: create
     credentials: str (Variable from file)
     ip_address: str (Variable from file)
     port: str (Variable from file)
     data:
     - spec: object
     - metadata: object

#UPDATE action, request to /subnets/{uuid}
- hosts: [hosts_group]
  tasks:
  - nutanix_subnets:
     action: update
     credentials: str (Variable from file)
     ip_address: str (Variable from file)
     port: str (Variable from file)
     data:
        metadata:
            uuid: string
        spec: object

#LIST action, request to /subnets/list
- hosts: [hosts_group]
  tasks:
  - nutanix_subnets:
     action: list
     data:
     - kind: string
     - sort_attribute: string
     - filter: string
     - length: integer
     - sort_order: string
     - offset: integer

#DELETE action, request to /subnets/{uuid}
- hosts: [hosts_group]
  tasks:
  - nutanix_subnets:
     action: delete
     data:
        metadata:
            uuid: string

"""

RETURN = r"""
CREATE:
    description: CREATE /subnets Response for nutanix subnets
    returned: (for CREATE /subnets  operation)
    type: str
    sample:
        - default Internal Error
        - 202 Request Accepted
UPDATE:
    description: UPDATE /subnets/{uuid} Response for nutanix subnets
    returned: (for UPDATE /subnets  operation)
    type: str
    sample:
        - default Internal Error
        - 404 Invalid UUID provided
        - 202 Request Accepted
LIST:
    description:  LIST /subnets/list Response for nutanix subnets
    returned: (for LIST /subnets  operation)
    type: str
    sample:
        - default Internal Error
        - 200 Success
DELETE:
    description: DELETE /subnets/{uuid} Response for nutanix subnets
    returned: (for DELETE /subnets  operation)
    type: str
    sample:
        - default Internal Error
        - 404 Invalid UUID provided
        - 202 Request Accepted
"""


def run_module():
    module = BaseModule()
    Subnet(module)


def main():
    run_module()


if __name__ == "__main__":
    main()
