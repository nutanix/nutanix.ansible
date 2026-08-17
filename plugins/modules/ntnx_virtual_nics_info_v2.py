#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_virtual_nics_info_v2
short_description: Fetch virtual NICs info in Nutanix Prism Central
version_added: 2.5.0
description:
  - This module allows you to fetch information about VirtualNic in Nutanix Prism Central.
  - If C(ext_id) is provided, fetch details of the specific VirtualNic on the given host.
  - If C(ext_id) is not provided, list multiple VirtualNic on the given host optionally
    filtered / paginated using C(filter), C(limit), C(page), C(orderby) and C(select).
  - Virtual NICs are the AHV / hypervisor level network interfaces attached to a Nutanix
    cluster host (for example br0, vnet0). They are read-only entities exposed by the
    V4 clustermgmt API.
  - This module uses PC v4 APIs based SDKs.
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user
      performing the operation.
    - >-
      B(Get virtual NIC by ext_id) -
      Required Roles: Cluster Admin, Cluster Viewer, Network Infra Admin,
      Prism Admin, Prism Viewer, Super Admin
    - >-
      B(List Virtual NICs on a host) -
      Required Roles: Cluster Admin, Cluster Viewer, Network Infra Admin,
      Prism Admin, Prism Viewer, Super Admin
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=clustermgmt)"
options:
  ext_id:
    description:
      - The external ID (UUID) of the virtual NIC.
      - When provided, C(cluster_ext_id) and C(host_ext_id) are also required and the
        specific virtual NIC is fetched via
        GET /clusters/{clusterExtId}/hosts/{hostExtId}/virtual-nics/{extId}.
      - When omitted, all virtual NICs on the given host are listed via
        GET /clusters/{clusterExtId}/hosts/{hostExtId}/virtual-nics.
    type: str
    required: false
  cluster_ext_id:
    description:
      - The external ID (UUID) of the cluster that owns the host whose virtual NICs
        are being queried.
      - Required for both get-by-ext_id and list operations.
    type: str
    required: true
  host_ext_id:
    description:
      - The external ID (UUID) of the host whose virtual NICs are being queried.
      - Required for both get-by-ext_id and list operations.
    type: str
    required: true
extends_documentation_fragment:
  - nutanix.ncp.ntnx_credentials
  - nutanix.ncp.ntnx_info_v2
  - nutanix.ncp.ntnx_logger
  - nutanix.ncp.ntnx_proxy_v2
author:
  - Abhinav Bansal (@abhinavbansal29)
"""

EXAMPLES = r"""
- name: Get a specific virtual NIC by external ID
  nutanix.ncp.ntnx_virtual_nics_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    cluster_ext_id: "00061de6-4a87-6b06-185b-ac1f6b6f97e2"
    host_ext_id: "af49a0bb-b3d7-41c0-b9c2-f4ca0e8763e9"
    ext_id: "7bea69e9-684c-4736-7805-d658ee17c1b6"
  register: result

- name: List all virtual NICs on a host
  nutanix.ncp.ntnx_virtual_nics_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    cluster_ext_id: "00061de6-4a87-6b06-185b-ac1f6b6f97e2"
    host_ext_id: "af49a0bb-b3d7-41c0-b9c2-f4ca0e8763e9"
  register: result

- name: List virtual NICs with limit and pagination
  nutanix.ncp.ntnx_virtual_nics_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    cluster_ext_id: "00061de6-4a87-6b06-185b-ac1f6b6f97e2"
    host_ext_id: "af49a0bb-b3d7-41c0-b9c2-f4ca0e8763e9"
    limit: 5
    page: 0
  register: result

- name: List virtual NICs filtered by name
  nutanix.ncp.ntnx_virtual_nics_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    cluster_ext_id: "00061de6-4a87-6b06-185b-ac1f6b6f97e2"
    host_ext_id: "af49a0bb-b3d7-41c0-b9c2-f4ca0e8763e9"
    filter: "name eq 'br0'"
  register: result
"""

RETURN = r"""
response:
  description:
    - The response from the Nutanix PC VirtualNic info v4 API.
    - It is a single VirtualNic dict if C(ext_id) is provided.
    - It is a list of VirtualNic dicts if C(ext_id) is not provided (optionally
      filtered / paginated by C(filter), C(limit), C(page), C(orderby), C(select)).
  returned: always
  type: dict
  sample:
    {
        "ext_id": "7bea69e9-684c-4736-7805-d658ee17c1b6",
        "host_description": "br0",
        "host_nics_uuids": [
            "c65eaeb1-3e0f-4a24-9c19-2a7fbf80f0d0"
        ],
        "interface_status": "UP",
        "ipv4_addresses": [
            {
                "prefix_length": 32,
                "value": "10.44.76.10"
            }
        ],
        "ipv6_addresses": null,
        "is_dhcp_enabled": false,
        "link_speed_in_kbps": 10000000,
        "links": null,
        "mac_address": "0c:c4:7a:12:34:56",
        "mtu_in_bytes": 1500,
        "name": "br0",
        "node_uuid": "af49a0bb-b3d7-41c0-b9c2-f4ca0e8763e9",
        "tenant_id": null,
        "vlan_id": 0
    }

ext_id:
  description:
    - The external ID of the virtual NIC (only returned when C(ext_id) input was provided).
  returned: when external ID is provided
  type: str
  sample: "7bea69e9-684c-4736-7805-d658ee17c1b6"

total_available_results:
  description:
    - The total number of virtual NICs available for the queried host in PC.
  returned: when all virtual NICs are fetched (list operation)
  type: int
  sample: 4

changed:
  description: This indicates whether the task resulted in any changes. Always false for info modules.
  returned: always
  type: bool
  sample: false

msg:
  description: This indicates the message if any message occurred.
  returned: When there is an error
  type: str
  sample: "Api Exception raised while fetching virtual NICs info"

error:
  description: This field typically holds information about errors during task execution.
  returned: When an error occurs
  type: str

failed:
  description: This field typically holds information about whether the task has failed.
  returned: always
  type: bool
  sample: false
"""

import traceback  # noqa: E402
import warnings  # noqa: E402

from ansible.module_utils.basic import missing_required_lib  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.clusters_mgmt.api_client import (  # noqa: E402
    get_clusters_api_instance,
)
from ..module_utils.v4.clusters_mgmt.helpers import get_virtual_nic  # noqa: E402
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
)

SDK_IMP_ERROR = None
try:
    import ntnx_clustermgmt_py_client as cluster_management_sdk  # noqa: E402, F401
except ImportError:

    from ..module_utils.v4.sdk_mock import (  # noqa: E402, F401
        mock_sdk as cluster_management_sdk,
    )

    SDK_IMP_ERROR = traceback.format_exc()

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():

    module_args = dict(
        ext_id=dict(type="str"),
        cluster_ext_id=dict(type="str", required=True),
        host_ext_id=dict(type="str", required=True),
    )

    return module_args


def get_virtual_nic_using_ext_id(module, api_instance, result):
    ext_id = module.params.get("ext_id")
    cluster_ext_id = module.params.get("cluster_ext_id")
    host_ext_id = module.params.get("host_ext_id")
    resp = get_virtual_nic(module, api_instance, ext_id, cluster_ext_id, host_ext_id)
    result["ext_id"] = ext_id
    result["response"] = strip_internal_attributes(resp.to_dict())


def get_virtual_nics(module, api_instance, result):
    sg = SpecGenerator(module)
    kwargs, err = sg.get_info_spec(attr=module.params)
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating virtual NICs info spec", **result)

    cluster_ext_id = module.params.get("cluster_ext_id")
    host_ext_id = module.params.get("host_ext_id")

    try:
        resp = api_instance.list_virtual_nics_by_host_id(
            clusterExtId=cluster_ext_id,
            hostExtId=host_ext_id,
            **kwargs,
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching virtual NICs info",
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
    if SDK_IMP_ERROR:
        module.fail_json(
            msg=missing_required_lib("ntnx_clustermgmt_py_client"),
            exception=SDK_IMP_ERROR,
        )

    remove_param_with_none_value(module.params)
    result = {"changed": False, "response": None, "failed": False}
    api_instance = get_clusters_api_instance(module)
    if module.params.get("ext_id"):
        get_virtual_nic_using_ext_id(module, api_instance, result)
    else:
        get_virtual_nics(module, api_instance, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
