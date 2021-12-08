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
- GET:   This operation gets a existing ngt.
    url: /subnets/{uuid}/ngt
    params:
      uuid
       - description: The UUID of the entity.
       - type: string
       - required: True
       - in: path
- POST:   Creates a subnet reset request task.
    url: /subnets/{uuid}/reset
    params:
      uuid
       - description: The UUID of the entity.
       - type: string
       - required: True
       - in: path
      body:
       - description: Request to change the power state of a subnet.
       - type: object
       - required: False
       - in: body
- PUT:   Write to an identity disk attached to a subnet at the provided offset.
    url: /subnets/{uuid}/subnet_disk/{subnet_disk_uuid}/data
    params:
      uuid
       - description: The UUID of the entity.
       - type: string
       - required: True
       - in: path
      subnet_disk_uuid
       - description: subnet disk device UUID
       - type: string
       - required: True
       - in: path
      offset
       - description: Offset within the disk. Defaults to 0.
       - type: integer
       - required: None
       - in: query
      data:
       - type: None
       - required: True
       - in: body
- GET:   Read from an identity disk attached to a subnet from the provided offset.
    url: /subnets/{uuid}/subnet_disk/{subnet_disk_uuid}/data
    params:
      uuid
       - description: The UUID of the entity.
       - type: string
       - required: True
       - in: path
      subnet_disk_uuid
       - description: subnet disk device UUID
       - type: string
       - required: True
       - in: path
      offset
       - description: Offset within the disk. Defaults to 0.
       - type: integer
       - required: None
       - in: query
      length
       - description: Amount to read from disk. By default this will be the max size (16 MB).
       - type: integer
       - required: None
       - in: query
- POST:   API to resume replication for a given subnet protected using sync protection policy.
    url: /subnets/{uuid}/resume_replication
    params:
      uuid
       - description: The UUID of the entity.
       - type: string
       - required: True
       - in: path
- POST:   Creates a subnet power_cycle request task.
    url: /subnets/{uuid}/power_cycle
    params:
      uuid
       - description: The UUID of the entity.
       - type: string
       - required: True
       - in: path
      body:
       - description: Request to change the power state of a subnet.
       - type: object
       - required: False
       - in: body
- POST:   API to pause replication for a given subnet protected using sync protection policy.
    url: /subnets/{uuid}/pause_replication
    params:
      uuid
       - description: The UUID of the entity.
       - type: string
       - required: True
       - in: path
- POST:   This operation gets a list of subnets, allowing for sorting and pagination. Note: Entities that have not been created successfully are not listed.
    url: /subnets/list
    params:
      get_entities_request:
       - description: All api calls that return a list will have this metadata block as input
       - type: object
       - required: True
       - in: body
- POST:   Creates a subnet acpi_shutdown request task.
    url: /subnets/{uuid}/acpi_shutdown
    params:
      uuid
       - description: The UUID of the entity.
       - type: string
       - required: True
       - in: path
      body:
       - description: Request to change the power state of a subnet.
       - type: object
       - required: False
       - in: body
- POST:   Submits a request to create a task handling subnet clone operation, returns a task reference. This creates a new subnet by cloning the current subnet.
    url: /subnets/{uuid}/clone
    params:
      uuid
       - description: The UUID of the entity.
       - type: string
       - required: True
       - in: path
      body:
       - description: Input object for the clone API. User can provide the optional UUID of the subnet that will be created as a result of this operation.
       - type: object
       - required: None
       - in: body
- OPTIONS:   List of dictionaries containing supported capability names and their descriptions for subnets.
  No Params required
- GET:   Get capability information for subnets.
    url: /subnets/capabilities
    params:
      name
       - description: Name of the capability
       - type: string
       - required: None
       - in: query
- PUT:   This operation submits a request to update an existing subnet based on the input parameters.
    url: /subnets/{uuid}
    params:
      uuid
       - description: The UUID of the entity.
       - type: string
       - required: True
       - in: path
      body:
       - description: An intentful representation of a subnet
       - type: object
       - required: True
       - in: body
- DELETE:   This operation submits a request to delete an existing subnet.
    url: /subnets/{uuid}
    params:
      uuid
       - description: The UUID of the entity.
       - type: string
       - required: True
       - in: path
- GET:   This operation gets an existing subnet.
    url: /subnets/{uuid}
    params:
      uuid
       - description: The UUID of the entity.
       - type: string
       - required: True
       - in: path
- POST:   Validates the feasibility of subnet migration to given migration target,
if not feasible returns the reason behind it.
    url: /subnets/{uuid}/validate_migration
    params:
      uuid
       - description: The UUID of the entity.
       - type: string
       - required: True
       - in: path
      body:
       - description: Contains reference to migration target to which the migrate validation
needs to be checked upon.
       - type: object
       - required: True
       - in: body
- POST:   API to migrate the subnet's selected disks to the specified container
    url: /subnets/{uuid}/migrate_disks
    params:
      uuid
       - description: The UUID of the entity.
       - type: string
       - required: True
       - in: path
      body:
       - description: Specifies the disks for migration and the target container.
       - type: object
       - required: None
       - in: body
- POST:   Submits a request to create a task handling the subnet revert to a recovery point operation, returns a task reference.
    url: /subnets/{uuid}/revert
    params:
      uuid
       - description: The UUID of the entity.
       - type: string
       - required: True
       - in: path
      body:
       - description: Input object for the revert API. Pass the UUID of the subnet_recovery_point to which the subnet is to be reverted to.
       - type: object
       - required: True
       - in: body
- PUT:   Request a new IP address the currently allocated IP address.
    url: /subnets/{uuid}/update_ip
    params:
      uuid
       - description: The UUID of the entity.
       - type: string
       - required: True
       - in: path
      body:
       - description: Input object for the API to update IP addresses. Users can provide the specific IP address they want to request.
       - type: object
       - required: True
       - in: body
- POST:   Submits a request to create a task handling OVA create operation, returns a task reference. This will export subnet and create an OVA object for it.
    url: /subnets/{uuid}/export
    params:
      uuid
       - description: The UUID of the entity.
       - type: string
       - required: True
       - in: path
      body:
       - description: Input object for the create OVA API.
       - type: object
       - required: None
       - in: body
- POST:   Creates a subnet acpi_reboot request task.
    url: /subnets/{uuid}/acpi_reboot
    params:
      uuid
       - description: The UUID of the entity.
       - type: string
       - required: True
       - in: path
      body:
       - description: Request to change the power state of a subnet.
       - type: object
       - required: False
       - in: body
- POST:   Creates a subnet guest_shutdown request task.
    url: /subnets/{uuid}/guest_shutdown
    params:
      uuid
       - description: The UUID of the entity.
       - type: string
       - required: True
       - in: path
      body:
       - description: Request to change the power state of a subnet.
       - type: object
       - required: False
       - in: body
- POST:   Submits a request to create a task handling the snapshot operation on the subnet, returns a task reference. This creates a point in time recovery point.
    url: /subnets/{uuid}/snapshot
    params:
      uuid
       - description: The UUID of the entity.
       - type: string
       - required: True
       - in: path
      body:
       - description: Input object for the snapshot API.
       User can provide optional UUID of the subnet_recovery_point that will be created as a result of this operation.
       - type: object
       - required: None
       - in: body
- POST:   This operation submits a request to create a new subnet based on the input parameters.
    url: /subnets
    params:
      body:
       - description: An intentful representation of a subnet
       - type: object
       - required: True
       - in: body
- POST:   Creates a subnet guest_reboot request task.
    url: /subnets/{uuid}/guest_reboot
    params:
      uuid
       - description: The UUID of the entity.
       - type: string
       - required: True
       - in: path
      body:
       - description: Request to change the power state of a subnet.
       - type: object
       - required: False
       - in: body

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

#GET request to /subnets/{uuid}/ngt
- hosts: [hosts_group]
  tasks:
  - subnets:
     action: get
     operations:
     - {uuid}
     - ngt

#POST request to /subnets/{uuid}/reset
- hosts: [hosts_group]
  tasks:
  - subnets:
     action: post
     data:
     - task_uuid: string
     operations:
     - {uuid}
     - reset

#PUT request to /subnets/{uuid}/subnet_disk/{subnet_disk_uuid}/data
- hosts: [hosts_group]
  tasks:
  - subnets:
     action: put
     operations:
     - {uuid}
     - subnet_disk: value
     - data

#GET request to /subnets/{uuid}/subnet_disk/{subnet_disk_uuid}/data
- hosts: [hosts_group]
  tasks:
  - subnets:
     action: get
     operations:
     - {uuid}
     - subnet_disk: value
     - data

#POST request to /subnets/{uuid}/resume_replication
- hosts: [hosts_group]
  tasks:
  - subnets:
     action: post
     operations:
     - {uuid}
     - resume_replication

#POST request to /subnets/{uuid}/power_cycle
- hosts: [hosts_group]
  tasks:
  - subnets:
     action: post
     data:
     - task_uuid: string
     operations:
     - {uuid}
     - power_cycle

#POST request to /subnets/{uuid}/pause_replication
- hosts: [hosts_group]
  tasks:
  - subnets:
     action: post
     operations:
     - {uuid}
     - pause_replication

#POST request to /subnets/list
- hosts: [hosts_group]
  tasks:
  - subnets:
     action: post
     data:
     - kind: string
     - sort_attribute: string
     - filter: string
     - length: integer
     - sort_order: string
     - offset: integer
    operations:
     - list

#POST request to /subnets/{uuid}/acpi_shutdown
- hosts: [hosts_group]
  tasks:
  - subnets:
     action: post
     data:
     - task_uuid: string
     operations:
     - {uuid}
     - acpi_shutdown

#POST request to /subnets/{uuid}/clone
- hosts: [hosts_group]
  tasks:
  - subnets:
     action: post
     data:
     - metadata: object
     - override_spec: object
     operations:
     - {uuid}
     - clone

#OPTIONS request to /subnets/capabilities
- hosts: [hosts_group]
  tasks:

#GET request to /subnets/capabilities
- hosts: [hosts_group]
  tasks:
  - subnets:
     action: get
    operations:
     - capabilities

#PUT request to /subnets/{uuid}
- hosts: [hosts_group]
  tasks:
  - subnets:
     action: put
     data:
     - spec: object
     - api_version: string
     - metadata: object
    operations:
     - {uuid}

#DELETE request to /subnets/{uuid}
- hosts: [hosts_group]
  tasks:
  - subnets:
     action: delete
    operations:
     - {uuid}

#GET request to /subnets/{uuid}
- hosts: [hosts_group]
  tasks:
  - subnets:
     action: get
    operations:
     - {uuid}

#POST request to /subnets/{uuid}/validate_migration
- hosts: [hosts_group]
  tasks:
  - subnets:
     action: post
     data:
     - migration_target: object
     operations:
     - {uuid}
     - validate_migration

#POST request to /subnets/{uuid}/migrate_disks
- hosts: [hosts_group]
  tasks:
  - subnets:
     action: post
     data:
     - disks_to_target_container_list: array
     - target_container_reference: object
     operations:
     - {uuid}
     - migrate_disks

#POST request to /subnets/{uuid}/revert
- hosts: [hosts_group]
  tasks:
  - subnets:
     action: post
     data:
     - subnet_recovery_point_uuid: string
     operations:
     - {uuid}
     - revert

#PUT request to /subnets/{uuid}/update_ip
- hosts: [hosts_group]
  tasks:
  - subnets:
     action: put
     data:
     - update_list: array
     operations:
     - {uuid}
     - update_ip

#POST request to /subnets/{uuid}/export
- hosts: [hosts_group]
  tasks:
  - subnets:
     action: post
     data:
     - name: string
     - disk_file_format: string
     operations:
     - {uuid}
     - export

#POST request to /subnets/{uuid}/acpi_reboot
- hosts: [hosts_group]
  tasks:
  - subnets:
     action: post
     data:
     - task_uuid: string
     operations:
     - {uuid}
     - acpi_reboot

#POST request to /subnets/{uuid}/guest_shutdown
- hosts: [hosts_group]
  tasks:
  - subnets:
     action: post
     data:
     - task_uuid: string
     operations:
     - {uuid}
     - guest_shutdown

#POST request to /subnets/{uuid}/snapshot
- hosts: [hosts_group]
  tasks:
  - subnets:
     action: post
     data:
     - creation_time: string
     - expiration_time: string
     - subnet_recovery_point_uuid: string
     - name: string
     - recovery_point_type: string
     operations:
     - {uuid}
     - snapshot

#POST request to /subnets
- hosts: [hosts_group]
  tasks:
  - subnets:
     action: post
     data:
     - spec: object
     - api_version: string
     - metadata: object

#POST request to /subnets/{uuid}/guest_reboot
- hosts: [hosts_group]
  tasks:
  - subnets:
     action: post
     data:
     - task_uuid: string
     operations:
     - {uuid}
     - guest_reboot
'''

RETURN = r'''

# GET /subnets/{uuid}/ngt
responses:
- default: Internal Error
- 200: Success
- 404: Invalid UUID provided

# POST /subnets/{uuid}/reset
responses:
- default: Internal Error
- 404: Invalid UUID provided
- 202: Request Accepted

# PUT /subnets/{uuid}/subnet_disk/{subnet_disk_uuid}/data
responses:
- default: Internal Error
- 200: Success

# GET /subnets/{uuid}/subnet_disk/{subnet_disk_uuid}/data
responses:
- default: Internal Error
- 200: Success

# POST /subnets/{uuid}/resume_replication
responses:
- default: Internal Error
- 404: Invalid UUID provided
- 202: Request Accepted

# POST /subnets/{uuid}/power_cycle
responses:
- default: Internal Error
- 404: Invalid UUID provided
- 202: Request Accepted

# POST /subnets/{uuid}/pause_replication
responses:
- default: Internal Error
- 404: Invalid UUID provided
- 202: Request Accepted

# POST /subnets/list
responses:
- default: Internal Error
- 200: Success

# POST /subnets/{uuid}/acpi_shutdown
responses:
- default: Internal Error
- 404: Invalid UUID provided
- 202: Request Accepted

# POST /subnets/{uuid}/clone
responses:
- default: Internal Error
- 404: Invalid UUID provided
- 202: Request Accepted

# OPTIONS /subnets/capabilities
responses:
- default: Internal Error
- 200: Success

# GET /subnets/capabilities
responses:
- default: Internal Error
- 200: Success

# PUT /subnets/{uuid}
responses:
- default: Internal Error
- 404: Invalid UUID provided
- 202: Request Accepted

# DELETE /subnets/{uuid}
responses:
- default: Internal Error
- 404: Invalid UUID provided
- 202: Request Accepted

# GET /subnets/{uuid}
responses:
- default: Internal Error
- 200: Success
- 404: Invalid UUID provided

# POST /subnets/{uuid}/validate_migration
responses:
- default: Internal Error
- 200: Success
- 404: Invalid UUID provided

# POST /subnets/{uuid}/migrate_disks
responses:
- default: Internal Error
- 404: Invalid UUID provided
- 202: Request Accepted

# POST /subnets/{uuid}/revert
responses:
- default: Internal Error
- 404: Invalid UUID provided
- 202: Request Accepted

# PUT /subnets/{uuid}/update_ip
responses:
- default: Internal Error
- 404: Invalid UUID provided
- 202: Request Accepted

# POST /subnets/{uuid}/export
responses:
- default: Internal Error
- 404: Invalid UUID provided
- 202: Request Accepted

# POST /subnets/{uuid}/acpi_reboot
responses:
- default: Internal Error
- 404: Invalid UUID provided
- 202: Request Accepted

# POST /subnets/{uuid}/guest_shutdown
responses:
- default: Internal Error
- 404: Invalid UUID provided
- 202: Request Accepted

# POST /subnets/{uuid}/snapshot
responses:
- default: Internal Error
- 404: Invalid UUID provided
- 202: Request Accepted

# POST /subnets
responses:
- default: Internal Error
- 202: Request Accepted

# POST /subnets/{uuid}/guest_reboot
responses:
- default: Internal Error
- 404: Invalid UUID provided
- 202: Request Accepted
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
