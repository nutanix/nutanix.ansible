#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_hardware_providerss_info_v2
short_description: Fetch hardware providers and connection resources info in Nutanix Foundation Central
version_added: 2.7.0
description:
  - This module allows you to fetch hardware providers, connections, discovered nodes,
    and resource pools (IP, MAC, server identity) info in Nutanix Foundation Central.
  - The specific datasource is selected based on which identifiers are provided and the
    C(resource_type) parameter.
  - This module uses Foundation Central (FCVM) v4 APIs based SDKs.
notes:
  - This module talks to B(Foundation Central / FCVM), B(not) Prism Central.
    Set C(nutanix_host) to the Foundation Central (FCVM) endpoint.
  - >-
    B(Get / List hardware providers and their resources) -
    Required Roles - Viewer or Admin role on Foundation Central.
  - "Ref: U(https://developers.nutanix.com/api-reference?namespace=lifecycle)"
options:
  resource_type:
    description:
      - The type of resource to fetch when a connection context is provided.
      - Used to disambiguate the discovered node and resource pool datasources.
      - C(connection) fetches connections (default).
      - C(node) fetches discovered nodes.
      - C(ip_pool) fetches IP address pools.
      - C(mac_pool) fetches MAC address pools.
      - C(server_identity_pool) fetches server identity pools.
    type: str
    choices:
      - connection
      - node
      - ip_pool
      - mac_pool
      - server_identity_pool
    default: connection
    required: false
  ext_id:
    description:
      - The external ID of the entity to fetch.
      - When only C(ext_id) is provided (no parent IDs), fetch a hardware provider by ID.
      - When C(hardware_provider_ext_id) is provided with C(ext_id), fetch a connection by ID.
      - When C(hardware_provider_ext_id) and C(connection_ext_id) are provided with C(ext_id),
        fetch a discovered node or resource pool by ID (see C(resource_type)).
    type: str
    required: false
  hardware_provider_ext_id:
    description:
      - External ID of the hardware provider.
      - Required to fetch connections and their resources.
    type: str
    required: false
  connection_ext_id:
    description:
      - External ID of the connection.
      - Required to fetch discovered nodes and resource pools.
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
- name: List all hardware providers
  nutanix.ncp.ntnx_hardware_providerss_info_v2:
    nutanix_host: "{{ foundation_host }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
  register: result
  ignore_errors: true

- name: Get a hardware provider by ext_id
  nutanix.ncp.ntnx_hardware_providerss_info_v2:
    nutanix_host: "{{ foundation_host }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    ext_id: "5e5a9d0b-8f3d-4c14-9f6f-6b3a3c9c6a01"
  register: result
  ignore_errors: true

- name: List connections for a hardware provider
  nutanix.ncp.ntnx_hardware_providerss_info_v2:
    nutanix_host: "{{ foundation_host }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    hardware_provider_ext_id: "5e5a9d0b-8f3d-4c14-9f6f-6b3a3c9c6a01"
  register: result
  ignore_errors: true

- name: Get a connection by ext_id
  nutanix.ncp.ntnx_hardware_providerss_info_v2:
    nutanix_host: "{{ foundation_host }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    hardware_provider_ext_id: "5e5a9d0b-8f3d-4c14-9f6f-6b3a3c9c6a01"
    ext_id: "8300384a-56ee-4750-aeb8-3d1c42908bee"
  register: result
  ignore_errors: true

- name: List discovered nodes for a connection
  nutanix.ncp.ntnx_hardware_providerss_info_v2:
    nutanix_host: "{{ foundation_host }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    resource_type: node
    hardware_provider_ext_id: "5e5a9d0b-8f3d-4c14-9f6f-6b3a3c9c6a01"
    connection_ext_id: "8300384a-56ee-4750-aeb8-3d1c42908bee"
  register: result
  ignore_errors: true

- name: List IP address pools for a connection
  nutanix.ncp.ntnx_hardware_providerss_info_v2:
    nutanix_host: "{{ foundation_host }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    resource_type: ip_pool
    hardware_provider_ext_id: "5e5a9d0b-8f3d-4c14-9f6f-6b3a3c9c6a01"
    connection_ext_id: "8300384a-56ee-4750-aeb8-3d1c42908bee"
  register: result
  ignore_errors: true

- name: Get a MAC address pool by ext_id
  nutanix.ncp.ntnx_hardware_providerss_info_v2:
    nutanix_host: "{{ foundation_host }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    resource_type: mac_pool
    hardware_provider_ext_id: "5e5a9d0b-8f3d-4c14-9f6f-6b3a3c9c6a01"
    connection_ext_id: "8300384a-56ee-4750-aeb8-3d1c42908bee"
    ext_id: "3f4a6d0b-1c2d-4e5f-8a9b-0c1d2e3f4a5b"
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
  description:
    - The response from the Nutanix hardware providers info v4 API.
    - The host is Foundation Central (FCVM), not Prism Central.
    - It can be a single hardware provider, connection, discovered node, or resource pool
      if external ID is provided.
    - List of multiple entities if external ID is not provided, with optional filter or limit.
  returned: always
  type: dict
  sample:
    {
      "auth_types": ["BASIC"],
      "available_connection_count": 0,
      "ext_id": "743577ce-17e3-458f-9c45-ff34265eb797",
      "links": null,
      "name": "Dell iDRAC",
      "tenant_id": null,
      "type": "STANDALONE",
      "vendor": "Dell Inc."
    }

changed:
  description: This indicates whether the task resulted in any changes. Always false for info modules.
  returned: always
  type: bool
  sample: false

msg:
  description: This indicates the status or error message.
  returned: When there is an error
  type: str
  sample: "Api Exception raised while fetching hardware providers info"

error:
  description: This field holds the error details if any error occurred during execution.
  type: str
  returned: when an error occurs

failed:
  description: This indicates whether the task failed.
  returned: when something fails
  type: bool
  sample: false

ext_id:
  description: External ID of the fetched entity.
  type: str
  returned: when external ID is provided
  sample: "743577ce-17e3-458f-9c45-ff34265eb797"

total_available_results:
  description: The total number of available results in Foundation Central.
  type: int
  returned: when a list of entities is fetched
  sample: 5
"""

import warnings  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.lcm.api_client import (  # noqa: E402
    get_hardware_providers_api_instance,
)
from ..module_utils.v4.lcm.helpers import (  # noqa: E402
    get_connection,
    get_connection_node,
    get_hardware_provider,
    get_ip_pool,
    get_mac_pool,
    get_server_identity_pool,
)
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
)

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    module_args = dict(
        resource_type=dict(
            type="str",
            choices=[
                "connection",
                "node",
                "ip_pool",
                "mac_pool",
                "server_identity_pool",
            ],
            default="connection",
        ),
        ext_id=dict(type="str"),
        hardware_provider_ext_id=dict(type="str"),
        connection_ext_id=dict(type="str"),
    )
    return module_args


def _set_list_response(result, resp):
    """Populate result with the total count and stripped list response."""
    total_available_results = resp.metadata.total_available_results
    result["total_available_results"] = total_available_results
    resp = strip_internal_attributes(resp.to_dict()).get("data")
    if not resp:
        resp = []
    result["response"] = resp


def _get_kwargs(module, result):
    sg = SpecGenerator(module)
    kwargs, err = sg.get_info_spec(attr=module.params)
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating hardware providers info spec", **result)
    return kwargs


def get_hardware_provider_using_ext_id(module, api_instance, result):
    ext_id = module.params.get("ext_id")
    resp = get_hardware_provider(module, api_instance, ext_id)
    result["ext_id"] = ext_id
    result["response"] = strip_internal_attributes(resp.to_dict())


def list_hardware_providers(module, api_instance, result):
    kwargs = _get_kwargs(module, result)
    try:
        resp = api_instance.list_hardware_providers(**kwargs)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching hardware providers info",
        )
    _set_list_response(result, resp)


def get_connection_using_ext_id(module, api_instance, result):
    hardware_provider_ext_id = module.params.get("hardware_provider_ext_id")
    ext_id = module.params.get("ext_id")
    resp = get_connection(module, api_instance, hardware_provider_ext_id, ext_id)
    result["ext_id"] = ext_id
    result["response"] = strip_internal_attributes(resp.to_dict())


def list_connections(module, api_instance, result):
    hardware_provider_ext_id = module.params.get("hardware_provider_ext_id")
    kwargs = _get_kwargs(module, result)
    try:
        resp = api_instance.list_connections_by_hardware_provider_id(
            hardwareProviderExtId=hardware_provider_ext_id, **kwargs
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching connections info",
        )
    _set_list_response(result, resp)


def get_node_using_ext_id(module, api_instance, result):
    hardware_provider_ext_id = module.params.get("hardware_provider_ext_id")
    connection_ext_id = module.params.get("connection_ext_id")
    ext_id = module.params.get("ext_id")
    resp = get_connection_node(
        module, api_instance, hardware_provider_ext_id, connection_ext_id, ext_id
    )
    result["ext_id"] = ext_id
    result["response"] = strip_internal_attributes(resp.to_dict())


def list_nodes(module, api_instance, result):
    hardware_provider_ext_id = module.params.get("hardware_provider_ext_id")
    connection_ext_id = module.params.get("connection_ext_id")
    kwargs = _get_kwargs(module, result)
    try:
        resp = api_instance.list_nodes_by_connection_id(
            hardwareProviderExtId=hardware_provider_ext_id,
            connectionExtId=connection_ext_id,
            **kwargs,
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching discovered nodes info",
        )
    _set_list_response(result, resp)


def get_ip_pool_using_ext_id(module, api_instance, result):
    hardware_provider_ext_id = module.params.get("hardware_provider_ext_id")
    connection_ext_id = module.params.get("connection_ext_id")
    ext_id = module.params.get("ext_id")
    resp = get_ip_pool(
        module, api_instance, hardware_provider_ext_id, connection_ext_id, ext_id
    )
    result["ext_id"] = ext_id
    result["response"] = strip_internal_attributes(resp.to_dict())


def list_ip_pools(module, api_instance, result):
    hardware_provider_ext_id = module.params.get("hardware_provider_ext_id")
    connection_ext_id = module.params.get("connection_ext_id")
    kwargs = _get_kwargs(module, result)
    try:
        resp = api_instance.list_ip_pools_by_connection_id(
            hardwareProviderExtId=hardware_provider_ext_id,
            connectionExtId=connection_ext_id,
            **kwargs,
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching IP address pools info",
        )
    _set_list_response(result, resp)


def get_mac_pool_using_ext_id(module, api_instance, result):
    hardware_provider_ext_id = module.params.get("hardware_provider_ext_id")
    connection_ext_id = module.params.get("connection_ext_id")
    ext_id = module.params.get("ext_id")
    resp = get_mac_pool(
        module, api_instance, hardware_provider_ext_id, connection_ext_id, ext_id
    )
    result["ext_id"] = ext_id
    result["response"] = strip_internal_attributes(resp.to_dict())


def list_mac_pools(module, api_instance, result):
    hardware_provider_ext_id = module.params.get("hardware_provider_ext_id")
    connection_ext_id = module.params.get("connection_ext_id")
    kwargs = _get_kwargs(module, result)
    try:
        resp = api_instance.list_mac_pools_by_connection_id(
            hardwareProviderExtId=hardware_provider_ext_id,
            connectionExtId=connection_ext_id,
            **kwargs,
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching MAC address pools info",
        )
    _set_list_response(result, resp)


def get_server_identity_pool_using_ext_id(module, api_instance, result):
    hardware_provider_ext_id = module.params.get("hardware_provider_ext_id")
    connection_ext_id = module.params.get("connection_ext_id")
    ext_id = module.params.get("ext_id")
    resp = get_server_identity_pool(
        module, api_instance, hardware_provider_ext_id, connection_ext_id, ext_id
    )
    result["ext_id"] = ext_id
    result["response"] = strip_internal_attributes(resp.to_dict())


def list_server_identity_pools(module, api_instance, result):
    hardware_provider_ext_id = module.params.get("hardware_provider_ext_id")
    connection_ext_id = module.params.get("connection_ext_id")
    kwargs = _get_kwargs(module, result)
    try:
        resp = api_instance.list_server_identity_pools_by_connection_id(
            hardwareProviderExtId=hardware_provider_ext_id,
            connectionExtId=connection_ext_id,
            **kwargs,
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching server identity pools info",
        )
    _set_list_response(result, resp)


# Dispatch tables for connection-scoped resource datasources.
_GET_BY_ID_DISPATCH = {
    "node": get_node_using_ext_id,
    "ip_pool": get_ip_pool_using_ext_id,
    "mac_pool": get_mac_pool_using_ext_id,
    "server_identity_pool": get_server_identity_pool_using_ext_id,
}

_LIST_DISPATCH = {
    "node": list_nodes,
    "ip_pool": list_ip_pools,
    "mac_pool": list_mac_pools,
    "server_identity_pool": list_server_identity_pools,
}


def run_module():
    module = BaseInfoModule(
        argument_spec=get_module_spec(),
        supports_check_mode=False,
        mutually_exclusive=[("ext_id", "filter")],
        required_by={
            "connection_ext_id": "hardware_provider_ext_id",
        },
    )
    remove_param_with_none_value(module.params)
    result = {"changed": False, "response": None, "failed": False}
    api_instance = get_hardware_providers_api_instance(module)

    resource_type = module.params.get("resource_type")
    ext_id = module.params.get("ext_id")
    hardware_provider_ext_id = module.params.get("hardware_provider_ext_id")
    connection_ext_id = module.params.get("connection_ext_id")

    if connection_ext_id:
        # Discovered node / resource pool scope.
        if ext_id:
            _GET_BY_ID_DISPATCH.get(resource_type, get_node_using_ext_id)(
                module, api_instance, result
            )
        else:
            _LIST_DISPATCH.get(resource_type, list_nodes)(module, api_instance, result)
    elif hardware_provider_ext_id:
        # Connection scope.
        if ext_id:
            get_connection_using_ext_id(module, api_instance, result)
        else:
            list_connections(module, api_instance, result)
    else:
        # Hardware provider scope.
        if ext_id:
            get_hardware_provider_using_ext_id(module, api_instance, result)
        else:
            list_hardware_providers(module, api_instance, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
