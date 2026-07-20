#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_monitoring_collect_log_v2
short_description: Trigger a Logbay log collection on a Nutanix cluster
version_added: 2.7.0
description:
    - Trigger an asynchronous log collection (Logbay bundle) on a Nutanix
      cluster via the Monitoring / Serviceability v4 API.
    - The API is invoked as an action
      C(POST /api/monitoring/v4.0/serviceability/clusters/{extId}/$actions/collect-logs)
      and returns a task reference; the module optionally waits for the task
      to complete.
    - This module uses PC v4 APIs based SDKs.
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the
      user performing the operation.
    - >-
      B(Collect logs) -
      Required Roles: Prism Admin, Super Admin, or any role granting
      "Collect Logs" permission on the target cluster.
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=monitoring)"
options:
    state:
        description:
            - State of the module.
            - If state is present, the module will trigger a log collection.
            - Any other value will fail.
        type: str
        choices:
            - present
        default: present
    cluster_ext_id:
        description:
            - External ID (UUID) of the Nutanix cluster on which to collect
              logs. This maps to C(extId) path parameter of the collect-logs
              action.
        type: str
        required: true
    start_time:
        description:
            - RFC 3339 timestamp marking the start of the log collection
              window (e.g. C(2026-07-19T00:00:00Z)).
            - Must precede C(end_time) and be within the last three months.
            - Required when C(state=present).
        type: str
        required: false
    end_time:
        description:
            - RFC 3339 timestamp marking the end of the log collection window
              (e.g. C(2026-07-20T00:00:00Z)).
            - Must be greater than C(start_time) and within the last three
              months.
            - Required when C(state=present).
        type: str
        required: false
    include_tags:
        description:
            - Logbay tag IDs to include in this collection. The list of tag
              IDs available on the cluster can be fetched with the
              C(ntnx_collect_logs_info_v2) module (GET tags).
            - If empty, all tags are collected which may take considerably
              longer. Nutanix recommends providing at least one tag.
        type: list
        elements: str
        required: false
    should_anonymize:
        description:
            - When true, sensitive data (IPs, hostnames, ...) will be masked
              in the collected bundle.
        type: bool
        required: false
        default: false
    node_ip_list:
        description:
            - List of node IPv4 addresses in the cluster from which logs will
              be collected. If unset, logs are collected from all nodes.
        type: list
        elements: dict
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
    should_collect_from_disabled_node:
        description:
            - When true, logs will also be collected from nodes where
              services are down. This flag is not supported on Prism
              Central and is only applicable on PE clusters.
        type: bool
        required: false
        default: false
    exclude_tags:
        description:
            - Logbay tag IDs to exclude from this collection. Cannot be
              used together with C(include_tags) for the same tag.
        type: list
        elements: str
        required: false
    archive_opts:
        description:
            - Archive options describing where the collected log bundle
              should be uploaded and, optionally, the archive name.
            - Required when C(state=present).
        type: dict
        required: false
        suboptions:
            archive_name:
                description:
                    - Optional archive file name (without extension) for the
                      generated bundle.
                type: str
                required: false
            upload_params:
                description:
                    - Upload destination configuration. Exactly one of
                      C(local), C(ntnx_server), C(custom_server) or
                      C(storage_container) must be provided.
                type: dict
                required: false
                suboptions:
                    local:
                        description:
                            - Store the archive on the local CVM disk. The
                              bundle can then be downloaded via the
                              C(downloadLogsById) API.
                        type: dict
                        required: false
                        suboptions:
                            path:
                                description:
                                    - Optional directory path on the CVM
                                      where the bundle will be stored.
                                type: str
                                required: false
                    ntnx_server:
                        description:
                            - Upload the archive to the Nutanix support
                              FTP/SFTP servers, attaching it to an existing
                              Nutanix support case.
                        type: dict
                        required: false
                        suboptions:
                            case_number:
                                description:
                                    - Nutanix Support case number to which
                                      the archive should be attached.
                                type: int
                                required: true
                            protocol:
                                description:
                                    - Protocol used to reach the Nutanix
                                      support server.
                                type: str
                                required: false
                                choices:
                                    - FTP
                                    - SFTP
                    custom_server:
                        description:
                            - Upload the archive to a customer-managed
                              FTP or SFTP server.
                        type: dict
                        required: false
                        suboptions:
                            protocol:
                                description:
                                    - Protocol used to reach the custom
                                      upload server.
                                type: str
                                required: true
                                choices:
                                    - FTP
                                    - SFTP
                            server_address:
                                description:
                                    - Address of the custom upload server.
                                      Provide either an IPv4/IPv6 address
                                      or an FQDN.
                                type: dict
                                required: true
                                suboptions:
                                    ipv4:
                                        description:
                                            - IPv4 address of the server.
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
                                            - IPv6 address of the server.
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
                                            - Fully-qualified domain name of
                                              the server.
                                        type: dict
                                        required: false
                                        suboptions:
                                            value:
                                                description:
                                                    - The FQDN value.
                                                type: str
                                                required: true
                            port:
                                description:
                                    - TCP port on which the upload server is
                                      reachable.
                                type: int
                                required: false
                            credential:
                                description:
                                    - Credentials used to authenticate against
                                      the custom upload server.
                                type: dict
                                required: false
                                suboptions:
                                    user_name:
                                        description:
                                            - Username used to authenticate.
                                        type: str
                                        required: false
                                    password:
                                        description:
                                            - Password used to authenticate.
                                        type: str
                                        required: false
                                    key_file_path:
                                        description:
                                            - Path to a private key file used
                                              for SFTP key-based auth.
                                        type: str
                                        required: false
                            path:
                                description:
                                    - Remote directory path on the upload
                                      server where the archive will be
                                      written.
                                type: str
                                required: false
                    storage_container:
                        description:
                            - Upload the archive to a Nutanix storage
                              container. This avoids consuming space on the
                              local C(/home) partition of the CVM.
                            - Not supported for Prism Central local storage
                              containers.
                        type: dict
                        required: false
                        suboptions:
                            ip_address:
                                description:
                                    - IPv4 address of the storage container.
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
                            port:
                                description:
                                    - TCP port used to reach the storage
                                      container.
                                type: int
                                required: false
                            credential:
                                description:
                                    - Credentials used to authenticate against
                                      the storage container.
                                type: dict
                                required: false
                                suboptions:
                                    user_name:
                                        description:
                                            - Username used to authenticate.
                                        type: str
                                        required: false
                                    password:
                                        description:
                                            - Password used to authenticate.
                                        type: str
                                        required: false
                                    key_file_path:
                                        description:
                                            - Path to a private key file for
                                              key-based auth.
                                        type: str
                                        required: false
                            path:
                                description:
                                    - Path (mount point / directory) inside
                                      the storage container.
                                type: str
                                required: false
    description:
        description:
            - Free-form description attached to the log-collection task.
        type: str
        required: false
    tag_opts:
        description:
            - Additional tag-specific options passed down to the underlying
              collection layer.
        type: dict
        required: false
        suboptions:
            msp_opts:
                description:
                    - MSP (Microservices Platform) specific options. Used in
                      combination with the C(msp) Logbay tag.
                type: dict
                required: false
                suboptions:
                    cluster_ext_ids:
                        description:
                            - List of MSP cluster external IDs to collect
                              logs from.
                        type: list
                        elements: str
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
- name: Trigger a log collection with LOCAL upload
  nutanix.ncp.ntnx_monitoring_collect_log_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    cluster_ext_id: "0006361b-6855-3644-7458-2268f8ffb2bd"
    start_time: "2026-07-19T00:00:00Z"
    end_time: "2026-07-19T01:00:00Z"
    include_tags:
      - "cluster_health_logs"
    should_anonymize: false
    description: "Collect logs from cluster - Ansible"
    archive_opts:
      archive_name: "ansible_bundle"
      upload_params:
        local: {}
  register: result

- name: Trigger a log collection restricted to specific nodes
  nutanix.ncp.ntnx_monitoring_collect_log_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    cluster_ext_id: "0006361b-6855-3644-7458-2268f8ffb2bd"
    start_time: "2026-07-19T00:00:00Z"
    end_time: "2026-07-19T01:00:00Z"
    node_ip_list:
      - value: "10.10.10.11"
      - value: "10.10.10.12"
    exclude_tags:
      - "file_server_logs"
    archive_opts:
      upload_params:
        local: {}

- name: Trigger a log collection and upload to Nutanix support case (SFTP)
  nutanix.ncp.ntnx_monitoring_collect_log_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    cluster_ext_id: "0006361b-6855-3644-7458-2268f8ffb2bd"
    start_time: "2026-07-19T00:00:00Z"
    end_time: "2026-07-19T01:00:00Z"
    include_tags:
      - "cluster_health_logs"
    archive_opts:
      archive_name: "support_bundle"
      upload_params:
        ntnx_server:
          case_number: 12345678
          protocol: SFTP
"""

RETURN = r"""
response:
    description:
        - Response for the collect-logs action.
        - Task details are returned when C(wait) is true; otherwise the
          initial task reference is returned.
    returned: always
    type: dict
    sample:
        {
            "app_name": null,
            "batch_summary": null,
            "cluster_ext_ids": [
                "0006555e-4e63-4a5e-185b-ac1f6b6f97e2"
            ],
            "completed_time": "2026-07-20T15:19:41.481209+00:00",
            "completion_details": [
                {
                    "name": "LogExtId",
                    "value": "7ca1ec29-5b87-4521-592d-be2732ecc94a"
                }
            ],
            "created_time": "2026-07-20T15:19:40.792880+00:00",
            "entities_affected": [
                {
                    "ext_id": "0006555e-4e63-4a5e-185b-ac1f6b6f97e2",
                    "name": "auto_cluster_prod_36acf9b012ca",
                    "rel": "clustermgmt:config:cluster"
                }
            ],
            "error_messages": null,
            "ext_id": "ZXJnb24=:7294b815-f3a4-43b9-6927-5335c78c825a",
            "is_background_task": false,
            "is_cancelable": false,
            "last_updated_time": "2026-07-20T15:19:41.481208+00:00",
            "legacy_error_message": null,
            "number_of_entities_affected": 1,
            "number_of_subtasks": 1,
            "operation": "LogCollectionFromPC",
            "operation_description": "Collect logs",
            "owned_by": {
                "ext_id": "00000000-0000-0000-0000-000000000000",
                "name": "admin"
            },
            "parent_task": null,
            "progress_percentage": 100,
            "started_time": "2026-07-20T15:19:40.821061+00:00",
            "status": "SUCCEEDED",
            "sub_steps": null,
            "sub_tasks": [
                {
                    "ext_id": "ZXJnb24=:5dcdf68c-9b7f-444e-72fc-851ea50ab5ce",
                    "href": "https://10.44.76.28:9440/api/prism/v4.3/config/tasks/ZXJnb24=:5dcdf68c-9b7f-444e-72fc-851ea50ab5ce",
                    "rel": "subtask"
                }
            ],
            "warnings": null
        }

changed:
    description: Whether the module made any change on the cluster.
    returned: always
    type: bool
    sample: true

failed:
    description: Whether the module failed.
    returned: always
    type: bool
    sample: false

ext_id:
    description: External ID of the target cluster.
    returned: always
    type: str
    sample: "0006555e-4e63-4a5e-185b-ac1f6b6f97e2"

task_ext_id:
    description: External ID of the collect-logs task.
    returned: always
    type: str
    sample: "ZXJnb24=:7294b815-f3a4-43b9-6927-5335c78c825a"

msg:
    description: Status or error message set by the module.
    returned: When there is an error
    type: str
    sample: "Api Exception raised while collecting logs"

error:
    description: Detailed error information if the operation failed.
    returned: When an error occurs
    type: str
"""

import traceback  # noqa: E402
import warnings  # noqa: E402

from ansible.module_utils.basic import missing_required_lib  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_module_v4 import BaseModuleV4  # noqa: E402
from ..module_utils.v4.monitoring.api_client import (  # noqa: E402
    get_cluster_logs_api_instance,
)
from ..module_utils.v4.prism.tasks import wait_for_completion  # noqa: E402
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
    validate_required_params,
)

SDK_IMP_ERROR = None
try:
    import ntnx_monitoring_py_client as monitoring_sdk  # noqa: E402
except ImportError:

    from ..module_utils.v4.sdk_mock import mock_sdk as monitoring_sdk  # noqa: E402

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
        value=dict(type="str", required=True),
    )

    ip_or_fqdn_spec = dict(
        ipv4=dict(
            type="dict",
            options=ipv4_address_spec,
            obj=monitoring_sdk.IPv4Address,
        ),
        ipv6=dict(
            type="dict",
            options=ipv6_address_spec,
            obj=monitoring_sdk.IPv6Address,
        ),
        fqdn=dict(
            type="dict",
            options=fqdn_spec,
            obj=monitoring_sdk.FQDN,
        ),
    )

    credential_spec = dict(
        user_name=dict(type="str"),
        password=dict(type="str", no_log=True),
        key_file_path=dict(type="str", no_log=True),
    )

    local_upload_spec = dict(
        path=dict(type="str"),
    )

    ntnx_server_upload_spec = dict(
        case_number=dict(type="int", required=True),
        protocol=dict(
            type="str",
            choices=["FTP", "SFTP"],
            obj=monitoring_sdk.ServerUploadProtocol,
        ),
    )

    custom_server_upload_spec = dict(
        protocol=dict(
            type="str",
            required=True,
            choices=["FTP", "SFTP"],
            obj=monitoring_sdk.ServerUploadProtocol,
        ),
        server_address=dict(
            type="dict",
            required=True,
            options=ip_or_fqdn_spec,
            obj=monitoring_sdk.IPAddressOrFQDN,
        ),
        port=dict(type="int"),
        credential=dict(
            type="dict",
            options=credential_spec,
            obj=monitoring_sdk.Credential,
            no_log=False,
        ),
        path=dict(type="str"),
    )

    storage_container_upload_spec = dict(
        ip_address=dict(
            type="dict",
            options=ipv4_address_spec,
            obj=monitoring_sdk.IPv4Address,
        ),
        port=dict(type="int"),
        credential=dict(
            type="dict",
            options=credential_spec,
            obj=monitoring_sdk.Credential,
            no_log=False,
        ),
        path=dict(type="str"),
    )

    upload_params_spec = dict(
        local=dict(
            type="dict",
            options=local_upload_spec,
            obj=monitoring_sdk.LocalUploadParams,
        ),
        ntnx_server=dict(
            type="dict",
            options=ntnx_server_upload_spec,
            obj=monitoring_sdk.NtnxServerUploadParams,
        ),
        custom_server=dict(
            type="dict",
            options=custom_server_upload_spec,
            obj=monitoring_sdk.CustomServerUploadParams,
        ),
        storage_container=dict(
            type="dict",
            options=storage_container_upload_spec,
            obj=monitoring_sdk.StorageContainerUploadParams,
        ),
    )

    archive_opts_spec = dict(
        archive_name=dict(type="str"),
        upload_params=dict(
            type="dict",
            options=upload_params_spec,
        ),
    )

    msp_opts_spec = dict(
        cluster_ext_ids=dict(type="list", elements="str"),
    )

    tag_opts_spec = dict(
        msp_opts=dict(
            type="dict",
            options=msp_opts_spec,
            obj=monitoring_sdk.MspOpts,
        ),
    )

    module_args = dict(
        state=dict(type="str", default="present", choices=["present"]),
        cluster_ext_id=dict(type="str", required=True),
        start_time=dict(type="str"),
        end_time=dict(type="str"),
        include_tags=dict(type="list", elements="str"),
        should_anonymize=dict(type="bool", default=False),
        node_ip_list=dict(
            type="list",
            elements="dict",
            options=ipv4_address_spec,
            obj=monitoring_sdk.IPv4Address,
        ),
        should_collect_from_disabled_node=dict(type="bool", default=False),
        exclude_tags=dict(type="list", elements="str"),
        archive_opts=dict(
            type="dict",
            options=archive_opts_spec,
            obj=monitoring_sdk.ArchiveOpts,
        ),
        description=dict(type="str"),
        tag_opts=dict(
            type="dict",
            options=tag_opts_spec,
            obj=monitoring_sdk.TagOpts,
        ),
    )

    return module_args


def _build_upload_params(module):
    """Resolve the oneOf upload_params user input into an SDK model instance.

    The SDK's ArchiveOpts.upload_params is a discriminated union across
    LocalUploadParams / NtnxServerUploadParams / CustomServerUploadParams /
    StorageContainerUploadParams. Ansible's argument spec cannot model that
    OneOf directly, so we accept a dict with named sub-keys (one per variant)
    and translate exactly one populated key into the corresponding SDK object.
    """
    archive_opts = module.params.get("archive_opts") or {}
    upload_params = archive_opts.get("upload_params") or {}
    populated = {k: v for k, v in upload_params.items() if v is not None}
    if not populated:
        return None
    if len(populated) > 1:
        module.fail_json(
            msg=(
                "archive_opts.upload_params must contain exactly one of "
                "'local', 'ntnx_server', 'custom_server' or "
                "'storage_container'. Got: {0}".format(sorted(populated))
            )
        )
    key, value = next(iter(populated.items()))
    sg = SpecGenerator(module)
    if key == "local":
        obj = monitoring_sdk.LocalUploadParams()
        module_args = get_module_spec()["archive_opts"]["options"]["upload_params"][
            "options"
        ]["local"]["options"]
    elif key == "ntnx_server":
        obj = monitoring_sdk.NtnxServerUploadParams()
        module_args = get_module_spec()["archive_opts"]["options"]["upload_params"][
            "options"
        ]["ntnx_server"]["options"]
    elif key == "custom_server":
        obj = monitoring_sdk.CustomServerUploadParams()
        module_args = get_module_spec()["archive_opts"]["options"]["upload_params"][
            "options"
        ]["custom_server"]["options"]
    else:
        obj = monitoring_sdk.StorageContainerUploadParams()
        module_args = get_module_spec()["archive_opts"]["options"]["upload_params"][
            "options"
        ]["storage_container"]["options"]
    spec, err = sg.generate_spec(obj=obj, attr=value, module_args=module_args)
    if err:
        module.fail_json(msg="Failed generating upload_params spec: {0}".format(err))
    return spec


def _build_collect_logs_spec(module):
    """Construct the LogCollectionSpec body for the collect-logs API."""
    upload = _build_upload_params(module)

    archive_opts_in = module.params.get("archive_opts") or {}
    archive_opts = monitoring_sdk.ArchiveOpts(
        archive_name=archive_opts_in.get("archive_name"),
        upload_params=upload,
    )

    tag_opts = None
    tag_opts_in = module.params.get("tag_opts")
    if tag_opts_in:
        msp_opts = None
        msp_in = tag_opts_in.get("msp_opts") or {}
        msp_cluster_ext_ids = msp_in.get("cluster_ext_ids")
        # The API rejects an empty MspOpts.cluster_ext_ids list (min=1); only
        # attach msp_opts when the user provided at least one cluster ext_id.
        if msp_cluster_ext_ids:
            msp_opts = monitoring_sdk.MspOpts(cluster_ext_ids=msp_cluster_ext_ids)
        if msp_opts is not None:
            tag_opts = monitoring_sdk.TagOpts(msp_opts=msp_opts)

    node_ip_list = None
    raw_nodes = module.params.get("node_ip_list")
    if raw_nodes:
        node_ip_list = [
            monitoring_sdk.IPv4Address(
                value=n.get("value"), prefix_length=n.get("prefix_length")
            )
            for n in raw_nodes
        ]

    spec_kwargs = dict(
        start_time=module.params.get("start_time"),
        end_time=module.params.get("end_time"),
        include_tags=module.params.get("include_tags"),
        should_anonymize=module.params.get("should_anonymize"),
        node_ip_list=node_ip_list,
        should_collect_from_disabled_node=module.params.get(
            "should_collect_from_disabled_node"
        ),
        exclude_tags=module.params.get("exclude_tags"),
        archive_opts=archive_opts,
        tag_opts=tag_opts,
    )
    if module.params.get("description") is not None:
        spec_kwargs["description"] = module.params.get("description")

    return monitoring_sdk.LogCollectionSpec(**spec_kwargs)


def collect_logs(module, api_instance, result):
    """Trigger a log-collection action on the target cluster."""
    validate_required_params(
        module, ["cluster_ext_id", "start_time", "end_time", "archive_opts"]
    )
    ext_id = module.params.get("cluster_ext_id")
    result["ext_id"] = ext_id

    spec = _build_collect_logs_spec(module)

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        return

    resp = None
    try:
        resp = api_instance.collect_logs(extId=ext_id, body=spec)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while collecting logs",
        )
    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        task = wait_for_completion(module, task_ext_id)
        result["response"] = strip_internal_attributes(task.to_dict())
    result["changed"] = True


def run_module():
    module = BaseModuleV4(
        argument_spec=get_module_spec(),
        supports_check_mode=True,
    )
    if SDK_IMP_ERROR:
        module.fail_json(
            msg=missing_required_lib("ntnx_monitoring_py_client"),
            exception=SDK_IMP_ERROR,
        )

    remove_param_with_none_value(module.params)

    result = {
        "changed": False,
        "response": None,
        "ext_id": None,
        "task_ext_id": None,
        "failed": False,
    }

    api_instance = get_cluster_logs_api_instance(module)
    collect_logs(module, api_instance, result)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
