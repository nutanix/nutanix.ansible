#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_create_csr_by_cluster_id_v2
short_description: Generate a Certificate Signing Request (CSR) on a cluster in Nutanix Prism Central
version_added: 2.7.0
description:
  - This module generates a Certificate Signing Request (CSR) on a cluster in Nutanix Prism Central.
  - This is an action module that triggers a task-based operation.
  - This module uses PC v4 APIs based SDKs.
notes:
  - >-
    This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
  - >-
    B(Generate a Certificate Signing Request) -
    Required Roles: Prism Admin, Super Admin
  - This module talks to Prism Central (PC), not FCVM/Foundation.
  - The referenced cluster must exist before generating a Certificate Signing Request on it.
  - "Ref: U(https://developers.nutanix.com/api-reference?namespace=clustermgmt)"
options:
  cluster_ext_id:
    description:
      - The external ID of the cluster on which the Certificate Signing Request will be generated.
    type: str
    required: true
  certificate_info:
    description:
      - Details of the certificate configuration used to generate the Certificate Signing Request.
      - The API requires C(common_name), C(city), C(state), and C(country_code) to be provided.
    type: dict
    required: true
    suboptions:
      common_name:
        description:
          - Common Name (CN) for the certificate request.
          - Required by the API when generating a Certificate Signing Request.
        type: str
        required: false
      subject_alternative_names:
        description:
          - List of Subject Alternative Names (SAN) for the certificate request.
        type: list
        elements: str
        required: false
      city:
        description:
          - City (L) for the certificate request.
          - Required by the API when generating a Certificate Signing Request.
        type: str
        required: false
      state:
        description:
          - State (ST) for the certificate request.
          - Required by the API when generating a Certificate Signing Request.
        type: str
        required: false
      country_code:
        description:
          - Country code (C) for the certificate request.
          - Required by the API when generating a Certificate Signing Request.
        type: str
        required: false
      private_key_algorithm:
        description:
          - Private key algorithm used for the certificate request.
        type: str
        required: false
        choices:
          - ECDSA_256
          - ECDSA_384
          - RSA_2048
          - RSA_4096
      key_size_bit:
        description:
          - Key size in bits for the certificate request.
        type: int
        required: false
      signature_algorithm:
        description:
          - Signature algorithm used for the certificate request.
        type: str
        required: false
        choices:
          - ECDSA_WITH_SHA256
          - ECDSA_WITH_SHA384
          - ECDSA_WITH_SHA512
          - ED25519
          - SHA256_WITH_RSA_ENCRYPTION
          - SHA384_WITH_RSA_ENCRYPTION
          - SHA512_WITH_RSA_ENCRYPTION
      extended_key_usages:
        description:
          - List of extended key usages for the certificate request.
        type: list
        elements: str
        required: false
        choices:
          - ANY
          - CLIENT_AUTH
          - CODE_SIGNING
          - EMAIL_PROTECTION
          - IPSEC_END_SYSTEM
          - IPSEC_TUNNEL
          - IPSEC_USER
          - OCSPSIGNING
          - SERVER_AUTH
          - TIMESTAMPING
      key_usages:
        description:
          - List of key usages for the certificate request.
        type: list
        elements: str
        required: false
        choices:
          - CERT_SIGN
          - CONTENT_COMMITMENT
          - CRL_SIGN
          - DATA_ENCIPHERMENT
          - DECIPHER_ONLY
          - DIGITAL_SIGNATURE
          - ENCIPHER_ONLY
          - KEY_AGREEMENT
          - KEY_ENCIPHERMENT
      organization:
        description:
          - Organization (O) for the certificate request.
        type: str
        required: false
      organizational_unit:
        description:
          - Organizational Unit (OU) for the certificate request.
        type: str
        required: false
  purpose:
    description:
      - Purpose of the Certificate Signing Request.
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
- name: Generate a Certificate Signing Request on a cluster
  nutanix.ncp.ntnx_create_csr_by_cluster_id_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    cluster_ext_id: "00061fa4-ef93-7dd8-185b-ac1f6b6f97e2"
    certificate_info:
      common_name: "ansible.nutanix.com"
      subject_alternative_names:
        - "ansible.nutanix.com"
        - "www.ansible.nutanix.com"
      city: "San Jose"
      state: "California"
      country_code: "US"
      private_key_algorithm: "RSA_2048"
      key_size_bit: 2048
      signature_algorithm: "SHA256_WITH_RSA_ENCRYPTION"
      extended_key_usages:
        - "SERVER_AUTH"
        - "CLIENT_AUTH"
      key_usages:
        - "DIGITAL_SIGNATURE"
        - "KEY_ENCIPHERMENT"
      organization: "Nutanix"
      organizational_unit: "Engineering"
    purpose: "SERVER_AUTH"
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
  description:
    - Response for generating a Certificate Signing Request on a cluster.
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
          "ext_id": "7c6bc5f3-c18c-4702-4c2d-b769fd5f94b0",
          "name": "csr",
          "rel": "clustermgmt:config:csr"
        }
      ],
      "error_messages": null,
      "ext_id": "ZXJnb24=:90458bc7-a12b-4616-ac66-562fdb00c209",
      "operation": "CreateCsr",
      "operation_description": "Generate a Certificate Signing Request (CSR)",
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
    - The external ID of the created Certificate Signing Request.
  returned: when applicable
  type: str
  sample: "7c6bc5f3-c18c-4702-4c2d-b769fd5f94b0"

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
  sample: "Certificate Signing Request will be generated on cluster with ext_id: 00061fa4-ef93-7dd8-185b-ac1f6b6f97e2."
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
    certificate_config_info_spec = dict(
        common_name=dict(type="str"),
        subject_alternative_names=dict(type="list", elements="str"),
        city=dict(type="str"),
        state=dict(type="str"),
        country_code=dict(type="str"),
        private_key_algorithm=dict(
            type="str",
            choices=["ECDSA_256", "ECDSA_384", "RSA_2048", "RSA_4096"],
        ),
        key_size_bit=dict(type="int"),
        signature_algorithm=dict(
            type="str",
            choices=[
                "ECDSA_WITH_SHA256",
                "ECDSA_WITH_SHA384",
                "ECDSA_WITH_SHA512",
                "ED25519",
                "SHA256_WITH_RSA_ENCRYPTION",
                "SHA384_WITH_RSA_ENCRYPTION",
                "SHA512_WITH_RSA_ENCRYPTION",
            ],
        ),
        extended_key_usages=dict(
            type="list",
            elements="str",
            choices=[
                "ANY",
                "CLIENT_AUTH",
                "CODE_SIGNING",
                "EMAIL_PROTECTION",
                "IPSEC_END_SYSTEM",
                "IPSEC_TUNNEL",
                "IPSEC_USER",
                "OCSPSIGNING",
                "SERVER_AUTH",
                "TIMESTAMPING",
            ],
        ),
        key_usages=dict(
            type="list",
            elements="str",
            choices=[
                "CERT_SIGN",
                "CONTENT_COMMITMENT",
                "CRL_SIGN",
                "DATA_ENCIPHERMENT",
                "DECIPHER_ONLY",
                "DIGITAL_SIGNATURE",
                "ENCIPHER_ONLY",
                "KEY_AGREEMENT",
                "KEY_ENCIPHERMENT",
            ],
        ),
        organization=dict(type="str"),
        organizational_unit=dict(type="str"),
    )

    module_args = dict(
        cluster_ext_id=dict(type="str", required=True),
        certificate_info=dict(
            type="dict",
            required=True,
            options=certificate_config_info_spec,
            obj=clustermgmt_sdk.CertificateConfigInfo,
        ),
        purpose=dict(type="str"),
    )
    return module_args


def create_csr(module, result, api_instance):
    validate_required_params(module, ["cluster_ext_id", "certificate_info"])
    cluster_ext_id = module.params.get("cluster_ext_id")

    sg = SpecGenerator(module)
    default_spec = clustermgmt_sdk.Csr()
    spec, err = sg.generate_spec(obj=default_spec)
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating create CSR spec", **result)

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        result["msg"] = (
            "Certificate Signing Request will be generated on cluster with ext_id: {0}.".format(
                cluster_ext_id
            )
        )
        return

    resp = None
    try:
        resp = api_instance.create_csr_by_cluster_id(
            clusterExtId=cluster_ext_id, body=spec
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while generating CSR on cluster with ext_id: {0}".format(
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


def run_module():
    module = BaseModuleV4(
        argument_spec=get_module_spec(),
        supports_check_mode=True,
    )
    if SDK_IMP_ERROR:
        module.fail_json(
            msg=missing_required_lib("ntnx_clustermgmt_py_client"),
            exception=SDK_IMP_ERROR,
        )

    remove_param_with_none_value(module.params)
    result = {
        "changed": False,
        "response": None,
        "ext_id": None,
        "task_ext_id": None,
    }
    api_instance = get_certificate_manager_api_instance(module)
    create_csr(module, result, api_instance)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
