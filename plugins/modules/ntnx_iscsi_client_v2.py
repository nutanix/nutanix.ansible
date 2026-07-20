#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_iscsi_client_v2
short_description: Update iSCSI clients (external attachments) in Nutanix Prism Central
version_added: 2.5.0
description:
  - This module allows you to update an iSCSI client (external attachment) in Nutanix Prism Central.
  - The Nutanix storage v4 iSCSI client entity is created and destroyed implicitly by
    attach-iscsi-client and detach-iscsi-client actions on a Volume Group; the storage
    IscsiClient API surface only exposes a GET and a PATCH for existing external
    attachments.
  - Use the M(nutanix.ncp.ntnx_volume_groups_iscsi_clients_v2) module to attach/detach
    iSCSI clients to a Volume Group.
  - This module uses PC v4 APIs based SDKs.
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
      The required roles depend on the operation being performed.
    - >-
      B(Update an iSCSI client) -
      Required Roles: Prism Admin, Storage Admin, Super Admin
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=storage)"
options:
  state:
    description:
      - If C(state) is set to C(present) and C(ext_id) is provided the module will update the iSCSI client.
      - If C(state) is set to C(present) and C(ext_id) is not provided the module fails because
        the storage v4 IscsiClient API does not expose a direct create endpoint -
        use M(nutanix.ncp.ntnx_volume_groups_iscsi_clients_v2) to attach a client to a Volume Group.
      - If C(state) is set to C(absent) the module fails because the storage v4 IscsiClient API
        does not expose a direct delete endpoint -
        use M(nutanix.ncp.ntnx_volume_groups_iscsi_clients_v2) to detach a client from a Volume Group.
    type: str
    required: false
    choices:
      - present
      - absent
    default: present
  ext_id:
    description:
      - The external identifier of the iSCSI client.
      - Required for update.
    type: str
    required: false
  iscsi_initiator_name:
    description:
      - iSCSI initiator name.
      - During the attach operation, exactly one of C(iscsi_initiator_name) and
        C(iscsi_initiator_network_id) is set on the client. This field is immutable
        once the client has been created; supply it only when the value already
        matches the existing client.
    type: str
    required: false
  iscsi_initiator_network_id:
    description:
      - Unique address that identifies the initiator on the network in IPv4/IPv6 format
        or as a fully qualified domain name.
      - During the attach operation, exactly one of C(iscsi_initiator_network_id) and
        C(iscsi_initiator_name) is set on the client.
    type: dict
    required: false
    suboptions:
      ipv4:
        description:
          - IPv4 address of the initiator.
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
          - IPv6 address of the initiator.
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
          - Fully qualified domain name of the initiator.
        type: dict
        required: false
        suboptions:
          value:
            description:
              - The FQDN value.
            type: str
            required: true
  client_secret:
    description:
      - iSCSI initiator client secret used for CHAP authentication.
      - This field should not be provided when C(enabled_authentications) is not set to C(CHAP).
    type: str
    required: false
  enabled_authentications:
    description:
      - Authentication type enabled for the iSCSI client.
      - If set to C(CHAP), C(client_secret) must be provided.
    type: str
    required: false
    choices:
      - CHAP
      - NONE
  target_params:
    description:
      - Target parameters governing the iSCSI target virtualization for this client.
    type: dict
    required: false
    suboptions:
      num_virtual_targets:
        description:
          - Number of virtual targets generated for the iSCSI target.
          - This field is immutable once the client is attached.
        type: int
        required: false
  cluster_reference:
    description:
      - External identifier of the Prism Element cluster that owns the iSCSI client.
      - This field is immutable.
    type: str
    required: false
  attachment_site:
    description:
      - The site where the Volume Group attach operation was processed.
      - Only meaningful when Metro DR is configured on the associated Volume Group.
    type: str
    required: false
    choices:
      - PRIMARY
      - SECONDARY
extends_documentation_fragment:
  - nutanix.ncp.ntnx_credentials
  - nutanix.ncp.ntnx_operations_v2
  - nutanix.ncp.ntnx_logger
  - nutanix.ncp.ntnx_proxy_v2
author:
  - Nutanix (@nutanix)
"""

EXAMPLES = r"""
- name: Update an existing iSCSI client to enable CHAP authentication
  nutanix.ncp.ntnx_iscsi_client_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: present
    ext_id: "aea43b5c-ae4d-4b60-934b-f8f581275dec"
    enabled_authentications: "CHAP"
    client_secret: "Nutanix.chapsecret1"
    target_params:
      num_virtual_targets: 32
    attachment_site: "PRIMARY"
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
  description:
    - Response for updating an iSCSI client.
    - If the operation is update and C(wait) is true, it will return the updated iSCSI client details.
    - If the operation is update and C(wait) is false, it will return the task details.
  returned: always
  type: dict
  sample:
    {
      "attachment_site": "PRIMARY",
      "client_secret": null,
      "cluster_name": "cluster1",
      "cluster_reference": "00061663-9fa0-28ca-185b-ac1f6b6f97e2",
      "created_time": "2026-05-20T05:19:00.229645+00:00",
      "enabled_authentications": "CHAP",
      "ext_id": "aea43b5c-ae4d-4b60-934b-f8f581275dec",
      "iscsi_initiator_name": "iqn.1991-05.com.microsoft:host-01",
      "iscsi_initiator_network_id": null,
      "iscsi_target_names": [
          "iqn.2010-06.com.nutanix:vg1-tgt0"
      ],
      "links": null,
      "target_params": {
          "num_virtual_targets": 32
      },
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
    - The external ID of the iSCSI client.
  returned: always
  type: str
  sample: "aea43b5c-ae4d-4b60-934b-f8f581275dec"

changed:
  description: This indicates whether the task resulted in any changes.
  returned: always
  type: bool
  sample: true

skipped:
  description:
    - This indicates whether the task was skipped due to idempotency.
    - Set when the requested state already matches the current state.
  returned: when applicable
  type: bool
  sample: true

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
  description: This indicates the message if any message occurred.
  returned: When there is an error, module is idempotent or check mode
  type: str
  sample: "Api Exception raised while updating iSCSI client"
"""

import traceback  # noqa: E402
import warnings  # noqa: E402
from copy import deepcopy  # noqa: E402

from ansible.module_utils.basic import missing_required_lib  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_module_v4 import BaseModuleV4  # noqa: E402
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
from ..module_utils.v4.storage.api_client import (  # noqa: E402
    get_etag,
    get_iscsi_client_api_instance,
)
from ..module_utils.v4.storage.helpers import get_iscsi_client  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
    strip_read_only_fields,
    validate_required_params,
)

SDK_IMP_ERROR = None
try:
    import ntnx_storage_py_client as storage_sdk  # noqa: E402
except ImportError:

    from ..module_utils.v4.sdk_mock import mock_sdk as storage_sdk  # noqa: E402

    SDK_IMP_ERROR = traceback.format_exc()

warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")

# Fields that are populated by the platform and MUST NOT be echoed back in a PATCH body.
ISCSI_CLIENT_READ_ONLY_FIELDS = (
    "ext_id",
    "tenant_id",
    "links",
    "created_time",
    "cluster_name",
    "iscsi_target_names",
)


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
        value=dict(type="str", required=True),
    )

    ip_address_or_fqdn_spec = dict(
        ipv4=dict(
            type="dict",
            options=ipv4_address_spec,
            required=False,
            obj=storage_sdk.IPv4Address,
        ),
        ipv6=dict(
            type="dict",
            options=ipv6_address_spec,
            required=False,
            obj=storage_sdk.IPv6Address,
        ),
        fqdn=dict(
            type="dict",
            options=fqdn_spec,
            required=False,
            obj=storage_sdk.FQDN,
        ),
    )

    target_params_spec = dict(
        num_virtual_targets=dict(type="int", required=False),
    )

    module_args = dict(
        ext_id=dict(type="str"),
        iscsi_initiator_name=dict(type="str"),
        iscsi_initiator_network_id=dict(
            type="dict",
            options=ip_address_or_fqdn_spec,
            required=False,
            obj=storage_sdk.IPAddressOrFQDN,
        ),
        client_secret=dict(type="str", no_log=True),
        enabled_authentications=dict(
            type="str",
            choices=["CHAP", "NONE"],
            obj=storage_sdk.AuthenticationType,
        ),
        target_params=dict(
            type="dict",
            options=target_params_spec,
            required=False,
            obj=storage_sdk.TargetParam,
        ),
        cluster_reference=dict(type="str"),
        attachment_site=dict(
            type="str",
            choices=["PRIMARY", "SECONDARY"],
            obj=storage_sdk.VolumeGroupAttachmentSite,
        ),
    )
    return module_args


def create_iscsi_client(module, result, api_instance):
    """Create is not supported by the storage v4 IscsiClient API surface.

    An iSCSI client is materialized as a by-product of attaching an initiator
    to a Volume Group via the ntnx_volume_groups_iscsi_clients_v2 module.
    Fail fast with a descriptive error rather than silently no-oping.
    """
    # api_instance is intentionally unused; signature mirrors sibling modules.
    del api_instance
    result["failed"] = True
    module.fail_json(
        msg=(
            "Creating an iSCSI client is not supported by the storage v4 IscsiClient API. "
            "Use nutanix.ncp.ntnx_volume_groups_iscsi_clients_v2 to attach an iSCSI client "
            "to a Volume Group."
        ),
        **result,
    )


def check_for_idempotency(old_spec_dict, update_spec_dict):
    """Compare the current iSCSI client with the requested spec for idempotency."""
    old = strip_internal_attributes(deepcopy(old_spec_dict))
    new = strip_internal_attributes(deepcopy(update_spec_dict))
    for field in ISCSI_CLIENT_READ_ONLY_FIELDS:
        old.pop(field, None)
        new.pop(field, None)
    # `client_secret` is a write-only field: the server always returns None so
    # we cannot compare it. If the caller provided one, treat that as a change.
    if new.get("client_secret") is not None:
        return False
    old.pop("client_secret", None)
    new.pop("client_secret", None)
    return old == new


def update_iscsi_client(module, result, api_instance):
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id

    validate_required_params(module, ["ext_id"])

    old_spec = get_iscsi_client(module, api_instance, ext_id)
    etag = get_etag(data=old_spec)
    if not etag:
        return module.fail_json(
            msg="Unable to fetch etag for updating iSCSI client",
            **result,
        )
    kwargs = {"if_match": etag}

    sg = SpecGenerator(module)
    update_spec, err = sg.generate_spec(obj=deepcopy(old_spec))
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating update iSCSI client spec", **result)

    if module.check_mode:
        result["response"] = strip_internal_attributes(update_spec.to_dict())
        return

    if check_for_idempotency(old_spec.to_dict(), update_spec.to_dict()):
        result["skipped"] = True
        result["response"] = strip_internal_attributes(old_spec.to_dict())
        module.exit_json(
            msg="Nothing to change. iSCSI client is already in the desired state.",
            **result,
        )

    strip_read_only_fields(update_spec, fields=ISCSI_CLIENT_READ_ONLY_FIELDS)

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

    task_ext_id = getattr(getattr(resp, "data", None), "ext_id", None)
    if task_ext_id:
        result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    # The IscsiClient PATCH returns the fresh object (not a task reference).
    # Re-fetch to normalize the shape so callers always see the persisted state.
    try:
        refreshed = get_iscsi_client(module, api_instance, ext_id)
        result["response"] = strip_internal_attributes(refreshed.to_dict())
    except Exception:
        # If the refresh fails for any transient reason, keep the PATCH response.
        pass
    result["changed"] = True


def delete_iscsi_client(module, result, api_instance):
    """Delete is not supported by the storage v4 IscsiClient API surface.

    An iSCSI client is removed by detaching the initiator from the Volume Group
    via the ntnx_volume_groups_iscsi_clients_v2 module.
    """
    # api_instance is intentionally unused; signature mirrors sibling modules.
    del api_instance
    ext_id = module.params.get("ext_id")
    if ext_id:
        result["ext_id"] = ext_id
    result["failed"] = True
    module.fail_json(
        msg=(
            "Deleting an iSCSI client is not supported by the storage v4 IscsiClient API. "
            "Use nutanix.ncp.ntnx_volume_groups_iscsi_clients_v2 to detach an iSCSI client "
            "from a Volume Group."
        ),
        **result,
    )


def run_module():
    module = BaseModuleV4(
        argument_spec=get_module_spec(),
        supports_check_mode=True,
        required_if=[
            ("state", "absent", ("ext_id",)),
        ],
    )
    if SDK_IMP_ERROR:
        module.fail_json(
            msg=missing_required_lib("ntnx_storage_py_client"),
            exception=SDK_IMP_ERROR,
        )

    remove_param_with_none_value(module.params)
    result = {
        "changed": False,
        "response": None,
        "failed": False,
        "ext_id": None,
        "task_ext_id": None,
    }
    api_instance = get_iscsi_client_api_instance(module)
    state = module.params.get("state")
    if state == "present":
        if module.params.get("ext_id"):
            update_iscsi_client(module, result, api_instance)
        else:
            create_iscsi_client(module, result, api_instance)
    else:
        delete_iscsi_client(module, result, api_instance)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
