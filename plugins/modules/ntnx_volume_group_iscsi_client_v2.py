#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_volume_group_iscsi_client_v2
short_description: Update iSCSI clients associated with Volume Groups in Nutanix Prism Central
version_added: 2.7.0
description:
  - This module allows you to update an iSCSI client entity that is associated with a Volume Group in Nutanix Prism Central.
  - iSCSI clients are auto-registered when they are attached to a Volume Group.
  - Use M(nutanix.ncp.ntnx_volume_groups_iscsi_clients_v2) to attach or detach an iSCSI client to/from a Volume Group.
  - The underlying Nutanix Volumes v4 API only exposes an update operation for standalone iSCSI clients.
  - This module uses PC v4 APIs based SDKs.
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
      The required roles depend on the operation being performed.
    - >-
      B(Update an iSCSI client) -
      Required Roles: Backup Admin, CSI System, Kubernetes Data Services System, Prism Admin, Project Manager,
      Storage Admin, Super Admin, Self-Service Admin (deprecated)
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=volumes)"
options:
  state:
    description:
      - If C(state) is set to C(present) and C(ext_id) is provided, the module will update the iSCSI client.
      - The Nutanix Volumes v4 API does not expose standalone create or delete operations for iSCSI clients;
        clients are created when an initiator is attached to a Volume Group and are removed on detach.
      - If C(state) is set to C(present) without C(ext_id), or set to C(absent), the module fails with a
        descriptive message and no API call is made.
    type: str
    required: false
    choices:
      - present
      - absent
    default: present
  ext_id:
    description:
      - The external ID of the iSCSI client.
      - Required for update operation.
    type: str
    required: false
  iscsi_initiator_name:
    description:
      - iSCSI initiator name of the client.
      - This field is immutable and returned by the API; it cannot be changed by an update.
      - Provided here for reference and for parity with the SDK model.
    type: str
    required: false
  iscsi_initiator_network_id:
    description:
      - Network identifier of the iSCSI initiator when the initiator is identified by IP address or FQDN.
      - Exactly one of ipv4, ipv6 or fqdn should be provided.
      - This field is immutable.
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
              - Prefix length of the IPv4 address.
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
              - The IPv6 address value.
            type: str
            required: true
          prefix_length:
            description:
              - Prefix length of the IPv6 address.
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
              - The FQDN value.
            type: str
            required: true
  client_secret:
    description:
      - Client secret used for CHAP authentication.
      - This is a sensitive value that is never returned by the API in read paths.
    type: str
    required: false
  enabled_authentications:
    description:
      - Authentication type enabled for the iSCSI client on the Volume Group.
    type: str
    required: false
    choices:
      - CHAP
      - NONE
  attached_targets:
    description:
      - List of iSCSI target parameters that will be visible and accessible to the iSCSI client.
      - Each element carries the target name and the number of virtual targets.
    type: list
    elements: dict
    required: false
    suboptions:
      iscsi_target_name:
        description:
          - Name of the iSCSI target.
        type: str
        required: false
      num_virtual_targets:
        description:
          - Number of virtual targets generated for the iSCSI target.
          - This field is immutable at the target level.
        type: int
        required: false
  num_virtual_targets:
    description:
      - Number of virtual targets generated for the iSCSI target used by this client.
      - This field is immutable and is set at attach time.
    type: int
    required: false
  cluster_reference:
    description:
      - UUID of the cluster that hosts this iSCSI client entity.
      - This field is immutable and is set by the platform when the client is attached.
    type: str
    required: false
  attachment_site:
    description:
      - The site where the Volume Group attach operation was processed.
      - Only meaningful when Metro DR has been configured for the referenced Volume Group.
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
  - Abhinav Bansal (@abhinavbansal29)
  - George Ghawali (@george-ghawali)
"""

EXAMPLES = r"""
- name: Update iSCSI client - refresh CHAP secret
  nutanix.ncp.ntnx_volume_group_iscsi_client_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: present
    ext_id: "aea43b5c-ae4d-4b60-934b-f8f581275dec"
    enabled_authentications: CHAP
    client_secret: "SuperSecretPass123"
  register: result
  ignore_errors: true

- name: Update iSCSI client - disable CHAP authentication
  nutanix.ncp.ntnx_volume_group_iscsi_client_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: present
    ext_id: "aea43b5c-ae4d-4b60-934b-f8f581275dec"
    enabled_authentications: NONE
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
  description:
    - Response for the update iSCSI client operation.
    - If C(wait) is true, returns the completed task details.
    - If C(wait) is false, returns the queued task reference.
  returned: always
  type: dict
  sample:
    {
      "cluster_ext_ids": [
          "0006555e-4e63-4a5e-185b-ac1f6b6f97e2"
      ],
      "completed_time": "2026-07-21T06:08:09.442036+00:00",
      "completion_details": null,
      "created_time": "2026-07-21T06:08:09.203393+00:00",
      "entities_affected": [
          {
              "ext_id": "97f41675-1833-4ba4-9206-2cfd8eb436b4",
              "name": null,
              "rel": "volumes:config:iscsi-client"
          }
      ],
      "error_messages": null,
      "ext_id": "ZXJnb24=:8e7b1a68-a40e-4ee2-814f-be38cc068ea3",
      "is_background_task": false,
      "is_cancelable": false,
      "last_updated_time": "2026-07-21T06:08:09.442035+00:00",
      "legacy_error_message": null,
      "number_of_entities_affected": 1,
      "number_of_subtasks": 1,
      "operation": "IscsiClientUpdate",
      "operation_description": "Update Iscsi client",
      "owned_by": {
          "ext_id": "00000000-0000-0000-0000-000000000000",
          "name": "admin"
      },
      "parent_task": null,
      "progress_percentage": 100,
      "started_time": "2026-07-21T06:08:09.203393+00:00",
      "status": "SUCCEEDED",
      "sub_steps": null,
      "sub_tasks": [
          {
              "ext_id": "ZXJnb24=:c88d8985-f3be-4cad-b812-77f5d84bb5f4",
              "href": "https://<pc-ip>:9440/api/prism/v4.3/config/tasks/ZXJnb24=:c88d8985-f3be-4cad-b812-77f5d84bb5f4",
              "rel": "subtask"
          }
      ],
      "warnings": null
    }

task_ext_id:
  description:
    - The external ID of the task that performed the update.
  returned: always
  type: str
  sample: "ZXJnb24=:8e7b1a68-a40e-4ee2-814f-be38cc068ea3"

ext_id:
  description:
    - The external ID of the iSCSI client.
  returned: always
  type: str
  sample: "97f41675-1833-4ba4-9206-2cfd8eb436b4"

changed:
  description: This indicates whether the task resulted in any changes.
  returned: always
  type: bool
  sample: true

skipped:
  description:
    - Set to true when the module detects that the update would be a no-op
      (idempotency), so no API call is made.
  returned: When applicable
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
  description:
    - Status/error message describing the outcome of the operation.
    - Set when an error occurs, when the module is idempotent, or when an
      unsupported operation (state=absent, or state=present without ext_id)
      is requested.
  returned: When an error occurs, when the module is idempotent, or when an unsupported operation is requested
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
    validate_required_params,
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

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")

# Read-only / server-managed fields that must be blanked on the SDK model
# before it is echoed back on an UpdateIscsiClientById call. SDK properties
# do not expose a deleter, so we set them to None instead of ``delattr``.
# ``cluster_reference`` and ``iscsi_initiator_name`` are immutable per the
# Volumes v4 API and the endpoint returns a validation error (VOL-40101) if
# they are included in the PUT body, even when the value is unchanged.
_ISCSI_CLIENT_READ_ONLY_FIELDS = (
    "links",
    "tenant_id",
    "cluster_reference",
    "iscsi_initiator_name",
    "iscsi_initiator_network_id",
    "attached_targets",
    "num_virtual_targets",
    "attachment_site",
)


def _clear_read_only_fields(spec, fields=_ISCSI_CLIENT_READ_ONLY_FIELDS):
    """Blank out platform-managed fields on an IscsiClient SDK model.

    The Volumes SDK objects are protobuf-derived and expose fields as
    properties without a deleter, so calling ``delattr`` raises
    ``AttributeError``. Setting them back to ``None`` is enough for the
    UpdateIscsiClientById endpoint to accept the payload as an in-place update.
    """
    for field in fields:
        if hasattr(spec, field):
            setattr(spec, field, None)
    return spec


def get_module_spec():
    address_spec = dict(
        value=dict(type="str", required=True),
        prefix_length=dict(type="int", required=False),
    )
    fqdn_spec = dict(
        value=dict(type="str", required=True),
    )

    iscsi_initiator_network_id_spec = dict(
        ipv4=dict(
            type="dict",
            options=address_spec,
            required=False,
            obj=volumes_sdk.IPv4Address,
        ),
        ipv6=dict(
            type="dict",
            options=address_spec,
            required=False,
            obj=volumes_sdk.IPv6Address,
        ),
        fqdn=dict(
            type="dict",
            options=fqdn_spec,
            required=False,
            obj=volumes_sdk.FQDN,
        ),
    )

    attached_target_spec = dict(
        iscsi_target_name=dict(type="str", required=False),
        num_virtual_targets=dict(type="int", required=False),
    )

    module_args = dict(
        ext_id=dict(type="str"),
        iscsi_initiator_name=dict(type="str"),
        iscsi_initiator_network_id=dict(
            type="dict",
            options=iscsi_initiator_network_id_spec,
            obj=volumes_sdk.IPAddressOrFQDN,
        ),
        client_secret=dict(type="str", no_log=True),
        enabled_authentications=dict(
            type="str",
            choices=["CHAP", "NONE"],
            obj=volumes_sdk.AuthenticationType,
        ),
        attached_targets=dict(
            type="list",
            elements="dict",
            options=attached_target_spec,
            obj=volumes_sdk.TargetParam,
        ),
        num_virtual_targets=dict(type="int"),
        cluster_reference=dict(type="str"),
        attachment_site=dict(
            type="str",
            choices=["PRIMARY", "SECONDARY"],
            obj=volumes_sdk.VolumeGroupAttachmentSite,
        ),
    )
    return module_args


def create_iscsi_client(module, result, api_instance):
    """
    Standalone create of an iSCSI client is not supported by the Nutanix
    Volumes v4 API. iSCSI client entities are created by attaching an
    initiator to a Volume Group via the AttachIscsiClient action; use
    M(nutanix.ncp.ntnx_volume_groups_iscsi_clients_v2) with C(state=present)
    instead.
    """
    del api_instance  # unused but kept for uniform signature with other CRUD helpers
    result["failed"] = True
    module.fail_json(
        msg=(
            "Standalone create of an iSCSI client is not supported by the "
            "Nutanix Volumes v4 API. Use the "
            "ntnx_volume_groups_iscsi_clients_v2 module with state=present "
            "to attach an iSCSI client to a Volume Group."
        ),
        **result,
    )


def check_for_idempotency(old_spec_dict, update_spec_dict):
    """
    Compare old and updated specs after stripping internal attributes.
    Returns True when the update would not change anything.
    """
    old_spec_dict = strip_internal_attributes(deepcopy(old_spec_dict))
    update_spec_dict = strip_internal_attributes(deepcopy(update_spec_dict))
    return old_spec_dict == update_spec_dict


def update_iscsi_client(module, result, api_instance):
    """
    Update an existing iSCSI client using UpdateIscsiClientById.
    """
    validate_required_params(module, ["ext_id"])
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id

    old_spec = get_iscsi_client(module, api_instance, ext_id)
    etag = get_etag(data=old_spec)
    if not etag:
        module.fail_json(
            msg="Unable to fetch etag for updating iSCSI client with ext_id: {0}".format(
                ext_id
            ),
            **result,
        )

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
            msg=(
                "Nothing to change. iSCSI client with ext_id '{0}' already has "
                "the requested configuration.".format(ext_id)
            ),
            **result,
        )

    _clear_read_only_fields(update_spec)

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
        task_status = wait_for_completion(module, task_ext_id)
        result["response"] = strip_internal_attributes(task_status.to_dict())
    result["changed"] = True


def delete_iscsi_client(module, result, api_instance):
    """
    Standalone delete of an iSCSI client is not supported by the Nutanix
    Volumes v4 API. To remove an iSCSI client attached to a Volume Group,
    use M(nutanix.ncp.ntnx_volume_groups_iscsi_clients_v2) with
    C(state=absent).
    """
    del api_instance  # unused but kept for uniform signature with other CRUD helpers
    result["failed"] = True
    module.fail_json(
        msg=(
            "Standalone delete of an iSCSI client is not supported by the "
            "Nutanix Volumes v4 API. Use the "
            "ntnx_volume_groups_iscsi_clients_v2 module with state=absent "
            "to detach an iSCSI client from a Volume Group."
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
            msg=missing_required_lib("ntnx_volumes_py_client"),
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
