#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_hardware_providers_v2
short_description: Update or delete a hardware provider connection in Nutanix Foundation Central
version_added: 2.7.0
description:
  - This module allows you to update and delete a connection to a hardware provider endpoint.
  - A connection enables node discovery and management through a hardware provider.
  - Use M(nutanix.ncp.ntnx_create_connection_by_hardware_provider_id_v2) to create a connection.
  - This module uses Foundation Central (FCVM) v4 APIs based SDKs.
notes:
  - This module talks to B(Foundation Central / FCVM), B(not) Prism Central.
    Set C(nutanix_host) to the Foundation Central (FCVM) endpoint.
  - >-
    B(Update a connection) -
    Required Roles - Admin role on Foundation Central.
  - >-
    B(Delete a connection) -
    Required Roles - Admin role on Foundation Central.
  - The referenced hardware provider must exist before managing its connections.
  - "Ref: U(https://developers.nutanix.com/api-reference?namespace=lifecycle)"
options:
  state:
    description:
      - If C(state) is C(present) and C(ext_id) is provided then the operation will be update connection.
      - If C(state) is C(absent) and C(ext_id) is provided then the operation will be delete connection.
      - Creation of a connection is not supported by this module.
        Use M(nutanix.ncp.ntnx_create_connection_by_hardware_provider_id_v2) instead.
    type: str
    required: false
    choices:
      - present
      - absent
    default: present
  hardware_provider_ext_id:
    description:
      - External ID of the hardware provider that owns the connection.
      - Required for all operations.
    type: str
    required: true
  ext_id:
    description:
      - The external ID of the connection.
      - Required for update and delete operations.
    type: str
    required: false
  name:
    description:
      - Name of the connection.
      - Maximum 40 characters.
      - Required when updating a connection.
    type: str
    required: false
  deployment_type:
    description:
      - Deployment type of the connection.
    type: str
    choices:
      - ONPREM
      - SAAS
      - STANDALONE
    required: false
  region:
    description:
      - Region for the connection.
      - Maximum 32 characters.
    type: str
    required: false
  access_details:
    description:
      - Access details including endpoint and authentication information.
      - Required when updating a connection.
    type: list
    elements: dict
    required: false
    suboptions:
      endpoint:
        description:
          - Endpoint configuration for the connection.
          - Exactly one of the endpoint types must be provided.
        type: dict
        required: true
        suboptions:
          url_endpoint:
            description:
              - URL based endpoint configuration.
            type: dict
            required: false
            suboptions:
              url:
                description:
                  - The URL of the endpoint.
                type: str
                required: true
          ip_range_endpoint:
            description:
              - IP range based endpoint configuration.
            type: dict
            required: false
            suboptions:
              ip_ranges:
                description:
                  - List of IP address ranges.
                type: list
                elements: dict
                required: true
                suboptions:
                  start_ip:
                    description:
                      - Starting IP address of the range.
                    type: dict
                    required: true
                    suboptions:
                      ipv4:
                        description:
                          - IPv4 address configuration.
                        type: dict
                        required: false
                        suboptions:
                          value:
                            description:
                              - The IPv4 address value.
                            type: str
                            required: true
                          prefix_length:
                            description:
                              - Prefix length of the network.
                            type: int
                            required: false
                            default: 32
                      ipv6:
                        description:
                          - IPv6 address configuration.
                        type: dict
                        required: false
                        suboptions:
                          value:
                            description:
                              - The IPv6 address value.
                            type: str
                            required: true
                          prefix_length:
                            description:
                              - Prefix length of the network.
                            type: int
                            required: false
                            default: 128
                  end_ip:
                    description:
                      - Ending IP address of the range.
                    type: dict
                    required: true
                    suboptions:
                      ipv4:
                        description:
                          - IPv4 address configuration.
                        type: dict
                        required: false
                        suboptions:
                          value:
                            description:
                              - The IPv4 address value.
                            type: str
                            required: true
                          prefix_length:
                            description:
                              - Prefix length of the network.
                            type: int
                            required: false
                            default: 32
                      ipv6:
                        description:
                          - IPv6 address configuration.
                        type: dict
                        required: false
                        suboptions:
                          value:
                            description:
                              - The IPv6 address value.
                            type: str
                            required: true
                          prefix_length:
                            description:
                              - Prefix length of the network.
                            type: int
                            required: false
                            default: 128
          ip_address_endpoint:
            description:
              - IP address or FQDN based endpoint configuration.
            type: dict
            required: false
            suboptions:
              ip_addresses:
                description:
                  - List of IP addresses or FQDNs.
                type: list
                elements: dict
                required: true
                suboptions:
                  ipv4:
                    description:
                      - IPv4 address configuration.
                    type: dict
                    required: false
                    suboptions:
                      value:
                        description:
                          - The IPv4 address value.
                        type: str
                        required: true
                      prefix_length:
                        description:
                          - Prefix length of the network.
                        type: int
                        required: false
                        default: 32
                  ipv6:
                    description:
                      - IPv6 address configuration.
                    type: dict
                    required: false
                    suboptions:
                      value:
                        description:
                          - The IPv6 address value.
                        type: str
                        required: true
                      prefix_length:
                        description:
                          - Prefix length of the network.
                        type: int
                        required: false
                        default: 128
                  fqdn:
                    description:
                      - Fully Qualified Domain Name configuration.
                    type: dict
                    required: false
                    suboptions:
                      value:
                        description:
                          - The FQDN value.
                        type: str
                        required: true
      auth:
        description:
          - Authentication configuration for the connection.
          - Exactly one of the authentication types must be provided.
        type: dict
        required: true
        suboptions:
          api_key_auth:
            description:
              - API key based authentication.
            type: dict
            required: false
            suboptions:
              api_key_id:
                description:
                  - The API key identifier.
                type: str
                required: true
              api_key_secret:
                description:
                  - The API key secret.
                type: str
                required: false
          basic_auth:
            description:
              - Username and password based authentication.
            type: dict
            required: false
            suboptions:
              username:
                description:
                  - The username for authentication.
                type: str
                required: true
              password:
                description:
                  - The password for authentication.
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
- name: Update a hardware provider connection
  nutanix.ncp.ntnx_hardware_providers_v2:
    nutanix_host: "{{ foundation_host }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: present
    hardware_provider_ext_id: "5e5a9d0b-8f3d-4c14-9f6f-6b3a3c9c6a01"
    ext_id: "8300384a-56ee-4750-aeb8-3d1c42908bee"
    name: "connection_ansible_updated"
    deployment_type: "ONPREM"
    region: "us-west"
    access_details:
      - endpoint:
          url_endpoint:
            url: "https://intersight.example.com"
        auth:
          basic_auth:
            username: "admin"
            password: "secret"
  register: result
  ignore_errors: true

- name: Delete a hardware provider connection
  nutanix.ncp.ntnx_hardware_providers_v2:
    nutanix_host: "{{ foundation_host }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: absent
    hardware_provider_ext_id: "5e5a9d0b-8f3d-4c14-9f6f-6b3a3c9c6a01"
    ext_id: "8300384a-56ee-4750-aeb8-3d1c42908bee"
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
  description:
    - Response for updating or deleting a hardware provider connection.
    - If the operation is update and C(wait) is true, it will return the connection details.
    - If the operation is update and C(wait) is false, it will return the task details.
    - If the operation is delete, it will return the task details.
  returned: always
  type: dict
  sample:
    {
      "access_details": [
        {
          "auth": {
            "password": null,
            "username": "admin"
          },
          "endpoint": {
            "ip_addresses": [
              {
                "fqdn": null,
                "ipv4": {
                  "prefix_length": 32,
                  "value": "10.97.44.181"
                },
                "ipv6": null
              }
            ]
          }
        }
      ],
      "created_time": "2026-09-09T04:59:21.397266+00:00",
      "deployment_type": "STANDALONE",
      "ext_id": "89af36d8-b9b2-4623-9406-799ee178757b",
      "links": null,
      "name": "connection_ansible_updated",
      "region": "us-east",
      "tenant_id": null
    }

task_ext_id:
  description:
    - The external ID of the task.
  returned: always
  type: str
  sample: "ZXJnb24=:90458bc7-a12b-4616-ac66-562fdb00c209"

ext_id:
  description:
    - The external ID of the connection.
  returned: always
  type: str
  sample: "89af36d8-b9b2-4623-9406-799ee178757b"

changed:
  description: This indicates whether the task resulted in any changes.
  returned: always
  type: bool
  sample: true

skipped:
  description: This indicates whether the task was skipped due to idempotency.
  returned: when applicable
  type: bool
  sample: false

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
  description: This indicates the status or error message.
  returned: When there is an error, module is idempotent or check mode.
  type: str
  sample: "Nothing to change."
"""

import traceback  # noqa: E402
import warnings  # noqa: E402
from copy import deepcopy  # noqa: E402

from ansible.module_utils.basic import missing_required_lib  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_module_v4 import BaseModuleV4  # noqa: E402
from ..module_utils.v4.lcm.api_client import (  # noqa: E402
    get_etag,
    get_hardware_providers_api_instance,
)
from ..module_utils.v4.lcm.helpers import get_connection  # noqa: E402
from ..module_utils.v4.prism.tasks import wait_for_completion  # noqa: E402
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
    validate_required_params,
)

SDK_IMP_ERROR = None
try:
    import ntnx_lifecycle_py_client as lifecycle_sdk  # noqa: E402
except ImportError:

    from ..module_utils.v4.sdk_mock import mock_sdk as lifecycle_sdk  # noqa: E402

    SDK_IMP_ERROR = traceback.format_exc()

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():

    ipv4_spec = dict(
        value=dict(type="str", required=True),
        prefix_length=dict(type="int", required=False, default=32),
    )
    ipv6_spec = dict(
        value=dict(type="str", required=True),
        prefix_length=dict(type="int", required=False, default=128),
    )
    fqdn_spec = dict(
        value=dict(type="str", required=True),
    )
    ip_address_or_fqdn_spec = dict(
        ipv4=dict(
            type="dict",
            options=ipv4_spec,
            obj=lifecycle_sdk.IPv4Address,
            required=False,
        ),
        ipv6=dict(
            type="dict",
            options=ipv6_spec,
            obj=lifecycle_sdk.IPv6Address,
            required=False,
        ),
        fqdn=dict(
            type="dict",
            options=fqdn_spec,
            obj=lifecycle_sdk.FQDN,
            required=False,
        ),
    )
    ip_address_spec = dict(
        ipv4=dict(
            type="dict",
            options=ipv4_spec,
            obj=lifecycle_sdk.IPv4Address,
            required=False,
        ),
        ipv6=dict(
            type="dict",
            options=ipv6_spec,
            obj=lifecycle_sdk.IPv6Address,
            required=False,
        ),
    )
    ip_range_spec = dict(
        start_ip=dict(
            type="dict",
            options=ip_address_spec,
            obj=lifecycle_sdk.IPAddress,
            required=True,
        ),
        end_ip=dict(
            type="dict",
            options=ip_address_spec,
            obj=lifecycle_sdk.IPAddress,
            required=True,
        ),
    )
    url_endpoint_spec = dict(
        url=dict(type="str", required=True),
    )
    ip_range_endpoint_spec = dict(
        ip_ranges=dict(
            type="list",
            elements="dict",
            options=ip_range_spec,
            obj=lifecycle_sdk.ConfigIpRange,
            required=True,
        ),
    )
    ip_address_endpoint_spec = dict(
        ip_addresses=dict(
            type="list",
            elements="dict",
            options=ip_address_or_fqdn_spec,
            obj=lifecycle_sdk.IPAddressOrFQDN,
            required=True,
        ),
    )
    endpoint_spec = dict(
        url_endpoint=dict(
            type="dict",
            options=url_endpoint_spec,
            obj=lifecycle_sdk.UrlEndpoint,
            required=False,
        ),
        ip_range_endpoint=dict(
            type="dict",
            options=ip_range_endpoint_spec,
            obj=lifecycle_sdk.IpRangeEndpoint,
            required=False,
        ),
        ip_address_endpoint=dict(
            type="dict",
            options=ip_address_endpoint_spec,
            obj=lifecycle_sdk.IpAddressEndpoint,
            required=False,
        ),
    )
    api_key_auth_spec = dict(
        api_key_id=dict(type="str", required=True, no_log=False),
        api_key_secret=dict(type="str", required=False, no_log=True),
    )
    basic_auth_spec = dict(
        username=dict(type="str", required=True),
        password=dict(type="str", required=False, no_log=True),
    )
    auth_spec = dict(
        api_key_auth=dict(
            type="dict",
            options=api_key_auth_spec,
            obj=lifecycle_sdk.ApiKeyAuth,
            required=False,
            no_log=False,
        ),
        basic_auth=dict(
            type="dict",
            options=basic_auth_spec,
            obj=lifecycle_sdk.LifecycleConfigBasicAuth,
            required=False,
        ),
    )
    access_detail_spec = dict(
        endpoint=dict(
            type="dict",
            options=endpoint_spec,
            obj=dict(
                url_endpoint=lifecycle_sdk.UrlEndpoint,
                ip_range_endpoint=lifecycle_sdk.IpRangeEndpoint,
                ip_address_endpoint=lifecycle_sdk.IpAddressEndpoint,
            ),
            required=True,
            mutually_exclusive=[
                ("url_endpoint", "ip_range_endpoint", "ip_address_endpoint")
            ],
        ),
        auth=dict(
            type="dict",
            options=auth_spec,
            obj=dict(
                api_key_auth=lifecycle_sdk.ApiKeyAuth,
                basic_auth=lifecycle_sdk.LifecycleConfigBasicAuth,
            ),
            required=True,
            mutually_exclusive=[("api_key_auth", "basic_auth")],
        ),
    )
    module_args = dict(
        hardware_provider_ext_id=dict(type="str", required=True),
        ext_id=dict(type="str"),
        name=dict(type="str"),
        deployment_type=dict(
            type="str",
            choices=["ONPREM", "SAAS", "STANDALONE"],
            obj=lifecycle_sdk.ConnectionDeploymentType,
        ),
        region=dict(type="str"),
        access_details=dict(
            type="list",
            elements="dict",
            options=access_detail_spec,
            obj=lifecycle_sdk.ConnectionDetail,
        ),
    )
    return module_args


def create_hardware_providers(module, result):
    """Creating a connection is not supported by this module."""
    module.fail_json(
        msg="Creating a connection is not supported by this module. "
        "Use the ntnx_create_connection_by_hardware_provider_id_v2 module to "
        "create a connection.",
        **result,
    )


def _strip_write_only_secrets(spec_dict):
    """Remove write-only auth secrets that GET responses never return.

    The connection GET API never returns ``password`` / ``api_key_secret``
    (they are write-only). Comparing them during idempotency checks would
    always report a difference, so strip them from both specs.
    """
    for access_detail in spec_dict.get("access_details") or []:
        auth = access_detail.get("auth") or {}
        auth.pop("password", None)
        auth.pop("api_key_secret", None)
    return spec_dict


def check_for_idempotency(old_spec_dict, update_spec_dict):
    """Compare the existing connection spec with the requested update spec."""
    old_spec_dict = _strip_write_only_secrets(
        strip_internal_attributes(deepcopy(old_spec_dict))
    )
    update_spec_dict = _strip_write_only_secrets(
        strip_internal_attributes(deepcopy(update_spec_dict))
    )
    old_spec_dict.pop("created_time", None)
    update_spec_dict.pop("created_time", None)
    return old_spec_dict == update_spec_dict


def update_hardware_providers(module, api_instance, result):
    hardware_provider_ext_id = module.params.get("hardware_provider_ext_id")
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id
    validate_required_params(module, ["name", "access_details"])

    old_spec = get_connection(module, api_instance, hardware_provider_ext_id, ext_id)
    etag = get_etag(data=old_spec)
    if not etag:
        return module.fail_json(
            msg="Unable to fetch etag for updating connection", **result
        )
    kwargs = {"if_match": etag}
    sg = SpecGenerator(module)
    update_spec, err = sg.generate_spec(obj=deepcopy(old_spec))
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating update connection spec", **result)

    if module.check_mode:
        result["response"] = strip_internal_attributes(update_spec.to_dict())
        return

    if check_for_idempotency(old_spec.to_dict(), update_spec.to_dict()):
        result["skipped"] = True
        module.exit_json(msg="Nothing to change.", **result)

    resp = None
    try:
        resp = api_instance.update_connection_by_id(
            hardwareProviderExtId=hardware_provider_ext_id,
            extId=ext_id,
            body=update_spec,
            **kwargs,
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while updating connection",
        )
    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        wait_for_completion(module, task_ext_id)
        resp = get_connection(module, api_instance, hardware_provider_ext_id, ext_id)
        result["response"] = strip_internal_attributes(resp.to_dict())
    result["changed"] = True


def delete_hardware_providers(module, api_instance, result):
    hardware_provider_ext_id = module.params.get("hardware_provider_ext_id")
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id

    if module.check_mode:
        result["msg"] = "Connection with ext_id:{0} will be deleted.".format(ext_id)
        return

    old_spec = get_connection(module, api_instance, hardware_provider_ext_id, ext_id)
    etag = get_etag(data=old_spec)
    if not etag:
        return module.fail_json(
            msg="Unable to fetch etag for deleting connection", **result
        )
    kwargs = {"if_match": etag}

    resp = None
    try:
        resp = api_instance.delete_connection_by_id(
            hardwareProviderExtId=hardware_provider_ext_id, extId=ext_id, **kwargs
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while deleting connection",
        )
    if resp is not None and getattr(resp, "data", None) is not None:
        task_ext_id = resp.data.ext_id
        result["task_ext_id"] = task_ext_id
        if task_ext_id and module.params.get("wait"):
            task_status = wait_for_completion(module, task_ext_id, True)
            result["response"] = strip_internal_attributes(task_status.to_dict())
    result["changed"] = True


def run_module():
    module = BaseModuleV4(
        argument_spec=get_module_spec(),
        supports_check_mode=True,
        required_if=[
            ("state", "absent", ("ext_id",)),
            ("state", "present", ("ext_id",)),
        ],
    )
    if SDK_IMP_ERROR:
        module.fail_json(
            msg=missing_required_lib("ntnx_lifecycle_py_client"),
            exception=SDK_IMP_ERROR,
        )

    remove_param_with_none_value(module.params)
    result = {
        "changed": False,
        "response": None,
        "failed": False,
        "ext_id": None,
    }
    api_instance = get_hardware_providers_api_instance(module)
    state = module.params.get("state")
    if state == "present":
        if module.params.get("ext_id"):
            update_hardware_providers(module, api_instance, result)
        else:
            create_hardware_providers(module, result)
    else:
        delete_hardware_providers(module, api_instance, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
