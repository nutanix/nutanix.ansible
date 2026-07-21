#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_files_antivirus_server_v2
short_description: Create, Update, Delete antivirus servers on a Nutanix Files file server
version_added: 2.7.0
description:
  - This module allows you to create, update, and delete antivirus (ICAP) servers on a Nutanix Files file server in Nutanix Prism Central.
  - An antivirus server configures the connection to an external ICAP appliance that Nutanix Files uses to scan files for viruses.
  - This module uses PC v4 APIs based SDKs.
notes:
  - This module requires an existing Nutanix Files file server. The antivirus server is configured under that file server.
  - "Ref: U(https://developers.nutanix.com/api-reference?namespace=files)"
options:
  state:
    description:
      - If C(state) is set to C(present) and C(ext_id) is not provided then the operation will be to create an antivirus server.
      - If C(state) is set to C(present) and C(ext_id) is provided then the operation will be to update the antivirus server.
      - If C(state) is set to C(absent) and C(ext_id) is provided then the operation will be to delete the antivirus server.
    type: str
    required: false
    choices:
      - present
      - absent
    default: present
  ext_id:
    description:
      - The external ID of the antivirus server.
      - Required for update and delete operations.
    type: str
    required: false
  file_server_ext_id:
    description:
      - The external identifier of the file server on which the antivirus server is configured.
      - Required for all operations.
    type: str
    required: true
  description:
    description:
      - Antivirus server description.
      - Maximum 180 characters.
    type: str
    required: false
  address:
    description:
      - The address (IP or fully qualified domain name) of the antivirus server.
      - Required for create operation only.
      - This field cannot be modified during an update operation.
    type: dict
    required: false
    suboptions:
      ipv4:
        description:
          - The IPv4 address of the antivirus server.
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
              - The prefix length of the network to which the IPv4 address belongs.
            type: int
            required: false
            default: 32
      ipv6:
        description:
          - The IPv6 address of the antivirus server.
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
              - The prefix length of the network to which the IPv6 address belongs.
            type: int
            required: false
            default: 128
      fqdn:
        description:
          - The fully qualified domain name of the antivirus server.
        type: dict
        required: false
        suboptions:
          value:
            description:
              - The fully qualified domain name value.
            type: str
            required: true
  port:
    description:
      - The port on which the antivirus (ICAP) server listens.
      - Required for create operation only.
      - This field cannot be modified during an update operation.
      - Value must be between 0 and 65535.
    type: int
    required: false
  partner_service_name:
    description:
      - The Internet Content Adaptation Protocol (ICAP) service name of the antivirus server.
      - Maximum 2048 characters.
    type: str
    required: false
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
- name: Create antivirus server with all attributes
  nutanix.ncp.ntnx_files_antivirus_server_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: present
    file_server_ext_id: "18f78959-14a6-4c47-b5db-920460c4b668"
    description: "Antivirus server created by Ansible"
    address:
      ipv4:
        value: "10.44.10.100"
    port: 1344
    partner_service_name: "avscan"
  register: result

- name: Update antivirus server
  nutanix.ncp.ntnx_files_antivirus_server_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: present
    file_server_ext_id: "18f78959-14a6-4c47-b5db-920460c4b668"
    ext_id: "b1c2d3e4-14a6-4c47-b5db-920460c4b668"
    description: "Antivirus server updated by Ansible"
    partner_service_name: "avscan-updated"
  register: result

- name: Delete antivirus server
  nutanix.ncp.ntnx_files_antivirus_server_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: absent
    file_server_ext_id: "18f78959-14a6-4c47-b5db-920460c4b668"
    ext_id: "b1c2d3e4-14a6-4c47-b5db-920460c4b668"
  register: result
"""

RETURN = r"""
response:
  description:
    - Response for creating, updating, or deleting an antivirus server.
    - If the operation is create or update and C(wait) is true, it will return the antivirus server details.
    - If the operation is create or update and C(wait) is false, it will return the task details.
    - If the operation is delete, it will return the task details.
  returned: always
  type: dict
  sample:
    {
      "address": {
          "fqdn": null,
          "ipv4": {
              "prefix_length": 32,
              "value": "10.44.10.100"
          },
          "ipv6": null
      },
      "connection_status": "NOT_TESTED",
      "description": "Antivirus server created by Ansible",
      "ext_id": "b1c2d3e4-14a6-4c47-b5db-920460c4b668",
      "links": null,
      "partner_service_name": "avscan",
      "port": 1344,
      "tenant_id": null
    }

task_ext_id:
  description:
    - The external ID of the task.
  returned: always
  type: str
  sample: "ZXJnb24=:90458bc7-a12b-4616-ac66-562fdb00c209"

ext_id:
  description:
    - The external ID of the antivirus server.
  returned: always
  type: str
  sample: "b1c2d3e4-14a6-4c47-b5db-920460c4b668"

changed:
  description: This indicates whether the task resulted in any changes
  returned: always
  type: bool
  sample: true

skipped:
  description: This indicates whether the task was skipped
  returned: always
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
  returned: When there is an error, module is idempotent or check mode (in delete operation)
  type: str
  sample: "Antivirus server with ext_id:b1c2d3e4-14a6-4c47-b5db-920460c4b668 will be deleted."
"""

import traceback  # noqa: E402
import warnings  # noqa: E402
from copy import deepcopy  # noqa: E402

from ansible.module_utils.basic import missing_required_lib  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_module_v4 import BaseModuleV4  # noqa: E402
from ..module_utils.v4.constants import Tasks as TASK_CONSTANTS  # noqa: E402
from ..module_utils.v4.files.api_client import (  # noqa: E402
    get_antivirus_servers_api_instance,
    get_etag,
)
from ..module_utils.v4.files.helpers import get_antivirus_server  # noqa: E402
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

# Read-only fields populated by the server that must be stripped before an update request
READ_ONLY_FIELDS = ["connection_status", "ext_id", "links", "tenant_id"]


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
        value=dict(type="str", required=True),
    )

    address_spec = dict(
        ipv4=dict(
            type="dict",
            options=ipv4_spec,
            required=False,
            obj=files_sdk.IPv4Address,
        ),
        ipv6=dict(
            type="dict",
            options=ipv6_spec,
            required=False,
            obj=files_sdk.IPv6Address,
        ),
        fqdn=dict(
            type="dict",
            options=fqdn_spec,
            required=False,
            obj=files_sdk.FQDN,
        ),
    )

    module_args = dict(
        ext_id=dict(type="str"),
        file_server_ext_id=dict(type="str", required=True),
        description=dict(type="str"),
        address=dict(
            type="dict",
            options=address_spec,
            mutually_exclusive=[("ipv4", "ipv6", "fqdn")],
            obj=files_sdk.IPAddressOrFQDN,
        ),
        port=dict(type="int"),
        partner_service_name=dict(type="str"),
    )
    return module_args


def create_antivirus_server(module, result, api_instance):
    file_server_ext_id = module.params.get("file_server_ext_id")
    validate_required_params(module, ["address", "port"])
    sg = SpecGenerator(module)
    default_spec = files_sdk.AntivirusServer()
    spec, err = sg.generate_spec(obj=default_spec)
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating create antivirus server spec", **result)

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        return

    resp = None
    try:
        resp = api_instance.create_antivirus_server(
            fileServerExtId=file_server_ext_id, body=spec
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while creating antivirus server",
        )
    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        task_status = wait_for_completion(module, task_ext_id)
        result["response"] = strip_internal_attributes(task_status.to_dict())
        ext_id = get_entity_ext_id_from_task(
            task_status, rel=TASK_CONSTANTS.RelEntityType.ANTIVIRUS_SERVER
        )
        if not ext_id:
            ext_id = get_entity_ext_id_from_task(task_status)
        if ext_id:
            result["ext_id"] = ext_id
            resp = get_antivirus_server(
                module, api_instance, ext_id, file_server_ext_id
            )
            result["response"] = strip_internal_attributes(resp.to_dict())
        else:
            raise_api_exception(
                module=module,
                exception=Exception(
                    "Failed to get entity ext_id from task for Antivirus Server"
                ),
                msg="Failed to get entity ext_id from task for Antivirus Server",
            )
    result["changed"] = True


def check_antivirus_server_idempotency(old_spec_dict, update_spec_dict):
    old_spec_dict = strip_internal_attributes(old_spec_dict)
    update_spec_dict = strip_internal_attributes(update_spec_dict)
    for field in READ_ONLY_FIELDS:
        old_spec_dict.pop(field, None)
        update_spec_dict.pop(field, None)
    return old_spec_dict == update_spec_dict


def update_antivirus_server(module, result, api_instance):
    ext_id = module.params.get("ext_id")
    file_server_ext_id = module.params.get("file_server_ext_id")
    result["ext_id"] = ext_id

    old_spec = get_antivirus_server(module, api_instance, ext_id, file_server_ext_id)
    etag = get_etag(data=old_spec)
    if not etag:
        return module.fail_json(
            "Unable to fetch etag for updating antivirus server", **result
        )
    kwargs = {"if_match": etag}
    sg = SpecGenerator(module)
    update_spec, err = sg.generate_spec(obj=deepcopy(old_spec))
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating update antivirus server spec", **result)

    if module.check_mode:
        result["response"] = strip_internal_attributes(update_spec.to_dict())
        return

    if check_antivirus_server_idempotency(old_spec.to_dict(), update_spec.to_dict()):
        result["skipped"] = True
        module.exit_json(msg="Nothing to change.")

    strip_read_only_fields(update_spec, fields=READ_ONLY_FIELDS)

    resp = None
    try:
        resp = api_instance.update_antivirus_server_by_id(
            fileServerExtId=file_server_ext_id, extId=ext_id, body=update_spec, **kwargs
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while updating antivirus server",
        )
    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        wait_for_completion(module, task_ext_id)
        resp = get_antivirus_server(module, api_instance, ext_id, file_server_ext_id)
        result["response"] = strip_internal_attributes(resp.to_dict())
    result["changed"] = True


def delete_antivirus_server(module, result, api_instance):
    ext_id = module.params.get("ext_id")
    file_server_ext_id = module.params.get("file_server_ext_id")
    result["ext_id"] = ext_id

    if module.check_mode:
        result["msg"] = "Antivirus server with ext_id:{0} will be deleted.".format(
            ext_id
        )
        return

    old_spec = get_antivirus_server(module, api_instance, ext_id, file_server_ext_id)
    etag = get_etag(data=old_spec)
    kwargs = {"if_match": etag} if etag else {}

    resp = None
    try:
        resp = api_instance.delete_antivirus_server_by_id(
            fileServerExtId=file_server_ext_id, extId=ext_id, **kwargs
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while deleting antivirus server",
        )
    task_ext_id = resp.data.ext_id
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
            ("state", "absent", ("ext_id",)),
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
    api_instance = get_antivirus_servers_api_instance(module)
    state = module.params.get("state")
    if state == "present":
        if module.params.get("ext_id"):
            update_antivirus_server(module, result, api_instance)
        else:
            create_antivirus_server(module, result, api_instance)
    else:
        delete_antivirus_server(module, result, api_instance)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
