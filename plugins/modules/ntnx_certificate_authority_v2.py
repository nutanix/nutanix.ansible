#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2027, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_certificate_authority_v2
short_description: Create or delete a Certificate Authority (CA) on a cluster in Nutanix Prism Central
version_added: 2.7.0
description:
  - This module creates or deletes a Certificate Authority (CA) on a cluster in Nutanix Prism Central.
  - When C(state) is C(present), a Certificate Authority is added (create).
  - When C(state) is C(absent), the Certificate Authority identified by C(ext_id) is deleted.
  - The underlying v4 API does not support updating an existing Certificate Authority.
  - This module uses PC v4 APIs based SDKs.
notes:
  - >-
    This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
  - >-
    B(Create Cluster Certificate Authority) -
    Required Roles: Cluster Admin, Prism Admin, Super Admin
  - >-
    B(Delete Cluster Certificate Authority) -
    Required Roles: Cluster Admin, Prism Admin, Super Admin
  - This module talks to B(Prism Central) (PC). It does not target FCVM/Foundation.
  - The referenced cluster must exist before adding or deleting a Certificate Authority on it.
  - "Ref: U(https://developers.nutanix.com/api-reference?namespace=clustermgmt)"
options:
  cluster_ext_id:
    description:
      - The external ID of the cluster that owns the Certificate Authority.
    type: str
    required: true
  ext_id:
    description:
      - The external ID of the Certificate Authority to delete.
      - Required when C(state) is C(absent).
    type: str
    required: false
  certificate:
    description:
      - Base64 encoded certificate data of the Certificate Authority.
      - Required when C(state) is C(present).
    type: str
    required: false
  description:
    description:
      - Description of the Certificate Authority.
      - Only applicable when C(state) is C(present).
    type: str
    required: false
  purpose:
    description:
      - Purpose of the Certificate Authority.
      - Only applicable when C(state) is C(present).
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
- name: Add a Certificate Authority to a cluster
  nutanix.ncp.ntnx_certificate_authority_v2:
    state: present
    cluster_ext_id: "00061fa4-ef93-7dd8-185b-ac1f6b6f97e2"
    certificate: "{{ ca_certificate_base64 }}"
    description: "Certificate Authority added by Ansible"
    purpose: "SERVER_AUTH"
  register: result
  ignore_errors: true

- name: Delete a Certificate Authority
  nutanix.ncp.ntnx_certificate_authority_v2:
    state: absent
    cluster_ext_id: "00061fa4-ef93-7dd8-185b-ac1f6b6f97e2"
    ext_id: "2e40ff57-20aa-4d2b-b179-298db969c20d"
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
  description:
    - Response for creating or deleting a Certificate Authority on a cluster.
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
      "operation": "CreateCertificateAuthority",
      "operation_description": "Add Certificate Authorities",
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
    - The external ID of the Certificate Authority.
  returned: when applicable
  type: str
  sample: "2e40ff57-20aa-4d2b-b179-298db969c20d"

changed:
  description: This indicates whether the action resulted in any changes.
  returned: always
  type: bool
  sample: true

error:
  description: This indicates the error message if any error occurred.
  returned: when an error occurs
  type: str

failed:
  description: This indicates whether the task failed.
  returned: always
  type: bool
  sample: false

msg:
  description: This indicates the status/error message if any message occurred.
  returned: When there is an error or in check mode
  type: str
  sample: "Certificate Authority will be added to cluster with ext_id: 00061fa4-ef93-7dd8-185b-ac1f6b6f97e2."
"""

import traceback  # noqa: E402
import warnings  # noqa: E402

from ansible.module_utils.basic import missing_required_lib  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_module_v4 import BaseModuleV4  # noqa: E402
from ..module_utils.v4.clusters_mgmt.api_client import (  # noqa: E402
    get_certificate_manager_api_instance,
)
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
    import ntnx_clustermgmt_py_client as clustermgmt_sdk  # noqa: E402
except ImportError:

    from ..module_utils.v4.sdk_mock import mock_sdk as clustermgmt_sdk  # noqa: E402

    SDK_IMP_ERROR = traceback.format_exc()

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    module_args = dict(
        cluster_ext_id=dict(type="str", required=True),
        ext_id=dict(type="str"),
        certificate=dict(type="str", no_log=True),
        description=dict(type="str"),
        purpose=dict(type="str"),
    )
    return module_args


def create_certificate_authority(module, result, api_instance):
    validate_required_params(module, ["cluster_ext_id", "certificate"])
    cluster_ext_id = module.params.get("cluster_ext_id")

    sg = SpecGenerator(module)
    default_spec = clustermgmt_sdk.CertificateAuthority()
    spec, err = sg.generate_spec(obj=default_spec)
    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed generating create certificate authority spec", **result
        )

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        result["msg"] = (
            "Certificate Authority will be added to cluster with ext_id: {0}.".format(
                cluster_ext_id
            )
        )
        return

    resp = None
    try:
        resp = api_instance.create_certificate_authority_by_cluster_id(
            clusterExtId=cluster_ext_id, body=spec
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while adding certificate authority to cluster with ext_id: {0}".format(
                cluster_ext_id
            ),
        )

    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        task_status = wait_for_completion(module, task_ext_id)
        result["response"] = strip_internal_attributes(task_status.to_dict())
        ext_id = get_entity_ext_id_from_task(task_status)
        if ext_id:
            result["ext_id"] = ext_id
    result["changed"] = True


def delete_certificate_authority(module, result, api_instance):
    validate_required_params(module, ["ext_id", "cluster_ext_id"])
    ext_id = module.params.get("ext_id")
    cluster_ext_id = module.params.get("cluster_ext_id")
    result["ext_id"] = ext_id

    if module.check_mode:
        result["msg"] = (
            "Certificate Authority with ext_id: {0} will be deleted.".format(ext_id)
        )
        return

    resp = None
    try:
        resp = api_instance.delete_certificate_authority_by_id(
            clusterExtId=cluster_ext_id, extId=ext_id
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while deleting Certificate Authority with ext_id: {0}".format(
                ext_id
            ),
        )

    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        task_status = wait_for_completion(module, task_ext_id)
        result["response"] = strip_internal_attributes(task_status.to_dict())
    result["changed"] = True


def run_module():
    module = BaseModuleV4(
        argument_spec=get_module_spec(),
        supports_check_mode=True,
        required_if=[
            ("state", "present", ("certificate",)),
            ("state", "absent", ("ext_id",)),
        ],
    )
    if SDK_IMP_ERROR:
        module.fail_json(
            msg=missing_required_lib("ntnx_clustermgmt_py_client"),
            exception=SDK_IMP_ERROR,
        )

    remove_param_with_none_value(module.params)
    result = {
        "changed": False,
        "failed": False,
        "response": None,
        "ext_id": None,
        "task_ext_id": None,
    }
    api_instance = get_certificate_manager_api_instance(module)
    if module.params.get("state") == "present":
        create_certificate_authority(module, result, api_instance)
    else:
        delete_certificate_authority(module, result, api_instance)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
