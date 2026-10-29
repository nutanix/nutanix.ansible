#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2027, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_certificate_manager_info_v2
short_description: Fetch Certificate Authorities, Certificates and Certificate Signing Requests info in Nutanix Prism Central
version_added: 2.7.0
description:
  - This module allows you to fetch Certificate Authority (CA), Certificate, and Certificate Signing Request (CSR)
    information for a cluster in Nutanix Prism Central.
  - If C(ext_id) is provided, fetch a particular Certificate Authority, Certificate, or Certificate Signing Request
    using its external ID.
  - If C(ext_id) is not provided, fetch a list of Certificate Authorities, Certificates, or Certificate Signing
    Requests for the cluster with/without using filters, limit, etc.
  - The C(type) parameter selects which certificate manager entity to query.
  - This module uses PC v4 APIs based SDKs.
notes:
  - >-
    This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
  - >-
    B(View Cluster Certificate Authority) -
    Required Roles: Cluster Admin, Cluster Viewer, Prism Admin, Prism Viewer, Super Admin
  - >-
    B(View Cluster Certificate) -
    Required Roles: Cluster Admin, Cluster Viewer, Prism Admin, Prism Viewer, Super Admin
  - >-
    B(View Cluster Certificate Signing Request) -
    Required Roles: Cluster Admin, Cluster Viewer, Prism Admin, Prism Viewer, Super Admin
  - This module talks to B(Prism Central) (PC). It does not target FCVM/Foundation.
  - The referenced cluster must exist before fetching certificate manager information from it.
  - "Ref: U(https://developers.nutanix.com/api-reference?namespace=clustermgmt)"
options:
  cluster_ext_id:
    description:
      - The external ID of the cluster to fetch certificate manager information from.
    type: str
    required: true
  ext_id:
    description:
      - The external ID of the Certificate Authority, Certificate, or Certificate Signing Request.
      - When provided, a single entity of the given C(type) is returned.
    type: str
    required: false
  type:
    description:
      - The type of certificate manager entity to fetch.
      - Use C(CERTIFICATE_AUTHORITY) to fetch Certificate Authorities (CA).
      - Use C(CERTIFICATE) to fetch Certificates.
      - Use C(CSR) to fetch Certificate Signing Requests (CSR).
    type: str
    required: true
    choices:
      - CERTIFICATE_AUTHORITY
      - CERTIFICATE
      - CSR
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
- name: Get a Certificate Authority using ext_id
  nutanix.ncp.ntnx_certificate_manager_info_v2:
    cluster_ext_id: "00061fa4-ef93-7dd8-185b-ac1f6b6f97e2"
    type: CERTIFICATE_AUTHORITY
    ext_id: "2e40ff57-20aa-4d2b-b179-298db969c20d"
  register: result
  ignore_errors: true

- name: List all Certificate Authorities on a cluster
  nutanix.ncp.ntnx_certificate_manager_info_v2:
    cluster_ext_id: "00061fa4-ef93-7dd8-185b-ac1f6b6f97e2"
    type: CERTIFICATE_AUTHORITY
  register: result
  ignore_errors: true

- name: List all Certificates on a cluster
  nutanix.ncp.ntnx_certificate_manager_info_v2:
    cluster_ext_id: "00061fa4-ef93-7dd8-185b-ac1f6b6f97e2"
    type: CERTIFICATE
  register: result
  ignore_errors: true

- name: List Certificate Signing Requests with filter
  nutanix.ncp.ntnx_certificate_manager_info_v2:
    cluster_ext_id: "00061fa4-ef93-7dd8-185b-ac1f6b6f97e2"
    type: CSR
    filter: "purpose eq 'SERVER_AUTH'"
  register: result
  ignore_errors: true

- name: List Certificate Signing Requests with limit
  nutanix.ncp.ntnx_certificate_manager_info_v2:
    cluster_ext_id: "00061fa4-ef93-7dd8-185b-ac1f6b6f97e2"
    type: CSR
    limit: 1
  register: result
  ignore_errors: true

- name: List all Certificate Authorities with fetch_all
  nutanix.ncp.ntnx_certificate_manager_info_v2:
    cluster_ext_id: "00061fa4-ef93-7dd8-185b-ac1f6b6f97e2"
    type: CERTIFICATE_AUTHORITY
    fetch_all: true
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
  description:
    - The response from the Nutanix certificate manager info v4 API. The host is Prism Central (PC).
    - It can be a single certificate manager entity if external ID is provided.
    - List of multiple certificate manager entities if external ID is not provided with optional filter or limit.
  returned: always
  type: dict
  sample:
    {
      "certificate_authority_details": {
        "common_name": "ansible.nutanix.com",
        "issuer": "CN=ansible.nutanix.com",
        "serial_number": "1234567890"
      },
      "description": "Certificate Authority added by Ansible",
      "ext_id": "2e40ff57-20aa-4d2b-b179-298db969c20d",
      "links": null,
      "purpose": "SERVER_AUTH",
      "tenant_id": null
    }

changed:
  description: This indicates whether the task resulted in any changes. Always false for info modules.
  returned: always
  type: bool
  sample: false

msg:
  description: This indicates the message if any message occurred.
  returned: When there is an error
  type: str
  sample: "Api Exception raised while fetching certificate managers info"

error:
  description: This field typically holds information about errors that occurred during the task execution.
  type: str
  returned: when an error occurs

failed:
  description: This field indicates whether the task failed.
  returned: always
  type: bool
  sample: false

ext_id:
  description: External ID of the fetched certificate manager entity.
  type: str
  returned: when external ID is provided
  sample: "2e40ff57-20aa-4d2b-b179-298db969c20d"

cluster_ext_id:
  description: External ID of the cluster whose certificate manager entities were queried.
  type: str
  returned: always
  sample: "00061fa4-ef93-7dd8-185b-ac1f6b6f97e2"

total_available_results:
  description: The total number of available certificate manager entities on the cluster.
  type: int
  returned: when all entities are fetched
  sample: 5
"""

import warnings  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.clusters_mgmt.api_client import (  # noqa: E402
    get_certificate_manager_api_instance,
)
from ..module_utils.v4.clusters_mgmt.helpers import (  # noqa: E402
    get_certificate,
    get_certificate_authority,
    get_csr,
)
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    list_entities,
    raise_api_exception,
    strip_internal_attributes,
)

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    module_args = dict(
        cluster_ext_id=dict(type="str", required=True),
        ext_id=dict(type="str"),
        type=dict(
            type="str",
            required=True,
            choices=["CERTIFICATE_AUTHORITY", "CERTIFICATE", "CSR"],
        ),
    )
    return module_args


def get_certificate_manager_using_ext_id(module, api_instance, result):
    ext_id = module.params.get("ext_id")
    cluster_ext_id = module.params.get("cluster_ext_id")
    entity_type = module.params.get("type")
    result["ext_id"] = ext_id
    result["cluster_ext_id"] = cluster_ext_id

    if entity_type == "CERTIFICATE_AUTHORITY":
        resp = get_certificate_authority(module, api_instance, ext_id, cluster_ext_id)
    elif entity_type == "CERTIFICATE":
        resp = get_certificate(module, api_instance, ext_id, cluster_ext_id)
    else:
        resp = get_csr(module, api_instance, ext_id, cluster_ext_id)

    result["response"] = strip_internal_attributes(resp.to_dict())


def get_certificate_managers(module, api_instance, result):
    cluster_ext_id = module.params.get("cluster_ext_id")
    entity_type = module.params.get("type")
    result["cluster_ext_id"] = cluster_ext_id

    sg = SpecGenerator(module)
    kwargs, err = sg.get_info_spec(attr=module.params)
    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed generating certificate managers info spec", **result
        )

    try:
        if entity_type == "CERTIFICATE_AUTHORITY":
            list_fn = api_instance.list_certificate_authorities_by_cluster_id
        elif entity_type == "CERTIFICATE":
            list_fn = api_instance.list_certificates_by_cluster_id
        else:
            list_fn = api_instance.list_csrs_by_cluster_id

        resp = list_entities(
            list_fn,
            kwargs=kwargs,
            clusterExtId=cluster_ext_id,
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching certificate managers info",
        )

    total_available_results = resp.metadata.total_available_results
    result["total_available_results"] = total_available_results
    if getattr(resp, "data", None):
        result["response"] = strip_internal_attributes(resp.to_dict()).get("data")
    else:
        result["response"] = []


def run_module():
    module = BaseInfoModule(
        argument_spec=get_module_spec(),
        supports_check_mode=False,
        mutually_exclusive=[
            ("ext_id", "filter"),
        ],
    )
    remove_param_with_none_value(module.params)
    result = {"changed": False, "response": None, "failed": False}
    api_instance = get_certificate_manager_api_instance(module)
    if module.params.get("ext_id"):
        get_certificate_manager_using_ext_id(module, api_instance, result)
    else:
        get_certificate_managers(module, api_instance, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
