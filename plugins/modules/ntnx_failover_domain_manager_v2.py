#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2027, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_failover_domain_manager_v2
short_description: Failover domain manager protection plan
version_added: "2.7.0"
description:
    - Failover domain manager using protection plan.
    - This module uses PC v4 APIs based SDKs
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to
      the user performing the operation.
    - >-
      B(Failover domain manager) -
      Required Roles: Super Admin, Prism Admin, Domain Manager Admin
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=prism)"
options:
    ext_id:
        description:
            - The external ID of the domain manager protection plan.
        type: str
        required: true
    failover_type:
        description:
            - Failover type for domain manager.
        type: str
        choices:
            - UNPLANNED
        required: true
    network_spec:
        description:
            - Network details to be used during failover.
        type: dict
        required: false
        suboptions:
            external_address:
                description:
                    - External address for failover.
                type: dict
                required: false
                suboptions:
                    ipv4:
                        description:
                            - IPv4 address.
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
                                    - Prefix length.
                                type: int
                                required: false
                    ipv6:
                        description:
                            - IPv6 address.
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
                                    - Prefix length.
                                type: int
                                required: false
            network_ext_id:
                description:
                    - The network external identifier to be used for failover.
                type: str
                required: false
            default_gateway:
                description:
                    - Default gateway for failover network.
                type: dict
                required: false
                suboptions:
                    ipv4:
                        description:
                            - IPv4 address.
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
                                    - Prefix length.
                                type: int
                                required: false
                    ipv6:
                        description:
                            - IPv6 address.
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
                                    - Prefix length.
                                type: int
                                required: false
                    fqdn:
                        description:
                            - Fully qualified domain name.
                        type: dict
                        required: false
                        suboptions:
                            value:
                                description:
                                    - FQDN value.
                                type: str
                                required: true
            subnet_mask:
                description:
                    - Subnet mask for failover network.
                type: dict
                required: false
                suboptions:
                    ipv4:
                        description:
                            - IPv4 address.
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
                                    - Prefix length.
                                type: int
                                required: false
                    ipv6:
                        description:
                            - IPv6 address.
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
                                    - Prefix length.
                                type: int
                                required: false
                    fqdn:
                        description:
                            - Fully qualified domain name.
                        type: dict
                        required: false
                        suboptions:
                            value:
                                description:
                                    - FQDN value.
                                type: str
                                required: true
            ip_ranges:
                description:
                    - List of IP ranges for failover network.
                type: list
                elements: dict
                required: false
                suboptions:
                    begin:
                        description:
                            - Beginning IP of range.
                        type: dict
                        required: false
                        suboptions:
                            ipv4:
                                description:
                                    - IPv4 address.
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
                                            - Prefix length.
                                        type: int
                                        required: false
                            ipv6:
                                description:
                                    - IPv6 address.
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
                                            - Prefix length.
                                        type: int
                                        required: false
                    end:
                        description:
                            - Ending IP of range.
                        type: dict
                        required: false
                        suboptions:
                            ipv4:
                                description:
                                    - IPv4 address.
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
                                            - Prefix length.
                                        type: int
                                        required: false
                            ipv6:
                                description:
                                    - IPv6 address.
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
                                            - Prefix length.
                                        type: int
                                        required: false
            ip_addresses:
                description:
                    - List of IP addresses for failover network.
                type: list
                elements: dict
                required: false
                suboptions:
                    ipv4:
                        description:
                            - IPv4 address.
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
                                    - Prefix length.
                                type: int
                                required: false
                    ipv6:
                        description:
                            - IPv6 address.
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
                                    - Prefix length.
                                type: int
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
- name: Failover domain manager
  hosts: localhost
  gather_facts: false
  module_defaults:
    group/nutanix.ncp.ntnx:
      nutanix_host: "{{ ip }}"
      nutanix_username: "{{ username }}"
      nutanix_password: "{{ password }}"
      validate_certs: false
  tasks:
    - name: Failover domain manager
      nutanix.ncp.ntnx_failover_domain_manager_v2:
        ext_id: "11111111-1111-1111-1111-111111111111"
        failover_type: "UNPLANNED"
        network_spec:
          network_ext_id: "00000000-0000-0000-0000-000000000003"
          external_address:
            ipv4:
              value: "10.0.0.20"
          default_gateway:
            ipv4:
              value: "10.0.0.1"
          subnet_mask:
            ipv4:
              value: "255.255.255.0"
      register: result
      ignore_errors: true
"""

RETURN = r"""
response:
  description:
      - Response for failover domain manager.
      - If C(wait) is true, it will contain the final task payload after
        completion.
      - If C(wait) is false, it will contain the initial task details.
  returned: always
  type: dict
  sample:
    {
        "completed_time": "2025-01-29T07:35:54.109510+00:00",
        "created_time": "2025-01-29T07:35:49.556281+00:00",
        "ext_id": "ZXJnb24=:5f63a855-6b6e-4aca-4efb-159a35ce0e52",
        "operation": "FailoverDomainManager",
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
    - The external ID of the domain manager protection plan.
  returned: always
  type: str
  sample: "11111111-1111-1111-1111-111111111111"

changed:
  description: This indicates whether the task resulted in any changes
  returned: always
  type: bool
  sample: true

error:
  description: This indicates the error message if any error occurred
  returned: When an error occurs
  type: str

failed:
  description: This indicates whether the task failed
  returned: always
  type: bool
  sample: false

msg:
  description: This indicates the message if any message occurred
  returned: When there is an error
  type: str
  sample: "Api Exception raised while failing over domain manager"
"""

import traceback  # noqa: E402
import warnings  # noqa: E402

from ansible.module_utils.basic import missing_required_lib  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_module_v4 import BaseModuleV4  # noqa: E402
from ..module_utils.v4.prism.pc_api_client import (  # noqa: E402
    get_domain_manager_protection_plan_api_instance,
)
from ..module_utils.v4.prism.tasks import wait_for_completion  # noqa: E402
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
    validate_required_params,
)

SDK_IMP_ERROR = None
try:
    import ntnx_prism_py_client as prism_sdk  # noqa: E402
except ImportError:

    from ..module_utils.v4.sdk_mock import mock_sdk as prism_sdk  # noqa: E402

    SDK_IMP_ERROR = traceback.format_exc()

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():

    ipv4_spec = dict(
        value=dict(type="str", required=True),
        prefix_length=dict(type="int"),
    )

    ipv6_spec = dict(
        value=dict(type="str", required=True),
        prefix_length=dict(type="int"),
    )

    fqdn_spec = dict(
        value=dict(type="str", required=True),
    )

    ip_address_spec = dict(
        ipv4=dict(type="dict", options=ipv4_spec, obj=prism_sdk.IPv4Address),
        ipv6=dict(type="dict", options=ipv6_spec, obj=prism_sdk.IPv6Address),
    )

    ip_address_or_fqdn_spec = dict(
        ipv4=dict(type="dict", options=ipv4_spec, obj=prism_sdk.IPv4Address),
        ipv6=dict(type="dict", options=ipv6_spec, obj=prism_sdk.IPv6Address),
        fqdn=dict(type="dict", options=fqdn_spec, obj=prism_sdk.FQDN),
    )

    ip_range_spec = dict(
        begin=dict(type="dict", options=ip_address_spec, obj=prism_sdk.IPAddress),
        end=dict(type="dict", options=ip_address_spec, obj=prism_sdk.IPAddress),
    )

    failover_network_details_spec = dict(
        external_address=dict(
            type="dict", options=ip_address_spec, obj=prism_sdk.IPAddress
        ),
        network_ext_id=dict(type="str"),
        default_gateway=dict(
            type="dict",
            options=ip_address_or_fqdn_spec,
            obj=prism_sdk.IPAddressOrFQDN,
        ),
        subnet_mask=dict(
            type="dict",
            options=ip_address_or_fqdn_spec,
            obj=prism_sdk.IPAddressOrFQDN,
        ),
        ip_ranges=dict(
            type="list",
            elements="dict",
            options=ip_range_spec,
            obj=prism_sdk.IpRange,
        ),
        ip_addresses=dict(
            type="list",
            elements="dict",
            options=ip_address_spec,
            obj=prism_sdk.IPAddress,
        ),
    )

    module_args = dict(
        ext_id=dict(type="str", required=True),
        failover_type=dict(
            type="str",
            required=True,
            choices=["UNPLANNED"],
            obj=prism_sdk.FailoverType,
        ),
        network_spec=dict(
            type="dict",
            options=failover_network_details_spec,
            obj=prism_sdk.FailoverNetworkDetails,
        ),
    )
    return module_args


def run_action(module, result, api_instance):
    validate_required_params(module, ["failover_type"])
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id
    sg = SpecGenerator(module)
    default_spec = prism_sdk.FailoverSpec()
    spec, err = sg.generate_spec(obj=default_spec)
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating failover domain manager spec", **result)

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        return

    resp = None
    try:
        resp = api_instance.failover_domain_manager(extId=ext_id, body=spec)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while failing over domain manager",
        )
    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        task = wait_for_completion(module, task_ext_id)
        result["response"] = strip_internal_attributes(task.to_dict())
    result["changed"] = True


def run_module():
    module = BaseModuleV4(
        argument_spec=get_module_spec(),
        supports_check_mode=True,
    )
    if SDK_IMP_ERROR:
        module.fail_json(
            msg=missing_required_lib("ntnx_prism_py_client"),
            exception=SDK_IMP_ERROR,
        )

    remove_param_with_none_value(module.params)
    result = {"changed": False, "failed": False, "response": None}
    api_instance = get_domain_manager_protection_plan_api_instance(module)
    run_action(module, result, api_instance)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
