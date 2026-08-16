#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_iscsi_clients_info_v2
short_description: Fetch iSCSI clients info in Nutanix Prism Central
version_added: 2.7.0
description:
  - This module allows you to fetch information about IscsiClient in Nutanix Prism Central.
  - If C(ext_id) is provided, fetch details of the specific IscsiClient.
  - If C(ext_id) is not provided, list multiple IscsiClient optionally filtered / paginated.
  - This module uses PC v4 APIs based SDKs.
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
    - >-
      B(Fetch an iSCSI client details) -
      Required Roles: Backup Admin, CSI System, Kubernetes Data Services System, Prism Admin, Prism Viewer,
      Project Manager, Storage Admin, Storage Viewer, Super Admin, Self-Service Admin (deprecated)
    - >-
      B(List all the iSCSI clients) -
      Required Roles: Backup Admin, CSI System, Kubernetes Data Services System, Prism Admin, Prism Viewer,
      Project Manager, Storage Admin, Storage Viewer, Super Admin, Self-Service Admin (deprecated)
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=volumes)"
options:
  ext_id:
    description:
      - The external ID of the iSCSI client.
      - When provided, only that iSCSI client is fetched.
    type: str
    required: false
  expand:
    description:
      - OData $expand parameter forwarded to the ListIscsiClients API.
      - Allows clients to request related resources for each returned iSCSI client.
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
- name: Fetch specific iSCSI client using ext_id
  nutanix.ncp.ntnx_iscsi_clients_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    ext_id: "aea43b5c-ae4d-4b60-934b-f8f581275dec"
  register: result
  ignore_errors: true

- name: List all iSCSI clients in Prism Central
  nutanix.ncp.ntnx_iscsi_clients_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
  register: result
  ignore_errors: true

- name: List iSCSI clients with filter
  nutanix.ncp.ntnx_iscsi_clients_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    filter: "iscsiInitiatorName eq 'iqn.1993-08.org.debian:01:abc'"
  register: result
  ignore_errors: true

- name: List iSCSI clients with limit
  nutanix.ncp.ntnx_iscsi_clients_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    limit: 5
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
  description:
    - The response from the Nutanix PC IscsiClient info v4 API.
    - It can be a single IscsiClient if external ID is provided.
    - List of multiple IscsiClient if external ID is not provided with optional filter or limit.
  returned: always
  type: dict
  sample:
    {
      "attached_targets": [
        {
          "iscsi_target_name": "iqn.2010-06.com.nutanix:vg1-37dec900-4c8e-48ed-77fc-93b6e173424a",
          "num_virtual_targets": 32
        }
      ],
      "attachment_site": null,
      "client_secret": null,
      "cluster_reference": "0006555e-4e63-4a5e-185b-ac1f6b6f97e2",
      "enabled_authentications": "CHAP",
      "ext_id": "97f41675-1833-4ba4-9206-2cfd8eb436b4",
      "iscsi_initiator_name": "iqn.1993-08.org.debian:01:rcpadmbuwv",
      "iscsi_initiator_network_id": null,
      "links": null,
      "num_virtual_targets": null,
      "tenant_id": null
    }

changed:
  description: This indicates whether the task resulted in any changes. Always False for info modules.
  returned: always
  type: bool
  sample: false

msg:
  description: This indicates the message if any message occurred.
  returned: When there is an error
  type: str
  sample: "Api Exception raised while fetching iSCSI clients info"

error:
  description: This field typically holds information about errors that occurred during the task execution.
  type: str
  returned: When an error occurs

failed:
  description: This indicates whether the task failed.
  returned: always
  type: bool
  sample: false

ext_id:
  description: External ID of the iSCSI client.
  type: str
  returned: When external ID is provided
  sample: "aea43b5c-ae4d-4b60-934b-f8f581275dec"

total_available_results:
  description: The total number of iSCSI clients available in Prism Central.
  type: int
  returned: When all iSCSI clients are fetched
  sample: 5
"""

import warnings  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
)
from ..module_utils.v4.volumes.api_client import (  # noqa: E402
    get_iscsi_client_api_instance,
)
from ..module_utils.v4.volumes.helpers import get_iscsi_client  # noqa: E402

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    module_args = dict(
        ext_id=dict(type="str"),
        expand=dict(type="str"),
    )
    return module_args


def get_iscsi_client_using_ext_id(module, api_instance, result):
    ext_id = module.params.get("ext_id")
    resp = get_iscsi_client(module, api_instance, ext_id)
    result["ext_id"] = ext_id
    result["response"] = strip_internal_attributes(resp.to_dict())


def get_iscsi_clients(module, api_instance, result):
    sg = SpecGenerator(module)
    kwargs, err = sg.get_info_spec(attr=module.params, extra_params=["expand"])

    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating iSCSI clients info spec", **result)

    try:
        resp = api_instance.list_iscsi_clients(**kwargs)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching iSCSI clients info",
        )

    total_available_results = resp.metadata.total_available_results
    result["total_available_results"] = total_available_results
    resp = strip_internal_attributes(resp.to_dict()).get("data")
    if not resp:
        resp = []
    result["response"] = resp


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
    api_instance = get_iscsi_client_api_instance(module)
    if module.params.get("ext_id"):
        get_iscsi_client_using_ext_id(module, api_instance, result)
    else:
        get_iscsi_clients(module, api_instance, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
