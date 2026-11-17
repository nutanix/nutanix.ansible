#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2027, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_iscsi_clients_v2
short_description: Update an iSCSI client
version_added: "2.7.0"
description:
    - Update an existing iSCSI client configuration identified by its External ID.
    - This module uses PC v4 APIs based SDKs
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
    - >-
      B(Update an iSCSI client) -
      Required Roles: Backup Admin, Prism Admin, Project Admin, Project Manager,
      Self-Service Admin (deprecated), Storage Admin, Super Admin
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=volumes)"
options:
    state:
        description:
            - State of the module.
            - If C(state) is C(present), the module will update the iSCSI client.
            - If C(state) is C(absent), the module will fail.
        type: str
        choices:
            - present
        default: present
    ext_id:
        description:
            - The External ID of the iSCSI client to update.
        type: str
        required: true
    iscsi_initiator_name:
        description:
            - iSCSI initiator name.
            - Exactly one of iscsiInitiatorName and iscsiInitiatorNetworkId must be specified during the attach operation.
            - This field is immutable.
        type: str
    iscsi_initiator_network_id:
        description:
            - iSCSI initiator network identifier.
            - During the attach operation, exactly one of iscsiInitiatorName and iscsiInitiatorNetworkId must be specified.
            - This field is immutable.
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
                prefix_length:
                  description:
                    - The prefix length of the network to which this host IPv4 address belongs.
                    - Defaults to 32 when omitted.
                  type: int
                  required: false
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
                prefix_length:
                  description:
                    - The prefix length of the network to which this host IPv6 address belongs.
                    - Defaults to 128 when omitted.
                  type: int
                  required: false
            fqdn:
              description:
                - Fully qualified domain name of the initiator.
              type: dict
              required: false
              suboptions:
                value:
                  description:
                    - The value of the FQDN address.
                  type: str
                  required: true
    client_secret:
        description:
            - iSCSI initiator client secret in case of CHAP authentication.
            - This field should not be provided if the authentication type is not set to CHAP.
        type: str
    enabled_authentications:
        description:
            - The authentication type enabled for the Volume Group.
            - If omitted, the authentication is not configured/remains unchanged for the Volume Group.
            - If this is set to CHAP, the target/client secret must be provided.
        type: str
        choices:
            - CHAP
            - NONE
    attachment_site:
        description:
            - The site where the Volume Group attach operation should be processed.
            - This is an optional field.
            - This field may only be set if Metro DR has been configured for this Volume Group.
        type: str
        choices:
            - PRIMARY
            - SECONDARY
    num_virtual_targets:
        description:
            - Number of virtual targets generated for the iSCSI target.
            - This field is immutable.
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
- name: Update iSCSI client authentication type to CHAP
  nutanix.ncp.ntnx_iscsi_clients_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    ext_id: "0005b6b1-0b3b-4b3b-8b3b-0b3b4b3b4b35"
    enabled_authentications: CHAP
    client_secret: "Nutanix.1234455"
    num_virtual_targets: 2
    attachment_site: PRIMARY
    iscsi_initiator_network_id:
      ipv4:
        value: "192.168.1.100"
        prefix_length: 24
  register: result

- name: Update iSCSI client authentication type to NONE
  nutanix.ncp.ntnx_iscsi_clients_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    ext_id: "0005b6b1-0b3b-4b3b-8b3b-0b3b4b3b4b35"
    enabled_authentications: NONE
    num_virtual_targets: 2
    attachment_site: PRIMARY
    iscsi_initiator_name: "iqn.2024-01.com.nutanix.test:ansibletest2"
  register: result
"""

RETURN = r"""
response:
    description:
        - Response for updating iSCSI client.
        - iSCSI client details if C(wait) is true.
        - Task details if C(wait) is false.
    returned: always
    type: dict
    sample: {
        "attached_targets": [
            {
                "iscsi_target_name": "iqn.2010-06.com.nutanix:volumegroup-816645fc-13bc-4213-4ba4-4a9f25d7570c",
                "num_virtual_targets": 2
            }
        ],
        "attachment_site": null,
        "client_secret": null,
        "cluster_reference": "00065ffe-0266-379f-0000-000000028f57",
        "enabled_authentications": null,
        "ext_id": "57e207c3-0c96-42fb-be12-39de6bc45175",
        "iscsi_initiator_name": "iqn.2024-01.com.nutanix.test:ansibletest2",
        "iscsi_initiator_network_id": null,
        "links": null,
        "num_virtual_targets": null,
        "project_ext_id": null,
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
        - The External ID of the iSCSI client.
    returned: always
    type: str
    sample: "63311404-8b2e-4dbf-9e33-7848cc88d330"
skipped:
    description: This indicates whether the task was skipped due to idempotency
    returned: when module is idempotent and no changes are made
    type: bool
    sample: false
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
    returned: When there is an error, module is idempotent or in check mode
    type: str
    sample: "Api Exception raised while updating iSCSI client"
"""

import traceback  # noqa: E402
import warnings  # noqa: E402
from copy import deepcopy  # noqa: E402

from ansible.module_utils.basic import missing_required_lib  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_module_v4 import BaseModuleV4  # noqa: E402
from ..module_utils.v4.prism.tasks import wait_for_completion  # noqa: E402
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
    strip_read_only_fields,
)
from ..module_utils.v4.volumes.api_client import (  # noqa: E402
    get_etag,
    get_iscsi_client_api_instance,
)
from ..module_utils.v4.volumes.helpers import get_iscsi_client  # noqa: E402

SDK_IMP_ERROR = None
try:
    import ntnx_volumes_py_client as volumes_sdk  # noqa: E402
except ImportError:
    from ..module_utils.v4.sdk_mock import mock_sdk as volumes_sdk  # noqa: E402

    SDK_IMP_ERROR = traceback.format_exc()

warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    ipv4_address_spec = dict(
        value=dict(type="str", required=True),
        prefix_length=dict(type="int", required=False),
    )
    ipv6_address_spec = dict(
        value=dict(type="str", required=True),
        prefix_length=dict(type="int", required=False),
    )
    fqdn_spec = dict(
        value=dict(type="str", required=True),
    )
    iscsi_initiator_network_id_spec = dict(
        ipv4=dict(type="dict", options=ipv4_address_spec, obj=volumes_sdk.IPv4Address),
        ipv6=dict(type="dict", options=ipv6_address_spec, obj=volumes_sdk.IPv6Address),
        fqdn=dict(type="dict", options=fqdn_spec, obj=volumes_sdk.FQDN),
    )
    module_args = dict(
        state=dict(type="str", default="present", choices=["present"]),
        ext_id=dict(type="str", required=True),
        client_secret=dict(type="str", no_log=True),
        enabled_authentications=dict(
            type="str", choices=["CHAP", "NONE"], obj=volumes_sdk.AuthenticationType
        ),
        attachment_site=dict(
            type="str",
            choices=["PRIMARY", "SECONDARY"],
            obj=volumes_sdk.VolumeGroupAttachmentSite,
        ),
        num_virtual_targets=dict(type="int"),
        iscsi_initiator_name=dict(type="str"),
        iscsi_initiator_network_id=dict(
            type="dict",
            options=iscsi_initiator_network_id_spec,
            obj=volumes_sdk.IPAddressOrFQDN,
        ),
    )
    return module_args


def check_iscsi_client_idempotency(old_spec, update_spec):
    strip_internal_attributes(old_spec)
    strip_internal_attributes(update_spec)
    return old_spec == update_spec


def update_iscsi_client(module, result, api_instance):
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id

    current_spec = get_iscsi_client(module, api_instance, ext_id)

    sg = SpecGenerator(module)
    update_spec, err = sg.generate_spec(obj=deepcopy(current_spec))

    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating update iSCSI client spec", **result)

    strip_read_only_fields(update_spec, fields=("cluster_reference",))

    if module.check_mode:
        result["response"] = strip_internal_attributes(update_spec.to_dict())
        return

    current_dict = current_spec.to_dict()
    current_dict.pop("cluster_reference", None)
    if check_iscsi_client_idempotency(current_dict, update_spec.to_dict()):
        result["skipped"] = True
        module.exit_json(msg="Nothing to change.", **result)

    etag = get_etag(data=current_spec)
    if not etag:
        return module.fail_json(
            "Unable to fetch etag for updating iSCSI client", **result
        )
    kwargs = {"if_match": etag}
    resp = None
    try:
        resp = api_instance.update_iscsi_client_by_id(
            extId=ext_id, body=update_spec, **kwargs
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while updating iSCSI client",
        )

    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        wait_for_completion(module, task_ext_id)
        resp = get_iscsi_client(module, api_instance, ext_id)
        result["response"] = strip_internal_attributes(resp.to_dict())

    result["changed"] = True


def run_module():
    module = BaseModuleV4(
        argument_spec=get_module_spec(),
        supports_check_mode=True,
    )

    if SDK_IMP_ERROR:
        module.fail_json(
            msg=missing_required_lib("ntnx_volumes_py_client"), exception=SDK_IMP_ERROR
        )

    remove_param_with_none_value(module.params)
    result = {"changed": False, "failed": False, "response": None}
    api_instance = get_iscsi_client_api_instance(module)
    update_iscsi_client(module, result, api_instance)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
