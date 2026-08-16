#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_files_partner_server_v2
short_description: Create, Update, Delete partner servers in Nutanix Files
version_added: 2.7.0
description:
  - This module allows you to create, update, and delete partner servers registered to a file server in Nutanix Prism Central.
  - A partner server registers a third-party vendor or service (for example a notification, migration or backup partner) with a file server.
  - This module uses PC v4 APIs based SDKs.
notes:
  - The attributes C(vendor_properties) and C(backup_server_config) are mutually exclusive.
  - "Ref: U(https://developers.nutanix.com/api-reference?namespace=files)"
options:
  state:
    description:
      - If C(state) is set to C(present) and C(ext_id) is not provided then the operation will be create partner server.
      - If C(state) is set to C(present) and C(ext_id) is provided then the operation will be update partner server.
      - If C(state) is set to C(absent) and C(ext_id) is provided then the operation will be delete partner server.
    type: str
    required: false
    choices:
      - present
      - absent
    default: present
  ext_id:
    description:
      - The external ID of the partner server.
      - Required for update and delete operations.
    type: str
    required: false
  file_server_ext_id:
    description:
      - The external identifier of the file server the partner server belongs to.
      - Required for all operations.
    type: str
    required: true
  name:
    description:
      - Partner server name.
      - Required for create operation.
      - Maximum 64 characters.
    type: str
    required: false
  vendor_name:
    description:
      - Vendor name of the partner server.
      - For partner type C(ANTIVIRUS), vendor name denotes the icapServiceName.
      - Required for create operation.
      - Maximum 256 characters.
    type: str
    required: false
  description:
    description:
      - Partner server details or any third-party vendors to register the server with AFS.
      - Maximum 180 characters.
    type: str
    required: false
  partner_type:
    description:
      - Usage type of the partner server.
      - Required for create operation.
    type: str
    required: false
    choices:
      - NOTIFICATION
      - BACKUP
      - MIGRATION
  vendor_properties:
    description:
      - Partner server configuration for servers of type C(NOTIFICATION), C(MIGRATION) and C(BACKUP).
      - Mutually exclusive with C(backup_server_config).
    type: dict
    required: false
    suboptions:
      custom_properties:
        description:
          - Indicates the vendor specific custom properties of the partner server.
          - It contains a list of key value pairs.
        type: list
        elements: dict
        required: false
        suboptions:
          name:
            description:
              - The key of this key-value string pair.
            type: str
            required: false
          value:
            description:
              - The value associated with the key for this key-value string pair.
            type: str
            required: false
      address:
        description:
          - An unique address that identifies a device on the network in IPv4/IPv6 format or a Fully Qualified Domain Name.
          - Required when C(vendor_properties) is provided.
        type: dict
        required: false
        suboptions:
          ipv4:
            description:
              - IPv4 address of the partner server.
            type: dict
            required: false
            suboptions:
              value:
                description:
                  - The IPv4 address value.
                type: str
                required: true
              prefix_length:
                description:
                  - The prefix length of the network to which this host IPv4 address belongs.
                type: int
                required: false
                default: 32
          ipv6:
            description:
              - IPv6 address of the partner server.
            type: dict
            required: false
            suboptions:
              value:
                description:
                  - The IPv6 address value.
                type: str
                required: true
              prefix_length:
                description:
                  - The prefix length of the network to which this host IPv6 address belongs.
                type: int
                required: false
                default: 128
          fqdn:
            description:
              - Fully Qualified Domain Name of the partner server.
            type: dict
            required: false
            suboptions:
              value:
                description:
                  - The fully qualified domain name value.
                type: str
                required: false
      port:
        description:
          - Partner server port.
          - Required when C(vendor_properties) is provided.
          - Value must be between 1 and 65536.
        type: int
        required: false
      server_type:
        description:
          - Type of the server. This field is only applicable to partner server of type C(NOTIFICATION).
        type: str
        required: false
        choices:
          - PRIMARY
          - SECONDARY
  backup_server_config:
    description:
      - Configuration for partner server of type C(BACKUP).
      - Mutually exclusive with C(vendor_properties).
    type: dict
    required: false
    suboptions:
      expiry_in_secs:
        description:
          - The expiry time in seconds for the backup client to access the shares.
          - The default value is 24 hours (86400 seconds).
        type: int
        required: false
      backup_client_access_configs:
        description:
          - List of backup client details along with request access permissions.
        type: list
        elements: dict
        required: false
        suboptions:
          address:
            description:
              - An unique address that identifies a device on the network in IPv4/IPv6 format or a Fully Qualified Domain Name.
            type: dict
            required: true
            suboptions:
              ipv4:
                description:
                  - IPv4 address of the backup client.
                type: dict
                required: false
                suboptions:
                  value:
                    description:
                      - The IPv4 address value.
                    type: str
                    required: true
                  prefix_length:
                    description:
                      - The prefix length of the network to which this host IPv4 address belongs.
                    type: int
                    required: false
                    default: 32
              ipv6:
                description:
                  - IPv6 address of the backup client.
                type: dict
                required: false
                suboptions:
                  value:
                    description:
                      - The IPv6 address value.
                    type: str
                    required: true
                  prefix_length:
                    description:
                      - The prefix length of the network to which this host IPv6 address belongs.
                    type: int
                    required: false
                    default: 128
              fqdn:
                description:
                  - Fully Qualified Domain Name of the backup client.
                type: dict
                required: false
                suboptions:
                  value:
                    description:
                      - The fully qualified domain name value.
                    type: str
                    required: false
          access_type:
            description:
              - Access type of the mount target.
            type: str
            required: true
            choices:
              - READ_WRITE
              - READ_ONLY
          mount_target_ext_id:
            description:
              - Mount target external identifier for the partner server.
            type: str
            required: false
          operation_type:
            description:
              - Backup server (client IP-address/FQDN) management operation.
            type: str
            required: true
            choices:
              - ADD
              - REMOVE
extends_documentation_fragment:
  - nutanix.ncp.ntnx_credentials
  - nutanix.ncp.ntnx_operations_v2
  - nutanix.ncp.ntnx_logger
  - nutanix.ncp.ntnx_proxy_v2
author:
  - Abhinav Bansal (@abhinavbansal29)
  - George Ghawali (@george-ghawali)
"""

EXAMPLES = r"""
- name: Create notification partner server
  nutanix.ncp.ntnx_files_partner_server_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: present
    file_server_ext_id: "18f78959-14a6-4c47-b5db-920460c4b668"
    name: "partner_server_ansible"
    vendor_name: "DataLens"
    description: "Notification partner server created by Ansible"
    partner_type: "NOTIFICATION"
    vendor_properties:
      address:
        ipv4:
          value: "10.44.77.10"
      port: 29092
      server_type: "PRIMARY"
      custom_properties:
        - name: "kafkatopic"
          value: "1P1R"
  register: result
  ignore_errors: true

- name: Create backup partner server
  nutanix.ncp.ntnx_files_partner_server_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: present
    file_server_ext_id: "18f78959-14a6-4c47-b5db-920460c4b668"
    name: "backup_partner_server_ansible"
    vendor_name: "BackupVendor"
    description: "Backup partner server created by Ansible"
    partner_type: "BACKUP"
    backup_server_config:
      expiry_in_secs: 86400
      backup_client_access_configs:
        - address:
            ipv4:
              value: "10.44.77.20"
          access_type: "READ_WRITE"
          operation_type: "ADD"
  register: result
  ignore_errors: true

- name: Update partner server
  nutanix.ncp.ntnx_files_partner_server_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: present
    file_server_ext_id: "18f78959-14a6-4c47-b5db-920460c4b668"
    ext_id: "aa04b8ce-6b23-4d5e-8f6a-9e0b3c1d2e4f"
    name: "partner_server_ansible_updated"
    vendor_name: "DataLens"
    description: "Notification partner server updated by Ansible"
    partner_type: "NOTIFICATION"
    vendor_properties:
      address:
        ipv4:
          value: "10.44.77.11"
      port: 39092
      server_type: "PRIMARY"
  register: result
  ignore_errors: true

- name: Delete partner server
  nutanix.ncp.ntnx_files_partner_server_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: absent
    file_server_ext_id: "18f78959-14a6-4c47-b5db-920460c4b668"
    ext_id: "aa04b8ce-6b23-4d5e-8f6a-9e0b3c1d2e4f"
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
  description:
    - Response for creating, updating, or deleting partner server.
    - If the operation is create or update and C(wait) is true, it will return the partner server details.
    - If the operation is create or update and C(wait) is false, it will return the task details.
    - If the operation is delete, it will return the task details.
  returned: always
  type: dict
  sample:
    {
      "backup_server_config": null,
      "description": "Notification partner server created by Ansible",
      "ext_id": "aa04b8ce-6b23-4d5e-8f6a-9e0b3c1d2e4f",
      "links": null,
      "name": "partner_server_ansible",
      "partner_type": "NOTIFICATION",
      "tenant_id": null,
      "vendor_name": "DataLens",
      "vendor_properties": {
          "address": {
              "fqdn": null,
              "ipv4": {
                  "prefix_length": 32,
                  "value": "10.44.77.10"
              },
              "ipv6": null
          },
          "connection_status": "NOT_TESTED",
          "custom_properties": [
              {
                  "name": "kafkatopic",
                  "value": "1P1R"
              }
          ],
          "port": 29092,
          "server_type": "PRIMARY"
      }
    }

task_ext_id:
  description:
    - The external ID of the task.
  returned: always
  type: str
  sample: "ZXJnb24=:90458bc7-a12b-4616-ac66-562fdb00c209"

ext_id:
  description:
    - The external ID of the partner server.
  returned: always
  type: str
  sample: "aa04b8ce-6b23-4d5e-8f6a-9e0b3c1d2e4f"

changed:
  description: This indicates whether the task resulted in any changes
  returned: always
  type: bool
  sample: true

skipped:
  description: This indicates whether the task was skipped due to idempotency
  returned: when applicable
  type: bool
  sample: false

error:
  description: This indicates the error message if any error occurred
  returned: When an error occurs
  type: str

failed:
  description: This indicates whether the task failed
  returned: always
  type: bool
  sample: false

msg:
  description: This indicates the message if any message occurred
  returned: When there is an error, module is idempotent or check mode
  type: str
  sample: "PartnerServer with name 'partner_server_ansible' already exists. Skipping creation."
"""

import traceback  # noqa: E402
import warnings  # noqa: E402
from copy import deepcopy  # noqa: E402

from ansible.module_utils.basic import missing_required_lib  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_module_v4 import BaseModuleV4  # noqa: E402
from ..module_utils.v4.constants import Tasks as TASK_CONSTANTS  # noqa: E402
from ..module_utils.v4.files.api_client import (  # noqa: E402
    get_etag,
    get_partner_servers_api_instance,
)
from ..module_utils.v4.files.helpers import (  # noqa: E402
    get_partner_server,
    get_partner_server_by_name,
)
from ..module_utils.v4.prism.tasks import (  # noqa: E402
    get_entity_ext_id_from_task,
    wait_for_completion,
)
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
    strip_read_only_fields,
    validate_required_params,
)

SDK_IMP_ERROR = None
try:
    import ntnx_files_py_client as files_sdk  # noqa: E402
except ImportError:

    from ..module_utils.v4.sdk_mock import mock_sdk as files_sdk  # noqa: E402

    SDK_IMP_ERROR = traceback.format_exc()

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():

    ipv4_spec = dict(
        value=dict(type="str", required=True),
        prefix_length=dict(type="int", required=False, default=32),
    )

    ipv6_spec = dict(
        value=dict(type="str", required=True),
        prefix_length=dict(type="int", required=False, default=128),
    )

    fqdn_spec = dict(
        value=dict(type="str", required=False),
    )

    ip_address_or_fqdn_spec = dict(
        ipv4=dict(type="dict", options=ipv4_spec, obj=files_sdk.IPv4Address),
        ipv6=dict(type="dict", options=ipv6_spec, obj=files_sdk.IPv6Address),
        fqdn=dict(type="dict", options=fqdn_spec, obj=files_sdk.FQDN),
    )

    kv_string_pair_spec = dict(
        name=dict(type="str", required=False),
        value=dict(type="str", required=False),
    )

    vendor_properties_spec = dict(
        custom_properties=dict(
            type="list",
            elements="dict",
            options=kv_string_pair_spec,
            obj=files_sdk.KVStringPair,
            required=False,
        ),
        address=dict(
            type="dict",
            options=ip_address_or_fqdn_spec,
            obj=files_sdk.IPAddressOrFQDN,
            required=False,
        ),
        port=dict(type="int", required=False),
        server_type=dict(
            type="str",
            choices=["PRIMARY", "SECONDARY"],
            obj=files_sdk.ServerType,
            required=False,
        ),
    )

    backup_client_access_config_spec = dict(
        address=dict(
            type="dict",
            options=ip_address_or_fqdn_spec,
            obj=files_sdk.IPAddressOrFQDN,
            required=True,
        ),
        access_type=dict(
            type="str",
            choices=["READ_WRITE", "READ_ONLY"],
            obj=files_sdk.BackupAccessType,
            required=True,
        ),
        mount_target_ext_id=dict(type="str", required=False),
        operation_type=dict(
            type="str",
            choices=["ADD", "REMOVE"],
            obj=files_sdk.OperationType,
            required=True,
        ),
    )

    backup_server_config_spec = dict(
        expiry_in_secs=dict(type="int", required=False),
        backup_client_access_configs=dict(
            type="list",
            elements="dict",
            options=backup_client_access_config_spec,
            obj=files_sdk.BackupServerAccessControlBlock,
            required=False,
        ),
    )

    module_args = dict(
        ext_id=dict(type="str"),
        file_server_ext_id=dict(type="str", required=True),
        name=dict(type="str"),
        vendor_name=dict(type="str"),
        description=dict(type="str"),
        partner_type=dict(
            type="str",
            choices=["NOTIFICATION", "BACKUP", "MIGRATION"],
            obj=files_sdk.PartnerType,
        ),
        vendor_properties=dict(
            type="dict",
            options=vendor_properties_spec,
            obj=files_sdk.VendorProperties,
        ),
        backup_server_config=dict(
            type="dict",
            options=backup_server_config_spec,
            obj=files_sdk.BackupServerConfig,
        ),
    )
    return module_args


def create_partner_server(module, result, api_instance):
    file_server_ext_id = module.params.get("file_server_ext_id")
    name = module.params.get("name")
    validate_required_params(module, ["name", "vendor_name", "partner_type"])

    sg = SpecGenerator(module)
    default_spec = files_sdk.PartnerServer()
    spec, err = sg.generate_spec(obj=default_spec)
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating create partner server spec", **result)

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        return

    # Create idempotency: skip if a partner server with the same name already exists
    existing = get_partner_server_by_name(
        module, api_instance, file_server_ext_id, name
    )
    if existing:
        result["skipped"] = True
        result["ext_id"] = existing.ext_id
        result["response"] = strip_internal_attributes(existing.to_dict())
        result["msg"] = (
            "PartnerServer with name '{0}' already exists. Skipping creation.".format(
                name
            )
        )
        return

    resp = None
    try:
        resp = api_instance.create_partner_server(
            fileServerExtId=file_server_ext_id, body=spec
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while creating partner server",
        )
    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        task_status = wait_for_completion(module, task_ext_id)
        result["response"] = strip_internal_attributes(task_status.to_dict())
        ext_id = get_entity_ext_id_from_task(
            task_status, rel=TASK_CONSTANTS.RelEntityType.PARTNER_SERVER
        )
        # entitiesAffected can be unreliable for partner server creation, so
        # fall back to resolving the external ID from the partner server name.
        if not ext_id:
            partner_server = get_partner_server_by_name(
                module, api_instance, file_server_ext_id, name
            )
            ext_id = getattr(partner_server, "ext_id", None)
        if ext_id:
            result["ext_id"] = ext_id
            resp = get_partner_server(module, api_instance, file_server_ext_id, ext_id)
            result["response"] = strip_internal_attributes(resp.to_dict())
        else:
            raise_api_exception(
                module=module,
                exception=Exception(
                    "Failed to get entity ext_id from task for Partner Server"
                ),
                msg="Failed to get entity ext_id from task for Partner Server",
            )
    result["changed"] = True


def check_for_idempotency(old_spec_dict, update_spec_dict):
    old_spec_dict = strip_internal_attributes(deepcopy(old_spec_dict))
    update_spec_dict = strip_internal_attributes(deepcopy(update_spec_dict))
    for spec in (old_spec_dict, update_spec_dict):
        spec.pop("ext_id", None)
        spec.pop("links", None)
        spec.pop("tenant_id", None)
        vendor_properties = spec.get("vendor_properties")
        if isinstance(vendor_properties, dict):
            vendor_properties.pop("connection_status", None)
    return old_spec_dict == update_spec_dict


def update_partner_server(module, result, api_instance):
    file_server_ext_id = module.params.get("file_server_ext_id")
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id

    old_spec = get_partner_server(module, api_instance, file_server_ext_id, ext_id)
    etag = get_etag(data=old_spec)
    if not etag:
        return module.fail_json(
            "Unable to fetch etag for updating partner server", **result
        )
    kwargs = {"if_match": etag}

    sg = SpecGenerator(module)
    update_spec, err = sg.generate_spec(obj=deepcopy(old_spec))
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating update partner server spec", **result)

    strip_read_only_fields(update_spec)

    if module.check_mode:
        result["response"] = strip_internal_attributes(update_spec.to_dict())
        return

    if check_for_idempotency(old_spec.to_dict(), update_spec.to_dict()):
        result["skipped"] = True
        module.exit_json(msg="Nothing to change.", **result)

    resp = None
    try:
        resp = api_instance.update_partner_server_by_id(
            fileServerExtId=file_server_ext_id, extId=ext_id, body=update_spec, **kwargs
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while updating partner server",
        )
    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        wait_for_completion(module, task_ext_id)
        resp = get_partner_server(module, api_instance, file_server_ext_id, ext_id)
        result["response"] = strip_internal_attributes(resp.to_dict())
    result["changed"] = True


def delete_partner_server(module, result, api_instance):
    file_server_ext_id = module.params.get("file_server_ext_id")
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id

    if module.check_mode:
        result["msg"] = "Partner server with ext_id:{0} will be deleted.".format(ext_id)
        return

    resp = None
    try:
        resp = api_instance.delete_partner_server_by_id(
            fileServerExtId=file_server_ext_id, extId=ext_id
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while deleting partner server",
        )
    task_ext_id = getattr(getattr(resp, "data", None), "ext_id", None)
    result["task_ext_id"] = task_ext_id
    if task_ext_id and module.params.get("wait"):
        task_status = wait_for_completion(module, task_ext_id, True)
        result["response"] = strip_internal_attributes(task_status.to_dict())
    result["changed"] = True


def run_module():
    module = BaseModuleV4(
        argument_spec=get_module_spec(),
        supports_check_mode=True,
        required_if=[
            ("state", "present", ("name", "ext_id"), True),
            ("state", "absent", ("ext_id",)),
        ],
        mutually_exclusive=[
            ("vendor_properties", "backup_server_config"),
        ],
    )
    if SDK_IMP_ERROR:
        module.fail_json(
            msg=missing_required_lib("ntnx_files_py_client"),
            exception=SDK_IMP_ERROR,
        )

    remove_param_with_none_value(module.params)
    result = {
        "changed": False,
        "response": None,
        "failed": False,
        "ext_id": None,
    }
    api_instance = get_partner_servers_api_instance(module)
    state = module.params.get("state")
    if state == "present":
        if module.params.get("ext_id"):
            update_partner_server(module, result, api_instance)
        else:
            create_partner_server(module, result, api_instance)
    else:
        delete_partner_server(module, result, api_instance)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
