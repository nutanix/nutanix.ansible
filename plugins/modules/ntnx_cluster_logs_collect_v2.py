#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2027, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_cluster_logs_collect_v2
short_description: Collect logs from a cluster in Nutanix Prism Central
version_added: "2.7.0"
description:
    - Collect logs from a cluster.
    - This module uses PC v4 APIs based SDKs
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
    - >-
      B(Collect Logs) -
      Required Roles: Monitoring Admin, Prism Admin, Project Manager, Super Admin
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=monitoring)"
options:
    state:
        description:
            - State of the module.
            - If C(state) is C(present), the module will collect logs from the cluster.
            - If C(state) is C(absent), the module will fail.
        type: str
        choices:
            - present
        default: present
    ext_id:
        description:
            - The UUID of the cluster for which you want to collect logs.
        type: str
        required: true
    start_time:
        description:
            - The time marking the start of a log collection window.
            - It should be in the following format
            - YYYY-MM-DDTHH:MM:SSZ or YYYY-MM-DDTHH:MM:SS+HH:MM or YYYY-MM-DDTHH:MM:SS-HH:MM.
            - The start time of log collection should be within the past three months.
            - For example
            - 1985-04-12T23:20:50.52Z represents 20 minutes and 50.52 seconds after the 23rd hour of
              April 12th, 1985 in UTC.
            - 1996-12-19T16:39:57-08:00 represents 39 minutes and 57 seconds after the 16th hour
              of December 19th, 1996 with an offset of -08:00 from UTC (Pacific Standard Time).
            - Note that this is equivalent to 1996-12-20T00:39:57Z in UTC.
        type: str
        required: true
    end_time:
        description:
            - The time marking the end of a log collection window.
            - It should be in the following format
            - YYYY-MM-DDTHH:MM:SSZ or YYYY-MM-DDTHH:MM:SS+HH:MM or YYYY-MM-DDTHH:MM:SS-HH:MM.
            - The end time of log collection should be within the past three months.
            - For example
            - 1985-04-12T23:20:50.52Z represents 20 minutes and 50.52 seconds after the 23rd hour of
              April 12th, 1985 in UTC.
            - 1996-12-19T16:39:57-08:00 represents 39 minutes and 57 seconds after the 16th hour
              of December 19th, 1996 with an offset of -08:00 from UTC (Pacific Standard Time).
            - Note that this is equivalent to 1996-12-20T00:39:57Z in UTC.
        type: str
        required: true
    include_tags:
        description:
            - Collect items associated with the tag IDs. The tag ID can be fetched from the GET tags
              operation.
            - If no tags are specified, all items will be collected by default, which will take a
              longer time.
            - It is recommended that at least one tag is selected.
        type: list
        elements: str
    should_anonymize:
        description:
            - Indicates whether to mask sensitive data in the collected logs or not.
        type: bool
    node_ip_list:
        description:
            - List of node IP addresses from where the logs will be collected.
        type: list
        elements: dict
        suboptions:
            value:
                description:
                    - The IPv4 address of the host.
                type: str
                required: true
            prefix_length:
                description:
                    - The prefix length of the network to which this host IPv4 address belongs.
                type: int
                default: 32
    should_collect_from_disabled_node:
        description:
            - Indicates whether to collect logs from a node where services are down or not.
            - This feature is not supported on PC.
        type: bool
    exclude_tags:
        description:
            - Exclude items associated with the tag IDs. The tag ID can be fetched from the GET tags
              operation.
        type: list
        elements: str
    archive_opts:
        description:
            - Arguments specifying details of the archive to be collected.
        type: dict
        required: true
        suboptions:
            archive_name:
                description:
                    - Custom name of the archive folder.
                type: str
            upload_params:
                description:
                    - This parameter specifies the target/destination location of collected archive.
                    - User must specify one of the below target/destination.
                    - LocalUploadParams
                    - Use this option to store archive on local disk.
                    - Full archive path can be found in the completion_details field of the task.
                    - NtnxServerUploadParams
                    - Use this option to upload archive to Nutanix server.
                    - CustomServerUploadParams
                    - Use this option to upload archive to custom FTP/SFTP server.
                    - StorageContainerUploadParams
                    - Use this option to upload archive to a storage container.
                    - Localhost storage container uploads are not supported on PC.
                type: dict
                required: true
                suboptions:
                    local_upload_params:
                        description:
                            - The parameters for uploading the archive if the destination is a
                              local server.
                        type: dict
                        suboptions:
                            path:
                                description:
                                    - Path where the archive will be stored. The path should
                                      pre-exist.
                                    - Note the Janitor service will not clean up the data from these
                                      custom paths. It only monitors the default path.
                                type: str
                    ntnx_server_upload_params:
                        description:
                            - The parameters for uploading the archive if the destination is a
                              Nutanix server.
                        type: dict
                        suboptions:
                            case_number:
                                description:
                                    - Nutanix support case number under which the archive will be
                                      stored.
                                type: int
                                required: true
                            protocol:
                                description:
                                    - Protocol used for uploading to the target destination.
                                type: str
                                choices:
                                    - SFTP
                                    - FTP
                    custom_server_upload_params:
                        description:
                            - The parameters for uploading the archive if the destination is a
                              custom server.
                        type: dict
                        suboptions:
                            protocol:
                                description:
                                    - Protocol used for uploading to the target destination.
                                type: str
                                required: true
                                choices:
                                    - SFTP
                                    - FTP
                            server_address:
                                description:
                                    - IP address or FQDN of the target server. Mandatory for SFTP
                                      and FTP protocol.
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
                                                default: 32
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
                                                default: 128
                                    fqdn:
                                        description:
                                            - A fully qualified domain name that specifies its exact
                                              location in the tree hierarchy of the Domain Name
                                              System.
                                        type: dict
                                        suboptions:
                                            value:
                                                description:
                                                    - The fully qualified domain name of the host.
                                                type: str
                                                required: true
                            port:
                                description:
                                    - Port of the target. Mandatory for SFTP and FTP protocol.
                                type: int
                            credential:
                                description:
                                    - Credentials for the destination where the collected archive
                                      will be uploaded. Mandatory for SFTP and FTP protocol.
                                type: dict
                                required: true
                                suboptions:
                                    user_name:
                                        description:
                                            - Username to access the archive destination. If it is
                                              not provided, the username that was used to call the
                                              API will be used.
                                        type: str
                                        required: true
                                    password:
                                        description:
                                            - Password to access the archive destination.
                                        type: str
                                    key_file_path:
                                        description:
                                            - Path to the key file that will be used for
                                              authentication of the archive destination.
                                        type: str
                            path:
                                description:
                                    - Path where the archive will be stored on the custom server.
                                    - The path should pre-exist. If not specified, the bundle will
                                      get stored in the location as set in $HOME.
                                type: str
                    storage_container_upload_params:
                        description:
                            - The parameters for uploading the archive if the destination is a
                              storage container.
                            - The local host storage container uploads are not supported on PC.
                        type: dict
                        suboptions:
                            ip_address:
                                description:
                                    - IP address of the cluster where target storage container is
                                      hosted
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
                                        default: 32
                            port:
                                description:
                                    - Port of the target. Mandatory for SFTP and FTP protocol.
                                type: int
                            credential:
                                description:
                                    - Credentials for the destination where the collected archive
                                      will be uploaded. Mandatory for SFTP and FTP protocol.
                                type: dict
                                required: true
                                suboptions:
                                    user_name:
                                        description:
                                            - Username to access the archive destination. If it is
                                              not provided, the username that was used to call the
                                              API will be used.
                                        type: str
                                        required: true
                                    password:
                                        description:
                                            - Password to access the archive destination.
                                        type: str
                                    key_file_path:
                                        description:
                                            - Path to the key file that will be used for
                                              authentication of the archive destination.
                                        type: str
                            path:
                                description:
                                    - Path of storage container where the archive will be uploaded.
                                type: str
                                required: true
    description:
        description:
            - Description to be attached with the associated log collection task.
        type: str
    tag_opts:
        description:
            - This parameter allows the user to pass additional arguments that are specific to a
              particular tag.
        type: dict
        suboptions:
            msp_opts:
                description:
                    - Additional arguments that are applicable only for MSP tag.
                type: dict
                suboptions:
                    cluster_ext_ids:
                        description:
                            - List of MSP cluster UUID from where logs would be collected.
                            - For NCC version 5.3.0, this field accepts only one clusterExtId.
                        type: list
                        elements: str
            ndb_opts:
                description:
                    - Additional arguments that are applicable only for NDB tag.
                type: dict
                suboptions:
                    cluster_ext_ids:
                        description:
                            - List of MSP cluster UUID from where logs would be collected.
                        type: list
                        elements: str
                    glob_categories:
                        description:
                            - List of predefined NDB glob categories specifying subgroups of NDB
                              logs to collect.
                        type: list
                        elements: str
                        choices:
                            - K8S_NDB_RESOURCES
                            - NDB_APPLICATION_LOGS
                            - ALL_LOGS
                    glob_patterns:
                        description:
                            - List of glob patterns for collecting subgroups of NDB logs.
                            - Each pattern collects logs from one or more services in the SMSP
                              cluster whose names match the provided pattern.
                        type: list
                        elements: str
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
- name: Collect cluster logs to local disk
  nutanix.ncp.ntnx_cluster_logs_collect_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    ext_id: "00061de6-4a87-6b06-185b-ac1f6b6f97e2"
    start_time: "2026-01-01T00:00:00Z"
    end_time: "2026-01-02T00:00:00Z"
    should_anonymize: true
    include_tags:
      - "e966cd7f-02ed-4ae4-b4a0-cab323701d7e"
    archive_opts:
      archive_name: "NTNX-Log"
      upload_params:
        local_upload_params:
          path: "/home/nutanix/data/logbay/bundles"
  register: result

- name: Collect cluster logs and upload to Nutanix support
  nutanix.ncp.ntnx_cluster_logs_collect_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    ext_id: "00061de6-4a87-6b06-185b-ac1f6b6f97e2"
    start_time: "2026-01-01T00:00:00Z"
    end_time: "2026-01-02T00:00:00Z"
    archive_opts:
      upload_params:
        ntnx_server_upload_params:
          case_number: 1753078
          protocol: SFTP
  register: result
"""

RETURN = r"""
response:
    description:
        - Response for collect logs.
        - If C(wait) is true, it will contain the final task payload after completion.
        - If C(wait) is false, it will contain the initial task details.
    type: dict
    returned: always
    sample:
        {
            "ext_id": "ZXJnb24=:1a1a1a1a-2b2b-3c3c-4d4d-5e5e5e5e5e5e",
        }
task_ext_id:
    description: The external ID of the task.
    type: str
    returned: always
    sample: "ZXJnb24=:1a1a1a1a-2b2b-3c3c-4d4d-5e5e5e5e5e5e"
ext_id:
    description: The external ID of the cluster.
    type: str
    returned: always
    sample: "00061de6-4a87-6b06-185b-ac1f6b6f97e2"
changed:
    description: This indicates whether the task resulted in any changes
    type: bool
    returned: always
    sample: true
failed:
    description: This indicates whether the task failed
    type: bool
    returned: always
    sample: false
msg:
    description: This indicates the message if any message occurred
    type: str
    returned: When there is an error or in check mode operation
    sample: "Logs will be collected for cluster with ext_id:00061de6-4a87-6b06-185b-ac1f6b6f97e2."
error:
    description: This indicates the error message if any error occurred
    type: str
    returned: When an error occurs
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
)

SDK_IMP_ERROR = None
try:
    import ntnx_monitoring_py_client as sdk  # noqa: E402
except ImportError:

    from ..module_utils.v4.sdk_mock import mock_sdk as sdk  # noqa: E402

    SDK_IMP_ERROR = traceback.format_exc()

warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")

UPLOAD_PARAM_KEYS = (
    "local_upload_params",
    "ntnx_server_upload_params",
    "custom_server_upload_params",
    "storage_container_upload_params",
)
PROTOCOL_CHOICES = ["SFTP", "FTP"]
NDB_GLOB_CATEGORY_CHOICES = [
    "K8S_NDB_RESOURCES",
    "NDB_APPLICATION_LOGS",
    "ALL_LOGS",
]


def get_module_spec():
    ipv4_address_spec = dict(
        value=dict(type="str", required=True),
        prefix_length=dict(type="int", default=32),
    )
    ipv6_address_spec = dict(
        value=dict(type="str", required=True),
        prefix_length=dict(type="int", default=128),
    )
    fqdn_spec = dict(
        value=dict(type="str", required=True),
    )
    ip_address_or_fqdn_spec = dict(
        ipv4=dict(type="dict", options=ipv4_address_spec, obj=sdk.IPv4Address),
        ipv6=dict(type="dict", options=ipv6_address_spec, obj=sdk.IPv6Address),
        fqdn=dict(type="dict", options=fqdn_spec, obj=sdk.FQDN),
    )
    credential_spec = dict(
        user_name=dict(type="str", required=True),
        password=dict(type="str", no_log=True),
        key_file_path=dict(type="str", no_log=True),
    )
    local_upload_params_spec = dict(
        path=dict(type="str"),
    )
    ntnx_server_upload_params_spec = dict(
        case_number=dict(type="int", required=True),
        protocol=dict(type="str", choices=PROTOCOL_CHOICES),
    )
    custom_server_upload_params_spec = dict(
        protocol=dict(type="str", required=True, choices=PROTOCOL_CHOICES),
        server_address=dict(
            type="dict",
            required=True,
            options=ip_address_or_fqdn_spec,
            obj=sdk.IPAddressOrFQDN,
        ),
        port=dict(type="int"),
        credential=dict(
            type="dict",
            required=True,
            options=credential_spec,
            obj=sdk.Credential,
            no_log=True,
        ),
        path=dict(type="str"),
    )
    storage_container_upload_params_spec = dict(
        ip_address=dict(
            type="dict",
            options=ipv4_address_spec,
            obj=sdk.IPv4Address,
        ),
        port=dict(type="int"),
        credential=dict(
            type="dict",
            required=True,
            options=credential_spec,
            obj=sdk.Credential,
            no_log=True,
        ),
        path=dict(type="str", required=True),
    )
    upload_params_spec = dict(
        local_upload_params=dict(
            type="dict",
            options=local_upload_params_spec,
        ),
        ntnx_server_upload_params=dict(
            type="dict",
            options=ntnx_server_upload_params_spec,
        ),
        custom_server_upload_params=dict(
            type="dict",
            options=custom_server_upload_params_spec,
        ),
        storage_container_upload_params=dict(
            type="dict",
            options=storage_container_upload_params_spec,
        ),
    )
    archive_opts_spec = dict(
        archive_name=dict(type="str"),
        upload_params=dict(
            type="dict",
            required=True,
            options=upload_params_spec,
            obj={
                "local_upload_params": sdk.LocalUploadParams,
                "ntnx_server_upload_params": sdk.NtnxServerUploadParams,
                "custom_server_upload_params": sdk.CustomServerUploadParams,
                "storage_container_upload_params": sdk.StorageContainerUploadParams,
            },
            mutually_exclusive=[list(UPLOAD_PARAM_KEYS)],
            required_one_of=[list(UPLOAD_PARAM_KEYS)],
        ),
    )
    msp_opts_spec = dict(
        cluster_ext_ids=dict(type="list", elements="str"),
    )
    ndb_opts_spec = dict(
        cluster_ext_ids=dict(type="list", elements="str"),
        glob_categories=dict(
            type="list",
            elements="str",
            choices=NDB_GLOB_CATEGORY_CHOICES,
        ),
        glob_patterns=dict(type="list", elements="str"),
    )
    tag_opts_spec = dict(
        msp_opts=dict(
            type="dict",
            options=msp_opts_spec,
            obj=sdk.MspOpts,
        ),
        ndb_opts=dict(
            type="dict",
            options=ndb_opts_spec,
            obj=sdk.NdbOpts,
        ),
    )
    module_args = dict(
        state=dict(type="str", default="present", choices=["present"]),
        ext_id=dict(type="str", required=True),
        start_time=dict(type="str", required=True),
        end_time=dict(type="str", required=True),
        include_tags=dict(type="list", elements="str"),
        should_anonymize=dict(type="bool"),
        node_ip_list=dict(
            type="list",
            elements="dict",
            options=ipv4_address_spec,
            obj=sdk.IPv4Address,
        ),
        should_collect_from_disabled_node=dict(type="bool"),
        exclude_tags=dict(type="list", elements="str"),
        archive_opts=dict(
            type="dict",
            required=True,
            options=archive_opts_spec,
            obj=sdk.ArchiveOpts,
        ),
        description=dict(type="str"),
        tag_opts=dict(
            type="dict",
            options=tag_opts_spec,
            obj=sdk.TagOpts,
        ),
    )
    return module_args


def collect_logs(module, result, api_instance):
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id

    sg = SpecGenerator(module)
    default_spec = sdk.LogCollectionSpec()
    spec, err = sg.generate_spec(obj=default_spec)
    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed generating spec for collecting cluster logs",
            **result,
        )

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        result["msg"] = "Logs will be collected for cluster with ext_id:{0}.".format(
            ext_id
        )
        return

    resp = None
    try:
        resp = api_instance.collect_logs(extId=ext_id, body=spec)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while collecting cluster logs",
        )

    task_ext_id = getattr(resp.data, "ext_id", None)
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
        "failed": False,
    }
    api_instance = get_cluster_logs_api_instance(module)
    collect_logs(module, result, api_instance)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
