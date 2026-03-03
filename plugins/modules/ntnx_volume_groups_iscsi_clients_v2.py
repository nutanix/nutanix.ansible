#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2024, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_volume_groups_iscsi_clients_v2
short_description: Manage Nutanix volume groups iscsi clients in Nutanix PC.
description:
    - This module allows you to attach & detach ISCSI clients to/from a volume group in a Nutanix cluster.
    - This module uses PC v4 APIs based SDKs
version_added: "2.0.0"
author:
 - Pradeepsingh Bhati (@bhati-pradeep)
options:
    state:
        description:
            - Specify state
            - If C(state) is set to C(present) then module will attach iscsi client to volume group.
            - If C(state) is set to C(present) then module will detach iscsi client to volume group.
        choices:
            - present
            - absent
        type: str
        default: present
    wait:
        description: Wait for the operation to complete.
        type: bool
        required: false
        default: True
    ext_id:
        description:
            - The external ID of the iscsi client.
            - Its required for delete.
        type: str
        required: false
    volume_group_ext_id:
        description:
            - The external ID of the volume group.
        type: str
        required: true
    iscsi_initiator_name:
        description:
            - iSCSI initiator name.
            - During the attach operation, exactly one of iscsiInitiatorName and iscsiInitiatorNetworkId must be specified.
            - This field is immutable.
        type: str
        required: false
    client_secret:
        description:
            - iSCSI initiator client secret in case of CHAP authentication.
            - This field should not be provided in case the authentication type is not set to CHAP.
        type: str
        required: false
    enabled_authentications:
        description:
            - The authentication type enabled for the Volume Group.
            - If omitted, authentication is not configured for attachment.
            - If this is set to CHAP, the target/client secret must be provided.
            - This is an optional field.
        required: false
        choices:
            - CHAP
            - NONE
        type: str
        default: NONE
    num_virtual_targets:
        description:
            - Number of virtual targets generated for the iSCSI target. This field is immutable.
        type: int
        required: false
    attachment_site:
        description:
            - The site where the Volume Group attach operation should be processed.
            - This is an optional field.
            - This field may only be set if Metro DR has been configured for this Volume Group.
        required: false
        type: str
        choices:
            - SECONDARY
            - PRIMARY
    iscsi_initiator_network_id:
        description:
            - An unique address that identifies a device on the internet or a local network in IPv4/IPv6 format or a Fully Qualified Domain Name
            - Mutually exclusive with C(iscsi_initiator_name).
        required: false
        type: dict
        suboptions:
            ipv4:
                description:
                    - IPv4 address of the initiator.
                type: dict
                required: false
                suboptions:
                    value:
                        description:
                            - The value of the IPv4 address.
                        type: str
                        required: true
            ipv6:
                description:
                    - IPv6 address of the initiator.
                type: dict
                required: false
                suboptions:
                    value:
                        description:
                            - The value of the IPv6 address.
                        type: str
                        required: true
            fqdn:
                description:
                    - fqdn address of the initiator.
                type: dict
                required: false
                suboptions:
                    value:
                        description:
                            - The value of the fqdn address.
                        type: str
                        required: true

extends_documentation_fragment:
    - nutanix.ncp.ntnx_credentials
    - nutanix.ncp.ntnx_operations_v2
    - nutanix.ncp.ntnx_logger
    - nutanix.ncp.ntnx_proxy_v2
"""

EXAMPLES = r"""
- name: Attach iscsi client to VG using initiator name
  nutanix.ncp.ntnx_volume_groups_iscsi_clients_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    state: "present"
    volume_group_ext_id: 0005b6b1-0b3b-4b3b-8b3b-0b3b4b3b4b35
    iscsi_initiator_name: iqn-1-05.com.microsoft:win-1234
    num_virtual_targets: 32
  register: result

- name: Attach using ipv4 address
  nutanix.ncp.ntnx_volume_groups_iscsi_clients_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    state: "present"
    volume_group_ext_id: 0005b6b1-0b3b-4b3b-8b3b-0b3b4b3b4b35
    num_virtual_targets: 32
    enabled_authentications: CHAP
    client_secret: "Nutanix.1234455"
    attachment_site: "PRIMARY"
    iscsi_initiator_network_id:
      ipv4:
        value: "0.0.0.0"
  register: result

- name: Detach client from VG
  nutanix.ncp.ntnx_volume_groups_iscsi_clients_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    volume_group_ext_id: 0005b6b1-0b3b-4b3b-8b3b-0b3b4b3b4b35
    ext_id: 9905b6b1-0b3b-4b3b-8b3b-0b3b4b3b4b35
    state: absent
  register: result
"""

RETURN = r"""
response:
    description:
       - Task details
    type: dict
    returned: always
    sample:  {
            "cluster_ext_ids": [
                "00061663-9fa0-28ca-185b-ac1f6b6f97e2"
            ],
            "completed_time": "2024-05-20T05:19:00.229645+00:00",
            "completion_details": null,
            "created_time": "2024-05-20T05:19:00.095273+00:00",
            "entities_affected": [
                {
                    "ext_id": "aea43b5c-ae4d-4b60-934b-f8f581275dec",
                    "rel": "volumes:config:iscsi-client"
                },
                {
                    "ext_id": "11ac5593-c9cf-403d-641c-3bf76eff2193",
                    "rel": "volumes:config:volume-group"
                }
            ],
            "error_messages": null,
            "ext_id": "ZXJnb24=:e7b6ff28-e5f1-4316-82e8-96368cc851d7",
            "is_cancelable": false,
            "last_updated_time": "2024-05-20T05:19:00.229642+00:00",
            "legacy_error_message": null,
            "operation": "VolumeGroupAttachExternal",
            "operation_description": "Volume group attach to iSCSI Client",
            "owned_by": {
                "ext_id": "00000000-0000-0000-0000-000000000000",
                "name": "admin"
            },
            "parent_task": null,
            "progress_percentage": 100,
            "started_time": "2024-05-20T05:19:00.122260+00:00",
            "status": "SUCCEEDED",
            "sub_steps": null,
            "sub_tasks": null,
            "warnings": null
        }
ext_id:
    description: Iscsi client external ID.
    type: str
    returned: always
    sample: "0005b6b1-0b3b-4b3b-8b3b-0b3b4b3b4b3b"
volume_group_ext_id:
    description: Volume group external ID.
    type: str
    returned: always
    sample: "0005b6b1-0b3b-4b3b-8b3b-0b3b4b3b4b3b"
task_ext_id:
    description: The task external ID.
    type: str
    returned: always
    sample: "0005b6b1-0b3b-4b3b-8b3b-0b3b4b3b4b3b"
msg:
    description: This indicates the message if any message occurred
    returned: When there is an error
    type: str
    sample: "Failed generating attach ISCSI client to volume group spec"
error:
    description: The error message if any.
    type: str
    returned: when error occurs
    sample: "Api Exception raised while attaching ISCSI client to volume group"
changed:
    description: Indicates whether the resource has changed.
    type: bool
    returned: always
    sample: true
"""
import traceback  # noqa: E402
import warnings  # noqa: E402

from ansible.module_utils.basic import missing_required_lib  # noqa: E402

from ..module_utils.base_module import BaseModule  # noqa: E402
from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.constants import Tasks as TASK_CONSTANTS  # noqa: E402
from ..module_utils.v4.prism.tasks import (  # noqa: E402
    get_entity_ext_id_from_task,
    wait_for_completion,
)
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
)
from ..module_utils.v4.volumes.api_client import (  # noqa: E402
    get_etag,
    get_vg_api_instance,
)
from ..module_utils.v4.volumes.helpers import get_volume_group  # noqa: E402

SDK_IMP_ERROR = None
try:
    import ntnx_volumes_py_client as volumes_sdk  # noqa: E402
except ImportError:

    from ..module_utils.v4.sdk_mock import mock_sdk as volumes_sdk  # noqa: E402

    SDK_IMP_ERROR = traceback.format_exc()

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    address = dict(
        value=dict(type="str", required=True),
    )
    iscsi_initiator_network_id = dict(
        ipv4=dict(type="dict", options=address, obj=volumes_sdk.IPv4Address),
        ipv6=dict(type="dict", options=address, obj=volumes_sdk.IPv6Address),
        fqdn=dict(type="dict", options=address, obj=volumes_sdk.FQDN),
    )
    module_args = dict(
        volume_group_ext_id=dict(type="str", required=True),
        ext_id=dict(type="str", required=False),
        iscsi_initiator_name=dict(type="str"),
        client_secret=dict(type="str", no_log=True),
        enabled_authentications=dict(
            type="str", choices=["CHAP", "NONE"], default="NONE"
        ),
        num_virtual_targets=dict(type="int"),
        attachment_site=dict(type="str", choices=["SECONDARY", "PRIMARY"]),
        iscsi_initiator_network_id=dict(
            type="dict",
            options=iscsi_initiator_network_id,
            obj=volumes_sdk.IPAddressOrFQDN,
        ),
    )

    return module_args


def get_iscsi_client(module, api_instance, ext_id):
    try:
        return api_instance.get_iscsi_client_by_id(extId=ext_id).data
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching Volume group disk info using ext_id",
        )


def attach_iscsi_client(module, result):
    vgs = get_vg_api_instance(module)
    volume_group_ext_id = module.params.get("volume_group_ext_id")
    result["volume_group_ext_id"] = volume_group_ext_id

    sg = SpecGenerator(module)
    default_spec = volumes_sdk.IscsiClient()
    spec, err = sg.generate_spec(obj=default_spec)

    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed generating attach ISCSI client to volume group spec", **result
        )

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        return

    vg = get_volume_group(module, vgs, volume_group_ext_id)
    etag = get_etag(vg)
    kwargs = {"if_match": etag}
    resp = None
    try:
        resp = vgs.attach_iscsi_client(body=spec, extId=volume_group_ext_id, **kwargs)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while attaching ISCSI client to volume group",
        )

    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        task_status = wait_for_completion(module, task_ext_id)
        result["response"] = strip_internal_attributes(task_status.to_dict())
        ext_id = get_entity_ext_id_from_task(
            task_status, rel=TASK_CONSTANTS.RelEntityType.ISCSI_CLIENT
        )
        if ext_id:
            result["ext_id"] = ext_id
    result["changed"] = True


def detach_iscsi_client(module, result):
    vgs = get_vg_api_instance(module)
    volume_group_ext_id = module.params.get("volume_group_ext_id")
    result["volume_group_ext_id"] = volume_group_ext_id

    sg = SpecGenerator(module)
    default_spec = volumes_sdk.IscsiClientAttachment()
    spec, err = sg.generate_spec(obj=default_spec)

    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed generating detach ISCSI client to volume group spec", **result
        )

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        return

    vg = get_volume_group(module, vgs, volume_group_ext_id)
    etag = get_etag(vg)
    kwargs = {"if_match": etag}
    resp = None
    try:
        resp = vgs.detach_iscsi_client(body=spec, extId=volume_group_ext_id, **kwargs)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while detaching ISCSI client from volume group",
        )

    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        task_status = wait_for_completion(module, task_ext_id)
        result["response"] = strip_internal_attributes(task_status.to_dict())
    result["changed"] = True


def run_module():
    module = BaseModule(
        support_proxy=True,
        argument_spec=get_module_spec(),
        supports_check_mode=True,
    )
    if SDK_IMP_ERROR:
        module.fail_json(
            msg=missing_required_lib("ntnx_volumes_py_client"), exception=SDK_IMP_ERROR
        )

    remove_param_with_none_value(module.params)
    result = {
        "changed": False,
        "error": None,
        "response": None,
        "ext_id": None,
        "task_ext_id": None,
    }
    state = module.params.get("state")
    if state == "present":
        attach_iscsi_client(module, result)
    else:
        detach_iscsi_client(module, result)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
