#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_files_mount_target_v2
short_description: Create, Update, Delete a Nutanix Files mount target (share/export)
version_added: 2.5.0
description:
  - This module allows you to create, update and delete a mount target on a Nutanix File Server.
  - A mount target represents an SMB share or an NFS export exposed by a File Server.
  - This module uses PC v4 APIs based SDKs.
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
      The required roles depend on the operation being performed.
    - >-
      B(Create a Mount Target) -
      Required Roles: Files Admin, Prism Admin, Super Admin
    - >-
      B(Update a Mount Target) -
      Required Roles: Files Admin, Prism Admin, Super Admin
    - >-
      B(Delete a Mount Target) -
      Required Roles: Files Admin, Prism Admin, Super Admin
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=files)"
options:
  state:
    description:
      - If C(state) is C(present) and C(ext_id) is not provided the operation is create.
      - If C(state) is C(present) and C(ext_id) is provided the operation is update.
      - If C(state) is C(absent) and C(ext_id) is provided the operation is delete.
    type: str
    required: false
    choices:
      - present
      - absent
    default: present
  ext_id:
    description:
      - The external ID of the mount target.
      - Required for update and delete operations.
    type: str
    required: false
  file_server_ext_id:
    description:
      - The external ID of the parent file server that owns the mount target.
      - Required for every operation.
    type: str
    required: true
  name:
    description:
      - Mount target name (share/export name).
      - Required for create operation.
    type: str
    required: false
  description:
    description:
      - Description of the mount target.
    type: str
    required: false
  max_size_gb:
    description:
      - Maximum size of the mount target, in GiB.
      - Setting this to 0 removes the quota (unlimited size).
    type: int
    required: false
  type:
    description:
      - Type of mount target.
      - Required for create operation.
    type: str
    required: false
    choices:
      - GENERAL
      - HOMES
      - DISTRIBUTED
      - STANDARD
  path:
    description:
      - Path used when creating a nested/child mount target beneath a parent mount target.
    type: str
    required: false
  connected_mount_target_path:
    description:
      - The connected mount target path (used for symbolic or reference mount targets).
    type: str
    required: false
  is_compression_enabled:
    description:
      - Whether compression is enabled on the mount target.
    type: bool
    required: false
  blocked_file_extensions:
    description:
      - List of file extensions blocked from being written to the mount target.
    type: list
    elements: str
    required: false
  protocol:
    description:
      - Primary protocol used to access the mount target.
      - Required for create operation.
    type: str
    required: false
    choices:
      - NFS
      - SMB
      - NONE
      - INCOMPATIBLE
  secondary_protocol:
    description:
      - Optional list of additional protocols used to access the mount target.
    type: list
    elements: str
    required: false
    choices:
      - NFS
      - SMB
      - NONE
      - INCOMPATIBLE
  is_previous_version_enabled:
    description:
      - Enable "Previous Versions" (Windows Volume Shadow Copy) support on the mount target.
    type: bool
    required: false
  is_long_name_enabled:
    description:
      - Enable long file/share name support.
    type: bool
    required: false
  is_snapshot_paused:
    description:
      - Pause user-visible previous-version snapshots.
    type: bool
    required: false
  workload_type:
    description:
      - Workload type hint used for optimisation.
    type: str
    required: false
    choices:
      - DEFAULT
      - RANDOM
      - SEQUENTIAL
      - UNDEFINED
  parent_mount_target_ext_id:
    description:
      - The parent mount target's external ID, used when creating a nested mount target.
    type: str
    required: false
  smb_properties:
    description:
      - SMB protocol properties for the mount target.
    type: dict
    required: false
    suboptions:
      is_access_based_enumeration_enabled:
        description:
          - Enable access-based enumeration (ABE) so users only see files/folders they have access to.
        type: bool
        required: false
      is_smb3_encryption_enabled:
        description:
          - Enable SMB3 encryption on the wire for this share.
        type: bool
        required: false
      is_ca_enabled:
        description:
          - Enable Continuous Availability (CA) for the SMB share.
        type: bool
        required: false
      share_acl:
        description:
          - Share-level ACL entries.
        type: list
        elements: dict
        required: false
        suboptions:
          user_or_group_name:
            description:
              - User or group name for the share permission entry.
            type: str
            required: false
          permission_type:
            description:
              - Whether the ACE grants (ALLOW) or denies (DENY) the access.
            type: str
            required: false
            choices:
              - ALLOW
              - DENY
          access_type:
            description:
              - Level of access granted by this ACE.
            type: str
            required: false
            choices:
              - CHANGE
              - FULL_CONTROL
              - READ
          sid:
            description:
              - Security Identifier (SID) associated with the ACE.
            type: str
            required: false
  nfs_properties:
    description:
      - NFS protocol properties for the mount target.
    type: dict
    required: false
    suboptions:
      authentication_type:
        description:
          - NFS authentication type used for the export.
        type: str
        required: false
        choices:
          - SYSTEM
          - KERBEROS5
          - KERBEROS5I
          - KERBEROS5P
          - NONE
      anonymous_identifier:
        description:
          - Anonymous UID/GID pair used when a client is squashed to anonymous.
        type: dict
        required: false
        suboptions:
          uid:
            description:
              - Anonymous user identifier. Defaults to -2 on the server side.
            type: int
            required: false
          gid:
            description:
              - Anonymous group identifier.
            type: int
            required: false
      squash_type:
        description:
          - Squash strategy applied to incoming clients.
        type: str
        required: false
        choices:
          - NONE
          - ROOT_SQUASH
          - ALL_SQUASH
      access_type:
        description:
          - Default access type applied to NFS clients not covered by an exception.
        type: str
        required: false
        choices:
          - READ_WRITE
          - READ_ONLY
          - NO_ACCESS
      client_exceptions:
        description:
          - Per-client access/squash overrides.
        type: list
        elements: dict
        required: false
        suboptions:
          access_type:
            description:
              - Access type granted to the matching clients.
            type: str
            required: false
            choices:
              - READ_WRITE
              - READ_ONLY
              - NO_ACCESS
          squash_type:
            description:
              - Squash type applied to the matching clients.
            type: str
            required: false
            choices:
              - NONE
              - ROOT_SQUASH
              - ALL_SQUASH
          clients:
            description:
              - Comma separated list of clients (IPs, subnets, netgroups) matched by this exception.
            type: str
            required: false
  multi_protocol_properties:
    description:
      - Properties applied when a mount target is exposed to both SMB and NFS clients.
    type: dict
    required: false
    suboptions:
      is_case_sensitive_namespace_enabled:
        description:
          - Enable case-sensitive namespace handling.
        type: bool
        required: false
      is_symlink_creation_enabled:
        description:
          - Allow creation of symbolic links on the multiprotocol share.
        type: bool
        required: false
      is_simultaneous_access_enabled:
        description:
          - Allow simultaneous access from both SMB and NFS clients.
        type: bool
        required: false
  blocked_clients:
    description:
      - Read-only, no-access and read-write client filters applied on top of the default access.
    type: dict
    required: false
    suboptions:
      ro_access_filters:
        description:
          - Filters describing clients forced to read-only access.
        type: list
        elements: dict
        required: false
        suboptions:
          vendor_name:
            description:
              - Partner server vendor name (for ANTIVIRUS partner types this is icapServiceName).
            type: str
            required: false
          ip_list:
            description:
              - IP addresses matched by this filter.
            type: list
            elements: dict
            required: false
            suboptions:
              ipv4:
                description:
                  - IPv4 address specification.
                type: dict
                required: false
                suboptions:
                  value:
                    description:
                      - IPv4 address literal.
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
                  - IPv6 address specification.
                type: dict
                required: false
                suboptions:
                  value:
                    description:
                      - IPv6 address literal.
                    type: str
                    required: true
                  prefix_length:
                    description:
                      - Prefix length of the IPv6 address.
                    type: int
                    required: false
                    default: 128
          sid_list:
            description:
              - List of SIDs matched by this filter.
            type: list
            elements: str
            required: false
          uid_list:
            description:
              - List of UIDs matched by this filter.
            type: list
            elements: int
            required: false
          gid_list:
            description:
              - List of GIDs matched by this filter.
            type: list
            elements: int
            required: false
          is_all_ips_blocked:
            description:
              - When true, block every client IP.
            type: bool
            required: false
      no_access_filters:
        description:
          - Filters describing clients that must be denied all access.
        type: list
        elements: dict
        required: false
        suboptions:
          vendor_name:
            description:
              - Partner server vendor name.
            type: str
            required: false
          ip_list:
            description:
              - IP addresses matched by this filter.
            type: list
            elements: dict
            required: false
            suboptions:
              ipv4:
                description:
                  - IPv4 address specification.
                type: dict
                required: false
                suboptions:
                  value:
                    description:
                      - IPv4 address literal.
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
                  - IPv6 address specification.
                type: dict
                required: false
                suboptions:
                  value:
                    description:
                      - IPv6 address literal.
                    type: str
                    required: true
                  prefix_length:
                    description:
                      - Prefix length of the IPv6 address.
                    type: int
                    required: false
                    default: 128
          sid_list:
            description:
              - List of SIDs matched by this filter.
            type: list
            elements: str
            required: false
          uid_list:
            description:
              - List of UIDs matched by this filter.
            type: list
            elements: int
            required: false
          gid_list:
            description:
              - List of GIDs matched by this filter.
            type: list
            elements: int
            required: false
          is_all_ips_blocked:
            description:
              - When true, block every client IP.
            type: bool
            required: false
      rw_access_filters:
        description:
          - Filters describing clients that must be granted read-write access.
        type: list
        elements: dict
        required: false
        suboptions:
          vendor_name:
            description:
              - Partner server vendor name.
            type: str
            required: false
          ip_list:
            description:
              - IP addresses matched by this filter.
            type: list
            elements: dict
            required: false
            suboptions:
              ipv4:
                description:
                  - IPv4 address specification.
                type: dict
                required: false
                suboptions:
                  value:
                    description:
                      - IPv4 address literal.
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
                  - IPv6 address specification.
                type: dict
                required: false
                suboptions:
                  value:
                    description:
                      - IPv6 address literal.
                    type: str
                    required: true
                  prefix_length:
                    description:
                      - Prefix length of the IPv6 address.
                    type: int
                    required: false
                    default: 128
          sid_list:
            description:
              - List of SIDs matched by this filter.
            type: list
            elements: str
            required: false
          uid_list:
            description:
              - List of UIDs matched by this filter.
            type: list
            elements: int
            required: false
          gid_list:
            description:
              - List of GIDs matched by this filter.
            type: list
            elements: int
            required: false
          is_all_ips_blocked:
            description:
              - When true, block every client IP.
            type: bool
            required: false
  worm_spec:
    description:
      - Write Once Read Many (WORM) specification for the mount target.
    type: dict
    required: false
    suboptions:
      worm_type:
        description:
          - WORM type controlling how retention is enforced.
        type: str
        required: false
        choices:
          - DISABLED
          - SHARE_LEVEL
      cooloff_interval_seconds:
        description:
          - Number of idle seconds after which a file is locked for WORM retention.
        type: int
        required: false
      retention_period_seconds:
        description:
          - Total retention period, in seconds, applied to a locked file.
        type: int
        required: false
      is_compliance_enabled:
        description:
          - Enable WORM compliance mode.
        type: bool
        required: false
      is_legal_hold_enabled:
        description:
          - Enable WORM legal hold on the mount target.
        type: bool
        required: false
extends_documentation_fragment:
  - nutanix.ncp.ntnx_credentials
  - nutanix.ncp.ntnx_operations_v2
  - nutanix.ncp.ntnx_logger
  - nutanix.ncp.ntnx_proxy_v2
author:
  - Nutanix (@nutanix)
"""

EXAMPLES = r"""
- name: Create an SMB mount target
  nutanix.ncp.ntnx_files_mount_target_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: present
    file_server_ext_id: "9c1e537d-6777-4c22-5d41-ddd0c3337aa9"
    name: "ansible_smb_share"
    description: "SMB share created by Ansible"
    type: "GENERAL"
    protocol: "SMB"
    max_size_gb: 100
    is_compression_enabled: true
    smb_properties:
      is_access_based_enumeration_enabled: true
      is_smb3_encryption_enabled: true
      is_ca_enabled: false
  register: result

- name: Create an NFS mount target with client exceptions
  nutanix.ncp.ntnx_files_mount_target_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: present
    file_server_ext_id: "9c1e537d-6777-4c22-5d41-ddd0c3337aa9"
    name: "ansible_nfs_export"
    type: "GENERAL"
    protocol: "NFS"
    max_size_gb: 50
    nfs_properties:
      authentication_type: "SYSTEM"
      squash_type: "ROOT_SQUASH"
      access_type: "READ_WRITE"
      anonymous_identifier:
        uid: -2
        gid: -2
      client_exceptions:
        - access_type: "READ_ONLY"
          squash_type: "NONE"
          clients: "10.0.0.0/8"
  register: result

- name: Update a mount target
  nutanix.ncp.ntnx_files_mount_target_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: present
    file_server_ext_id: "9c1e537d-6777-4c22-5d41-ddd0c3337aa9"
    ext_id: "b8f1cc23-1111-2222-3333-4441c4d5aa11"
    description: "Updated by Ansible"
    max_size_gb: 200
    is_previous_version_enabled: true
  register: result

- name: Delete a mount target
  nutanix.ncp.ntnx_files_mount_target_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: absent
    file_server_ext_id: "9c1e537d-6777-4c22-5d41-ddd0c3337aa9"
    ext_id: "b8f1cc23-1111-2222-3333-4441c4d5aa11"
  register: result
"""

RETURN = r"""
response:
  description:
    - Response for the create, update or delete operation on the mount target.
    - When the operation is create or update and C(wait) is true, the mount target details are returned.
    - When C(wait) is false the task details are returned.
    - For delete, the task details are returned.
  returned: always
  type: dict
  sample:
    {
      "blocked_clients": null,
      "blocked_file_extensions": null,
      "connected_mount_target_path": null,
      "description": "SMB share created by Ansible",
      "ext_id": "b8f1cc23-1111-2222-3333-4441c4d5aa11",
      "is_compression_enabled": true,
      "is_long_name_enabled": null,
      "is_previous_version_enabled": null,
      "is_snapshot_paused": null,
      "links": null,
      "max_size_gb": 100,
      "multi_protocol_properties": null,
      "name": "ansible_smb_share",
      "nfs_properties": null,
      "parent_mount_target_ext_id": null,
      "path": null,
      "protocol": "SMB",
      "secondary_protocol": null,
      "smb_properties": {
          "is_access_based_enumeration_enabled": true,
          "is_ca_enabled": false,
          "is_smb3_encryption_enabled": true,
          "share_acl": null
      },
      "state": "ONLINE",
      "status_type": null,
      "tenant_id": null,
      "type": "GENERAL",
      "workload_type": null,
      "worm_spec": null
    }

task_ext_id:
  description:
    - The external ID of the task.
  returned: always
  type: str
  sample: "ZXJnb24=:90458bc7-a12b-4616-ac66-562fdb00c209"

ext_id:
  description:
    - The external ID of the mount target.
  returned: always
  type: str
  sample: "b8f1cc23-1111-2222-3333-4441c4d5aa11"

changed:
  description: Whether the task resulted in any change.
  returned: always
  type: bool
  sample: true

skipped:
  description: True when the operation was a no-op (for example an idempotent update).
  returned: when applicable
  type: bool
  sample: false

error:
  description: Error details when the task fails.
  returned: When an error occurs
  type: str

failed:
  description: Whether the module task failed.
  returned: always
  type: bool
  sample: false

msg:
  description: Contextual status/informational message from the module.
  returned: When there is an error, module is idempotent or check mode (in delete operation)
  type: str
  sample: "MountTarget with name 'ansible_smb_share' already exists. Skipping creation."
"""

import traceback  # noqa: E402
import warnings  # noqa: E402
from copy import deepcopy  # noqa: E402

from ansible.module_utils.basic import missing_required_lib  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_module_v4 import BaseModuleV4  # noqa: E402
from ..module_utils.v4.constants import Tasks as TASK_CONSTANTS  # noqa: E402
from ..module_utils.v4.files.api_client import (  # noqa: E402
    get_etag,
    get_mount_targets_api_instance,
)
from ..module_utils.v4.files.helpers import get_mount_target  # noqa: E402
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
    import ntnx_files_py_client as files_sdk  # noqa: E402
except ImportError:

    from ..module_utils.v4.sdk_mock import mock_sdk as files_sdk  # noqa: E402

    SDK_IMP_ERROR = traceback.format_exc()

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
    ip_address_spec = dict(
        ipv4=dict(
            type="dict",
            options=ipv4_address_spec,
            required=False,
            obj=files_sdk.IPv4Address,
        ),
        ipv6=dict(
            type="dict",
            options=ipv6_address_spec,
            required=False,
            obj=files_sdk.IPv6Address,
        ),
    )

    client_blocking_filter_spec = dict(
        vendor_name=dict(type="str", required=False),
        ip_list=dict(
            type="list",
            elements="dict",
            options=ip_address_spec,
            required=False,
            obj=files_sdk.IPAddress,
        ),
        sid_list=dict(type="list", elements="str", required=False),
        uid_list=dict(type="list", elements="int", required=False),
        gid_list=dict(type="list", elements="int", required=False),
        is_all_ips_blocked=dict(type="bool", required=False),
    )

    blocked_clients_spec = dict(
        ro_access_filters=dict(
            type="list",
            elements="dict",
            options=client_blocking_filter_spec,
            required=False,
            obj=files_sdk.ClientBlockingFilter,
        ),
        no_access_filters=dict(
            type="list",
            elements="dict",
            options=client_blocking_filter_spec,
            required=False,
            obj=files_sdk.ClientBlockingFilter,
        ),
        rw_access_filters=dict(
            type="list",
            elements="dict",
            options=client_blocking_filter_spec,
            required=False,
            obj=files_sdk.ClientBlockingFilter,
        ),
    )

    share_acl_spec = dict(
        user_or_group_name=dict(type="str", required=False),
        permission_type=dict(
            type="str",
            required=False,
            choices=["ALLOW", "DENY"],
            obj=files_sdk.PermissionType,
        ),
        access_type=dict(
            type="str",
            required=False,
            choices=["CHANGE", "FULL_CONTROL", "READ"],
            obj=files_sdk.SMBAccessType,
        ),
        sid=dict(type="str", required=False),
    )

    smb_properties_spec = dict(
        is_access_based_enumeration_enabled=dict(type="bool", required=False),
        is_smb3_encryption_enabled=dict(type="bool", required=False),
        is_ca_enabled=dict(type="bool", required=False),
        share_acl=dict(
            type="list",
            elements="dict",
            options=share_acl_spec,
            required=False,
            obj=files_sdk.SMBShareACE,
        ),
    )

    anonymous_identifier_spec = dict(
        uid=dict(type="int", required=False),
        gid=dict(type="int", required=False),
    )

    client_exception_spec = dict(
        access_type=dict(
            type="str",
            required=False,
            choices=["READ_WRITE", "READ_ONLY", "NO_ACCESS"],
            obj=files_sdk.AccessType,
        ),
        squash_type=dict(
            type="str",
            required=False,
            choices=["NONE", "ROOT_SQUASH", "ALL_SQUASH"],
            obj=files_sdk.SquashType,
        ),
        clients=dict(type="str", required=False),
    )

    nfs_properties_spec = dict(
        authentication_type=dict(
            type="str",
            required=False,
            choices=["SYSTEM", "KERBEROS5", "KERBEROS5I", "KERBEROS5P", "NONE"],
            obj=files_sdk.FilesAuthenticationType,
        ),
        anonymous_identifier=dict(
            type="dict",
            options=anonymous_identifier_spec,
            required=False,
            obj=files_sdk.AnonymousIdentifier,
        ),
        squash_type=dict(
            type="str",
            required=False,
            choices=["NONE", "ROOT_SQUASH", "ALL_SQUASH"],
            obj=files_sdk.SquashType,
        ),
        access_type=dict(
            type="str",
            required=False,
            choices=["READ_WRITE", "READ_ONLY", "NO_ACCESS"],
            obj=files_sdk.AccessType,
        ),
        client_exceptions=dict(
            type="list",
            elements="dict",
            options=client_exception_spec,
            required=False,
            obj=files_sdk.ClientException,
        ),
    )

    multi_protocol_properties_spec = dict(
        is_case_sensitive_namespace_enabled=dict(type="bool", required=False),
        is_symlink_creation_enabled=dict(type="bool", required=False),
        is_simultaneous_access_enabled=dict(type="bool", required=False),
    )

    worm_spec = dict(
        worm_type=dict(
            type="str",
            required=False,
            choices=["DISABLED", "SHARE_LEVEL"],
            obj=files_sdk.WormType,
        ),
        cooloff_interval_seconds=dict(type="int", required=False),
        retention_period_seconds=dict(type="int", required=False),
        is_compliance_enabled=dict(type="bool", required=False),
        is_legal_hold_enabled=dict(type="bool", required=False),
    )

    module_args = dict(
        file_server_ext_id=dict(type="str", required=True),
        ext_id=dict(type="str"),
        name=dict(type="str"),
        description=dict(type="str"),
        max_size_gb=dict(type="int"),
        type=dict(
            type="str",
            choices=["GENERAL", "HOMES", "DISTRIBUTED", "STANDARD"],
            obj=files_sdk.MountTargetType,
        ),
        path=dict(type="str"),
        connected_mount_target_path=dict(type="str"),
        is_compression_enabled=dict(type="bool"),
        blocked_file_extensions=dict(type="list", elements="str"),
        protocol=dict(
            type="str",
            choices=["NFS", "SMB", "NONE", "INCOMPATIBLE"],
            obj=files_sdk.MountTargetProtocolType,
        ),
        secondary_protocol=dict(
            type="list",
            elements="str",
            choices=["NFS", "SMB", "NONE", "INCOMPATIBLE"],
        ),
        is_previous_version_enabled=dict(type="bool"),
        is_long_name_enabled=dict(type="bool"),
        is_snapshot_paused=dict(type="bool"),
        workload_type=dict(
            type="str",
            choices=["DEFAULT", "RANDOM", "SEQUENTIAL", "UNDEFINED"],
            obj=files_sdk.MountTargetWorkloadType,
        ),
        parent_mount_target_ext_id=dict(type="str"),
        smb_properties=dict(
            type="dict",
            options=smb_properties_spec,
            obj=files_sdk.SmbProtocolProperties,
        ),
        nfs_properties=dict(
            type="dict",
            options=nfs_properties_spec,
            obj=files_sdk.NfsProtocolProperties,
        ),
        multi_protocol_properties=dict(
            type="dict",
            options=multi_protocol_properties_spec,
            obj=files_sdk.MultiProtocolProperties,
        ),
        blocked_clients=dict(
            type="dict",
            options=blocked_clients_spec,
            obj=files_sdk.BlockedClient,
        ),
        worm_spec=dict(
            type="dict",
            options=worm_spec,
            obj=files_sdk.WormSpec,
        ),
    )
    return module_args


def _find_mount_target_by_name(module, api_instance, file_server_ext_id, name):
    """Return an existing mount target matching ``name`` under ``file_server_ext_id``, or None."""
    try:
        resp = api_instance.list_mount_targets(
            fileServerExtId=file_server_ext_id,
            _filter="name eq '{0}'".format(name),
            _limit=1,
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while checking for existing mount target",
        )
    if resp is None or not getattr(resp, "data", None):
        return None
    return resp.data[0]


def create_mount_target(module, api_instance, result):
    validate_required_params(module, ["name", "type", "protocol"])
    file_server_ext_id = module.params.get("file_server_ext_id")

    sg = SpecGenerator(module)
    default_spec = files_sdk.MountTarget()
    spec, err = sg.generate_spec(obj=default_spec)
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating create mount target spec", **result)

    # check_mode must be fully offline — no idempotency probe, no API call.
    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        return

    existing = _find_mount_target_by_name(
        module, api_instance, file_server_ext_id, module.params.get("name")
    )
    if existing is not None:
        result["ext_id"] = existing.ext_id
        result["response"] = strip_internal_attributes(existing.to_dict())
        result["skipped"] = True
        result["changed"] = False
        result["msg"] = (
            "MountTarget with name '{0}' already exists. Skipping creation.".format(
                module.params.get("name")
            )
        )
        return

    try:
        resp = api_instance.create_mount_target(
            fileServerExtId=file_server_ext_id, body=spec
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while creating mount target",
        )
    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        completed = wait_for_completion(module, task_ext_id)
        result["response"] = strip_internal_attributes(completed.to_dict())
        ext_id = get_entity_ext_id_from_task(
            completed, rel=TASK_CONSTANTS.RelEntityType.MOUNT_TARGET
        )
        if ext_id:
            result["ext_id"] = ext_id
            new_entity = get_mount_target(
                module, api_instance, file_server_ext_id, ext_id
            )
            result["response"] = strip_internal_attributes(new_entity.to_dict())
        else:
            raise_api_exception(
                module=module,
                exception=Exception(
                    "Failed to get entity ext_id from task for Mount Target"
                ),
                msg="Failed to get entity ext_id from task for Mount Target",
            )
    result["changed"] = True


def check_for_idempotency(old_spec_dict, update_spec_dict):
    old_spec_dict = strip_internal_attributes(deepcopy(old_spec_dict))
    update_spec_dict = strip_internal_attributes(deepcopy(update_spec_dict))
    return old_spec_dict == update_spec_dict


def update_mount_target(module, api_instance, result):
    file_server_ext_id = module.params.get("file_server_ext_id")
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id

    old_spec = get_mount_target(module, api_instance, file_server_ext_id, ext_id)
    etag = get_etag(data=old_spec)
    if not etag:
        return module.fail_json(
            msg="Unable to fetch etag for updating mount target", **result
        )
    kwargs = {"if_match": etag}

    sg = SpecGenerator(module)
    update_spec, err = sg.generate_spec(obj=deepcopy(old_spec))
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating update mount target spec", **result)

    if module.check_mode:
        result["response"] = strip_internal_attributes(update_spec.to_dict())
        return

    if check_for_idempotency(old_spec.to_dict(), update_spec.to_dict()):
        result["skipped"] = True
        result["changed"] = False
        result["response"] = strip_internal_attributes(old_spec.to_dict())
        module.exit_json(
            msg="Nothing to change. MountTarget is already in the desired state.",
            **result,
        )

    try:
        resp = api_instance.update_mount_target_by_id(
            fileServerExtId=file_server_ext_id,
            extId=ext_id,
            body=update_spec,
            **kwargs,
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while updating mount target",
        )
    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        wait_for_completion(module, task_ext_id)
        refreshed = get_mount_target(module, api_instance, file_server_ext_id, ext_id)
        result["response"] = strip_internal_attributes(refreshed.to_dict())
    result["changed"] = True


def delete_mount_target(module, api_instance, result):
    file_server_ext_id = module.params.get("file_server_ext_id")
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id

    if module.check_mode:
        result["msg"] = (
            "MountTarget with ext_id:{0} on file server {1} will be deleted.".format(
                ext_id, file_server_ext_id
            )
        )
        return

    try:
        resp = api_instance.delete_mount_target_by_id(
            fileServerExtId=file_server_ext_id, extId=ext_id
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while deleting mount target",
        )
    task_ext_id = resp.data.ext_id
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
            ("state", "present", ("name", "ext_id"), True),
        ],
    )
    if SDK_IMP_ERROR:
        module.fail_json(
            msg=missing_required_lib("ntnx_files_py_client"),
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
    api_instance = get_mount_targets_api_instance(module)
    state = module.params.get("state")

    if state == "present":
        if module.params.get("ext_id"):
            update_mount_target(module, api_instance, result)
        else:
            create_mount_target(module, api_instance, result)
    else:
        delete_mount_target(module, api_instance, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
