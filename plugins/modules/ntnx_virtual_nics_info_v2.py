#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2027, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_virtual_nics_info_v2
short_description: Fetch virtual NICs info of a Nutanix host in Prism Central
version_added: 2.7.0
description:
  - This module allows you to fetch information about virtual NICs associated with a host in Nutanix Prism Central.
  - If C(ext_id) is provided, fetch details of the specific virtual NIC belonging to the given host in the given cluster.
  - If C(ext_id) is not provided, list all virtual NICs of the host optionally filtered / paginated.
  - This module uses PC v4 APIs based SDKs.
notes:
  - >-
    This module requires the following Nutanix IAM roles to be assigned to the
    user performing the operation.
    The required roles depend on the operation being performed.
  - >-
    B(Get virtual NIC) -
    Required Roles: Cluster Admin, Cluster Viewer, Prism Admin, Prism Viewer, Project Manager, Super Admin,
    Self-Service Admin (deprecated)
  - >-
    B(Get the list of virtual NICs) -
    Required Roles: Cluster Admin, Cluster Viewer, Prism Admin, Prism Viewer, Project Manager, Super Admin,
    Self-Service Admin (deprecated)
  - "Ref: U(https://developers.nutanix.com/api-reference?namespace=clustermgmt)"
options:
  cluster_ext_id:
    description:
      - External identifier (UUID) of the parent cluster whose host virtual NICs should be fetched.
    type: str
    required: true
  host_ext_id:
    description:
      - External identifier (UUID) of the host whose virtual NICs should be fetched.
    type: str
    required: true
  ext_id:
    description:
      - External identifier of a specific virtual NIC on the given host.
      - If provided, the module returns a single virtual NIC; otherwise, it returns the list of virtual NICs for the host.
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
- name: Get virtual NIC using ext_id
  nutanix.ncp.ntnx_virtual_nics_info_v2:
    cluster_ext_id: "000647b8-ddb3-6bbb-0000-000000028f57"
    host_ext_id: "f28e7475-f835-42ef-ac35-ecbc48d5421e"
    ext_id: "2e40ff57-20aa-4d2b-b179-298db969c20d"
  register: result
  ignore_errors: true

- name: List all virtual NICs of a host
  nutanix.ncp.ntnx_virtual_nics_info_v2:
    cluster_ext_id: "000647b8-ddb3-6bbb-0000-000000028f57"
    host_ext_id: "f28e7475-f835-42ef-ac35-ecbc48d5421e"
  register: result
  ignore_errors: true

- name: List virtual NICs of a host with filter
  nutanix.ncp.ntnx_virtual_nics_info_v2:
    cluster_ext_id: "000647b8-ddb3-6bbb-0000-000000028f57"
    host_ext_id: "f28e7475-f835-42ef-ac35-ecbc48d5421e"
    filter: "name eq 'br0'"
  register: result
  ignore_errors: true

- name: List virtual NICs of a host with limit
  nutanix.ncp.ntnx_virtual_nics_info_v2:
    cluster_ext_id: "000647b8-ddb3-6bbb-0000-000000028f57"
    host_ext_id: "f28e7475-f835-42ef-ac35-ecbc48d5421e"
    limit: 1
  register: result
  ignore_errors: true

- name: List virtual NICs of a host with ordering
  nutanix.ncp.ntnx_virtual_nics_info_v2:
    cluster_ext_id: "000647b8-ddb3-6bbb-0000-000000028f57"
    host_ext_id: "f28e7475-f835-42ef-ac35-ecbc48d5421e"
    orderby: "name desc"
  register: result
  ignore_errors: true

- name: List virtual NICs of a host with selection
  nutanix.ncp.ntnx_virtual_nics_info_v2:
    cluster_ext_id: "000647b8-ddb3-6bbb-0000-000000028f57"
    host_ext_id: "f28e7475-f835-42ef-ac35-ecbc48d5421e"
    select: "name,macAddress,vlanId"
  register: result
  ignore_errors: true

- name: List all virtual NICs of a host with fetch_all
  nutanix.ncp.ntnx_virtual_nics_info_v2:
    cluster_ext_id: "000647b8-ddb3-6bbb-0000-000000028f57"
    host_ext_id: "f28e7475-f835-42ef-ac35-ecbc48d5421e"
    fetch_all: true
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
  description:
    - The response from the Nutanix PC virtual NICs info v4 API.
    - It can be a single virtual NIC if external ID is provided.
    - List of multiple virtual NICs of the host if external ID is not provided with optional filter, limit, orderby, or select.
  returned: always
  type: dict
  sample:
    {
        "ext_id": "0a0a0a0a-1111-2222-3333-444455556666",
        "name": "br0",
        "host_description": "AHV host",
        "mac_address": "aa:bb:cc:dd:ee:ff",
        "ipv4_addresses": [
            {
                "ipv4": {
                    "value": "10.44.76.30",
                    "prefix_length": 32
                },
                "ipv6": null
            }
        ],
        "ipv6_addresses": null,
        "interface_status": "UP",
        "is_dhcp_enabled": false,
        "link_speed_in_kbps": 10000000,
        "mtu_in_bytes": 1500,
        "node_uuid": "f28e7475-f835-42ef-ac35-ecbc48d5421e",
        "vlan_id": 0,
        "host_nics_uuids": [
            "b1a1c1d1-1111-2222-3333-444455556666"
        ],
        "links": null,
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
  sample: "Api Exception raised while fetching virtual NICs info"

error:
  description: This field typically holds information about if the task have errors that occurred during the task execution.
  type: str
  returned: when an error occurs

failed:
  description: This field typically holds information about if the task have failed.
  returned: always
  type: bool
  sample: false

ext_id:
  description: External ID of the virtual NIC (when requested via C(ext_id)).
  type: str
  returned: When external ID is provided
  sample: "0a0a0a0a-1111-2222-3333-444455556666"

total_available_results:
  description: The total number of available virtual NICs for the host.
  type: int
  returned: When listing virtual NICs for a host
  sample: 4
"""


import warnings  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.clusters_mgmt.api_client import (  # noqa: E402
    get_clusters_api_instance,
)
from ..module_utils.v4.clusters_mgmt.helpers import get_virtual_nic  # noqa: E402
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
        host_ext_id=dict(type="str", required=True),
        ext_id=dict(type="str"),
    )

    return module_args


def get_virtual_nic_using_ext_id(module, api_instance, result):
    cluster_ext_id = module.params.get("cluster_ext_id")
    host_ext_id = module.params.get("host_ext_id")
    ext_id = module.params.get("ext_id")
    resp = get_virtual_nic(module, api_instance, ext_id, cluster_ext_id, host_ext_id)
    result["ext_id"] = ext_id
    result["response"] = strip_internal_attributes(resp.to_dict())


def get_virtual_nics(module, api_instance, result):
    cluster_ext_id = module.params.get("cluster_ext_id")
    host_ext_id = module.params.get("host_ext_id")

    sg = SpecGenerator(module)
    kwargs, err = sg.get_info_spec(attr=module.params)

    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating virtual NICs info spec", **result)

    try:
        resp = list_entities(
            api_instance.list_virtual_nics_by_host_id,
            kwargs=kwargs,
            clusterExtId=cluster_ext_id,
            hostExtId=host_ext_id,
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching virtual NICs info",
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
    result = {"changed": False, "error": None, "response": None, "failed": False}
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
