#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2027, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_domain_manager_protection_plan_v2
short_description: Create, Update and Delete domain manager protection plan
version_added: "2.7.0"
description:
    - Create, Update and Delete domain manager protection plan for disaster
      recovery of Prism Central.
    - This module uses PC v4 APIs based SDKs
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to
      the user performing the operation.
    - >-
      B(Create domain manager protection plan) -
      Required Roles: Super Admin, Prism Admin, Domain Manager Admin
    - >-
      B(Update domain manager protection plan) -
      Required Roles: Super Admin, Prism Admin, Domain Manager Admin
    - >-
      B(Delete domain manager protection plan) -
      Required Roles: Super Admin, Prism Admin, Domain Manager Admin
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=prism)"
options:
    state:
        description:
            - State of the protection plan whether to create, update or
              delete.
            - If C(state) is present, it will create or update the
              protection plan.
            - If C(state) is set to C(present) and C(ext_id) is not
              provided then it will create a new protection plan.
            - If C(state) is set to C(present) and C(ext_id) is provided
              then it will update the protection plan.
            - If C(state) is absent, it will delete the protection plan.
        type: str
        choices: ['present', 'absent']
        default: present
    ext_id:
        description:
            - The external ID of the domain manager protection plan.
            - Required for update and delete operations.
        type: str
        required: false
    domain_manager_ext_id:
        description:
            - Domain manager external ID which needs to be protected.
        type: str
        required: false
    remote_location:
        description:
            - Model which contains the information about the remote site for
              domain manager protection plan.
        type: dict
        required: false
        suboptions:
            cluster_reference:
                description:
                    - Cluster reference of the remote cluster to be
                      connected.
                type: dict
                required: false
                suboptions:
                    ext_id:
                        description:
                            - Cluster External ID of a remote cluster.
                        type: str
                        required: true
                    name:
                        description:
                            - Name of the cluster.
                        type: str
                        required: false
    remote_site:
        description:
            - Remote site details.
        type: dict
        required: false
        suboptions:
            remote_cluster:
                description:
                    - Details of the remote cluster such as name and address.
                type: dict
                required: false
                suboptions:
                    name:
                        description:
                            - Cluster name of a remote cluster.
                        type: str
                        required: false
                    external_address:
                        description:
                            - External address of the cluster.
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
                    node_ip_addresses:
                        description:
                            - Node IP addresses of a registered cluster.
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
                    cluster_type:
                        description:
                            - Type of cluster.
                        type: str
                        choices:
                            - DOMAIN_MANAGER
                            - AOS
                            - WITNESS_SERVICE
                        required: false
                    cluster_version:
                        description:
                            - Version of the cluster.
                        type: str
                        required: false
                    port:
                        description:
                            - Port of the cluster exposed externally.
                        type: int
                        required: false
    failover_network_details:
        description:
            - Network details which will be used while failover of Prism
              Central using domain manager protection plan.
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
- name: Manage domain manager protection plan
  hosts: localhost
  gather_facts: false
  module_defaults:
    group/nutanix.ncp.ntnx:
      nutanix_host: "{{ ip }}"
      nutanix_username: "{{ username }}"
      nutanix_password: "{{ password }}"
      validate_certs: false
  tasks:
    - name: Create domain manager protection plan
      nutanix.ncp.ntnx_domain_manager_protection_plan_v2:
        state: present
        domain_manager_ext_id: "00000000-0000-0000-0000-000000000001"
        remote_location:
          cluster_reference:
            ext_id: "00000000-0000-0000-0000-000000000002"
            name: "remote-cluster"
        remote_site:
          remote_cluster:
            name: "remote-pc-cluster"
            external_address:
              ipv4:
                value: "10.0.0.10"
            cluster_type: "AOS"
            port: 9440
        failover_network_details:
          network_ext_id: "00000000-0000-0000-0000-000000000003"
          default_gateway:
            ipv4:
              value: "10.0.0.1"
          subnet_mask:
            ipv4:
              value: "255.255.255.0"
      register: result
      ignore_errors: true

    - name: Update domain manager protection plan
      nutanix.ncp.ntnx_domain_manager_protection_plan_v2:
        state: present
        ext_id: "11111111-1111-1111-1111-111111111111"
        domain_manager_ext_id: "00000000-0000-0000-0000-000000000001"
        remote_location:
          cluster_reference:
            ext_id: "00000000-0000-0000-0000-000000000002"
        remote_site:
          remote_cluster:
            name: "remote-pc-cluster-updated"
            external_address:
              ipv4:
                value: "10.0.0.11"
            cluster_type: "AOS"
        failover_network_details:
          network_ext_id: "00000000-0000-0000-0000-000000000003"
          default_gateway:
            ipv4:
              value: "10.0.0.1"
          subnet_mask:
            ipv4:
              value: "255.255.255.0"
      register: result
      ignore_errors: true

    - name: Delete domain manager protection plan
      nutanix.ncp.ntnx_domain_manager_protection_plan_v2:
        state: absent
        ext_id: "11111111-1111-1111-1111-111111111111"
      register: result
      ignore_errors: true
"""

RETURN = r"""
response:
  description:
      - Response for creating, updating, or deleting domain manager
        protection plan.
      - If C(wait) is true and the operation is Create or Update, it will
        contain the domain manager protection plan details.
      - If C(wait) is false or the operation is Delete, it will contain the
        task details.
  returned: always
  type: dict
  sample:
    {
        "domain_manager_ext_id": "00000000-0000-0000-0000-000000000001",
        "ext_id": "11111111-1111-1111-1111-111111111111",
        "failover_network_details": {
            "network_ext_id": "00000000-0000-0000-0000-000000000003"
        },
        "remote_location": {
            "ext_id": "00000000-0000-0000-0000-000000000002",
            "name": "remote-cluster"
        },
        "remote_site": {
            "cluster_type": "AOS",
            "external_address": {
                "ipv4": {
                    "value": "10.0.0.10"
                }
            },
            "name": "remote-pc-cluster",
            "port": 9440
        },
        "status": "SYNCED"
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

skipped:
  description: This indicates whether the task was skipped
  returned: when module is idempotent
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
  sample: "Api Exception raised while creating domain manager protection plan"
"""

import traceback  # noqa: E402
import warnings  # noqa: E402
from copy import deepcopy  # noqa: E402

from ansible.module_utils.basic import missing_required_lib  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_module_v4 import BaseModuleV4  # noqa: E402
from ..module_utils.v4.prism.helpers import (  # noqa: E402
    get_domain_manager_protection_plan,
)
from ..module_utils.v4.prism.pc_api_client import (  # noqa: E402
    get_domain_manager_protection_plan_api_instance,
    get_etag,
)
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

    cluster_reference_spec = dict(
        ext_id=dict(type="str", required=True),
        name=dict(type="str"),
    )

    remote_location_spec = dict(
        cluster_reference=dict(
            type="dict",
            options=cluster_reference_spec,
            obj=prism_sdk.ClusterReference,
        ),
    )

    remote_cluster_spec = dict(
        name=dict(type="str"),
        external_address=dict(
            type="dict",
            options=ip_address_or_fqdn_spec,
            obj=prism_sdk.IPAddressOrFQDN,
        ),
        node_ip_addresses=dict(
            type="list",
            elements="dict",
            options=ip_address_or_fqdn_spec,
            obj=prism_sdk.IPAddressOrFQDN,
        ),
        cluster_type=dict(
            type="str",
            choices=["DOMAIN_MANAGER", "AOS", "WITNESS_SERVICE"],
            obj=prism_sdk.ClusterType,
        ),
        cluster_version=dict(type="str"),
        port=dict(type="int"),
    )

    remote_site_spec = dict(
        remote_cluster=dict(
            type="dict",
            options=remote_cluster_spec,
            obj=prism_sdk.RemoteCluster,
        ),
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
        ext_id=dict(type="str"),
        domain_manager_ext_id=dict(type="str"),
        remote_location=dict(
            type="dict",
            options=remote_location_spec,
            obj={
                "cluster_reference": prism_sdk.ClusterReference,
            },
        ),
        remote_site=dict(
            type="dict",
            options=remote_site_spec,
            obj={"remote_cluster": prism_sdk.RemoteCluster},
        ),
        failover_network_details=dict(
            type="dict",
            options=failover_network_details_spec,
            obj=prism_sdk.FailoverNetworkDetails,
        ),
    )
    return module_args


def create_domain_manager_protection_plan(module, result, api_instance):
    validate_required_params(
        module, ["domain_manager_ext_id", "remote_location", "remote_site"]
    )
    sg = SpecGenerator(module)
    default_spec = prism_sdk.DomainManagerProtectionPlan()
    spec, err = sg.generate_spec(obj=default_spec)
    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed generating create domain manager protection plan spec", **result
        )

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        return

    resp = None
    try:
        resp = api_instance.create_domain_manager_protection_plan(body=spec)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while creating domain manager protection plan",
        )
    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        resp = wait_for_completion(module, task_ext_id)
        result["response"] = strip_internal_attributes(resp.to_dict())
        ext_id = get_entity_ext_id_from_task(resp)
        if ext_id:
            result["ext_id"] = ext_id
            resp = get_domain_manager_protection_plan(module, api_instance, ext_id)
            result["response"] = strip_internal_attributes(resp.to_dict())
        else:
            raise_api_exception(
                module=module,
                exception=Exception(
                    "Failed to get entity ext_id from task for Domain Manager Protection Plan"
                ),
                msg="Failed to get entity ext_id from task for Domain Manager Protection Plan",
            )
    result["changed"] = True


def check_domain_manager_protection_plan_idempotency(old_spec, update_spec):
    old_spec = strip_internal_attributes(old_spec)
    update_spec = strip_internal_attributes(update_spec)
    return old_spec == update_spec


def update_domain_manager_protection_plan(module, result, api_instance):
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id
    old_spec = get_domain_manager_protection_plan(module, api_instance, ext_id)
    etag = get_etag(data=old_spec)
    if not etag:
        return module.fail_json(
            "Unable to fetch etag for updating domain manager protection plan", **result
        )
    kwargs = {"if_match": etag}
    sg = SpecGenerator(module)
    update_spec, err = sg.generate_spec(obj=deepcopy(old_spec))
    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed generating update domain manager protection plan spec", **result
        )

    if module.check_mode:
        result["response"] = strip_internal_attributes(update_spec.to_dict())
        return

    if check_domain_manager_protection_plan_idempotency(
        old_spec.to_dict(), update_spec.to_dict()
    ):
        result["skipped"] = True
        module.exit_json(msg="Nothing to change.", **result)

    resp = None
    try:
        resp = api_instance.update_domain_manager_protection_plan_by_id(
            extId=ext_id, body=update_spec, **kwargs
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while updating domain manager protection plan",
        )
    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        wait_for_completion(module, task_ext_id)
        resp = get_domain_manager_protection_plan(module, api_instance, ext_id)
        result["response"] = strip_internal_attributes(resp.to_dict())
    result["changed"] = True


def delete_domain_manager_protection_plan(module, result, api_instance):
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id

    if module.check_mode:
        result["msg"] = (
            "Domain manager protection plan with ext_id:{0} will be deleted.".format(
                ext_id
            )
        )
        return

    current_spec = get_domain_manager_protection_plan(module, api_instance, ext_id)
    etag = get_etag(data=current_spec)
    if not etag:
        return module.fail_json(
            "Unable to fetch etag for deleting domain manager protection plan", **result
        )
    kwargs = {"if_match": etag}

    resp = None
    try:
        resp = api_instance.delete_domain_manager_protection_plan_by_id(
            extId=ext_id, **kwargs
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while deleting domain manager protection plan",
        )
    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        task_status = wait_for_completion(module, task_ext_id)
        result["response"] = strip_internal_attributes(task_status.to_dict())
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
    state = module.params.get("state")
    if state == "present":
        if module.params.get("ext_id"):
            update_domain_manager_protection_plan(module, result, api_instance)
        else:
            create_domain_manager_protection_plan(module, result, api_instance)
    else:
        delete_domain_manager_protection_plan(module, result, api_instance)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
