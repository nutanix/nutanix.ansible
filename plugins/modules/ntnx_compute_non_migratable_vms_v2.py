#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2027, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_compute_non_migratable_vms_v2
short_description: Compute non-migratable VMs for a cluster
version_added: "2.7.0"
description:
    - Compute non-migratable VMs for hosts associated with a Nutanix cluster.
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
  hosts:
    description:
      - List of host UUIDs associated with the cluster.
    type: list
    elements: str
  vcenter_info:
    description:
      - Vcenter information for ESX.
    type: dict
    suboptions:
      address:
        description:
          - Vcenter IP address or FQDN.
        type: dict
        required: true
        suboptions:
          ipv4:
            description:
              - IPv4 address of the vCenter server.
            type: dict
            suboptions:
              value:
                description:
                  - The IPv4 address of the host.
                type: str
                required: true
              prefix_length:
                description:
                  - The prefix length of the network to which this host IPv4
                    address belongs.
                type: int
          ipv6:
            description:
              - IPv6 address of the vCenter server.
            type: dict
            suboptions:
              value:
                description:
                  - The IPv6 address of the host.
                type: str
                required: true
              prefix_length:
                description:
                  - The prefix length of the network to which this host IPv6
                    address belongs.
                type: int
          fqdn:
            description:
              - Fully qualified domain name of the vCenter server.
            type: dict
            suboptions:
              value:
                description:
                  - The fully qualified domain name of the host.
                type: str
                required: true
      credentials:
        description:
          - Credentials used to authenticate with vCenter (username and
            password).
        type: dict
        required: true
        suboptions:
          username:
            description:
              - Username for vCenter Server extension registration/unregistration.
            type: str
            required: true
          password:
            description:
              - Password for vCenter Server extension registration/unregistration.
            type: str
            required: true
          port:
            description:
              - vCenter port to connect for registering/unregistering extension.
            type: int
  wait:
    description:
      - Wait for the task to complete.
    type: bool
    default: true
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
- name: Compute non-migratable VMs for hosts
  nutanix.ncp.ntnx_compute_non_migratable_vms_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    cluster_ext_id: "00061de6-4a87-6b06-185b-ac1f6b6f97e2"
    hosts:
      - "af49a0bb-b3d7-41c0-b9c2-f4ca0e8763e9"
  register: result

- name: Compute non-migratable VMs with vCenter info
  nutanix.ncp.ntnx_compute_non_migratable_vms_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    cluster_ext_id: "00061de6-4a87-6b06-185b-ac1f6b6f97e2"
    hosts:
      - "af49a0bb-b3d7-41c0-b9c2-f4ca0e8763e9"
    vcenter_info:
      address:
        ipv4:
          value: "10.44.76.29"
          prefix_length: 32
      credentials:
        username: "administrator@vsphere.local"
        password: "vcenter-password"
        port: 443
  register: result
"""

RETURN = r"""
response:
  description:
    - Response for computing non-migratable VMs.
    - If C(wait) is true, it will contain the final task payload after completion.
    - If C(wait) is false, it will contain the initial task details.
  returned: always
  type: dict
  sample: {}
task_ext_id:
  description:
    - The external ID of the task.
  returned: always
  type: str
  sample: "ZXJnb24=:90458bc7-a12b-4616-ac66-562fdb00c209"
ext_id:
  description:
    - The external ID of the non-migratable VMs result when available from the
      completed task.
  returned: when wait is true and the result entity is present on the task
  type: str
  sample: "63311404-8b2e-4dbf-9e33-7848cc88d330"
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
  sample: "Api Exception raised while computing non-migratable VMs"
"""

import traceback  # noqa: E402
import warnings  # noqa: E402

from ansible.module_utils.basic import missing_required_lib  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_module_v4 import BaseModuleV4  # noqa: E402
from ..module_utils.v4.clusters_mgmt.api_client import (  # noqa: E402
    get_clusters_api_instance,
)
from ..module_utils.v4.constants import Tasks as TASK_CONSTANTS  # noqa: E402
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
    import ntnx_clustermgmt_py_client as sdk  # noqa: E402
except ImportError:
    from ..module_utils.v4.sdk_mock import mock_sdk as sdk  # noqa: E402

    SDK_IMP_ERROR = traceback.format_exc()

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
    ip_address_or_fqdn_spec = dict(
        ipv4=dict(
            type="dict",
            options=ipv4_spec,
            obj=sdk.IPv4Address,
        ),
        ipv6=dict(
            type="dict",
            options=ipv6_spec,
            obj=sdk.IPv6Address,
        ),
        fqdn=dict(
            type="dict",
            options=fqdn_spec,
            obj=sdk.FQDN,
        ),
    )
    vcenter_credentials_spec = dict(
        username=dict(type="str", required=True),
        password=dict(type="str", required=True, no_log=True),
        port=dict(type="int"),
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
        cluster_ext_id=dict(type="str"),
        hosts=dict(type="list", elements="str"),
        vcenter_info=dict(
            type="dict",
            options=vcenter_info_spec,
            obj=sdk.VcenterInfo,
        ),
    )
    return module_args


def compute_non_migratable_vms(module, result, api_instance):
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

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        return

    resp = None
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

    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        task_status = wait_for_completion(module, task_ext_id)
        result["response"] = strip_internal_attributes(task_status.to_dict())
        ext_id = get_entity_ext_id_from_task(
            task_status,
            rel=TASK_CONSTANTS.RelEntityType.NON_MIGRATABLE_VMS_RESULT,
        )
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
    result = {"changed": False, "response": None, "failed": False, "ext_id": None}
    api_instance = get_clusters_api_instance(module)
    compute_non_migratable_vms(module, result, api_instance)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
