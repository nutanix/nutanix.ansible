#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_vss_metadata_by_vm_recovery_point_ids_info_v2
short_description: Fetch VSS metadata for a VM recovery point in Nutanix Prism Central
version_added: 2.7.0
description:
  - This module allows you to fetch the Volume Shadow Copy Service (VSS) metadata
    associated with a specific VM recovery point that is part of a top-level
    (composite) recovery point in Nutanix Prism Central.
  - The API returns the metadata payload (Windows CAB file) that backup vendors
    save alongside application-consistent VM snapshots so that VSS writer/requester
    state can be restored later.
  - Both the parent recovery point external ID and the VM recovery point external
    ID are required — this endpoint is a child datasource that cannot be listed.
  - This module uses PC v4 APIs based SDKs.
notes:
  - >-
    This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
  - >-
    B(Get VSS metadata by VM recovery point ID) -
    Required Roles: Backup Admin, Disaster Recovery Admin, Prism Admin, Super Admin
  - "Ref: U(https://developers.nutanix.com/api-reference?namespace=dataprotection)"
options:
  recovery_point_ext_id:
    description:
      - The external identifier of the top-level (composite) recovery point that
        contains the VM recovery point whose VSS metadata is being fetched.
    type: str
    required: true
  vm_recovery_point_ext_id:
    description:
      - The external identifier of the VM recovery point (nested inside the
        top-level recovery point) whose VSS metadata is being fetched.
    type: str
    required: true
extends_documentation_fragment:
  - nutanix.ncp.ntnx_credentials
  - nutanix.ncp.ntnx_info_v2
  - nutanix.ncp.ntnx_logger
  - nutanix.ncp.ntnx_proxy_v2
author:
  - Abhinav Bansal (@abhinavbansal29)
  - George Ghawali (@george-ghawali)
"""
EXAMPLES = r"""
- name: Fetch VSS metadata for a VM recovery point
  nutanix.ncp.ntnx_vss_metadata_by_vm_recovery_point_ids_info_v2:
    recovery_point_ext_id: "1ca2963d-77b6-453a-ae23-2c19e7a954a3"
    vm_recovery_point_ext_id: "522670d7-e92d-45c5-9139-76ccff6813c2"
  register: result
"""
RETURN = r"""
response:
  description:
    - The response from the Nutanix PC VssMetadataByVmRecoveryPointId info v4 API.
    - Contains the VSS metadata payload wrapper for the requested VM recovery point.
    - The API streams the VSS metadata as an C(application/octet-stream) payload
      (a Windows CAB file). In the Python SDK the payload is downloaded to a
      temporary file and the response wraps a path-like reference to that file.
    - This module always returns a single object (there is no list variant for
      this endpoint).
  returned: always
  type: dict
  sample:
    {
        "payload_reference": "/tmp/tmpxyz1234.cab"
    }

changed:
  description: This indicates whether the task resulted in any changes.
  returned: always
  type: bool
  sample: false

ext_id:
  description:
    - External ID of the VM recovery point whose VSS metadata was fetched.
  type: str
  returned: always
  sample: "522670d7-e92d-45c5-9139-76ccff6813c2"

recovery_point_ext_id:
  description:
    - External ID of the parent (top-level) recovery point.
  type: str
  returned: always
  sample: "1ca2963d-77b6-453a-ae23-2c19e7a954a3"

msg:
  description: Human-readable status message. Populated when there is an error
    or when a non-default status is being surfaced.
  returned: When there is an error
  type: str
  sample: "Api Exception raised while fetching VSS metadata for a VM recovery point using ext_ids"

error:
  description: Error details when the task fails.
  type: str
  returned: when an error occurs

failed:
  description: This field typically holds information about if the task have failed.
  returned: always
  type: bool
  sample: false
"""

import warnings  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.data_protection.api_client import (  # noqa: E402
    get_recovery_point_api_instance,
)
from ..module_utils.v4.data_protection.helpers import (  # noqa: E402
    get_vss_metadata_by_vm_recovery_point,
)
from ..module_utils.v4.utils import strip_internal_attributes  # noqa: E402

warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():

    module_args = dict(
        recovery_point_ext_id=dict(type="str", required=True),
        vm_recovery_point_ext_id=dict(type="str", required=True),
    )

    return module_args


def _serialize_vss_metadata_response(resp):
    """Normalise the SDK response so Ansible can JSON-serialise it.

    The VSS metadata endpoint returns C(application/octet-stream); the Python
    SDK downloads it into a temp file and exposes the object via
    C(GetVssMetadataApiResponse.data). Depending on the SDK version this can
    be a model instance (``to_dict`` supported), a ``pathlib.Path`` (file
    on disk), or a raw ``bytes`` payload. Coerce each variant into a plain
    JSON-friendly dict so the module return is stable.
    """
    if resp is None:
        return None
    if hasattr(resp, "to_dict"):
        return strip_internal_attributes(resp.to_dict())
    if isinstance(resp, dict):
        return strip_internal_attributes(resp)
    return {"payload_reference": str(resp)}


def get_vss_metadata_using_vm_rp_ext_id(module, recovery_points, result):
    recovery_point_ext_id = module.params.get("recovery_point_ext_id")
    vm_recovery_point_ext_id = module.params.get("vm_recovery_point_ext_id")
    resp = get_vss_metadata_by_vm_recovery_point(
        module, recovery_points, recovery_point_ext_id, vm_recovery_point_ext_id
    )
    result["ext_id"] = vm_recovery_point_ext_id
    result["recovery_point_ext_id"] = recovery_point_ext_id
    result["response"] = _serialize_vss_metadata_response(resp)


def run_module():
    module = BaseInfoModule(
        argument_spec=get_module_spec(),
        supports_check_mode=False,
    )
    remove_param_with_none_value(module.params)
    result = {"changed": False, "error": None, "response": None, "failed": False}
    recovery_points = get_recovery_point_api_instance(module)
    get_vss_metadata_using_vm_rp_ext_id(module, recovery_points, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
