#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2027, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_compute_non_migratable_vms_info_v2
short_description: Compute non-migratable VMs for a Nutanix cluster
version_added: "2.7.0"
description:
  - Compute non-migratable VMs for hosts in a Nutanix cluster.
  - Returns the task reference created by the compute operation.
  - This module uses PC v4 APIs based SDKs
notes:
  - >-
    This module requires the following Nutanix IAM roles to be assigned to the
    user performing the operation.
  - >-
    B(Compute Cluster Non Migratable Vms) -
    Required Roles: Cluster Admin, Prism Admin, Super Admin
  - "Ref: U(https://developers.nutanix.com/api-reference?namespace=clustermgmt)"
options:
  cluster_ext_id:
    description:
      - Indicates the UUID of a cluster.
    type: str
    required: true
  hosts:
    description:
      - List of host UUIDs associated with the cluster.
    type: list
    elements: str
    required: true
  vcenter_info:
    description:
      - Vcenter information for ESX.
    type: dict
    required: false
    suboptions:
      address:
        description:
          - Vcenter IP address or FQDN.
        type: dict
        required: true
        suboptions:
          ipv4:
            description:
              - IPv4 address configuration.
            type: dict
            suboptions:
              value:
                description:
                  - The IPv4 address value.
                type: str
                required: true
              prefix_length:
                description:
                  - The prefix length of the IPv4 address.
                type: int
          ipv6:
            description:
              - IPv6 address configuration.
            type: dict
            suboptions:
              value:
                description:
                  - The IPv6 address value.
                type: str
                required: true
              prefix_length:
                description:
                  - The prefix length of the IPv6 address.
                type: int
          fqdn:
            description:
              - Fully qualified domain name configuration.
            type: dict
            suboptions:
              value:
                description:
                  - The FQDN value.
                type: str
                required: true
      credentials:
        description:
          - Credentials used to authenticate with vCenter.
        type: dict
        required: true
        suboptions:
          username:
            description:
              - Username for vCenter Server.
            type: str
            required: true
          password:
            description:
              - Password for vCenter Server.
            type: str
            required: true
          port:
            description:
              - vCenter port to connect.
            type: int
  read_timeout:
    description: Read timeout in milliseconds for API calls.
    type: int
    required: false
    default: 30000
extends_documentation_fragment:
  - nutanix.ncp.ntnx_credentials
  - nutanix.ncp.ntnx_logger
  - nutanix.ncp.ntnx_proxy_v2
author:
  - Abhinav Bansal (@abhinavbansal29)
  - George Ghawali (@george-ghawali)
"""

EXAMPLES = r"""
- name: Compute non-migratable VMs for hosts in a cluster
  nutanix.ncp.ntnx_compute_non_migratable_vms_info_v2:
    cluster_ext_id: "00061de6-4a87-6b06-185b-ac1f6b6f97e2"
    hosts:
      - "af49a0bb-b3d7-41c0-b9c2-f4ca0e8763e9"
  register: result
  ignore_errors: true

- name: Compute non-migratable VMs with vCenter info for ESXi
  nutanix.ncp.ntnx_compute_non_migratable_vms_info_v2:
    cluster_ext_id: "00061de6-4a87-6b06-185b-ac1f6b6f97e2"
    hosts:
      - "af49a0bb-b3d7-41c0-b9c2-f4ca0e8763e9"
    vcenter_info:
      address:
        ipv4:
          value: "10.0.0.10"
      credentials:
        username: "administrator@vsphere.local"
        password: "SecretPassword"
        port: 443
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
  description:
    - The response from the Nutanix PC compute non-migratable VMs v4 API.
    - Contains the task reference for the compute operation.
  returned: always
  type: dict
  sample:
    {
      "ext_id": "ZXJnb24=:90458bc7-a12b-4616-ac66-562fdb00c209"
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
  sample: "Api Exception raised while computing non-migratable VMs"

error:
  description: This indicates the error message if any error occurred
  type: str
  returned: when an error occurs

failed:
  description: This indicates whether the task failed
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
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
    validate_required_params,
)

SDK_IMP_ERROR = None
try:
    import ntnx_clustermgmt_py_client as sdk  # noqa: E402
except ImportError:
    from ..module_utils.v4.sdk_mock import mock_sdk as sdk  # noqa: E402

    SDK_IMP_ERROR = traceback.format_exc()

warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    ipv4_spec = dict(
        value=dict(type="str", required=True),
        prefix_length=dict(type="int", required=False),
    )
    ipv6_spec = dict(
        value=dict(type="str", required=True),
        prefix_length=dict(type="int", required=False),
    )
    fqdn_spec = dict(
        value=dict(type="str", required=True),
    )
    ip_address_or_fqdn_spec = dict(
        ipv4=dict(
            type="dict",
            options=ipv4_spec,
            obj=sdk.IPv4Address,
            required=False,
        ),
        ipv6=dict(
            type="dict",
            options=ipv6_spec,
            obj=sdk.IPv6Address,
            required=False,
        ),
        fqdn=dict(
            type="dict",
            options=fqdn_spec,
            obj=sdk.FQDN,
            required=False,
        ),
    )
    vcenter_credentials_spec = dict(
        username=dict(type="str", required=True),
        password=dict(type="str", required=True, no_log=True),
        port=dict(type="int", required=False),
    )
    vcenter_info_spec = dict(
        address=dict(
            type="dict",
            required=True,
            options=ip_address_or_fqdn_spec,
            obj=sdk.IPAddressOrFQDN,
            mutually_exclusive=[("ipv4", "ipv6", "fqdn")],
            required_one_of=[("ipv4", "ipv6", "fqdn")],
        ),
        credentials=dict(
            type="dict",
            required=True,
            options=vcenter_credentials_spec,
            obj=sdk.VcenterCredentials,
        ),
    )
    module_args = dict(
        cluster_ext_id=dict(type="str", required=True),
        hosts=dict(type="list", elements="str", required=True),
        vcenter_info=dict(
            type="dict",
            required=False,
            options=vcenter_info_spec,
            obj=sdk.VcenterInfo,
        ),
    )
    return module_args


def compute_non_migratable_vms(module, api_instance, result):
    validate_required_params(module, ["cluster_ext_id", "hosts"])
    cluster_ext_id = module.params.get("cluster_ext_id")

    sg = SpecGenerator(module)
    default_spec = sdk.ComputeNonMigratableVmsSpec()
    spec, err = sg.generate_spec(obj=default_spec)
    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed generating compute non-migratable VMs spec", **result
        )

    try:
        resp = api_instance.compute_non_migratable_vms(
            clusterExtId=cluster_ext_id, body=spec
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while computing non-migratable VMs",
        )

    if getattr(resp, "data", None):
        result["response"] = strip_internal_attributes(resp.data.to_dict())
    else:
        result["response"] = strip_internal_attributes(resp.to_dict())


def run_module():
    module = BaseInfoModule(
        argument_spec=get_module_spec(),
        supports_check_mode=False,
        skip_info_args=True,
    )
    if SDK_IMP_ERROR:
        module.fail_json(
            msg=missing_required_lib("ntnx_clustermgmt_py_client"),
            exception=SDK_IMP_ERROR,
        )

    remove_param_with_none_value(module.params)
    result = {"changed": False, "response": None, "failed": False}
    api_instance = get_clusters_api_instance(module)
    compute_non_migratable_vms(module, api_instance, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
