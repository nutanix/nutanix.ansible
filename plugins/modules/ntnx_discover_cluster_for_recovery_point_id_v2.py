#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_discover_cluster_for_recovery_point_id_v2
short_description: Discover the cluster hosting a recovery point in Nutanix Prism Central
version_added: 2.7.0
description:
  - This module allows you to discover the cluster hosting a recovery point in Nutanix Prism Central.
  - The API returns the redirect cluster IP and a JWT token that must be set as a session
    cookie while invoking the follow-up Changed Block Tracking (CBT) or VSS metadata endpoints
    on that cluster.
  - Use C(operation=COMPUTE_CHANGED_REGIONS) to discover the cluster before invoking the
    compute changed regions APIs.
  - Use C(operation=GET_VSS_METADATA) to discover the cluster before invoking the VSS
    metadata API for a VM recovery point.
  - This module uses PC v4 APIs based SDKs.
notes:
  - >-
    This module requires the following Nutanix IAM roles to be assigned to the user
    performing the operation.
  - >-
    B(Discover cluster for a recovery point) -
    Required Roles: Backup Admin, CSI System, Disaster Recovery Admin, Kubernetes Data
    Services System, NCM Connector, Prism Admin, Project Manager, Super Admin,
    Self-Service Admin (deprecated)
  - "Ref: U(https://developers.nutanix.com/api-reference?namespace=dataprotection)"
options:
  state:
    description:
      - State of the module.
      - If C(state) is set to C(present), the module will discover the cluster for the recovery point.
      - The action is idempotent from the API perspective. C(changed) is set to C(false) since no
        persistent server-side change is made.
    type: str
    choices:
      - present
    default: present
  ext_id:
    description:
      - The external identifier of the recovery point whose cluster is to be discovered.
    type: str
    required: true
  operation:
    description:
      - The follow-up operation for which the cluster is being discovered.
      - Use C(COMPUTE_CHANGED_REGIONS) for CBT (compute changed regions) workflows.
      - Use C(GET_VSS_METADATA) to fetch VSS metadata for a VM recovery point.
    type: str
    required: true
    choices:
      - COMPUTE_CHANGED_REGIONS
      - GET_VSS_METADATA
  spec:
    description:
      - The operation-specific request specification.
      - Exactly one of C(get_vss_metadata) or C(compute_changed_regions) must be provided,
        matching the C(operation) selected.
    type: dict
    required: true
    suboptions:
      get_vss_metadata:
        description:
          - Specification for the C(GET_VSS_METADATA) operation.
          - Required when C(operation=GET_VSS_METADATA).
        type: dict
        suboptions:
          vm_recovery_point_ext_id:
            description:
              - The external identifier of the VM recovery point whose VSS metadata is to be fetched.
            type: str
            required: true
      compute_changed_regions:
        description:
          - Specification for the C(COMPUTE_CHANGED_REGIONS) operation.
          - Required when C(operation=COMPUTE_CHANGED_REGIONS).
        type: dict
        suboptions:
          disk_recovery_point:
            description:
              - Reference to the disk recovery point for which changed regions will be computed.
              - Exactly one of C(vm_disk_recovery_point) or C(volume_group_disk_recovery_point)
                must be provided.
            type: dict
            suboptions:
              vm_disk_recovery_point:
                description:
                  - Reference to a VM disk recovery point.
                type: dict
                suboptions:
                  vm_recovery_point_ext_id:
                    description:
                      - External identifier of the VM recovery point.
                    type: str
                  recovery_point_ext_id:
                    description:
                      - External identifier of the top level recovery point.
                    type: str
                  disk_recovery_point_ext_id:
                    description:
                      - Disk recovery point identifier.
                    type: str
              volume_group_disk_recovery_point:
                description:
                  - Reference to a volume group disk recovery point.
                type: dict
                suboptions:
                  volume_group_recovery_point_ext_id:
                    description:
                      - External identifier of the volume group recovery point.
                    type: str
                  recovery_point_ext_id:
                    description:
                      - External identifier of the top level recovery point.
                    type: str
                  disk_recovery_point_ext_id:
                    description:
                      - Disk recovery point identifier.
                    type: str
          reference_disk_recovery_point:
            description:
              - Optional reference disk recovery point to compute changed regions against.
              - Exactly one of C(vm_disk_recovery_point) or C(volume_group_disk_recovery_point)
                must be provided when set.
            type: dict
            suboptions:
              vm_disk_recovery_point:
                description:
                  - Reference to a VM disk recovery point.
                type: dict
                suboptions:
                  vm_recovery_point_ext_id:
                    description:
                      - External identifier of the VM recovery point.
                    type: str
                  recovery_point_ext_id:
                    description:
                      - External identifier of the top level recovery point.
                    type: str
                  disk_recovery_point_ext_id:
                    description:
                      - Disk recovery point identifier.
                    type: str
              volume_group_disk_recovery_point:
                description:
                  - Reference to a volume group disk recovery point.
                type: dict
                suboptions:
                  volume_group_recovery_point_ext_id:
                    description:
                      - External identifier of the volume group recovery point.
                    type: str
                  recovery_point_ext_id:
                    description:
                      - External identifier of the top level recovery point.
                    type: str
                  disk_recovery_point_ext_id:
                    description:
                      - Disk recovery point identifier.
                    type: str
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
- name: Discover cluster for a recovery point (GET_VSS_METADATA)
  nutanix.ncp.ntnx_discover_cluster_for_recovery_point_id_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    ext_id: "1ca2963d-77b6-453a-ae23-2c19e7a954a3"
    operation: "GET_VSS_METADATA"
    spec:
      get_vss_metadata:
        vm_recovery_point_ext_id: "522670d7-e92d-45c5-9139-76ccff6813c2"
  register: result
  ignore_errors: true

- name: Discover cluster for a recovery point (COMPUTE_CHANGED_REGIONS - VM)
  nutanix.ncp.ntnx_discover_cluster_for_recovery_point_id_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    ext_id: "1ca2963d-77b6-453a-ae23-2c19e7a954a3"
    operation: "COMPUTE_CHANGED_REGIONS"
    spec:
      compute_changed_regions:
        disk_recovery_point:
          vm_disk_recovery_point:
            vm_recovery_point_ext_id: "522670d7-e92d-45c5-9139-76ccff6813c2"
            recovery_point_ext_id: "1ca2963d-77b6-453a-ae23-2c19e7a954a3"
            disk_recovery_point_ext_id: "94e61902-1954-4d54-917a-a28205454fce"
        reference_disk_recovery_point:
          vm_disk_recovery_point:
            vm_recovery_point_ext_id: "6f2d4f89-cba1-4a45-b3b3-3ec8b71ac13f"
            recovery_point_ext_id: "aa2963d1-77b6-453a-ae23-2c19e7a95400"
            disk_recovery_point_ext_id: "1b96075e-4786-4409-82bd-764e23d877a6"
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
  description:
    - Response from the discover cluster for recovery point API.
    - Contains the cluster IP address and the JWT token to be used for the follow-up
      CBT or VSS metadata calls.
  returned: always
  type: dict
  sample:
    {
      "cluster_ip": {
        "ipv4": {
          "value": "10.44.76.29",
          "prefix_length": 32
        },
        "ipv6": null
      },
      "jwt_token": "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9..."
    }

changed:
  description: This indicates whether the task resulted in any changes.
  returned: always
  type: bool
  sample: false

msg:
  description: This indicates the message if any message occurred.
  returned: When there is an error
  type: str
  sample: "Api Exception raised while discovering cluster for recovery point"

error:
  description: This field typically holds information about if the task have errors that occurred during the task execution.
  returned: when an error occurs
  type: str

failed:
  description: This field typically holds information about if the task have failed.
  returned: always
  type: bool
  sample: false

ext_id:
  description: The external ID of the recovery point.
  returned: always
  type: str
  sample: "1ca2963d-77b6-453a-ae23-2c19e7a954a3"
"""

import traceback  # noqa: E402
import warnings  # noqa: E402

from ansible.module_utils.basic import missing_required_lib  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_module_v4 import BaseModuleV4  # noqa: E402
from ..module_utils.v4.data_protection.api_client import (  # noqa: E402
    get_recovery_point_api_instance,
)
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
)

SDK_IMP_ERROR = None
try:
    import ntnx_dataprotection_py_client as data_protection_sdk  # noqa: E402
except ImportError:

    from ..module_utils.v4.sdk_mock import mock_sdk as data_protection_sdk  # noqa: E402

    SDK_IMP_ERROR = traceback.format_exc()

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():

    disk_recovery_point_options = dict(
        vm_disk_recovery_point=dict(
            type="dict",
            options=dict(
                vm_recovery_point_ext_id=dict(type="str"),
                recovery_point_ext_id=dict(type="str"),
                disk_recovery_point_ext_id=dict(type="str"),
            ),
        ),
        volume_group_disk_recovery_point=dict(
            type="dict",
            options=dict(
                volume_group_recovery_point_ext_id=dict(type="str"),
                recovery_point_ext_id=dict(type="str"),
                disk_recovery_point_ext_id=dict(type="str"),
            ),
        ),
    )

    compute_changed_regions_sub_spec = dict(
        disk_recovery_point=dict(
            type="dict",
            options=disk_recovery_point_options,
            mutually_exclusive=[
                ("vm_disk_recovery_point", "volume_group_disk_recovery_point"),
            ],
        ),
        reference_disk_recovery_point=dict(
            type="dict",
            options=disk_recovery_point_options,
            mutually_exclusive=[
                ("vm_disk_recovery_point", "volume_group_disk_recovery_point"),
            ],
        ),
    )

    get_vss_metadata_sub_spec = dict(
        vm_recovery_point_ext_id=dict(type="str", required=True),
    )

    spec_sub_spec = dict(
        get_vss_metadata=dict(type="dict", options=get_vss_metadata_sub_spec),
        compute_changed_regions=dict(
            type="dict", options=compute_changed_regions_sub_spec
        ),
    )

    module_args = dict(
        state=dict(type="str", default="present", choices=["present"]),
        ext_id=dict(type="str", required=True),
        operation=dict(
            type="str",
            required=True,
            choices=["COMPUTE_CHANGED_REGIONS", "GET_VSS_METADATA"],
        ),
        spec=dict(
            type="dict",
            required=True,
            options=spec_sub_spec,
            mutually_exclusive=[("get_vss_metadata", "compute_changed_regions")],
        ),
    )
    return module_args


def _build_disk_recovery_point_reference(reference):
    """Build the disk recovery point reference SDK object.

    ``reference`` is the dict from the module spec containing exactly one of
    ``vm_disk_recovery_point`` or ``volume_group_disk_recovery_point``.
    Returns ``None`` if neither is provided.
    """
    if not reference:
        return None
    vm_ref = reference.get("vm_disk_recovery_point")
    vg_ref = reference.get("volume_group_disk_recovery_point")
    if vm_ref:
        obj = data_protection_sdk.VmDiskRecoveryPointReference()
        if vm_ref.get("vm_recovery_point_ext_id") is not None:
            obj.vm_recovery_point_ext_id = vm_ref.get("vm_recovery_point_ext_id")
        if vm_ref.get("recovery_point_ext_id") is not None:
            obj.recovery_point_ext_id = vm_ref.get("recovery_point_ext_id")
        if vm_ref.get("disk_recovery_point_ext_id") is not None:
            obj.disk_recovery_point_ext_id = vm_ref.get("disk_recovery_point_ext_id")
        return obj
    if vg_ref:
        obj = data_protection_sdk.VolumeGroupDiskRecoveryPointReference()
        if vg_ref.get("volume_group_recovery_point_ext_id") is not None:
            obj.volume_group_recovery_point_ext_id = vg_ref.get(
                "volume_group_recovery_point_ext_id"
            )
        if vg_ref.get("recovery_point_ext_id") is not None:
            obj.recovery_point_ext_id = vg_ref.get("recovery_point_ext_id")
        if vg_ref.get("disk_recovery_point_ext_id") is not None:
            obj.disk_recovery_point_ext_id = vg_ref.get("disk_recovery_point_ext_id")
        return obj
    return None


def _build_cluster_discover_spec(module, result):
    """Build the ClusterDiscoverSpec SDK object from module params."""
    operation = module.params.get("operation")
    spec_params = module.params.get("spec") or {}

    body = data_protection_sdk.ClusterDiscoverSpec()
    body.operation = operation

    if operation == "GET_VSS_METADATA":
        vss_params = spec_params.get("get_vss_metadata")
        if not vss_params:
            module.fail_json(
                msg="spec.get_vss_metadata is required when operation is GET_VSS_METADATA",
                **result,
            )
        vss_spec = data_protection_sdk.GetVssMetadataClusterDiscoverSpec()
        vss_spec.vm_recovery_point_ext_id = vss_params.get("vm_recovery_point_ext_id")
        body.spec = vss_spec
    else:  # COMPUTE_CHANGED_REGIONS
        ccr_params = spec_params.get("compute_changed_regions")
        if not ccr_params:
            module.fail_json(
                msg="spec.compute_changed_regions is required when operation is COMPUTE_CHANGED_REGIONS",
                **result,
            )
        ccr_spec = data_protection_sdk.ComputeChangedRegionsClusterDiscoverSpec()
        ccr_spec.disk_recovery_point = _build_disk_recovery_point_reference(
            ccr_params.get("disk_recovery_point")
        )
        ccr_spec.reference_disk_recovery_point = _build_disk_recovery_point_reference(
            ccr_params.get("reference_disk_recovery_point")
        )
        body.spec = ccr_spec

    return body


def discover_cluster_for_recovery_point(module, result, api_instance):
    """Invoke the discover-cluster action for the recovery point."""
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id

    body = _build_cluster_discover_spec(module, result)

    if module.check_mode:
        result["response"] = strip_internal_attributes(body.to_dict())
        return

    try:
        resp = api_instance.discover_cluster_for_recovery_point_id(
            extId=ext_id, body=body
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while discovering cluster for recovery point",
        )

    result["response"] = strip_internal_attributes(resp.data.to_dict())


def run_module():
    module = BaseModuleV4(
        argument_spec=get_module_spec(),
        supports_check_mode=True,
        required_if=[
            ("operation", "GET_VSS_METADATA", ("spec",)),
            ("operation", "COMPUTE_CHANGED_REGIONS", ("spec",)),
        ],
    )
    if SDK_IMP_ERROR:
        module.fail_json(
            msg=missing_required_lib("ntnx_dataprotection_py_client"),
            exception=SDK_IMP_ERROR,
        )

    remove_param_with_none_value(module.params)
    result = {
        "changed": False,
        "error": None,
        "response": None,
        "ext_id": None,
    }
    api_instance = get_recovery_point_api_instance(module)
    discover_cluster_for_recovery_point(module, result, api_instance)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
