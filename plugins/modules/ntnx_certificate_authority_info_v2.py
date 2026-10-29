#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2027, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_certificate_authority_info_v2
short_description: Fetch Certificate Authority (CA) info in Nutanix Prism Central
version_added: 2.7.0
description:
  - This module fetches Certificate Authority (CA) information for a cluster in Nutanix Prism Central.
  - If C(ext_id) is provided, fetch a particular Certificate Authority using its external ID.
  - If C(ext_id) is not provided, fetch a list of Certificate Authorities for the cluster with/without
    using filters, limit, etc.
  - This module uses PC v4 APIs based SDKs.
notes:
  - >-
    This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
  - >-
    B(View Cluster Certificate Authority) -
    Required Roles: Cluster Admin, Cluster Viewer, Prism Admin, Prism Viewer, Super Admin
  - This module talks to B(Prism Central) (PC). It does not target FCVM/Foundation.
  - The referenced cluster must exist before fetching Certificate Authority information from it.
  - "Ref: U(https://developers.nutanix.com/api-reference?namespace=clustermgmt)"
options:
  cluster_ext_id:
    description:
      - The external ID of the cluster to fetch Certificate Authority information from.
    type: str
    required: true
  ext_id:
    description:
      - The external ID of the Certificate Authority.
      - When provided, a single Certificate Authority is returned.
    type: str
    required: false
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
  nutanix.ncp.ntnx_certificate_authority_info_v2:
    cluster_ext_id: "00061fa4-ef93-7dd8-185b-ac1f6b6f97e2"
    ext_id: "2e40ff57-20aa-4d2b-b179-298db969c20d"
  register: result
  ignore_errors: true

- name: List all Certificate Authorities on a cluster
  nutanix.ncp.ntnx_certificate_authority_info_v2:
    cluster_ext_id: "00061fa4-ef93-7dd8-185b-ac1f6b6f97e2"
  register: result
  ignore_errors: true

- name: List all Certificate Authorities with fetch_all
  nutanix.ncp.ntnx_certificate_authority_info_v2:
    cluster_ext_id: "00061fa4-ef93-7dd8-185b-ac1f6b6f97e2"
    fetch_all: true
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
  description:
    - The response from the Certificate Authority info v4 API. The host is Prism Central (PC).
    - It can be a single Certificate Authority if external ID is provided.
    - List of multiple Certificate Authorities if external ID is not provided with optional filter or limit.
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
  sample: "Api Exception raised while fetching Certificate Authority info"

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
  description: External ID of the fetched Certificate Authority.
  type: str
  returned: when external ID is provided
  sample: "2e40ff57-20aa-4d2b-b179-298db969c20d"

cluster_ext_id:
  description: External ID of the cluster whose Certificate Authorities were queried.
  type: str
  returned: always
  sample: "00061fa4-ef93-7dd8-185b-ac1f6b6f97e2"

total_available_results:
  description: The total number of available Certificate Authorities on the cluster.
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
    get_certificate_authority,
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
    )
    return module_args


def get_certificate_authority_using_ext_id(module, api_instance, result):
    ext_id = module.params.get("ext_id")
    cluster_ext_id = module.params.get("cluster_ext_id")
    result["ext_id"] = ext_id
    result["cluster_ext_id"] = cluster_ext_id

    resp = get_certificate_authority(module, api_instance, ext_id, cluster_ext_id)
    result["response"] = strip_internal_attributes(resp.to_dict())


def get_certificate_authorities(module, api_instance, result):
    cluster_ext_id = module.params.get("cluster_ext_id")
    result["cluster_ext_id"] = cluster_ext_id

    sg = SpecGenerator(module)
    kwargs, err = sg.get_info_spec(attr=module.params)
    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed generating Certificate Authority info spec", **result
        )

    try:
        resp = list_entities(
            api_instance.list_certificate_authorities_by_cluster_id,
            kwargs=kwargs,
            clusterExtId=cluster_ext_id,
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching Certificate Authority info",
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
        get_certificate_authority_using_ext_id(module, api_instance, result)
    else:
        get_certificate_authorities(module, api_instance, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
