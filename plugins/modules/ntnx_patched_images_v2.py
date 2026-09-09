#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_patched_images_v2
short_description: Create and delete Life Cycle Management (LCM) patched images
version_added: 2.7.0
description:
  - This module allows you to create and delete patched hypervisor or host OS
    images in Nutanix Life Cycle Management (LCM).
  - A patched image is a customized hypervisor or host OS image that combines a
    base image with patches for specific node deployments.
  - If C(state) is C(present) and C(ext_id) is not provided, a patched image is created.
  - If C(state) is C(absent) and C(ext_id) is provided, the patched image is deleted.
  - This module uses v4 APIs based SDKs.
notes:
  - The patched images APIs are part of the Life Cycle Management (LCM) namespace
    and are served by Foundation Central (FCVM), NOT by Prism Central (PC).
    Set C(nutanix_host) to the Foundation Central (FCVM) endpoint.
  - Creating a patched image requires an already claimed node (referenced through
    C(claim_token_ext_id)) and an uploaded local host image referenced by
    C(image_details.ext_id).
  - The patched ISO must be reachable from the cluster through C(patched_iso_url)
    and its C(patched_iso_sha256_checksum) must match the ISO content.
  - This module requires the appropriate administrative role on Foundation Central
    to be assigned to the user performing the operation.
  - "Ref: U(https://developers.nutanix.com/api-reference?namespace=lifecycle)"
options:
  state:
    description:
      - If C(state) is set to C(present) and C(ext_id) is not provided then the operation will create a patched image.
      - If C(state) is set to C(absent) and C(ext_id) is provided then the operation will delete the patched image.
    type: str
    required: false
    choices:
      - present
      - absent
    default: present
  ext_id:
    description:
      - The external ID of the patched image.
      - Required for the delete operation.
    type: str
    required: false
  host_type:
    description:
      - Type of the host installed or to be installed on the node.
      - Required for the create operation.
    type: str
    required: false
    choices:
      - AHV
      - ESX
  name:
    description:
      - Patched image name.
      - Required for the create operation.
      - Minimum 1 character, maximum 64 characters.
    type: str
    required: false
  version:
    description:
      - Version of the base hypervisor or host OS image used for patching.
    type: str
    required: false
  image_details:
    description:
      - Details of the local host image used for patching.
      - Required for the create operation.
    type: dict
    required: false
    suboptions:
      ext_id:
        description:
          - External ID of the uploaded local host image.
        type: str
        required: true
  claim_token_ext_id:
    description:
      - External ID of the claim token used in the patched image.
      - Required for the create operation.
    type: str
    required: false
  patched_iso_url:
    description:
      - URL for downloading the patched image.
      - Required for the create operation.
    type: str
    required: false
  patched_iso_sha256_checksum:
    description:
      - SHA-256 checksum of the patched image.
      - Required for the create operation.
    type: str
    required: false
  node_configurations:
    description:
      - List of node configurations used for patching the image.
      - Required for the create operation.
    type: list
    elements: dict
    required: false
    suboptions:
      node_ext_id:
        description:
          - External ID of the node.
        type: str
        required: false
      host_configuration:
        description:
          - Configuration of the hypervisor or host OS used for patching.
        type: dict
        required: false
        suboptions:
          network_details:
            description:
              - Network details of the host used for patching.
            type: dict
            required: false
            suboptions:
              management:
                description:
                  - Management network configuration of the host.
                type: dict
                required: false
                suboptions:
                  mtu_bytes:
                    description:
                      - Maximum transmission unit of the management network.
                    type: int
                    required: false
                  vlan_id:
                    description:
                      - VLAN ID of the management network.
                    type: int
                    required: false
                  ip:
                    description:
                      - IP address of the management network.
                    type: dict
                    required: false
                    suboptions:
                      ipv4:
                        description:
                          - IPv4 address of the management network.
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
                              - Prefix length of the IPv4 address.
                            type: int
                            required: false
                            default: 32
                      ipv6:
                        description:
                          - IPv6 address of the management network.
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
                              - Prefix length of the IPv6 address.
                            type: int
                            required: false
                            default: 128
                  gateway:
                    description:
                      - Gateway IP address of the management network.
                    type: dict
                    required: false
                    suboptions:
                      ipv4:
                        description:
                          - IPv4 gateway of the management network.
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
                              - Prefix length of the IPv4 address.
                            type: int
                            required: false
                            default: 32
                      ipv6:
                        description:
                          - IPv6 gateway of the management network.
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
                              - Prefix length of the IPv6 address.
                            type: int
                            required: false
                            default: 128
                  bond_settings:
                    description:
                      - Bond configuration of the management network.
                    type: dict
                    required: false
                    suboptions:
                      bond_config:
                        description:
                          - Bond configuration type.
                          - Provide exactly one of C(active_backup_bond) or C(lacp_bond).
                        type: dict
                        required: false
                        suboptions:
                          active_backup_bond:
                            description:
                              - Active-backup bond configuration.
                              - Mutually exclusive with C(lacp_bond).
                            type: dict
                            required: false
                            suboptions:
                              nics:
                                description:
                                  - NICs participating in the bond.
                                type: dict
                                required: false
                                suboptions:
                                  mac_address:
                                    description:
                                      - List of MAC addresses of the NICs in the bond.
                                    type: list
                                    elements: str
                                    required: false
                          lacp_bond:
                            description:
                              - LACP bond configuration.
                              - Mutually exclusive with C(active_backup_bond).
                            type: dict
                            required: false
                            suboptions:
                              lacp_settings:
                                description:
                                  - LACP settings of the bond.
                                type: dict
                                required: false
                                suboptions:
                                  rate:
                                    description:
                                      - Rate at which LACP control packets are sent.
                                    type: str
                                    required: false
                                    choices:
                                      - SLOW
                                      - FAST
                              nics:
                                description:
                                  - NICs participating in the bond.
                                type: dict
                                required: false
                                suboptions:
                                  mac_address:
                                    description:
                                      - List of MAC addresses of the NICs in the bond.
                                    type: list
                                    elements: str
                                    required: false
          hostname:
            description:
              - Hostname of the hypervisor or host OS.
            type: str
            required: false
          nameservers:
            description:
              - List of nameserver IP addresses to be used by the host.
            type: list
            elements: dict
            required: false
            suboptions:
              ipv4:
                description:
                  - IPv4 address of the nameserver.
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
                      - Prefix length of the IPv4 address.
                    type: int
                    required: false
                    default: 32
              ipv6:
                description:
                  - IPv6 address of the nameserver.
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
                      - Prefix length of the IPv6 address.
                    type: int
                    required: false
                    default: 128
          ntpservers:
            description:
              - List of NTP server IP addresses or FQDNs to be used by the host.
            type: list
            elements: dict
            required: false
            suboptions:
              ipv4:
                description:
                  - IPv4 address of the NTP server.
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
                      - Prefix length of the IPv4 address.
                    type: int
                    required: false
                    default: 32
              ipv6:
                description:
                  - IPv6 address of the NTP server.
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
                      - Prefix length of the IPv6 address.
                    type: int
                    required: false
                    default: 128
              fqdn:
                description:
                  - Fully qualified domain name of the NTP server.
                type: dict
                required: false
                suboptions:
                  value:
                    description:
                      - The fully qualified domain name value.
                    type: str
                    required: false
  owner_ext_id:
    description:
      - External ID of the owner of the patched image.
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
- name: Create AHV patched image
  nutanix.ncp.ntnx_patched_images_v2:
    nutanix_host: "{{ fcvm_ip }}"
    nutanix_username: "{{ fcvm_username }}"
    nutanix_password: "{{ fcvm_password }}"
    validate_certs: false
    state: present
    host_type: "AHV"
    name: "ahv_patched_image_ansible"
    version: "10.0"
    claim_token_ext_id: "5f1b1b3a-1b3a-4b3a-8b3a-1b3a4b3a8b3a"
    patched_iso_url: "https://example.com/isos/ahv-patched.iso"
    patched_iso_sha256_checksum: "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
    image_details:
      ext_id: "b6c8f0a2-4d1e-4f0a-9c1a-2d3e4f5a6b7c"
    owner_ext_id: "a1b2c3d4-e5f6-4a5b-8c9d-0e1f2a3b4c5d"
    node_configurations:
      - node_ext_id: "c1d2e3f4-a5b6-4c7d-8e9f-0a1b2c3d4e5f"
        host_configuration:
          hostname: "ahv-host-01"
          network_details:
            management:
              mtu_bytes: 1500
              vlan_id: 1
              ip:
                ipv4:
                  value: "10.0.0.11"
                  prefix_length: 24
              gateway:
                ipv4:
                  value: "10.0.0.1"
                  prefix_length: 24
              bond_settings:
                bond_config:
                  active_backup_bond:
                    nics:
                      mac_address:
                        - "aa:bb:cc:dd:ee:01"
          nameservers:
            - ipv4:
                value: "8.8.8.8"
          ntpservers:
            - fqdn:
                value: "pool.ntp.org"
  register: result
  ignore_errors: true

- name: Delete patched image
  nutanix.ncp.ntnx_patched_images_v2:
    nutanix_host: "{{ fcvm_ip }}"
    nutanix_username: "{{ fcvm_username }}"
    nutanix_password: "{{ fcvm_password }}"
    validate_certs: false
    state: absent
    ext_id: "b6c8f0a2-4d1e-4f0a-9c1a-2d3e4f5a6b7c"
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
  description:
    - Response for creating or deleting the patched image.
    - If the operation is create and C(wait) is true, it returns the patched image details.
    - If the operation is create and C(wait) is false, it returns the task details.
    - If the operation is delete, it returns the task details.
  returned: always
  type: dict
  sample:
    {
      "claim_token_ext_id": "5f1b1b3a-1b3a-4b3a-8b3a-1b3a4b3a8b3a",
      "created_time": "2026-09-09T04:38:00.000000+00:00",
      "ext_id": "b6c8f0a2-4d1e-4f0a-9c1a-2d3e4f5a6b7c",
      "host_type": "AHV",
      "image_details": {
        "ext_id": "b6c8f0a2-4d1e-4f0a-9c1a-2d3e4f5a6b7c"
      },
      "links": null,
      "name": "ahv_patched_image_ansible",
      "node_configurations": [
        {
          "host_configuration": {
            "hostname": "ahv-host-01"
          },
          "node_ext_id": "c1d2e3f4-a5b6-4c7d-8e9f-0a1b2c3d4e5f"
        }
      ],
      "owner_ext_id": "a1b2c3d4-e5f6-4a5b-8c9d-0e1f2a3b4c5d",
      "patched_iso_sha256_checksum": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
      "patched_iso_url": "https://example.com/isos/ahv-patched.iso",
      "tenant_id": null,
      "version": "10.0"
    }

task_ext_id:
  description:
    - The external ID of the task.
  returned: always
  type: str
  sample: "ZXJnb24=:90458bc7-a12b-4616-ac66-562fdb00c209"

ext_id:
  description:
    - The external ID of the patched image.
  returned: always
  type: str
  sample: "b6c8f0a2-4d1e-4f0a-9c1a-2d3e4f5a6b7c"

changed:
  description: This indicates whether the task resulted in any changes.
  returned: always
  type: bool
  sample: true

skipped:
  description: This indicates whether the operation was skipped.
  returned: when applicable
  type: bool
  sample: false

error:
  description: This indicates the error message if any error occurred.
  returned: When an error occurs
  type: str

failed:
  description: This indicates whether the task failed.
  returned: when something fails
  type: bool
  sample: false

msg:
  description: This indicates the message if any message occurred.
  returned: When there is an error, or in check mode (delete operation)
  type: str
  sample: "Patched image with ext_id:b6c8f0a2-4d1e-4f0a-9c1a-2d3e4f5a6b7c will be deleted."
"""

import traceback  # noqa: E402
import warnings  # noqa: E402

from ansible.module_utils.basic import missing_required_lib  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_module_v4 import BaseModuleV4  # noqa: E402
from ..module_utils.v4.constants import Tasks as TASK_CONSTANTS  # noqa: E402
from ..module_utils.v4.lcm.api_client import (  # noqa: E402
    get_patched_images_api_instance,
)
from ..module_utils.v4.lcm.helpers import get_patched_image  # noqa: E402
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
    import ntnx_lifecycle_py_client as lifecycle_sdk  # noqa: E402
except ImportError:

    from ..module_utils.v4.sdk_mock import mock_sdk as lifecycle_sdk  # noqa: E402

    SDK_IMP_ERROR = traceback.format_exc()

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():

    ipv4_address_spec = dict(
        value=dict(type="str", required=True),
        prefix_length=dict(type="int", required=False, default=32),
    )

    ipv6_address_spec = dict(
        value=dict(type="str", required=True),
        prefix_length=dict(type="int", required=False, default=128),
    )

    fqdn_spec = dict(
        value=dict(type="str", required=False),
    )

    ip_address_spec = dict(
        ipv4=dict(
            type="dict",
            options=ipv4_address_spec,
            required=False,
            obj=lifecycle_sdk.IPv4Address,
        ),
        ipv6=dict(
            type="dict",
            options=ipv6_address_spec,
            required=False,
            obj=lifecycle_sdk.IPv6Address,
        ),
    )

    ip_address_or_fqdn_spec = dict(
        ipv4=dict(
            type="dict",
            options=ipv4_address_spec,
            required=False,
            obj=lifecycle_sdk.IPv4Address,
        ),
        ipv6=dict(
            type="dict",
            options=ipv6_address_spec,
            required=False,
            obj=lifecycle_sdk.IPv6Address,
        ),
        fqdn=dict(
            type="dict",
            options=fqdn_spec,
            required=False,
            obj=lifecycle_sdk.FQDN,
        ),
    )

    nics_spec = dict(
        mac_address=dict(type="list", elements="str", required=False),
    )

    lacp_settings_spec = dict(
        rate=dict(type="str", required=False, choices=["SLOW", "FAST"]),
    )

    active_backup_bond_spec = dict(
        nics=dict(
            type="dict",
            options=nics_spec,
            required=False,
            obj=lifecycle_sdk.Nics,
        ),
    )

    lacp_bond_spec = dict(
        lacp_settings=dict(
            type="dict",
            options=lacp_settings_spec,
            required=False,
            obj=lifecycle_sdk.LacpSettings,
        ),
        nics=dict(
            type="dict",
            options=nics_spec,
            required=False,
            obj=lifecycle_sdk.Nics,
        ),
    )

    bond_config_spec = dict(
        active_backup_bond=dict(
            type="dict",
            options=active_backup_bond_spec,
            required=False,
        ),
        lacp_bond=dict(
            type="dict",
            options=lacp_bond_spec,
            required=False,
        ),
    )

    bond_settings_spec = dict(
        bond_config=dict(
            type="dict",
            options=bond_config_spec,
            required=False,
            obj=dict(
                active_backup_bond=lifecycle_sdk.ActiveBackupBond,
                lacp_bond=lifecycle_sdk.LacpBond,
            ),
        ),
    )

    management_network_spec = dict(
        mtu_bytes=dict(type="int", required=False),
        vlan_id=dict(type="int", required=False),
        ip=dict(
            type="dict",
            options=ip_address_spec,
            required=False,
            obj=lifecycle_sdk.IPAddress,
        ),
        gateway=dict(
            type="dict",
            options=ip_address_spec,
            required=False,
            obj=lifecycle_sdk.IPAddress,
        ),
        bond_settings=dict(
            type="dict",
            options=bond_settings_spec,
            required=False,
            obj=lifecycle_sdk.BondSettings,
        ),
    )

    host_network_details_spec = dict(
        management=dict(
            type="dict",
            options=management_network_spec,
            required=False,
            obj=lifecycle_sdk.ManagementNetwork,
        ),
    )

    host_configuration_spec = dict(
        network_details=dict(
            type="dict",
            options=host_network_details_spec,
            required=False,
            obj=lifecycle_sdk.HostNetworkDetails,
        ),
        hostname=dict(type="str", required=False),
        nameservers=dict(
            type="list",
            elements="dict",
            options=ip_address_spec,
            required=False,
            obj=lifecycle_sdk.IPAddress,
        ),
        ntpservers=dict(
            type="list",
            elements="dict",
            options=ip_address_or_fqdn_spec,
            required=False,
            obj=lifecycle_sdk.IPAddressOrFQDN,
        ),
    )

    node_configuration_spec = dict(
        node_ext_id=dict(type="str", required=False),
        host_configuration=dict(
            type="dict",
            options=host_configuration_spec,
            required=False,
            obj=lifecycle_sdk.HostConfiguration,
        ),
    )

    image_details_spec = dict(
        ext_id=dict(type="str", required=True),
    )

    module_args = dict(
        ext_id=dict(type="str"),
        host_type=dict(
            type="str",
            choices=["AHV", "ESX"],
            obj=lifecycle_sdk.HostType,
        ),
        name=dict(type="str"),
        version=dict(type="str"),
        image_details=dict(
            type="dict",
            options=image_details_spec,
            obj=lifecycle_sdk.LocalHostImageDetails,
        ),
        claim_token_ext_id=dict(type="str"),
        patched_iso_url=dict(type="str"),
        patched_iso_sha256_checksum=dict(type="str"),
        node_configurations=dict(
            type="list",
            elements="dict",
            options=node_configuration_spec,
            obj=lifecycle_sdk.NodeConfiguration,
        ),
        owner_ext_id=dict(type="str"),
    )

    return module_args


def create_patched_images(module, result, api_instance):
    validate_required_params(
        module,
        [
            "host_type",
            "name",
            "image_details",
            "claim_token_ext_id",
            "patched_iso_url",
            "patched_iso_sha256_checksum",
            "node_configurations",
        ],
    )

    sg = SpecGenerator(module)
    default_spec = lifecycle_sdk.PatchedImage()
    spec, err = sg.generate_spec(obj=default_spec)
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating create patched image spec", **result)

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        return

    resp = None
    try:
        resp = api_instance.create_patched_image(body=spec)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while creating patched image",
        )

    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        task_status = wait_for_completion(module, task_ext_id)
        result["response"] = strip_internal_attributes(task_status.to_dict())
        ext_id = get_entity_ext_id_from_task(
            task_status, rel=TASK_CONSTANTS.RelEntityType.PATCHED_IMAGE
        )
        if ext_id:
            result["ext_id"] = ext_id
            resp = get_patched_image(module, api_instance, ext_id)
            result["response"] = strip_internal_attributes(resp.to_dict())
    result["changed"] = True


def delete_patched_images(module, result, api_instance):
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id

    if module.check_mode:
        result["msg"] = "Patched image with ext_id:{0} will be deleted.".format(ext_id)
        return

    resp = None
    try:
        resp = api_instance.delete_patched_image_by_id(extId=ext_id)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while deleting patched image with ext_id: {0}".format(
                ext_id
            ),
        )

    task_ext_id = getattr(getattr(resp, "data", None), "ext_id", None)
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
            ("state", "present", ("name",)),
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
    api_instance = get_patched_images_api_instance(module)
    state = module.params.get("state")
    if state == "present":
        create_patched_images(module, result, api_instance)
    else:
        delete_patched_images(module, result, api_instance)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
