#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2027, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_notification_v2
short_description: Compute LCM upgrade plan and notifications for a set of entities
version_added: "2.7.0"
description:
  - Compute upgrade notifications for a set of LCM entities and their target versions.
  - Notifications describe the impact of the planned upgrade on cluster nodes and entities,
    including disruptive actions such as host reboots, VM migrations, and maintenance-mode entry.
  - Submit a NotificationsSpec containing entity update specifications
    (entity UUID and target version pairs) and optional credentials for third-party
    vendor management.
  - This module uses PC v4 APIs based SDKs.
notes:
  - >-
    This module requires the following Nutanix IAM roles to be assigned to the user
    performing the operation.
  - >-
    B(Compute LCM upgrade notifications) -
    Required Roles: Cluster Admin, Prism Admin, Super Admin
  - "Ref: U(https://developers.nutanix.com/api-reference?namespace=lifecycle&version=v4.3"
options:
  state:
    description:
      - State of the module.
      - If C(state) is C(present) the module will compute LCM upgrade notifications.
      - If C(state) is C(absent) the module will fail.
    type: str
    choices:
      - present
    default: present
  notifications_spec:
    description:
      - List of entity update specifications (entity UUID and target version pairs)
        describing the intended upgrade for which notifications are computed.
      - Corresponds to the API C(notificationsSpec) request field.
    type: list
    elements: dict
    required: true
    suboptions:
      entity_uuid:
        description:
          - UUID of the LCM entity.
        type: str
        required: true
      to_version:
        description:
          - The target version that the entity will be upgraded to.
        type: str
        required: true
  credentials:
    description:
      - Credentials to be provided by the user for LCM operations that require
        authentication with external systems such as vCenter or Intersight.
    type: list
    elements: dict
    required: false
    suboptions:
      credential_detail:
        description:
          - The credential details, provided as either a reference to a pre-created
            credential in the credential store (CredentialReference) or raw vendor
            management credentials (VendorManagementCredential).
          - Exactly one of the mutually exclusive suboptions must be provided.
        type: dict
        required: true
        suboptions:
          credential_reference:
            description:
              - A reference to a pre-created credential in the Nutanix credential
                store, identified by its UUID.
              - Mutually exclusive with I(vendor_management_credential).
            type: dict
            suboptions:
              credential_ext_id:
                description:
                  - The UUID of the credential stored in the credential store.
                type: str
                required: true
          vendor_management_credential:
            description:
              - Credentials for third-party vendor management platforms
                (for example vCenter, Intersight, UCS).
              - Mutually exclusive with I(credential_reference).
            type: dict
            suboptions:
              credential_spec:
                description:
                  - Credentials to be provided by the user for LCM operations that
                    require authentication with external systems such as vCenter
                    or Intersight.
                  - Exactly one of the mutually exclusive suboptions must be provided.
                type: dict
                required: true
                suboptions:
                  vcenter_credential:
                    description:
                      - A credential used for authentication with VCenter server.
                      - Mutually exclusive with I(intersight_credential).
                    type: dict
                    suboptions:
                      address:
                        description:
                          - Vcenter IP address or FQDN.
                          - An unique address that identifies a device on the internet
                            or a local network in IPv4/IPv6 format or a Fully Qualified
                            Domain Name.
                        type: dict
                        required: true
                        suboptions:
                          ipv4:
                            description:
                              - An unique address that identifies a device on the
                                internet or a local network in IPv4 format.
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
                              - An unique address that identifies a device on the
                                internet or a local network in IPv6 format.
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
                          fqdn:
                            description:
                              - A fully qualified domain name that specifies its exact
                                location in the tree hierarchy of the Domain Name System.
                            type: dict
                            suboptions:
                              value:
                                description:
                                  - The fully qualified domain name of the host.
                                type: str
                      credential:
                        description:
                          - An authentication scheme that requires the client to present
                            a username and password.
                        type: dict
                        required: true
                        suboptions:
                          username:
                            description:
                              - Username required for the basic auth scheme.
                              - As per RFC 2617 usernames might be case sensitive.
                            type: str
                            required: true
                          password:
                            description:
                              - Password required for the basic auth scheme.
                            type: str
                            required: true
                  intersight_credential:
                    description:
                      - Intersight connection used for authentication.
                      - Mutually exclusive with I(vcenter_credential).
                    type: dict
                    suboptions:
                      url:
                        description:
                          - Intersight connection url.
                        type: str
                        required: true
                      deployment_type:
                        description:
                          - Type of Intersight connection.
                        type: str
                        required: true
                        choices:
                          - INTERSIGHT_SAAS
                          - INTERSIGHT_VIRTUAL_APPLIANCE
                      credential:
                        description:
                          - Secret fields of a key based authentication credential.
                        type: dict
                        required: true
                        suboptions:
                          api_key:
                            description:
                              - Intersight connection API key.
                            type: str
                            required: true
                          secret_key:
                            description:
                              - Secret key of the Intersight connection.
                            type: str
                            required: true
  cluster_ext_id:
    description:
      - The cluster UUID on which the resource is present or the operation is being
        performed.
      - Passed to the API as the C(X-Cluster-Id) header.
      - When omitted, the operation targets the Prism Central cluster itself; when a
        Prism Element cluster external ID is provided, the operation targets that PE
        cluster.
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
- name: Compute LCM upgrade notifications for a PC entity
  nutanix.ncp.ntnx_notification_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    notifications_spec:
      - entity_uuid: "3c196eac-e1d5-4c8a-9b01-c133f6907ca2"
        to_version: "4.1.0"
  register: notification_result

- name: Compute LCM upgrade notifications for a PE cluster entity
  nutanix.ncp.ntnx_notification_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    cluster_ext_id: "00062db4-a450-e685-0fda-cdf9ca935bfd"
    notifications_spec:
      - entity_uuid: "15570c98-beaf-4633-afd2-b6a306ff1001"
        to_version: "5.0.0"
      - entity_uuid: "7f8e2a1c-1234-4321-9abc-def012345678"
        to_version: "3.2.1"
  register: notification_result

- name: Compute LCM upgrade notifications using a stored credential reference
  nutanix.ncp.ntnx_notification_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    notifications_spec:
      - entity_uuid: "3c196eac-e1d5-4c8a-9b01-c133f6907ca2"
        to_version: "4.1.0"
    credentials:
      - credential_detail:
          credential_reference:
            credential_ext_id: "2270f0dd-6d2b-4af5-9940-83f9017c707f"
  register: notification_result

- name: Compute LCM upgrade notifications with inline vCenter credentials
  nutanix.ncp.ntnx_notification_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    notifications_spec:
      - entity_uuid: "3c196eac-e1d5-4c8a-9b01-c133f6907ca2"
        to_version: "4.1.0"
    credentials:
      - credential_detail:
          vendor_management_credential:
            credential_spec:
              vcenter_credential:
                address:
                  ipv4:
                    value: "10.0.0.2"
                credential:
                  username: "admin"
                  password: "password"
  register: notification_result
"""

RETURN = r"""
response:
  description:
    - Response for the compute-notifications operation.
    - When C(wait) is true and the task succeeds, this contains the LCM upgrade
      notification resource (list of per-entity notification items with severity
      levels, messages, target versions, location info and hypervisor type).
    - When C(wait) is false, this contains the task reference details.
  returned: always
  type: dict
  sample:
    {
        "cluster_ext_id": null,
        "ext_id": "b9c1a8a0-1e5f-4e07-9c9e-90a1c2d3e4f5",
        "links": null,
        "notifications": [
            {
                "details": [
                    {
                        "message": "Host will enter maintenance mode during upgrade.",
                        "severity_level": "WARNING"
                    }
                ],
                "entity_class": "PC CORE CLUSTER",
                "entity_model": "Calm Policy Engine",
                "entity_type": "SOFTWARE",
                "entity_version": "3.8.0",
                "ext_id": "3c196eac-e1d5-4c8a-9b01-c133f6907ca2",
                "hardware_family": null,
                "hypervisor_type": null,
                "location_info": null,
                "notification_type": "ENTITY",
                "to_version": "4.1.0"
            }
        ],
        "tenant_id": null
    }

task_ext_id:
  description:
    - The external ID of the task.
  returned: always
  type: str
  sample: "ZXJnb24=:a784c0b7-1038-49cf-40b5-2845231d242f"

ext_id:
  description:
    - The external ID of the generated LCM upgrade notification resource.
    - Populated once the task completes and the notification ext_id can be resolved
      from the task; used by M(nutanix.ncp.ntnx_lcm_notifications_info_v2) to fetch
      the same resource later.
  returned: when C(wait) is true and the task succeeds
  type: str
  sample: "b9c1a8a0-1e5f-4e07-9c9e-90a1c2d3e4f5"

changed:
  description: This indicates whether the task resulted in any changes
  returned: always
  type: bool
  sample: true

msg:
  description: This indicates the message if any message occurred
  returned: When there is an error or an informational message is emitted
  type: str
  sample: "Api Exception raised while computing LCM upgrade notifications"

error:
  description: This indicates the error message if any error occurred
  returned: When an error occurs
  type: str
  sample: "Failed generating spec for computing LCM upgrade notifications"

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
from ..module_utils.v4.base_module_v4 import BaseModuleV4  # noqa: E402
from ..module_utils.v4.lcm.api_client import (  # noqa: E402
    get_notifications_api_instance,
)
from ..module_utils.v4.lcm.helpers import get_lcm_notification  # noqa: E402
from ..module_utils.v4.prism.tasks import (  # noqa: E402
    get_entity_ext_id_from_task,
    get_ext_id_from_task_completion_details,
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

    BasicAuth = None
    SDK_IMP_ERROR = traceback.format_exc()
else:
    from ntnx_lifecycle_py_client.models.common.v1.config.BasicAuth import (  # noqa: E402
        BasicAuth,
    )

warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():

    entity_update_spec = dict(
        entity_uuid=dict(type="str", required=True),
        to_version=dict(type="str", required=True),
    )

    ipv4_address_spec = dict(
        value=dict(type="str", required=True),
        prefix_length=dict(type="int"),
    )
    ipv6_address_spec = dict(
        value=dict(type="str", required=True),
        prefix_length=dict(type="int"),
    )
    fqdn_spec = dict(
        value=dict(type="str"),
    )
    ip_address_or_fqdn_spec = dict(
        ipv4=dict(
            type="dict",
            options=ipv4_address_spec,
            obj=lifecycle_sdk.IPv4Address,
        ),
        ipv6=dict(
            type="dict",
            options=ipv6_address_spec,
            obj=lifecycle_sdk.IPv6Address,
        ),
        fqdn=dict(
            type="dict",
            options=fqdn_spec,
            obj=lifecycle_sdk.FQDN,
        ),
    )

    basic_auth_spec = dict(
        username=dict(type="str", required=True),
        password=dict(type="str", required=True, no_log=True),
    )

    key_based_auth_spec = dict(
        api_key=dict(type="str", required=True, no_log=True),
        secret_key=dict(type="str", required=True, no_log=True),
    )

    vcenter_credential_spec = dict(
        address=dict(
            type="dict",
            required=True,
            options=ip_address_or_fqdn_spec,
            obj=lifecycle_sdk.IPAddressOrFQDN,
            mutually_exclusive=[("ipv4", "ipv6", "fqdn")],
            required_one_of=[("ipv4", "ipv6", "fqdn")],
        ),
        credential=dict(
            type="dict",
            required=True,
            options=basic_auth_spec,
            obj=BasicAuth,
            no_log=True,
        ),
    )

    intersight_credential_spec = dict(
        url=dict(type="str", required=True),
        deployment_type=dict(
            type="str",
            required=True,
            choices=["INTERSIGHT_SAAS", "INTERSIGHT_VIRTUAL_APPLIANCE"],
        ),
        credential=dict(
            type="dict",
            required=True,
            options=key_based_auth_spec,
            obj=lifecycle_sdk.KeyBasedAuth,
            no_log=True,
        ),
    )

    credential_spec_options = dict(
        vcenter_credential=dict(
            type="dict",
            options=vcenter_credential_spec,
            obj=lifecycle_sdk.VcenterCredential,
        ),
        intersight_credential=dict(
            type="dict",
            options=intersight_credential_spec,
            obj=lifecycle_sdk.IntersightCredential,
        ),
    )

    vendor_management_credential_spec = dict(
        credential_spec=dict(
            type="dict",
            required=True,
            options=credential_spec_options,
            mutually_exclusive=[("vcenter_credential", "intersight_credential")],
            required_one_of=[("vcenter_credential", "intersight_credential")],
            obj={
                "vcenter_credential": lifecycle_sdk.VcenterCredential,
                "intersight_credential": lifecycle_sdk.IntersightCredential,
            },
        ),
    )

    credential_reference_spec = dict(
        credential_ext_id=dict(type="str", required=True),
    )

    credential_detail_options = dict(
        credential_reference=dict(
            type="dict",
            options=credential_reference_spec,
            obj=lifecycle_sdk.CredentialReference,
        ),
        vendor_management_credential=dict(
            type="dict",
            options=vendor_management_credential_spec,
            obj=lifecycle_sdk.VendorManagementCredential,
        ),
    )

    credential_spec = dict(
        credential_detail=dict(
            type="dict",
            required=True,
            options=credential_detail_options,
            mutually_exclusive=[
                ("credential_reference", "vendor_management_credential")
            ],
            required_one_of=[("credential_reference", "vendor_management_credential")],
            obj={
                "credential_reference": lifecycle_sdk.CredentialReference,
                "vendor_management_credential": lifecycle_sdk.VendorManagementCredential,
            },
        ),
    )

    module_args = dict(
        state=dict(type="str", default="present", choices=["present"]),
        notifications_spec=dict(
            type="list",
            elements="dict",
            options=entity_update_spec,
            required=True,
            obj=lifecycle_sdk.EntityUpdateSpec,
        ),
        credentials=dict(
            type="list",
            elements="dict",
            options=credential_spec,
            obj=lifecycle_sdk.Credential,
        ),
        cluster_ext_id=dict(type="str", required=False),
    )

    return module_args


def _resolve_notification_ext_id(task):
    """
    Best-effort resolution of the notification resource ext_id from the compute
    notifications task. The task's entities_affected typically carries the newly
    created notification's ext_id; the completion_details may also carry it under
    a name such as "notificationExtId"/"resourceId".
    """
    ext_id = get_entity_ext_id_from_task(task)
    if ext_id:
        return ext_id
    for name in ("notificationExtId", "resourceId", "resource_id"):
        ext_id = get_ext_id_from_task_completion_details(task, name=name)
        if ext_id:
            return ext_id
    return None


def compute_notifications(module, api_instance, result):
    cluster_ext_id = module.params.get("cluster_ext_id")

    validate_required_params(module, ["notifications_spec"])

    sg = SpecGenerator(module)
    default_spec = lifecycle_sdk.NotificationsSpec(notifications_spec=[])
    spec, err = sg.generate_spec(obj=default_spec)

    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed generating spec for computing LCM upgrade notifications",
            **result,
        )

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        return

    resp = None
    try:
        resp = api_instance.compute_notifications(
            body=spec, X_Cluster_Id=cluster_ext_id
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while computing LCM upgrade notifications",
        )

    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    result["changed"] = True

    if task_ext_id and module.params.get("wait"):
        task = wait_for_completion(module, task_ext_id)
        result["response"] = strip_internal_attributes(task.to_dict())

        notification_ext_id = _resolve_notification_ext_id(task)
        if notification_ext_id:
            result["ext_id"] = notification_ext_id
            notification = get_lcm_notification(
                module, api_instance, notification_ext_id
            )
            if notification is not None:
                result["response"] = strip_internal_attributes(notification.to_dict())
        else:
            raise_api_exception(
                module=module,
                exception=Exception(
                    "Failed to resolve LCM notification ext_id from the compute-notifications task"
                ),
                msg="Failed to resolve LCM notification ext_id from the compute-notifications task",
            )


def run_module():
    module = BaseModuleV4(
        argument_spec=get_module_spec(),
        supports_check_mode=True,
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
        "ext_id": None,
        "task_ext_id": None,
    }

    api_instance = get_notifications_api_instance(module)
    compute_notifications(module, api_instance, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
