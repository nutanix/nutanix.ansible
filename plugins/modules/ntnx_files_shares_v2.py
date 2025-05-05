#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2025, Prem Karat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_files_shares_v2
short_description: Module for file server mount targets
version_added: 2.2.0
description: 'Module for create, update and delete of file server mount target'
options:
  file_server_ext_id:
    description:
      - External ID of the file server.
    type: str
    required: true

  ext_id:
    description:
      - External ID of mount target.
      - If C(state) is present and ext_id exists, it will update.
      - If C(state) is present and ext_id doesn't exists, it will create new with given ID.
      - If C(state) is absent, it will delete.
      - If C(state) is absent, ext_id is mandatory.
    type: str
    required: false

  name:
    description:
      - Mount target name.
    type: str
    required: false

  description:
    description:
      - Mount target description.
    type: str
    required: false

  type:
    description:
      - Supported mount target types.
    type: str
    choices:
      - HOMES
      - GENERAL
      - DISTRIBUTED
      - STANDARD
    required: false

  max_size_gb:
    description:
      - Maximum size of mount target in GiB.
    type: int
    required: false

  protocol:
    description:
      - Protocol type of the mount target.
    type: str
    choices:
      - SMB
      - NFS
      - NONE
      - INCOMPATIBLE
    required: false

  secondary_protocol:
    description:
      -  List of secondary protocol type for the mount target.
    type: list
    elements: str
    choices:
      - SMB
      - NFS
      - NONE
      - INCOMPATIBLE
    required: false

  path:
    description:
      - Path of the nested mount target.
    type: str
    required: false

  connected_mount_target_path:
    description:
      - The Connected Shares feature allows you to connect an empty folder, called a junction folder, in one share to another share.
      - This allows you to share content from any part of a share's directory.
      - For example, when creating a connected share, the connectedMountTargetPath is the path of the junction folder.
    type: str
    required: false

  smb_properties:
    description:
      - SMB protocol properties for mount target.
    type: dict
    required: false
    suboptions:
      is_access_based_enumeration_enabled:
        description:
            - Flag to enable access based enumeration.
        type: bool

      is_smb3_encryption_enabled:
        description:
          -  Flag to enable SMB3 encryption.
        type: bool

      is_ca_enabled:
        description:
          - Flag to enable continuous availability feature for SMB mount targets.
        type: bool

      share_acl:
        description:
          - Access control list(ACL) for SMB share.
        type: list
        elements: dict
        required: false
        suboptions:
          permission_type:
            description:
              - Permission type for SMB share access control entry(ACE).
            type: str
            choices:
              - ALLOW
              - DENY
            required: true
          access_type:
            description:
              - Access type for SMB share access control entry(ACE).
            type: str
            choices:
              - READ
              - CHANGE
              - FULL_CONTROL
            required: true
          user_or_group_name:
            description:
              - User or group name for share permission.
            type: str
            required: true

  nfs_properties:
    description:
      - NFS protocol properties for mount target.
    type: dict
    required: false
    suboptions:
      authentication_type:
        description:
          - Authentication type of the mount target
        type: str
        choices:
          - KERBEROS5
          - NONE
          - SYSTEM
          - KERBEROS5P
          - KERBEROS5I
        required: false

      anonymous_identifier:
        description:
          - Anonymous identifier for the mount target.
        type: dict
        required: false
        suboptions:
          uid:
            description:
              - User identifier. Default value of the user identifier is -2.
            type: int
            required: false
            default: -2

          gid:
            description:
              - Group identifier. Default value of the group identifier is -2.
            type: int
            required: false
            default: -2
      
      squash_type:
        description:
          - Squash type for the mount target.
        type: str
        choices:
          - ROOT_SQUASH
          - ALL_SQUASH
          - NONE
        required: false
      
      access_type:
        description:
          - Access type for the mount target.
        type: str
        choices:
          - READ_ONLY
          - READ_WRITE
          - NO_ACCESS
        required: false
      
      client_exceptions:
        description:
          - Access exception client list of the mount target.
        type: list
        elements: dict
        required: false
        suboptions:
          access_type:
            description:
              - Access type of the mount target.
            type: str
            choices:
              - READ_ONLY
              - READ_WRITE
              - NO_ACCESS
            required: false

          squash_type:
            description:
              - Squash type of the mount target.
            type: str
            choices:
              - ROOT_SQUASH
              - ALL_SQUASH
              - NONE
            required: false

          clients:
            description:
              - Comma-separated client list.
            type: str
            required: false

  multi_protocol_properties:
    description:
      - Properties for multiprotocol supported mount target.
    type: dict
    required: false
    suboptions:
        is_case_sensitive_namespace_enabled:
          description:
            - Flag to enable case sensitive namespace.
          type: bool
          default: false

        is_symlink_creation_enabled:
          description:
            - Flag to enable symlink creation.
          type: bool
          default: false

        is_simultaneous_access_enabled:
          description:
            - Flag to enable simultaneous access to same files across protocols.
          type: bool
          default: false

  blocked_clients:
    description:
      - Blocked clients due to read-only, no access or read-write access.
    type: dict
    required: false
    suboptions:
      ro_access_filters:
        description:
          - Read only access clients
        type: list
        elements: dict
        required: false
        suboptions:
          vendor_name:
            description:
              - Vendor name of the partner server. For ANTIVIRUS type partner server this denotes the icapServiceName
            type: str
            required: false

          ip_list:
            description:
              - IP address list
            type: list
            elements: dict
            required: false
            suboptions:
                ipv4:
                  description:
                    - IPv4 address configuration.
                  type: dict
                  required: false
                  suboptions:
                    value:
                      description:
                        - IPv4 address value.
                      type: str
                      required: true

                    prefix_length:
                      description:
                        - The prefix length of the network to which this host IPv4 address belongs.
                      type: int
                      required: false
                      default: 32
                ipv6:
                  description:
                    - IPv6 address configuration.
                  type: dict
                  required: false
                  suboptions:
                    value:
                      description:
                        - IPv6 address value.
                      type: str
                      required: true

                    prefix_length:
                      description:
                        - The prefix length of the network to which this host IPv6 address belongs.
                      type: int
                      required: false
                      default: 128
          sid_list:
            description:
              - SID list
            type: list
            elements: str
            required: false

          uid_list:
            description:
              - UID list
            type: list
            elements: int
            required: false

          gid_list:
            description:
              - GID list
            type: list
            elements: int
            required: false

          is_all_ips_blocked:
            description:
              - Block all IP addresses.
            type: bool
            default: false
            required: false

      no_access_filters:
        description:
          - No access clients
        type: list
        elements: dict
        required: false
        suboptions:
          vendor_name:
            description:
              - Vendor name for the client blocking filter.
            type: str
            required: false

          ip_list:
            description:
              - IP address list
            type: list
            elements: dict
            required: false
            suboptions:
                ipv4:
                  description:
                    - IPv4 address configuration.
                  type: dict
                  required: false
                  suboptions:
                    value:
                      description:
                        - IPv4 address value.
                      type: str
                      required: true

                    prefix_length:
                      description:
                        - The prefix length of the network to which this host IPv4 address belongs.
                      type: int
                      required: false
                      default: 32
                ipv6:
                  description:
                    - IPv6 address configuration.
                  type: dict
                  required: false
                  suboptions:
                    value:
                      description:
                        - IPv6 address value.
                      type: str
                      required: true

                    prefix_length:
                      description:
                        - The prefix length of the network to which this host IPv6 address belongs.
                      type: int
                      required: false
                      default: 128
          sid_list:
            description:
              - SID list
            type: list
            elements: str
            required: false

          uid_list:
            description:
              - UID list
            type: list
            elements: int
            required: false

          gid_list:
            description:
              - GID list
            type: list
            elements: int
            required: false

          is_all_ips_blocked:
            description:
              - Block all IP addresses.
            type: bool
            default: false
            required: false

      rw_access_filters:
        description:
          - Read and write access clients
        type: list
        elements: dict
        required: false
        suboptions:
          vendor_name:
            description:
              - Vendor name of the partner server. For ANTIVIRUS type partner server this denotes the icapServiceName
            type: str
            required: false

          ip_list:
            description:
              - IP address list
            type: list
            elements: dict
            required: false
            suboptions:
                ipv4:
                  description:
                    - IPv4 address configuration.
                  type: dict
                  required: false
                  suboptions:
                    value:
                      description:
                        - IPv4 address value.
                      type: str
                      required: true

                    prefix_length:
                      description:
                        - The prefix length of the network to which this host IPv4 address belongs.
                      type: int
                      required: false
                      default: 32
                ipv6:
                  description:
                    - IPv6 address configuration.
                  type: dict
                  required: false
                  suboptions:
                    value:
                      description:
                        - IPv6 address value.
                      type: str
                      required: true

                    prefix_length:
                      description:
                        - The prefix length of the network to which this host IPv6 address belongs.
                      type: int
                      required: false
                      default: 128
          sid_list:
            description:
              - SID list
            type: list
            elements: str
            required: false

          uid_list:
            description:
              - UID list
            type: list
            elements: int
            required: false

          gid_list:
            description:
              - GID list
            type: list
            elements: int
            required: false

          is_all_ips_blocked:
            description:
              - Block all IP addresses.
            type: bool
            default: false
            required: false

  is_long_name_enabled:
    description:
      - Enable long name support.
    type: bool
    required: false
    default: false

  status_type:
    description:
      - Status type.
      - It's not supported from this module.
    type: str
    choices:
      - AVAILABLE
      - UNAVAILABLE
    required: false

  worm_spec:
    description:
      - WORM share details.
    type: dict
    required: false
    suboptions:
        worm_type:
          description:
            - WORM type for share.
          type: str
          choices:
            - SHARE_LEVEL
            - DISABLED
          required: false

        cooloff_interval_seconds:
          description:
            -  Cooloff interval in seconds for WORM share.
          type: int
          required: false
          default: 600

        retention_period_seconds:
          description:
            - Retention period in seconds for WORM share.
          type: int
          required: false
          default: 31449600

  workload_type:
    description:
      - Supported mount target workload types.
    type: str
    choices:
      - RANDOM
      - DEFAULT
      - SEQUENTIAL
      - UNDEFINED
    required: false

  is_snapshot_paused:
    description:
      - Pause snapshot operations on share.
    type: bool
    required: false

  is_compression_enabled:
    description:
      - Flag to enable compression.
    type: bool
    required: false

  blocked_file_extensions:
    description:
      - List of blocked file extensions.
    type: list
    elements: str
    required: false

  is_previous_version_enabled:
    description:
      - Flag to enable windows previous version.
    type: bool
    required: false
    default: false

extends_documentation_fragment:
      - nutanix.ncp.ntnx_credentials
      - nutanix.ncp.ntnx_operations_v2
author:
 - Prem Karat (@premkarat)
 - Pradeepsingh Bhati (@bhati-pradeep)
 - Alaa Bishtawi (@alaa-bish)
 - Abhinav Bansal (@abhinavbansal29)
"""
EXAMPLES = r"""
"""

RETURN = r"""
"""
import json  # noqa: E402
import traceback  # noqa: E402
import warnings  # noqa: E402
from copy import deepcopy  # noqa: E402

FILES_SDK_IMP_ERROR = None
try:
    import ntnx_files_py_client as files_sdk  # noqa: E402
except ImportError:
    from ansible.module_utils.basic import missing_required_lib  # noqa: E402

    from ..module_utils.v4.sdk_mock import mock_sdk as files_sdk  # noqa: E402

    FILES_SDK_IMP_ERROR = traceback.format_exc()


from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.files.base_module import FilesBaseModule  # noqa: E402
from ..module_utils.v4.files.api_client import (  # noqa: E402
    get_etag,
    get_files_api_client,
)
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
)

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    worm_spec = dict(
        worm_type=dict(type="str", choices=["SHARE_LEVEL", "DISABLED"], required=False),
        cooloff_interval_seconds=dict(type="int", required=False, default=600),
        retention_period_seconds=dict(type="int", required=False, default=31449600),
    )
    ipv4_address = dict(
        value=dict(type="str", required=True),
        prefix_length=dict(type="int", required=False, default=32),
    )
    ipv6_address = dict(
        value=dict(type="str", required=True),
        prefix_length=dict(type="int", required=False, default=128),
    )
    ip_address = dict(
        ipv4=dict(
            type="dict", options=ipv4_address, obj=files_sdk.IPv4Address, required=False
        ),
        ipv6=dict(
            type="dict", options=ipv6_address, obj=files_sdk.IPv6Address, required=False
        ),
    )
    client_blocking_filter = dict(
        vendor_name=dict(type="str", required=False),
        ip_list=dict(
            type="list",
            elements="dict",
            options=ip_address,
            obj=files_sdk.IPAddress,
            required=False,
        ),
        sid_list=dict(type="list", elements="str", required=False),
        uid_list=dict(type="list", elements="int", required=False),
        gid_list=dict(type="list", elements="int", required=False),
        is_all_ips_blocked=dict(type="bool", default=False, required=False),
    )
    blocked_clients_spec = dict(
        ro_access_filters=dict(
            type="list",
            elements="dict",
            options=client_blocking_filter,
            obj=files_sdk.ClientBlockingFilter,
            required=False,
        ),
        no_access_filters=dict(
            type="list",
            elements="dict",
            options=client_blocking_filter,
            obj=files_sdk.ClientBlockingFilter,
            required=False,
        ),
        rw_access_filters=dict(
            type="list",
            elements="dict",
            options=client_blocking_filter,
            obj=files_sdk.ClientBlockingFilter,
            required=False,
        ),
    )
    multi_protocol_properties = dict(
        is_case_sensitive_namespace_enabled=dict(type="bool", default=False),
        is_symlink_creation_enabled=dict(type="bool", default=False),
        is_simultaneous_access_enabled=dict(type="bool", default=False),
    )
    smb_properties = dict(
        is_access_based_enumeration_enabled=dict(type="bool"),
        is_smb3_encryption_enabled=dict(type="bool"),
        is_ca_enabled=dict(type="bool"),
        share_acl=dict(
            type="list",
            elements="dict",
            options=smb_share_acl,
            obj=files_sdk.SMBShareACE,
            required=False,
        ),
    )
    anonymous_identifier = dict(
        uid=dict(type="int", required=False, default=-2), gid=dict(type="int", required=False, default=-2)
    )
    squash_type_spec = dict(
        type="str",
        choices=["ROOT_SQUASH", "ALL_SQUASH", "NONE"],
        required=False,
    )
    access_type_spec = dict(
            type="str",
            choices=["READ_ONLY", "READ_WRITE", "NO_ACCESS"],
            required=False,
        )
    client_exceptions_spec = dict(
        access_type=access_type_spec,
        squash_type=squash_type_spec,
        clients=dict(
            type="str",
            required=False,
        ),
    )
        
    nfs_properties = dict(
        authentication_type=dict(
            type="str",
            choices=["KERBEROS5", "NONE", "SYSTEM", "KERBEROS5P", "KERBEROS5I"],
            required=False,
        ),
        anonymous_identifier=dict(
            type="dict",
            options=anonymous_identifier,
            obj=files_sdk.AnonymousIdentifier,
            required=False,
        ),
        squash_type=squash_type_spec,
        access_type=access_type_spec,
        client_exceptions=dict(
            type="list",
            elements="dict",
            options=client_exceptions_spec,
            obj=files_sdk.ClientException,
            required=False,
        ),
    )
    smb_share_acl = dict(
        permission_type=dict(type="str", choices=["ALLOW", "DENY"], required=True),
        access_type=dict(
            type="str", choices=["READ", "CHANGE", "FULL_CONTROL"], required=True
        ),
        user_or_group_name=dict(type="str", required=True),
    )
    module_args = dict(
        file_server_ext_id=dict(type="str", required=True),
        ext_id=dict(type="str", required=False),
        name=dict(type="str", required=False),
        description=dict(type="str", required=False),
        type=dict(
            type="str",
            choices=["HOMES", "GENERAL", "DISTRIBUTED", "STANDARD"],
            required=False,
        ),
        max_size_gb=dict(type="int", required=False),
        protocol=dict(type="str", choices=["SMB", "NFS", "NONE", "INCOMPATIBLE"], required=False),
        secondary_protocol=dict(
            type="list", elements="str", choices=["SMB", "NFS", "NONE", "INCOMPATIBLE"], required=False
        ),
        path=dict(type="str", required=False),
        connected_mount_target_path=dict(type="str", required=False),
        smb_properties=dict(
            type="dict",
            options=smb_properties,
            obj=files_sdk.SmbProtocolProperties,
            required=False,
        ),
        nfs_properties=dict(
            type="dict",
            options=nfs_properties,
            obj=files_sdk.NfsProtocolProperties,
            required=False,
        ),
        multi_protocol_properties=dict(
            type="dict",
            options=multi_protocol_properties,
            obj=files_sdk.MultiProtocolProperties,
            required=False,
        ),
        blocked_clients=dict(
            type="dict",
            options=blocked_clients_spec,
            obj=files_sdk.BlockedClient,
            required=False,
        ),
        is_long_name_enabled=dict(type="bool", required=False, default=False),
        status_type=dict(
            type="str", choices=["AVAILABLE", "UNAVAILABLE"], required=False
        ),
        worm_spec=dict(
            type="dict", options=worm_spec, obj=files_sdk.WormSpec, required=False
        ),
        workload_type=dict(
            type="str", choices=["RANDOM", "DEFAULT", "SEQUENTIAL", "UNDEFINED"], required=False
        ),
        is_snapshot_paused=dict(type="bool", required=False),
        is_compression_enabled=dict(type="bool", required=False),
        blocked_file_extensions=dict(type="list", elements="str", required=False),
        is_previous_version_enabled=dict(type="bool", required=False, default=False),
    )
    return module_args


_SHARES_API = None


def get_shares_api(module):
    global _SHARES_API
    if not _SHARES_API:
        client = get_files_api_client(module)
        _SHARES_API = files_sdk.MountTargetsApi(api_client=client)

    return _SHARES_API


def check_if_share_exists(module, ext_id, file_server_ext_id):
    shares = get_shares_api(module)
    try:
        shares.get_mount_target_by_uuid(
            extId=ext_id, fileServerExtId=file_server_ext_id
        )
    except Exception as e:
        error = json.loads(e.body).get("data", {}).get("error", [])
        if error and len(error) == 1:
            if error[0].get("errorGroup") == "ENTITY_NOT_FOUND":
                return False
        else:
            raise_api_exception(
                module=module,
                exception=e,
                msg="Api Exception raised while fetching shares info",
            )
    return True


def get_share_by_name(module, name, file_server_ext_id):
    shares = get_shares_api(module)
    filter = "name eq '{0}'".format(name)
    resp = None
    try:
        resp = shares.get_all_mount_targets(
            fileServerExtId=file_server_ext_id, _filter=filter
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching share by name {0}".format(name),
        )

    if not resp.get("data", []):
        return None, "Share with name {0} not found".format(name)

    return resp.data[0], None


def get_share(module, ext_id, file_server_ext_id):
    shares = get_shares_api(module)
    try:
        return shares.get_mount_target_by_uuid(
            fileServerExtId=file_server_ext_id, extId=ext_id
        ).data
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching file server share",
        )


def create_or_update_share(module, result):
    ext_id = module.params.get("ext_id")
    file_server_ext_id = module.params.get("file_server_ext_id")
    result["file_server_ext_id"] = file_server_ext_id

    if ext_id and check_if_share_exists(
        module, ext_id=ext_id, file_server_ext_id=file_server_ext_id
    ):
        update_share(module, result)
    else:
        create_share(module, result)


def create_share(module, result):
    shares = get_shares_api(module)
    sg = SpecGenerator(module)
    default_spec = files_sdk.MountTarget()
    spec, err = sg.generate_spec(obj=default_spec)
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating share create spec", **result)
    spec.state = None
    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        return

    resp = None
    file_server_ext_id = module.params.get("file_server_ext_id")
    try:
        resp = shares.create_mount_targets(
            fileServerExtId=file_server_ext_id, body=spec
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while creating file server share",
        )

    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if spec.ext_id:
        result["share_ext_id"] = spec.ext_id

    result["changed"] = True


def update_share(module, result):
    ext_id = module.params.get("ext_id")
    file_server_ext_id = module.params.get("file_server_ext_id")

    current_spec = get_share(
        module=module, ext_id=ext_id, file_server_ext_id=file_server_ext_id
    )

    sg = SpecGenerator(module)
    update_spec, err = sg.generate_spec(obj=deepcopy(current_spec))
    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed generating file server share update spec", **result
        )

    # state is also used internally for lifecycle
    update_spec.state = current_spec.state

    if not update_spec.parent_mount_target_ext_id:
        update_spec.parent_mount_target_ext_id = None

    if module.check_mode:
        result["response"] = strip_internal_attributes(update_spec.to_dict())
        return

    resp = None
    shares = get_shares_api(module)
    try:
        resp = shares.update_mount_targets(
            extId=ext_id, fileServerExtId=file_server_ext_id, body=update_spec
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while updating file server share",
        )

    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    result["changed"] = True


def delete_share(module, result):
    ext_id = module.params.get("ext_id")
    file_server_ext_id = module.params.get("file_server_ext_id")

    shares = get_shares_api(module)
    current_spec = None
    try:
        current_spec = shares.get_mount_target_by_uuid(
            extId=ext_id, fileServerExtId=file_server_ext_id
        ).data
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching file server share",
        )

    etag = get_etag(current_spec)

    resp = None
    shares = get_shares_api(module)
    force = module.params.get("force_delete", False)
    try:
        resp = shares.delete_mount_target_by_id(
            extId=ext_id, fileServerExtId=file_server_ext_id, force=force, if_match=etag
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while deleting file server share",
        )

    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    result["changed"] = True


def run_module():
    module = FilesBaseModule(
        argument_spec=get_module_spec(),
        supports_check_mode=True,
    )

    if FILES_SDK_IMP_ERROR:
        module.fail_json(
            missing_required_lib("ntnx_files_py_client"), FILES_SDK_IMP_ERROR
        )

    remove_param_with_none_value(module.params)

    result = {
        "changed": False,
        "error": None,
        "response": None,
        "ext_id": None,
        "file_server_ext_id": None,
    }

    if module.params.get("state") == "present":
        if module.params.get("ext_id"):
            # Update
            create_or_update_share(module, result)
        else:
            # Create
            pass
    else:
        delete_share(module, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
