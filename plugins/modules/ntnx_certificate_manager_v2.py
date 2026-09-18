#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_certificate_manager_v2
short_description: Delete Certificate Authorities (CA) and Certificate Signing Requests (CSR) in Nutanix Prism Central
version_added: 2.7.0
description:
  - This module allows you to delete Certificate Authorities (CA) and Certificate Signing Requests (CSR) on a cluster in Nutanix Prism Central.
  - Certificate Authorities and Certificate Signing Requests are created using the dedicated action modules
    M(nutanix.ncp.ntnx_create_certificate_authority_by_cluster_id_v2) and M(nutanix.ncp.ntnx_create_csr_by_cluster_id_v2).
  - This module only supports delete operations as the underlying v4 API for Certificate Authority and
    Certificate Signing Request supports only delete on an existing entity.
  - This module uses PC v4 APIs based SDKs.
notes:
  - >-
    This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
    The required roles depend on the operation being performed.
  - >-
    B(Delete a Certificate Authority) -
    Required Roles: Prism Admin, Super Admin
  - >-
    B(Delete a Certificate Signing Request) -
    Required Roles: Prism Admin, Super Admin
  - This module talks to Prism Central (PC), not FCVM/Foundation.
  - The referenced cluster must exist before deleting a Certificate Authority or Certificate Signing Request from it.
  - "Ref: U(https://developers.nutanix.com/api-reference?namespace=clustermgmt)"
options:
  state:
    description:
      - If C(state) is set to C(absent) then the operation will delete the certificate authority or
        certificate signing request identified by C(ext_id).
      - C(present) is accepted for interface parity with other v2 modules but is not supported by this module
        because the certificate manager entities are created using the dedicated action modules.
    type: str
    required: false
    choices:
      - present
      - absent
    default: present
  ext_id:
    description:
      - The external ID of the Certificate Authority or Certificate Signing Request to delete.
      - Required for delete operation.
    type: str
    required: false
  cluster_ext_id:
    description:
      - The external ID of the cluster that owns the Certificate Authority or Certificate Signing Request.
      - Required for delete operation.
    type: str
    required: false
  type:
    description:
      - The type of certificate manager entity to delete.
      - Use C(CERTIFICATE_AUTHORITY) to delete a Certificate Authority (CA).
      - Use C(CSR) to delete a Certificate Signing Request (CSR).
      - Required for delete operation.
    type: str
    required: false
    choices:
      - CERTIFICATE_AUTHORITY
      - CSR
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
- name: Delete a Certificate Authority
  nutanix.ncp.ntnx_certificate_manager_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: absent
    type: CERTIFICATE_AUTHORITY
    cluster_ext_id: "00061fa4-ef93-7dd8-185b-ac1f6b6f97e2"
    ext_id: "2e40ff57-20aa-4d2b-b179-298db969c20d"
  register: result
  ignore_errors: true

- name: Delete a Certificate Signing Request (CSR)
  nutanix.ncp.ntnx_certificate_manager_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: absent
    type: CSR
    cluster_ext_id: "00061fa4-ef93-7dd8-185b-ac1f6b6f97e2"
    ext_id: "7c6bc5f3-c18c-4702-4c2d-b769fd5f94b0"
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
  description:
    - Response for deleting a Certificate Authority or Certificate Signing Request.
    - Task details when C(wait) is true.
  returned: always
  type: dict
  sample:
    {
      "cluster_ext_ids": ["00061fa4-ef93-7dd8-185b-ac1f6b6f97e2"],
      "completed_time": "2026-09-18T06:26:51.524581+00:00",
      "created_time": "2026-09-18T06:26:47.167906+00:00",
      "entities_affected": [
        {
          "ext_id": "2e40ff57-20aa-4d2b-b179-298db969c20d",
          "name": "certificate-authority",
          "rel": "clustermgmt:config:certificate-authority"
        }
      ],
      "error_messages": null,
      "ext_id": "ZXJnb24=:90458bc7-a12b-4616-ac66-562fdb00c209",
      "operation": "DeleteCertificateAuthority",
      "operation_description": "Delete a Certificate Authority (CA)",
      "progress_percentage": 100,
      "status": "SUCCEEDED"
    }

task_ext_id:
  description:
    - The external ID of the task.
  returned: always
  type: str
  sample: "ZXJnb24=:90458bc7-a12b-4616-ac66-562fdb00c209"

ext_id:
  description:
    - The external ID of the Certificate Authority or Certificate Signing Request.
  returned: always
  type: str
  sample: "2e40ff57-20aa-4d2b-b179-298db969c20d"

changed:
  description: This indicates whether the task resulted in any changes.
  returned: always
  type: bool
  sample: true

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
  description: This indicates the status/error message if any message occurred.
  returned: When there is an error or in check mode (in delete operation)
  type: str
  sample: "Certificate Authority with ext_id: 2e40ff57-20aa-4d2b-b179-298db969c20d will be deleted."
"""

import warnings  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_module_v4 import BaseModuleV4  # noqa: E402
from ..module_utils.v4.clusters_mgmt.api_client import (  # noqa: E402
    get_certificate_manager_api_instance,
)
from ..module_utils.v4.prism.tasks import wait_for_completion  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
    validate_required_params,
)

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    module_args = dict(
        ext_id=dict(type="str"),
        cluster_ext_id=dict(type="str"),
        type=dict(type="str", choices=["CERTIFICATE_AUTHORITY", "CSR"]),
    )
    return module_args


def delete_certificate_manager(module, result, api_instance):
    validate_required_params(module, ["ext_id", "cluster_ext_id", "type"])
    ext_id = module.params.get("ext_id")
    cluster_ext_id = module.params.get("cluster_ext_id")
    entity_type = module.params.get("type")
    result["ext_id"] = ext_id

    entity_name = (
        "Certificate Authority"
        if entity_type == "CERTIFICATE_AUTHORITY"
        else "Certificate Signing Request"
    )

    if module.check_mode:
        result["msg"] = "{0} with ext_id: {1} will be deleted.".format(
            entity_name, ext_id
        )
        return

    resp = None
    try:
        if entity_type == "CERTIFICATE_AUTHORITY":
            resp = api_instance.delete_certificate_authority_by_id(
                clusterExtId=cluster_ext_id, extId=ext_id
            )
        else:
            resp = api_instance.delete_csr_by_id(
                clusterExtId=cluster_ext_id, extId=ext_id
            )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while deleting {0} with ext_id: {1}".format(
                entity_name, ext_id
            ),
        )

    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        task_status = wait_for_completion(module, task_ext_id, True)
        result["response"] = strip_internal_attributes(task_status.to_dict())
    result["changed"] = True


def run_module():
    module = BaseModuleV4(
        argument_spec=get_module_spec(),
        supports_check_mode=True,
        required_if=[
            ("state", "absent", ("ext_id", "cluster_ext_id", "type")),
        ],
    )
    remove_param_with_none_value(module.params)
    result = {
        "changed": False,
        "response": None,
        "failed": False,
        "ext_id": None,
    }
    api_instance = get_certificate_manager_api_instance(module)
    state = module.params.get("state")
    if state == "present":
        module.fail_json(
            msg="Certificate manager entities are created using the dedicated action modules. "
            "This module only supports state=absent (delete). "
            "Use ntnx_create_certificate_authority_by_cluster_id_v2 or "
            "ntnx_create_csr_by_cluster_id_v2 to create entities.",
            **result,
        )
    else:
        delete_certificate_manager(module, result, api_instance)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
