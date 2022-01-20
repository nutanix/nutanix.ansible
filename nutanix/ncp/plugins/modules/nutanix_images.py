#!/usr/bin/python

# Copyright: (c) 2021
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type


DOCUMENTATION = r'''
---
module: nutanix_images

short_description: This module allows to communicate with the resource /images

version_added: "1.0.0"

description: This module allows to perform the following tasks on /images

options:
    state:
        description: This is the action used to indicate the type of request
        aliases: ['action']
        required: true
        type: str
    auth:
        description: Credentials needed for authenticating to the subnet
        required: true
        type: dict #(Variable from file)
    data:
        description: This acts as either the params or the body payload depending on the HTTP action
        required: false
        type: dict
    operations:
        description: This acts as the sub_url in the requested url
        required: false
        type: list
        elements: str
    wait_timeout: ###
        description: This is the wait_timeout description
        required: False
        type: int
        default: 300
    wait: ###
        description: This is the wait description
        required: False
        type: bool
        default: true
    validate_certs: ###
        description: This is the validate_certs description
        required: False
        type: bool
        default: False

author:
 - Gevorg Khachatryan (@gevorg_khachatryan)
'''

EXAMPLES = r'''

#CREATE action, request to /images
- hosts: [hosts_group]
  tasks:
  - name: create Image
    nutanix_images:
      action: create
      credentials: str (Variable from file)
      ip_address: str (Variable from file)
      port: str (Variable from file)
      data:
        spec:
         name: string
         resources:
           image_type: string
           source_uri: string

#UPDATE action, request to /images/{uuid}
- hosts: [hosts_group]
  tasks:
  - name: update Image
    nutanix_images:
      action: update
      credentials: str (Variable from file)
      ip_address: str (Variable from file)
      port: str (Variable from file)
      data:
        metadata:
          uuid: string
        spec:
          name: string
          resources:
            image_type: string
            source_uri: string

#LIST action, request to /images/list
- hosts: [hosts_group]
  tasks:
  - name: List Images
    nutanix_images:
      action: list
      credentials: str (Variable from file)
      ip_address: str (Variable from file)
      port: str (Variable from file)
      data:
      - kind: string
      - sort_attribute: string
      - filter: string
      - length: integer
      - sort_order: string
      - offset: integer

#DELETE action, request to /images/{uuid}
- hosts: [hosts_group]
  tasks:
  - name: delete Image
    nutanix_images:
      action: delete
      credentials: str (Variable from file)
      ip_address: str (Variable from file)
      port: str (Variable from file)
      data:
        metadata:
          uuid: string
'''

RETURN = r'''
CREATE:
    description: CREATE /images Response for nutanix imagese
    returned: (for CREATE /images  operation)
    type: str
    sample:
      - default Internal Error
      - 202 Request Accepted
UPDATE:
    description: UPDATE /images/{uuid} Response for nutanix images
    returned: (for UPDATE /images  operation)
    type: str
    sample:
      - default Internal Error
      - 404 Invalid UUID provided
      - 202 Request Accepted
LIST:
    description:  LIST /images/list Response for nutanix imagese
    returned: (for LIST /images  operation)
    type: str
    sample:
      - default Internal Error
      - 200 Success
DELETE:
    description: DELETE /images/{uuid} Response for nutanix images
    returned: (for DELETE /images  operation)
    type: str
    sample:
      - default Internal Error
      - 404 Invalid UUID provided
      - 202 Request Accepted
'''
from ..module_utils.prism.images import Image
from ..module_utils.base_module import BaseModule


def run_module():
    module = BaseModule()
    Image(module)


def main():
    run_module()


if __name__ == '__main__':
    main()
