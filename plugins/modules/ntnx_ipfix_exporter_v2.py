#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_ipfix_exporter_v2
short_description: Create, Update, Delete IPFIX Exporter in Nutanix Prism Central
version_added: 2.5.0
description:
  - This module allows you to create, update, and delete IPFIX Exporters in Nutanix Prism Central.
  - An IPFIX Exporter exports IP Flow Information Export (IPFIX) records
    from AHV hosts to an external collector for network traffic visibility
    and security analytics.
  - This module uses PC v4 APIs based SDKs.
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
      The required roles depend on the operation being performed.
    - >-
      B(Create an IPFIX Exporter) -
      Required Roles: Prism Admin, Super Admin
    - >-
      B(Delete an IPFIX Exporter) -
      Required Roles: Prism Admin, Super Admin
    - >-
      B(Update an IPFIX Exporter) -
      Required Roles: Prism Admin, Super Admin
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=networking)"
options:
  state:
    description:
      - If C(state) is set to C(present) and C(ext_id) is not provided then the operation will be create IPFIX exporter.
      - If C(state) is set to C(present) and C(ext_id) is provided then the operation will be update IPFIX exporter.
      - If C(state) is set to C(absent) and C(ext_id) is provided then the operation will be delete IPFIX exporter.
    type: str
    required: false
    choices:
      - present
      - absent
    default: present
  ext_id:
    description:
      - The external ID (UUID) of the IPFIX exporter.
      - Required for update and delete operations.
    type: str
    required: false
  name:
    description:
      - Name of the IPFIX Exporter.
      - Required for create operation.
      - Maximum 128 characters.
    type: str
    required: false
  description:
    description:
      - User provided description for the IPFIX Exporter.
    type: str
    required: false
  collector_ip:
    description:
      - IP address of the external IPFIX collector to which flow records are exported.
      - Required for create operation.
    type: str
    required: false
  collector_port:
    description:
      - UDP/TCP port on the external IPFIX collector to which flow records are exported.
      - Required for create operation.
    type: int
    required: false
  protocol:
    description:
      - Transport protocol used to send IPFIX flow records to the collector.
      - Required for create operation.
    type: str
    required: false
    choices:
      - TCP
      - UDP
      - TLS_TCP
  export_rate_limit_per_node_bps:
    description:
      - Maximum export rate limit per node in bits per second.
      - Used to cap the outgoing IPFIX traffic per AHV node to avoid overwhelming the collector.
    type: int
    required: false
  export_scopes:
    description:
      - List of scopes (Prism Central or Prism Element clusters) whose flow records
        should be exported by this IPFIX exporter.
      - Required for create operation.
    type: list
    elements: dict
    required: false
    suboptions:
      uuid:
        description:
          - UUID of the Prism Central (PC) or Prism Element (PE) cluster.
        type: str
        required: true
      scope_type:
        description:
          - Whether the referenced UUID belongs to a PC or a PE cluster.
        type: str
        required: false
        choices:
          - PC
          - PE
      ip_family:
        description:
          - IP address family for which flow records should be exported.
        type: str
        required: false
        choices:
          - V4
          - V6
          - BOTH
  metadata:
    description:
      - Metadata associated with the IPFIX exporter.
    type: dict
    required: false
    suboptions:
      owner_reference_id:
        description:
          - A globally unique identifier that represents the owner of this resource.
        type: str
        required: false
      owner_user_name:
        description:
          - The userName of the owner of this resource.
        type: str
        required: false
      project_reference_id:
        description:
          - A globally unique identifier that represents the project this resource belongs to.
        type: str
        required: false
      project_name:
        description:
          - The name of the project this resource belongs to.
        type: str
        required: false
      category_ids:
        description:
          - A list of globally unique identifiers that represent all the
            categories the resource is associated with.
        type: list
        elements: str
        required: false
extends_documentation_fragment:
  - nutanix.ncp.ntnx_credentials
  - nutanix.ncp.ntnx_operations_v2
  - nutanix.ncp.ntnx_logger
  - nutanix.ncp.ntnx_proxy_v2
author:
  - George Ghawali (@george-ghawali)
"""

EXAMPLES = r"""
- name: Create IPFIX exporter with all attributes
  nutanix.ncp.ntnx_ipfix_exporter_v2:
    state: present
    name: "ipfix_exporter_ansible_full"
    description: "IPFIX exporter created by Ansible"
    collector_ip: "10.44.10.20"
    collector_port: 4739
    protocol: "TCP"
    export_rate_limit_per_node_bps: 1000000
    export_scopes:
      - uuid: "bde7fc02-fe9c-4ce3-9212-2ca4e4b4d258"
        scope_type: "PE"
        ip_family: "V4"
  register: result

- name: Update IPFIX exporter
  nutanix.ncp.ntnx_ipfix_exporter_v2:
    state: present
    ext_id: "2e40ff57-20aa-4d2b-b179-298db969c20d"
    name: "ipfix_exporter_ansible_updated"
    description: "Updated IPFIX exporter description"
    collector_ip: "10.44.10.30"
    collector_port: 4739
    protocol: "TCP"
    export_rate_limit_per_node_bps: 2000000
    export_scopes:
      - uuid: "bde7fc02-fe9c-4ce3-9212-2ca4e4b4d258"
        scope_type: "PE"
        ip_family: "BOTH"
  register: result

- name: Delete IPFIX exporter
  nutanix.ncp.ntnx_ipfix_exporter_v2:
    state: absent
    ext_id: "2e40ff57-20aa-4d2b-b179-298db969c20d"
  register: result
"""

RETURN = r"""
response:
  description:
    - Response for creating, updating, or deleting IPFIX exporter.
    - If the operation is create or update and C(wait) is true, it will return the IPFIX exporter details.
    - If the operation is create or update and C(wait) is false, it will return the task details.
    - If the operation is delete, it will return the task details.
  returned: always
  type: dict
  sample:
    {
      "collector_ip": "10.44.10.20",
      "collector_port": 4739,
      "description": "IPFIX exporter created by Ansible example playbook",
      "export_rate_limit_per_node_bps": 1000000,
      "export_scopes": [
          {
              "ip_family": "V4",
              "scope_type": "PE",
              "uuid": "0006555e-4e63-4a5e-185b-ac1f6b6f97e2"
          }
      ],
      "ext_id": "db5429c8-f3a1-4cff-9d51-208a0fb175be",
      "links": null,
      "metadata": {
          "category_ids": null,
          "owner_reference_id": "00000000-0000-0000-0000-000000000000",
          "owner_user_name": "admin",
          "project_name": "_internal",
          "project_reference_id": "00000000-0000-0000-0000-000000000000"
      },
      "name": "ipfix_exporter_ansible_example",
      "protocol": "TCP",
      "tenant_id": null
    }

task_ext_id:
  description:
    - The external ID of the task associated with this operation.
  returned: always
  type: str
  sample: "ZXJnb24=:3b7a0e2a-e515-4fdd-ad01-1fe13aef79bc"

ext_id:
  description:
    - The external ID of the IPFIX exporter.
  returned: always
  type: str
  sample: "db5429c8-f3a1-4cff-9d51-208a0fb175be"

changed:
  description: This indicates whether the task resulted in any changes.
  returned: always
  type: bool
  sample: true

skipped:
  description: This indicates whether the task was skipped.
  returned: always
  type: bool
  sample: false

error:
  description: This indicates the error message if any error occurred.
  returned: When an error occurs
  type: str

failed:
  description: This indicates whether the task failed.
  returned: always
  type: bool
  sample: false

msg:
  description:
    - This indicates the message if any message occurred.
    - Populated on error, on idempotent runs, and on delete check_mode.
  returned: When there is an error, module is idempotent or check mode (in delete operation)
  type: str
  sample: "Api Exception raised while creating IPFIX exporter"
"""

import traceback  # noqa: E402
import warnings  # noqa: E402
from copy import deepcopy  # noqa: E402

from ansible.module_utils.basic import missing_required_lib  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_module_v4 import BaseModuleV4  # noqa: E402
from ..module_utils.v4.constants import Tasks as TASK_CONSTANTS  # noqa: E402
from ..module_utils.v4.network.api_client import (  # noqa: E402
    get_etag,
    get_ipfix_exporters_api_instance,
)
from ..module_utils.v4.network.helpers import get_ipfix_exporter  # noqa: E402
from ..module_utils.v4.prism.tasks import (  # noqa: E402
    get_entity_ext_id_from_task,
    wait_for_completion,
)
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
    validate_required_params,
)

SDK_IMP_ERROR = None
try:
    import ntnx_networking_py_client as networking_sdk  # noqa: E402
except ImportError:
    from ..module_utils.v4.sdk_mock import mock_sdk as networking_sdk  # noqa: E402

    SDK_IMP_ERROR = traceback.format_exc()

warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():

    export_scope_spec = dict(
        uuid=dict(type="str", required=True),
        scope_type=dict(
            type="str",
            required=False,
            choices=["PC", "PE"],
            obj=networking_sdk.ScopeType,
        ),
        ip_family=dict(
            type="str",
            required=False,
            choices=["V4", "V6", "BOTH"],
            obj=networking_sdk.IpFamily,
        ),
    )

    metadata_spec = dict(
        owner_reference_id=dict(type="str", required=False),
        owner_user_name=dict(type="str", required=False),
        project_reference_id=dict(type="str", required=False),
        project_name=dict(type="str", required=False),
        category_ids=dict(type="list", elements="str", required=False),
    )

    module_args = dict(
        ext_id=dict(type="str"),
        name=dict(type="str"),
        description=dict(type="str"),
        collector_ip=dict(type="str"),
        collector_port=dict(type="int"),
        protocol=dict(
            type="str",
            choices=["TCP", "UDP", "TLS_TCP"],
            obj=networking_sdk.ExporterProtocol,
        ),
        export_rate_limit_per_node_bps=dict(type="int"),
        export_scopes=dict(
            type="list",
            elements="dict",
            options=export_scope_spec,
            obj=networking_sdk.ExportScope,
        ),
        metadata=dict(
            type="dict",
            options=metadata_spec,
            obj=networking_sdk.Metadata,
        ),
    )
    return module_args


def create_IpfixExporter(module, result, api_instance):
    validate_required_params(
        module,
        ["name", "collector_ip", "collector_port", "protocol", "export_scopes"],
    )

    sg = SpecGenerator(module)
    default_spec = networking_sdk.IPFIXExporter()
    spec, err = sg.generate_spec(obj=default_spec)
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating create IPFIX exporter spec", **result)

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        return

    resp = None
    try:
        resp = api_instance.create_ipfix_exporter(body=spec)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while creating IPFIX exporter",
        )

    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())

    if task_ext_id and module.params.get("wait"):
        task_status = wait_for_completion(module, task_ext_id)
        result["response"] = strip_internal_attributes(task_status.to_dict())
        ext_id = get_entity_ext_id_from_task(
            task_status, rel=TASK_CONSTANTS.RelEntityType.IPFIX_EXPORTER
        )
        if ext_id:
            result["ext_id"] = ext_id
            resp = get_ipfix_exporter(module, api_instance, ext_id)
            result["response"] = strip_internal_attributes(resp.to_dict())
        else:
            raise_api_exception(
                module=module,
                exception=Exception(
                    "Failed to get entity ext_id from task for IPFIX Exporter"
                ),
                msg="Failed to get entity ext_id from task for IPFIX Exporter",
            )
    result["changed"] = True


def check_for_idempotency(old_spec_dict, update_spec_dict):
    old_spec_dict = strip_internal_attributes(deepcopy(old_spec_dict))
    update_spec_dict = strip_internal_attributes(deepcopy(update_spec_dict))
    return old_spec_dict == update_spec_dict


def update_IpfixExporter(module, result, api_instance):
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id

    old_spec = get_ipfix_exporter(module, api_instance, ext_id)
    etag = get_etag(data=old_spec)
    if not etag:
        return module.fail_json(
            msg="Unable to fetch etag for updating IPFIX exporter", **result
        )
    kwargs = {"if_match": etag}

    sg = SpecGenerator(module)
    update_spec, err = sg.generate_spec(obj=deepcopy(old_spec))
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating update IPFIX exporter spec", **result)

    if module.check_mode:
        result["response"] = strip_internal_attributes(update_spec.to_dict())
        return

    if check_for_idempotency(old_spec.to_dict(), update_spec.to_dict()):
        result["skipped"] = True
        module.exit_json(msg="Nothing to change.", **result)

    resp = None
    try:
        resp = api_instance.update_ipfix_exporter_by_id(
            extId=ext_id, body=update_spec, **kwargs
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while updating IPFIX exporter",
        )

    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())

    if task_ext_id and module.params.get("wait"):
        wait_for_completion(module, task_ext_id)
        resp = get_ipfix_exporter(module, api_instance, ext_id)
        result["response"] = strip_internal_attributes(resp.to_dict())
    result["changed"] = True


def delete_IpfixExporter(module, result, api_instance):
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id

    if module.check_mode:
        result["msg"] = "IPFIX exporter with ext_id:{0} will be deleted.".format(ext_id)
        return

    current_spec = get_ipfix_exporter(module, api_instance, ext_id)
    etag = get_etag(data=current_spec)
    kwargs = {}
    if etag:
        kwargs["if_match"] = etag

    resp = None
    try:
        resp = api_instance.delete_ipfix_exporter_by_id(extId=ext_id, **kwargs)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while deleting IPFIX exporter",
        )

    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())

    if task_ext_id and module.params.get("wait"):
        task_status = wait_for_completion(module, task_ext_id, raise_error=True)
        result["response"] = strip_internal_attributes(task_status.to_dict())
    result["changed"] = True


def run_module():
    module = BaseModuleV4(
        argument_spec=get_module_spec(),
        supports_check_mode=True,
        required_if=[
            ("state", "absent", ("ext_id",)),
            ("state", "present", ("name", "ext_id"), True),
        ],
    )
    if SDK_IMP_ERROR:
        module.fail_json(
            msg=missing_required_lib("ntnx_networking_py_client"),
            exception=SDK_IMP_ERROR,
        )

    remove_param_with_none_value(module.params)
    result = {
        "changed": False,
        "response": None,
        "failed": False,
        "ext_id": None,
        "task_ext_id": None,
    }
    api_instance = get_ipfix_exporters_api_instance(module)
    state = module.params.get("state")
    if state == "present":
        if module.params.get("ext_id"):
            update_IpfixExporter(module, result, api_instance)
        else:
            create_IpfixExporter(module, result, api_instance)
    else:
        delete_IpfixExporter(module, result, api_instance)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
