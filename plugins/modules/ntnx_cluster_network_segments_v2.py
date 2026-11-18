#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2027, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_cluster_network_segments_v2
short_description: Create or Delete cluster network segments
version_added: "2.7.0"
description:
    - Create or Delete network segments associated with a Nutanix cluster.
    - This module uses PC v4 APIs based SDKs
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the
      user performing the operation.
    - >-
      B(Create Cluster Network Segment) -
      Required Roles: Cluster Admin, Prism Admin, Super Admin
    - >-
      B(Delete Cluster Network Segment) -
      Required Roles: Cluster Admin, Prism Admin, Super Admin
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=clustermgmt)"
options:
  state:
    description:
      - If C(state) is C(present), create a network segment.
      - If C(state) is C(absent), delete the network segment identified by
        C(ext_id).
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
      - Network Segment UUID.
      - Required for delete operations.
    type: str
  name:
    description:
      - Network Segment name.
    type: str
  vlan_id:
    description:
      - Vlan ID for network segment.
    type: int
  mtu:
    description:
      - Maximum Transmission Unit for the network segment.
    type: int
  ip_pool_ext_id:
    description:
      - External ID (UUID) of the IP Pool resource.
    type: str
  network_segment_info:
    description:
      - Network segment information discriminator field for different segment
        types.
    type: dict
    suboptions:
      backplane_info:
        description:
          - Backplane network segment information.
        type: dict
        suboptions:
          ahv_network_backing:
            description:
              - AHV network backing configuration. This is optional, but at
                least one of ahvNetworkBacking or esxiNetworkBacking must be
                provided.
            type: dict
            suboptions:
              hypervisor_interface_backing:
                description:
                  - Hypervisor virtual switch backing for AHV.
                type: str
                required: true
          esxi_network_backing:
            description:
              - ESXi network backing configuration. This is optional, but at
                least one of ahvNetworkBacking or esxiNetworkBacking must be
                provided.
            type: dict
            suboptions:
              hypervisor_interface_backing:
                description:
                  - Backing for hypervisor interface of the network segment
                    (ESX-specific).
                type: str
                required: true
              cvm_interface_backing:
                description:
                  - Backing for CVM interface of the network segment
                    (ESX-specific).
                type: str
      service_info:
        description:
          - Service network segment information.
        type: dict
        suboptions:
          ahv_network_backing:
            description:
              - AHV network backing configuration. This is optional, but at
                least one of ahvNetworkBacking or esxiNetworkBacking must be
                provided.
            type: dict
            suboptions:
              hypervisor_interface_backing:
                description:
                  - Hypervisor virtual switch backing for AHV.
                type: str
                required: true
          esxi_network_backing:
            description:
              - ESXi network backing configuration. This is optional, but at
                least one of ahvNetworkBacking or esxiNetworkBacking must be
                provided.
            type: dict
            suboptions:
              hypervisor_interface_backing:
                description:
                  - Backing for hypervisor interface of the network segment
                    (ESX-specific).
                type: str
                required: true
              cvm_interface_backing:
                description:
                  - Backing for CVM interface of the network segment
                    (ESX-specific).
                type: str
          gateway:
            description:
              - Gateway IP address for the service network segment.
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
                      - The prefix length of the network to which this host
                        IPv4 address belongs.
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
                      - The prefix length of the network to which this host
                        IPv6 address belongs.
                    type: int
          service:
            description:
              - Service configuration which is using the network segment.
            type: dict
            suboptions:
              volumes_service:
                description:
                  - Volumes service configuration.
                type: dict
                suboptions:
                  client_subnets:
                    description:
                      - List of subnets of clients who need to connect to the
                        network.
                    type: list
                    elements: dict
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
                              - The prefix length of the network to which this
                                host IPv4 address belongs.
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
                              - The prefix length of the network to which this
                                host IPv6 address belongs.
                            type: int
                  virtual_ip_address:
                    description:
                      - Virtual IP for the service.
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
                              - The prefix length of the network to which this
                                host IPv4 address belongs.
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
                              - The prefix length of the network to which this
                                host IPv6 address belongs.
                            type: int
                  storage_protocol:
                    description:
                      - List of storage protocols used by the volumes service.
                    type: list
                    elements: str
                    choices:
                      - ISCSI
              dr_service:
                description:
                  - Disaster recovery service configuration.
                type: dict
                suboptions:
                  virtual_ip_address:
                    description:
                      - Virtual IP for the service.
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
                              - The prefix length of the network to which this
                                host IPv4 address belongs.
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
                              - The prefix length of the network to which this
                                host IPv6 address belongs.
                            type: int
                  is_stretched_network:
                    description:
                      - Indicates whether this is a stretched network
                        configuration. When enabled, the gateway is optional
                        for DR segmentation.
                    type: bool
              external_storage_service:
                description:
                  - External storage service configuration.
                type: dict
                suboptions:
                  routable_subnets:
                    description:
                      - Routable subnet for external storage.
                    type: list
                    elements: dict
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
                              - The prefix length of the network to which this
                                host IPv4 address belongs.
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
                              - The prefix length of the network to which this
                                host IPv6 address belongs.
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
- name: Create a backplane network segment
  nutanix.ncp.ntnx_cluster_network_segments_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: present
    cluster_ext_id: "00061de6-4a87-6b06-185b-ac1f6b6f97e2"
    name: "ansible-backplane-segment"
    vlan_id: 100
    mtu: 1500
    ip_pool_ext_id: "63311404-8b2e-4dbf-9e33-7848cc88d330"
    network_segment_info:
      backplane_info:
        ahv_network_backing:
          hypervisor_interface_backing: "vs0"
  register: result

- name: Create a volumes service network segment
  nutanix.ncp.ntnx_cluster_network_segments_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: present
    cluster_ext_id: "00061de6-4a87-6b06-185b-ac1f6b6f97e2"
    name: "ansible-volumes-segment"
    vlan_id: 200
    mtu: 1500
    network_segment_info:
      service_info:
        ahv_network_backing:
          hypervisor_interface_backing: "vs0"
        gateway:
          ipv4:
            value: "10.10.10.1"
            prefix_length: 32
        service:
          volumes_service:
            client_subnets:
              - ipv4:
                  value: "10.10.20.0"
                  prefix_length: 24
            virtual_ip_address:
              ipv4:
                value: "10.10.10.50"
                prefix_length: 32
            storage_protocol:
              - ISCSI
  register: result

- name: Delete a network segment
  nutanix.ncp.ntnx_cluster_network_segments_v2:
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
    - Response for network segment operations.
    - Network segment details if C(wait) is true for create.
    - Task details if C(wait) is false, or for delete.
  returned: always
  type: dict
  sample:
    {
        "ext_id": "ZXJnb24=:fc0f5074-4da9-5593-bfdc-a08c13df963d"
    }
task_ext_id:
  description:
    - The external ID of the task.
  returned: always
  type: str
  sample: "ZXJnb24=:90458bc7-a12b-4616-ac66-562fdb00c209"
ext_id:
  description:
    - The external ID of the network segment.
  returned: always
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
  returned: When there is an error or in check mode operation
  type: str
  sample: "Api Exception raised while creating network segment"
"""

import traceback  # noqa: E402
import warnings  # noqa: E402

from ansible.module_utils.basic import missing_required_lib  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_module_v4 import BaseModuleV4  # noqa: E402
from ..module_utils.v4.clusters_mgmt.api_client import (  # noqa: E402
    get_network_segments_api_instance,
)
from ..module_utils.v4.clusters_mgmt.helpers import get_network_segment  # noqa: E402
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
    ahv_backing_spec = dict(
        hypervisor_interface_backing=dict(type="str", required=True),
    )
    esxi_backing_spec = dict(
        hypervisor_interface_backing=dict(type="str", required=True),
        cvm_interface_backing=dict(type="str"),
    )
    volumes_service_spec = dict(
        client_subnets=dict(
            type="list",
            elements="dict",
            options=ip_address_spec,
            obj=sdk.IPAddress,
        ),
        virtual_ip_address=dict(
            type="dict",
            options=ip_address_spec,
            obj=sdk.IPAddress,
            required=True,
        ),
        storage_protocol=dict(
            type="list",
            elements="str",
            choices=["ISCSI"],
        ),
    )
    dr_service_spec = dict(
        virtual_ip_address=dict(
            type="dict",
            options=ip_address_spec,
            obj=sdk.IPAddress,
        ),
        is_stretched_network=dict(type="bool"),
    )
    external_storage_service_spec = dict(
        routable_subnets=dict(
            type="list",
            elements="dict",
            options=ip_address_spec,
            obj=sdk.IPAddress,
        ),
    )
    service_spec = dict(
        volumes_service=dict(
            type="dict",
            options=volumes_service_spec,
        ),
        dr_service=dict(
            type="dict",
            options=dr_service_spec,
        ),
        external_storage_service=dict(
            type="dict",
            options=external_storage_service_spec,
        ),
    )
    backplane_spec = dict(
        ahv_network_backing=dict(
            type="dict",
            options=ahv_backing_spec,
            obj=sdk.NetworkSegmentAhvBacking,
        ),
        esxi_network_backing=dict(
            type="dict",
            options=esxi_backing_spec,
            obj=sdk.NetworkSegmentEsxBacking,
        ),
    )
    service_info_spec = dict(
        ahv_network_backing=dict(
            type="dict",
            options=ahv_backing_spec,
            obj=sdk.NetworkSegmentAhvBacking,
        ),
        esxi_network_backing=dict(
            type="dict",
            options=esxi_backing_spec,
            obj=sdk.NetworkSegmentEsxBacking,
        ),
        gateway=dict(
            type="dict",
            options=ip_address_spec,
            obj=sdk.IPAddress,
        ),
        service=dict(
            type="dict",
            options=service_spec,
            obj={
                "volumes_service": sdk.NetworkSegmentVolumesService,
                "dr_service": sdk.NetworkSegmentDRService,
                "external_storage_service": sdk.NetworkSegmentExternalStorageService,
            },
            mutually_exclusive=[
                ("volumes_service", "dr_service", "external_storage_service")
            ],
        ),
    )
    network_segment_info_spec = dict(
        backplane_info=dict(
            type="dict",
            options=backplane_spec,
        ),
        service_info=dict(
            type="dict",
            options=service_info_spec,
        ),
    )
    module_args = dict(
        cluster_ext_id=dict(type="str"),
        ext_id=dict(type="str"),
        name=dict(type="str"),
        vlan_id=dict(type="int"),
        mtu=dict(type="int"),
        ip_pool_ext_id=dict(type="str"),
        network_segment_info=dict(
            type="dict",
            options=network_segment_info_spec,
            obj={
                "backplane_info": sdk.NetworkSegmentBackplaneInfo,
                "service_info": sdk.NetworkSegmentServiceInfo,
            },
            mutually_exclusive=[("backplane_info", "service_info")],
        ),
    )
    return module_args


def create_network_segment(module, result, api_instance):
    validate_required_params(module, ["cluster_ext_id", "name", "network_segment_info"])
    cluster_ext_id = module.params.get("cluster_ext_id")

    sg = SpecGenerator(module)
    default_spec = sdk.NetworkSegment()
    spec, err = sg.generate_spec(obj=default_spec)
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating create network segment spec", **result)

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        return

    resp = None
    try:
        resp = api_instance.create_network_segment_by_cluster_id(
            clusterExtId=cluster_ext_id, body=spec
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while creating network segment",
        )

    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        task_status = wait_for_completion(module, task_ext_id)
        ext_id = get_entity_ext_id_from_task(
            task_status, rel=TASK_CONSTANTS.RelEntityType.NETWORK_SEGMENT
        )
        if ext_id:
            resp = get_network_segment(module, api_instance, cluster_ext_id, ext_id)
            result["ext_id"] = ext_id
            result["response"] = strip_internal_attributes(resp.to_dict())
        else:
            raise_api_exception(
                module=module,
                exception=Exception(
                    "Failed to get entity ext_id from task for network segment"
                ),
                msg="Failed to get entity ext_id from task for network segment",
            )
    result["changed"] = True


def delete_network_segment(module, result, api_instance):
    validate_required_params(module, ["cluster_ext_id", "ext_id"])
    cluster_ext_id = module.params.get("cluster_ext_id")
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id

    if module.check_mode:
        result["msg"] = "Network segment with ext_id:{0} will be deleted.".format(
            ext_id
        )
        return

    try:
        resp = api_instance.delete_network_segment_by_id(
            clusterExtId=cluster_ext_id, extId=ext_id
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while deleting network segment",
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
            ("state", "present", ("name",)),
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
    if module.params.get("state") == "present":
        create_network_segment(module, result, api_instance)
    else:
        delete_network_segment(module, result, api_instance)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
