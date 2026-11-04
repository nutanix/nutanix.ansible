#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2027, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_cluster_ip_pools_v2
short_description: Create, Update, Delete cluster IP pools
version_added: "2.7.0"
description:
    - Create, Update, Delete IP pools associated with a Nutanix cluster.
    - This module uses PC v4 APIs based SDKs
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the
      user performing the operation.
    - >-
      B(Create Cluster IP Pool) -
      Required Roles: Cluster Admin, Prism Admin, Super Admin
    - >-
      B(Update Cluster IP Pool) -
      Required Roles: Cluster Admin, Prism Admin, Super Admin
    - >-
      B(Delete Cluster IP Pool) -
      Required Roles: Cluster Admin, Prism Admin, Super Admin
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=clustermgmt)"
options:
  state:
    description:
      - If C(state) is C(present) and C(ext_id) is not provided, create an IP pool.
      - If C(state) is C(present) and C(ext_id) is provided, update the IP pool.
      - If C(state) is C(absent), delete the IP pool identified by C(ext_id).
    type: str
    choices:
      - present
      - absent
    default: present
  cluster_ext_id:
    description:
      - Indicates the UUID of a cluster.
    type: str
  ext_id:
    description:
      - IP Pool UUID.
      - Required for update and delete operations.
    type: str
  name:
    description:
      - Name of the IP Pool.
    type: str
  ranges:
    description:
      - List of IP address ranges in the IP Pool.
    type: list
    elements: dict
    suboptions:
      start_address:
        description:
          - Starting IP address of the range.
        type: dict
        required: true
        suboptions:
          ipv4:
            description:
              - IPv4 address.
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
              - IPv6 address.
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
      end_address:
        description:
          - Ending IP address of the range.
        type: dict
        required: true
        suboptions:
          ipv4:
            description:
              - IPv4 address.
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
              - IPv6 address.
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
  netmask:
    description:
      - Netmask for IP Pool.
    type: dict
    suboptions:
      ipv4:
        description:
          - IPv4 address.
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
          - IPv6 address.
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
- name: Create a cluster IP pool
  nutanix.ncp.ntnx_cluster_ip_pools_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: present
    cluster_ext_id: "00061de6-4a87-6b06-185b-ac1f6b6f97e2"
    name: "ansible-ip-pool"
    ranges:
      - start_address:
          ipv4:
            value: "10.10.10.10"
            prefix_length: 32
        end_address:
          ipv4:
            value: "10.10.10.20"
            prefix_length: 32
    netmask:
      ipv4:
        value: "255.255.255.0"
        prefix_length: 32
  register: result

- name: Update a cluster IP pool
  nutanix.ncp.ntnx_cluster_ip_pools_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: present
    cluster_ext_id: "00061de6-4a87-6b06-185b-ac1f6b6f97e2"
    ext_id: "{{ result.ext_id }}"
    name: "ansible-ip-pool-updated"
    ranges:
      - start_address:
          ipv4:
            value: "10.10.10.30"
            prefix_length: 32
        end_address:
          ipv4:
            value: "10.10.10.40"
            prefix_length: 32
    netmask:
      ipv4:
        value: "255.255.255.0"
        prefix_length: 32
  register: result

- name: Delete a cluster IP pool
  nutanix.ncp.ntnx_cluster_ip_pools_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: absent
    cluster_ext_id: "00061de6-4a87-6b06-185b-ac1f6b6f97e2"
    ext_id: "{{ result.ext_id }}"
  register: result
"""

RETURN = r"""
response:
  description:
    - Response for IP pool operations.
    - IP pool details if C(wait) is true for create or update.
    - Task details if C(wait) is false, or for delete.
  returned: always
  type: dict
  sample:
    {
        "ext_id": "f8832e28-0bb5-4a5e-af73-ed65711b7522",
        "is_in_use": false,
        "links": null,
        "name": "ansible-ip-pool-updated",
        "netmask": {
            "ipv4": {
                "prefix_length": null,
                "value": "255.255.255.0"
            },
            "ipv6": null
        },
        "ranges": [
            {
                "end_address": {
                    "ipv4": {
                        "prefix_length": null,
                        "value": "10.77.88.40"
                    },
                    "ipv6": null
                },
                "start_address": {
                    "ipv4": {
                        "prefix_length": null,
                        "value": "10.77.88.30"
                    },
                    "ipv6": null
                }
            }
        ],
        "tenant_id": null,
        "type": "PE_IP_POOL"
    }
task_ext_id:
  description:
    - The external ID of the task.
  returned: always
  type: str
  sample: "ZXJnb24=:90458bc7-a12b-4616-ac66-562fdb00c209"
ext_id:
  description:
    - The external ID of the IP pool.
  returned: always
  type: str
  sample: "63311404-8b2e-4dbf-9e33-7848cc88d330"
changed:
  description: This indicates whether the task resulted in any changes
  returned: always
  type: bool
  sample: true
skipped:
  description: This indicates whether the task was skipped
  returned: always
  type: bool
  sample: false
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
  returned: When there is an error, module is idempotent or check mode
  type: str
  sample: "Api Exception raised while creating IP pool"
"""

import traceback  # noqa: E402
import warnings  # noqa: E402
from copy import deepcopy  # noqa: E402

from ansible.module_utils.basic import missing_required_lib  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_module_v4 import BaseModuleV4  # noqa: E402
from ..module_utils.v4.clusters_mgmt.api_client import (  # noqa: E402
    get_etag,
    get_network_segments_api_instance,
)
from ..module_utils.v4.clusters_mgmt.helpers import get_ip_pool  # noqa: E402
from ..module_utils.v4.constants import Tasks as TASK_CONSTANTS  # noqa: E402
from ..module_utils.v4.prism.tasks import (  # noqa: E402
    get_entity_ext_id_from_task,
    wait_for_completion,
)
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
    strip_read_only_fields,
    validate_required_params,
)

SDK_IMP_ERROR = None
try:
    import ntnx_clustermgmt_py_client as sdk  # noqa: E402
except ImportError:
    from ..module_utils.v4.sdk_mock import mock_sdk as sdk  # noqa: E402

    SDK_IMP_ERROR = traceback.format_exc()

warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")

_IP_POOL_READ_ONLY_FIELDS = (
    "type",
    "is_in_use",
    "ext_id",
    "links",
    "tenant_id",
)


def get_module_spec():
    ipv4_spec = dict(
        value=dict(type="str", required=True),
        prefix_length=dict(type="int"),
    )
    ipv6_spec = dict(
        value=dict(type="str", required=True),
        prefix_length=dict(type="int"),
    )
    ip_address_spec = dict(
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
    )
    ip_pool_range_spec = dict(
        start_address=dict(
            type="dict",
            options=ip_address_spec,
            obj=sdk.IPAddress,
            required=True,
        ),
        end_address=dict(
            type="dict",
            options=ip_address_spec,
            obj=sdk.IPAddress,
            required=True,
        ),
    )
    module_args = dict(
        cluster_ext_id=dict(type="str"),
        ext_id=dict(type="str"),
        name=dict(type="str"),
        ranges=dict(
            type="list",
            elements="dict",
            options=ip_pool_range_spec,
            obj=sdk.IpPoolRange,
        ),
        netmask=dict(
            type="dict",
            options=ip_address_spec,
            obj=sdk.IPAddress,
        ),
    )
    return module_args


def create_ip_pool(module, result, api_instance):
    validate_required_params(module, ["cluster_ext_id", "name", "ranges", "netmask"])
    cluster_ext_id = module.params.get("cluster_ext_id")

    sg = SpecGenerator(module)
    default_spec = sdk.IpPool()
    spec, err = sg.generate_spec(obj=default_spec)
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating create IP pool spec", **result)

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        return

    resp = None
    try:
        resp = api_instance.create_ip_pool_by_cluster_id(
            clusterExtId=cluster_ext_id, body=spec
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while creating IP pool",
        )

    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        task_status = wait_for_completion(module, task_ext_id)
        ext_id = get_entity_ext_id_from_task(
            task_status, rel=TASK_CONSTANTS.RelEntityType.IP_POOL
        )
        if ext_id:
            resp = get_ip_pool(module, api_instance, cluster_ext_id, ext_id)
            result["ext_id"] = ext_id
            result["response"] = strip_internal_attributes(resp.to_dict())
        else:
            raise_api_exception(
                module=module,
                exception=Exception(
                    "Failed to get entity ext_id from task for IP pool"
                ),
                msg="Failed to get entity ext_id from task for IP pool",
            )
    result["changed"] = True


def _normalize_ip_pool_dict(data):
    """Normalize IP pool dicts for idempotency comparison.

    The create/update APIs accept nested prefix_length on IP addresses, but
    GetIpPoolById returns those as null. Drop Nones and prefix_length so a
    no-op update is detected correctly.
    """
    if isinstance(data, dict):
        normalized = {}
        for key, val in data.items():
            if val is None or key == "prefix_length":
                continue
            normalized[key] = _normalize_ip_pool_dict(val)
        return normalized
    if isinstance(data, list):
        return [_normalize_ip_pool_dict(item) for item in data]
    return data


def check_ip_pool_idempotency(old_spec, update_spec):
    old_spec = _normalize_ip_pool_dict(strip_internal_attributes(old_spec))
    update_spec = _normalize_ip_pool_dict(strip_internal_attributes(update_spec))
    for field in _IP_POOL_READ_ONLY_FIELDS:
        old_spec.pop(field, None)
        update_spec.pop(field, None)
    return old_spec == update_spec


def update_ip_pool(module, result, api_instance):
    validate_required_params(module, ["cluster_ext_id", "ext_id"])
    cluster_ext_id = module.params.get("cluster_ext_id")
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id

    current_spec = get_ip_pool(module, api_instance, cluster_ext_id, ext_id)
    sg = SpecGenerator(module)
    update_spec, err = sg.generate_spec(obj=deepcopy(current_spec))
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating IP pool update spec", **result)

    strip_read_only_fields(update_spec, fields=_IP_POOL_READ_ONLY_FIELDS)

    if module.check_mode:
        result["response"] = strip_internal_attributes(update_spec.to_dict())
        return

    if check_ip_pool_idempotency(current_spec.to_dict(), update_spec.to_dict()):
        result["skipped"] = True
        module.exit_json(msg="Nothing to change.")

    etag = get_etag(data=current_spec)
    if not etag:
        return module.fail_json("Unable to fetch etag for updating IP pool", **result)
    kwargs = {"if_match": etag}

    try:
        resp = api_instance.update_ip_pool_by_id(
            clusterExtId=cluster_ext_id,
            extId=ext_id,
            body=update_spec,
            **kwargs,
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while updating IP pool",
        )

    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        wait_for_completion(module, task_ext_id)
        resp = get_ip_pool(module, api_instance, cluster_ext_id, ext_id)
        result["response"] = strip_internal_attributes(resp.to_dict())
    result["changed"] = True


def delete_ip_pool(module, result, api_instance):
    validate_required_params(module, ["cluster_ext_id", "ext_id"])
    cluster_ext_id = module.params.get("cluster_ext_id")
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id

    if module.check_mode:
        result["msg"] = "IP pool with ext_id:{0} will be deleted.".format(ext_id)
        return

    try:
        resp = api_instance.delete_ip_pool_by_id(
            clusterExtId=cluster_ext_id, extId=ext_id
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while deleting IP pool",
        )

    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        resp = wait_for_completion(module, task_ext_id)
        result["response"] = strip_internal_attributes(resp.to_dict())
    result["changed"] = True


def run_module():
    module = BaseModuleV4(
        argument_spec=get_module_spec(),
        supports_check_mode=True,
        required_if=[
            ("state", "present", ("name", "ext_id"), True),
            ("state", "absent", ("ext_id",)),
        ],
    )
    if SDK_IMP_ERROR:
        module.fail_json(
            msg=missing_required_lib("ntnx_clustermgmt_py_client"),
            exception=SDK_IMP_ERROR,
        )

    remove_param_with_none_value(module.params)
    result = {"changed": False, "response": None, "failed": False, "ext_id": None}
    api_instance = get_network_segments_api_instance(module)
    state = module.params.get("state")
    if state == "present":
        if module.params.get("ext_id"):
            update_ip_pool(module, result, api_instance)
        else:
            create_ip_pool(module, result, api_instance)
    else:
        delete_ip_pool(module, result, api_instance)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
