#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_data_services_ip_mapping_v2
short_description: Create, Update, Delete Data Services IP Mapping of a Recovery Plan in Nutanix Prism Central
version_added: 2.7.0
description:
  - This module allows you to create, update, and delete a Data Services IP Mapping under a Recovery Plan in Nutanix Prism Central.
  - Data Services IP Mapping defines the mapping between the data services IP of primary and recovery Prism Elements
    used to establish the iSCSI connection between recovered VMs and recovered Volume Groups when network segmentation
    is enabled.
  - This module uses PC v4 APIs based SDKs.
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
      The required roles depend on the operation being performed.
    - >-
      B(Create a Data Services IP Mapping) -
      Required Roles: Account Owner, Administrator, Disaster Recovery Admin, Prism Admin, Super Admin
    - >-
      B(Update a Data Services IP Mapping) -
      Required Roles: Account Owner, Administrator, Disaster Recovery Admin, Prism Admin, Super Admin
    - >-
      B(Delete a Data Services IP Mapping) -
      Required Roles: Account Owner, Administrator, Disaster Recovery Admin, Prism Admin, Super Admin
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=datapolicies)"
options:
  state:
    description:
      - If C(state) is set to C(present) and C(ext_id) is not provided then the operation will create a Data Services IP Mapping.
      - If C(state) is set to C(present) and C(ext_id) is provided then the operation will update the Data Services IP Mapping.
      - If C(state) is set to C(absent) and C(ext_id) is provided then the operation will delete the Data Services IP Mapping.
    type: str
    required: false
    choices:
      - present
      - absent
    default: present
  ext_id:
    description:
      - The external ID of the Data Services IP Mapping.
      - Required for update and delete operations.
    type: str
    required: false
  recovery_plan_ext_id:
    description:
      - External identifier of the recovery plan under which the Data Services IP Mapping exists.
      - Required for all operations.
    type: str
    required: true
  primary_cluster:
    description:
      - Reference to the primary Prism Element cluster.
      - Required for create operation.
    type: dict
    required: false
    suboptions:
      ext_id:
        description:
          - External identifier of the primary cluster entity.
        type: str
        required: true
  recovery_cluster:
    description:
      - Reference to the recovery Prism Element cluster.
    type: dict
    required: false
    suboptions:
      ext_id:
        description:
          - External identifier of the recovery cluster entity.
        type: str
        required: true
  primary_data_services_ip:
    description:
      - Data Services IP address of the primary Prism Element cluster.
      - Provide exactly one of I(ipv4) or I(ipv6) inside this mapping.
    type: dict
    required: false
    suboptions:
      ipv4:
        description:
          - IPv4 address of the primary Data Services IP.
        type: dict
        required: false
        suboptions:
          value:
            description:
              - IPv4 address value.
            type: str
            required: true
          prefix_length:
            description:
              - Prefix length of the IPv4 network.
            type: int
            required: false
            default: 32
      ipv6:
        description:
          - IPv6 address of the primary Data Services IP.
        type: dict
        required: false
        suboptions:
          value:
            description:
              - IPv6 address value.
            type: str
            required: true
          prefix_length:
            description:
              - Prefix length of the IPv6 network.
            type: int
            required: false
            default: 128
  recovery_data_services_ip:
    description:
      - Data Services IP address of the recovery Prism Element cluster used during planned or unplanned failover.
      - Provide exactly one of I(ipv4) or I(ipv6) inside this mapping.
    type: dict
    required: false
    suboptions:
      ipv4:
        description:
          - IPv4 address of the recovery Data Services IP.
        type: dict
        required: false
        suboptions:
          value:
            description:
              - IPv4 address value.
            type: str
            required: true
          prefix_length:
            description:
              - Prefix length of the IPv4 network.
            type: int
            required: false
            default: 32
      ipv6:
        description:
          - IPv6 address of the recovery Data Services IP.
        type: dict
        required: false
        suboptions:
          value:
            description:
              - IPv6 address value.
            type: str
            required: true
          prefix_length:
            description:
              - Prefix length of the IPv6 network.
            type: int
            required: false
            default: 128
  primary_test_data_services_ip:
    description:
      - Data Services IP address of the primary Prism Element cluster used during test failback.
      - Provide exactly one of I(ipv4) or I(ipv6) inside this mapping.
    type: dict
    required: false
    suboptions:
      ipv4:
        description:
          - IPv4 address of the primary test Data Services IP.
        type: dict
        required: false
        suboptions:
          value:
            description:
              - IPv4 address value.
            type: str
            required: true
          prefix_length:
            description:
              - Prefix length of the IPv4 network.
            type: int
            required: false
            default: 32
      ipv6:
        description:
          - IPv6 address of the primary test Data Services IP.
        type: dict
        required: false
        suboptions:
          value:
            description:
              - IPv6 address value.
            type: str
            required: true
          prefix_length:
            description:
              - Prefix length of the IPv6 network.
            type: int
            required: false
            default: 128
  recovery_test_data_services_ip:
    description:
      - Data Services IP address of the recovery Prism Element cluster used during test failover.
      - Provide exactly one of I(ipv4) or I(ipv6) inside this mapping.
    type: dict
    required: false
    suboptions:
      ipv4:
        description:
          - IPv4 address of the recovery test Data Services IP.
        type: dict
        required: false
        suboptions:
          value:
            description:
              - IPv4 address value.
            type: str
            required: true
          prefix_length:
            description:
              - Prefix length of the IPv4 network.
            type: int
            required: false
            default: 32
      ipv6:
        description:
          - IPv6 address of the recovery test Data Services IP.
        type: dict
        required: false
        suboptions:
          value:
            description:
              - IPv6 address value.
            type: str
            required: true
          prefix_length:
            description:
              - Prefix length of the IPv6 network.
            type: int
            required: false
            default: 128
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
- name: Create Data Services IP Mapping
  nutanix.ncp.ntnx_data_services_ip_mapping_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: present
    recovery_plan_ext_id: "b3a6932b-f64e-49ee-924d-c5a5b8ce2f3f"
    primary_cluster:
      ext_id: "0005f7bf-3e2b-4a41-0000-000000029d0e"
    recovery_cluster:
      ext_id: "000647b8-ddb3-6bbb-0000-000000028f57"
    primary_data_services_ip:
      ipv4:
        value: "10.44.76.55"
        prefix_length: 32
    recovery_data_services_ip:
      ipv4:
        value: "10.44.77.55"
        prefix_length: 32
    primary_test_data_services_ip:
      ipv4:
        value: "10.44.76.56"
        prefix_length: 32
    recovery_test_data_services_ip:
      ipv4:
        value: "10.44.77.56"
        prefix_length: 32
  register: result

- name: Update Data Services IP Mapping
  nutanix.ncp.ntnx_data_services_ip_mapping_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: present
    recovery_plan_ext_id: "b3a6932b-f64e-49ee-924d-c5a5b8ce2f3f"
    ext_id: "e7ae4b0d-726d-410d-87c2-af46f8bea264"
    primary_cluster:
      ext_id: "0005f7bf-3e2b-4a41-0000-000000029d0e"
    recovery_cluster:
      ext_id: "000647b8-ddb3-6bbb-0000-000000028f57"
    primary_data_services_ip:
      ipv4:
        value: "10.44.76.65"
        prefix_length: 32
    recovery_data_services_ip:
      ipv4:
        value: "10.44.77.65"
        prefix_length: 32
    primary_test_data_services_ip:
      ipv4:
        value: "10.44.76.66"
        prefix_length: 32
    recovery_test_data_services_ip:
      ipv4:
        value: "10.44.77.66"
        prefix_length: 32
  register: result

- name: Delete Data Services IP Mapping
  nutanix.ncp.ntnx_data_services_ip_mapping_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: absent
    recovery_plan_ext_id: "b3a6932b-f64e-49ee-924d-c5a5b8ce2f3f"
    ext_id: "e7ae4b0d-726d-410d-87c2-af46f8bea264"
  register: result
"""

RETURN = r"""
response:
  description:
    - Response for creating, updating, or deleting a Data Services IP Mapping.
    - If the operation is create or update and C(wait) is true, it will return the Data Services IP Mapping details.
    - If the operation is create or update and C(wait) is false, it will return the task details.
    - If the operation is delete, it will return the task details.
  returned: always
  type: dict
  sample:
    {
        "ext_id": "e7ae4b0d-726d-410d-87c2-af46f8bea264",
        "links": null,
        "primary_cluster": {
            "ext_id": "0005f7bf-3e2b-4a41-0000-000000029d0e",
            "name": null
        },
        "primary_data_services_ip": {
            "ipv4": {
                "prefix_length": 32,
                "value": "10.44.76.55"
            },
            "ipv6": null
        },
        "primary_test_data_services_ip": {
            "ipv4": {
                "prefix_length": 32,
                "value": "10.44.76.56"
            },
            "ipv6": null
        },
        "recovery_cluster": {
            "ext_id": "000647b8-ddb3-6bbb-0000-000000028f57",
            "name": null
        },
        "recovery_data_services_ip": {
            "ipv4": {
                "prefix_length": 32,
                "value": "10.44.77.55"
            },
            "ipv6": null
        },
        "recovery_test_data_services_ip": {
            "ipv4": {
                "prefix_length": 32,
                "value": "10.44.77.56"
            },
            "ipv6": null
        },
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
    - The external ID of the Data Services IP Mapping.
  returned: always
  type: str
  sample: "e7ae4b0d-726d-410d-87c2-af46f8bea264"

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
  description: This indicates the message if any message occurred.
  returned: When there is an error, module is idempotent or check mode (in delete operation)
  type: str
  sample: "Api Exception raised while creating Data Services IP Mapping"
"""

import traceback  # noqa: E402
import warnings  # noqa: E402
from copy import deepcopy  # noqa: E402

from ansible.module_utils.basic import missing_required_lib  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_module_v4 import BaseModuleV4  # noqa: E402
from ..module_utils.v4.constants import Tasks as TASK_CONSTANTS  # noqa: E402
from ..module_utils.v4.data_policies.api_client import (  # noqa: E402
    get_etag,
    get_recovery_plans_api_instance,
)
from ..module_utils.v4.data_policies.helpers import (  # noqa: E402
    get_data_services_ip_mapping,
)
from ..module_utils.v4.prism.tasks import (  # noqa: E402
    get_entity_ext_id_from_task,
    get_ext_id_from_task_completion_details,
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
    import ntnx_datapolicies_py_client as data_policies_sdk  # noqa: E402
except ImportError:

    from ..module_utils.v4.sdk_mock import mock_sdk as data_policies_sdk  # noqa: E402

    SDK_IMP_ERROR = traceback.format_exc()

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():

    ipv4_address_spec = dict(
        value=dict(type="str", required=True),
        prefix_length=dict(type="int", required=False, default=32),
    )

    ipv6_address_spec = dict(
        value=dict(type="str", required=True),
        prefix_length=dict(type="int", required=False, default=128),
    )

    ip_address_spec = dict(
        ipv4=dict(
            type="dict",
            options=ipv4_address_spec,
            required=False,
            obj=data_policies_sdk.IPv4Address,
        ),
        ipv6=dict(
            type="dict",
            options=ipv6_address_spec,
            required=False,
            obj=data_policies_sdk.IPv6Address,
        ),
    )

    entity_reference_spec = dict(
        ext_id=dict(type="str", required=True),
    )

    module_args = dict(
        ext_id=dict(type="str"),
        recovery_plan_ext_id=dict(type="str", required=True),
        primary_cluster=dict(
            type="dict",
            options=entity_reference_spec,
            obj=data_policies_sdk.EntityReference,
        ),
        recovery_cluster=dict(
            type="dict",
            options=entity_reference_spec,
            obj=data_policies_sdk.EntityReference,
        ),
        primary_data_services_ip=dict(
            type="dict",
            options=ip_address_spec,
            obj=data_policies_sdk.IPAddress,
            mutually_exclusive=[("ipv4", "ipv6")],
            required_one_of=[("ipv4", "ipv6")],
        ),
        recovery_data_services_ip=dict(
            type="dict",
            options=ip_address_spec,
            obj=data_policies_sdk.IPAddress,
            mutually_exclusive=[("ipv4", "ipv6")],
            required_one_of=[("ipv4", "ipv6")],
        ),
        primary_test_data_services_ip=dict(
            type="dict",
            options=ip_address_spec,
            obj=data_policies_sdk.IPAddress,
            mutually_exclusive=[("ipv4", "ipv6")],
            required_one_of=[("ipv4", "ipv6")],
        ),
        recovery_test_data_services_ip=dict(
            type="dict",
            options=ip_address_spec,
            obj=data_policies_sdk.IPAddress,
            mutually_exclusive=[("ipv4", "ipv6")],
            required_one_of=[("ipv4", "ipv6")],
        ),
    )
    return module_args


def create_DataServicesIpMapping(module, result, api_instance):
    validate_required_params(module, ["primary_cluster"])
    recovery_plan_ext_id = module.params.get("recovery_plan_ext_id")

    sg = SpecGenerator(module)
    default_spec = data_policies_sdk.DataServicesIpMapping()
    spec, err = sg.generate_spec(obj=default_spec)
    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed generating create Data Services IP Mapping spec", **result
        )

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        return

    resp = None
    try:
        resp = api_instance.create_data_services_ip_mapping(
            recoveryPlanExtId=recovery_plan_ext_id, body=spec
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while creating Data Services IP Mapping",
        )
    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        resp = wait_for_completion(module, task_ext_id)
        result["response"] = strip_internal_attributes(resp.to_dict())
        ext_id = _extract_data_services_ip_mapping_ext_id(resp, recovery_plan_ext_id)
        if ext_id:
            result["ext_id"] = ext_id
            resp = get_data_services_ip_mapping(
                module, api_instance, recovery_plan_ext_id, ext_id
            )
            result["response"] = strip_internal_attributes(resp.to_dict())
        else:
            raise_api_exception(
                module=module,
                exception=Exception(
                    "Failed to get entity ext_id from task for Data Services IP Mapping"
                ),
                msg="Failed to get entity ext_id from task for Data Services IP Mapping",
            )
    result["changed"] = True


def _extract_data_services_ip_mapping_ext_id(task, recovery_plan_ext_id):
    """
    Resolve the Data Services IP Mapping ext_id from a completed task.

    Order of resolution:
    1. entities_affected entry whose ``rel`` matches DATA_SERVICES_IP_MAPPING.
    2. completion_details entry named ``dataServicesIpMappingExtId``.
    3. First entities_affected entry whose ext_id differs from the parent
       recovery plan ext_id (fallback for evolving task rel strings).
    """
    ext_id = get_entity_ext_id_from_task(
        task, rel=TASK_CONSTANTS.RelEntityType.DATA_SERVICES_IP_MAPPING
    )
    if ext_id:
        return ext_id

    ext_id = get_ext_id_from_task_completion_details(
        task, name="dataServicesIpMappingExtId"
    )
    if ext_id:
        return ext_id

    for entity in getattr(task, "entities_affected", []) or []:
        entity_ext_id = getattr(entity, "ext_id", None)
        if entity_ext_id and entity_ext_id != recovery_plan_ext_id:
            return entity_ext_id
    return None


def check_for_idempotency(old_spec, update_spec):
    old_spec = strip_internal_attributes(old_spec)
    update_spec = strip_internal_attributes(update_spec)
    return old_spec == update_spec


def update_DataServicesIpMapping(module, result, api_instance):
    ext_id = module.params.get("ext_id")
    recovery_plan_ext_id = module.params.get("recovery_plan_ext_id")
    result["ext_id"] = ext_id

    old_spec = get_data_services_ip_mapping(
        module, api_instance, recovery_plan_ext_id, ext_id
    )
    etag = get_etag(data=old_spec)
    if not etag:
        return module.fail_json(
            "Unable to fetch etag for updating Data Services IP Mapping", **result
        )

    sg = SpecGenerator(module)
    update_spec, err = sg.generate_spec(obj=deepcopy(old_spec))
    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed generating update Data Services IP Mapping spec", **result
        )

    if module.check_mode:
        result["response"] = strip_internal_attributes(update_spec.to_dict())
        return

    if check_for_idempotency(old_spec.to_dict(), update_spec.to_dict()):
        result["skipped"] = True
        module.exit_json(msg="Nothing to change.", **result)

    strip_read_only_fields(update_spec, fields=["links", "tenant_id"])

    kwargs = {"if_match": etag}
    resp = None
    try:
        resp = api_instance.update_data_services_ip_mapping_by_id(
            recoveryPlanExtId=recovery_plan_ext_id,
            extId=ext_id,
            body=update_spec,
            **kwargs,
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while updating Data Services IP Mapping",
        )
    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        wait_for_completion(module, task_ext_id)
        resp = get_data_services_ip_mapping(
            module, api_instance, recovery_plan_ext_id, ext_id
        )
        result["response"] = strip_internal_attributes(resp.to_dict())
    result["changed"] = True


def delete_DataServicesIpMapping(module, result, api_instance):
    ext_id = module.params.get("ext_id")
    recovery_plan_ext_id = module.params.get("recovery_plan_ext_id")
    result["ext_id"] = ext_id

    if module.check_mode:
        result["msg"] = (
            "Data Services IP Mapping with ext_id:{0} will be deleted.".format(ext_id)
        )
        return

    resp = None
    try:
        resp = api_instance.delete_data_services_ip_mapping_by_id(
            recoveryPlanExtId=recovery_plan_ext_id, extId=ext_id
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while deleting Data Services IP Mapping",
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
            msg=missing_required_lib("ntnx_datapolicies_py_client"),
            exception=SDK_IMP_ERROR,
        )

    remove_param_with_none_value(module.params)
    result = {
        "changed": False,
        "response": None,
        "ext_id": None,
        "task_ext_id": None,
    }
    api_instance = get_recovery_plans_api_instance(module)
    state = module.params.get("state")
    if state == "present":
        if module.params.get("ext_id"):
            update_DataServicesIpMapping(module, result, api_instance)
        else:
            create_DataServicesIpMapping(module, result, api_instance)
    else:
        delete_DataServicesIpMapping(module, result, api_instance)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
