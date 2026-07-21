#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_files_ad_dns_failover_v2
short_description: Perform an AD-DNS failover between Nutanix Files file servers
version_added: 2.7.0
description:
  - This module performs an Active Directory (AD) and DNS failover between a primary and a secondary file server in Nutanix Prism Central.
  - The failover switches the AD computer account and DNS records so that clients continue to resolve and authenticate against the surviving file server.
  - This is an action module, it triggers the AD-DNS failover operation and does not create, update or delete a persistent resource.
  - This module uses PC v4 APIs based SDKs.
notes:
  - >-
    This module requires the appropriate Nutanix IAM roles for Files replication and disaster recovery operations to be
    assigned to the user performing the operation.
  - "Ref: U(https://developers.nutanix.com/api-reference?namespace=files)"
options:
  state:
    description:
      - State of the module.
      - If C(state) is C(present), the module performs the AD-DNS failover.
    type: str
    choices:
      - present
    default: present
  primary_file_server_ext_id:
    description:
      - The external identifier of the primary file server for the replication.
      - This is the file server that is failing over.
    type: str
    required: false
  secondary_file_server_ext_id:
    description:
      - The external identifier of the secondary file server for the replication.
      - This is the file server that takes over the AD computer account and DNS records.
    type: str
    required: false
  active_directory:
    description:
      - Configuration used to access the file server Active Directory server during the failover.
    type: dict
    required: false
    suboptions:
      credential:
        description:
          - Active Directory user credential used to perform the AD failover.
        type: dict
        required: false
        suboptions:
          username:
            description:
              - Name of the Active Directory user.
            type: str
            required: false
          password:
            description:
              - Password of the Active Directory user.
            type: str
            required: false
      preferred_domain_controller:
        description:
          - Preferred domain controller to use for the AD failover.
        type: str
        required: false
  dns:
    description:
      - DNS record configuration used during the failover.
    type: dict
    required: false
    suboptions:
      preferred_name_server:
        description:
          - Preferred name server for the file server.
        type: str
        required: false
      action:
        description:
          - The DNS action to perform for the file server records during the failover.
        type: str
        choices:
          - ADD
          - REMOVE
        required: false
      credential:
        description:
          - DNS user credential used to update the DNS records.
        type: dict
        required: false
        suboptions:
          username:
            description:
              - Name of the DNS user.
            type: str
            required: false
          password:
            description:
              - Password of the DNS user.
            type: str
            required: false
  type:
    description:
      - The type of failover to perform.
      - C(PLANNED) performs a graceful, coordinated failover to the secondary file server.
      - C(UNPLANNED) performs a failover when the primary file server is unavailable.
      - C(FAILBACK) reverts a previous failover back to the original primary file server.
    type: str
    choices:
      - PLANNED
      - UNPLANNED
      - FAILBACK
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
- name: Perform a planned AD-DNS failover with all attributes
  nutanix.ncp.ntnx_files_ad_dns_failover_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    primary_file_server_ext_id: "c66fcb19-01f0-49de-9d35-4b90ebbca2d9"
    secondary_file_server_ext_id: "483ca0d4-855e-4f92-a5a0-fc56907d919b"
    type: "PLANNED"
    active_directory:
      credential:
        username: "ad-admin"
        password: "ad-password"
      preferred_domain_controller: "dc1.ansible.local"
    dns:
      preferred_name_server: "10.44.76.10"
      action: "ADD"
      credential:
        username: "dns-admin"
        password: "dns-password"
  register: result
  ignore_errors: true

- name: Perform an unplanned AD-DNS failover
  nutanix.ncp.ntnx_files_ad_dns_failover_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    primary_file_server_ext_id: "c66fcb19-01f0-49de-9d35-4b90ebbca2d9"
    secondary_file_server_ext_id: "483ca0d4-855e-4f92-a5a0-fc56907d919b"
    type: "UNPLANNED"
    active_directory:
      credential:
        username: "ad-admin"
        password: "ad-password"
  register: result
  ignore_errors: true

- name: Perform an AD-DNS failback to the original primary file server
  nutanix.ncp.ntnx_files_ad_dns_failover_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    primary_file_server_ext_id: "483ca0d4-855e-4f92-a5a0-fc56907d919b"
    secondary_file_server_ext_id: "c66fcb19-01f0-49de-9d35-4b90ebbca2d9"
    type: "FAILBACK"
    dns:
      preferred_name_server: "10.44.76.10"
      action: "REMOVE"
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
  description:
    - Response for the AD-DNS failover operation.
    - Task details if C(wait) is true.
    - Task reference details if C(wait) is false.
  returned: always
  type: dict
  sample:
    {
      "cluster_ext_ids": [
        "00061fa4-ef93-7dd8-185b-ac1f6b6f97e2"
      ],
      "completed_time": "2026-07-21T06:26:51.524581+00:00",
      "created_time": "2026-07-21T06:26:47.167906+00:00",
      "entities_affected": [
        {
          "ext_id": "c66fcb19-01f0-49de-9d35-4b90ebbca2d9",
          "rel": "files:config:file-server"
        }
      ],
      "error_messages": null,
      "ext_id": "ZXJnb24=:0e040d14-5dcf-5302-8b48-d3c6cf115cd1",
      "is_cancelable": false,
      "last_updated_time": "2026-07-21T06:26:51.524581+00:00",
      "legacy_error_message": null,
      "operation": "AdDnsFailover",
      "operation_description": "Perform an AD-DNS failover",
      "owned_by": {
        "ext_id": "00000000-0000-0000-0000-000000000000",
        "name": "admin"
      },
      "parent_task": null,
      "progress_percentage": 100,
      "started_time": "2026-07-21T06:26:47.185754+00:00",
      "status": "SUCCEEDED",
      "sub_steps": null,
      "sub_tasks": null,
      "warnings": null
    }

changed:
  description: This indicates whether the task resulted in any changes
  returned: always
  type: bool
  sample: true

msg:
  description: This indicates the message if any message occurred
  returned: When there is an error
  type: str
  sample: "Api Exception raised while performing AD-DNS failover"

error:
  description: This field typically holds information about if the task have errors that occurred during the task execution
  returned: when an error occurs
  type: str
  sample: "Failed generating spec for AD-DNS failover"

failed:
  description: This field typically holds information about if the task have failed
  returned: always
  type: bool
  sample: false

task_ext_id:
  description: The external ID of the task
  returned: always
  type: str
  sample: "ZXJnb24=:0e040d14-5dcf-5302-8b48-d3c6cf115cd1"

ext_id:
  description: The external ID of the primary file server on which the AD-DNS failover is performed
  returned: always
  type: str
  sample: "c66fcb19-01f0-49de-9d35-4b90ebbca2d9"
"""

import traceback  # noqa: E402
import warnings  # noqa: E402

from ansible.module_utils.basic import missing_required_lib  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_module_v4 import BaseModuleV4  # noqa: E402
from ..module_utils.v4.files.api_client import (  # noqa: E402
    get_replication_policies_api_instance,
)
from ..module_utils.v4.prism.tasks import wait_for_completion  # noqa: E402
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
)

SDK_IMP_ERROR = None
try:
    import ntnx_files_py_client as files_sdk  # noqa: E402
except ImportError:

    from ..module_utils.v4.sdk_mock import mock_sdk as files_sdk  # noqa: E402

    SDK_IMP_ERROR = traceback.format_exc()

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():

    credential_spec = dict(
        username=dict(type="str"),
        password=dict(type="str", no_log=True),
    )

    ad_server_spec = dict(
        credential=dict(
            type="dict",
            options=credential_spec,
            obj=files_sdk.Credential,
            no_log=False,
        ),
        preferred_domain_controller=dict(type="str"),
    )

    dns_record_spec = dict(
        preferred_name_server=dict(type="str"),
        action=dict(type="str", choices=["ADD", "REMOVE"], obj=files_sdk.DnsActionType),
        credential=dict(
            type="dict",
            options=credential_spec,
            obj=files_sdk.Credential,
            no_log=False,
        ),
    )

    module_args = dict(
        state=dict(type="str", default="present", choices=["present"]),
        primary_file_server_ext_id=dict(type="str"),
        secondary_file_server_ext_id=dict(type="str"),
        active_directory=dict(
            type="dict",
            options=ad_server_spec,
            obj=files_sdk.ADServerSpec,
        ),
        dns=dict(
            type="dict",
            options=dns_record_spec,
            obj=files_sdk.DnsRecordSpec,
        ),
        type=dict(
            type="str",
            choices=["PLANNED", "UNPLANNED", "FAILBACK"],
            obj=files_sdk.FailoverType,
        ),
    )

    return module_args


def perform_ad_dns_failover(module, result, replication_policies_api):
    result["ext_id"] = module.params.get("primary_file_server_ext_id")

    sg = SpecGenerator(module)
    default_spec = files_sdk.AdDnsFailoverSpec()
    spec, err = sg.generate_spec(obj=default_spec)

    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating spec for AD-DNS failover", **result)

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        return

    resp = None
    try:
        resp = replication_policies_api.ad_dns_failover(body=spec)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while performing AD-DNS failover",
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
            msg=missing_required_lib("ntnx_files_py_client"),
            exception=SDK_IMP_ERROR,
        )

    remove_param_with_none_value(module.params)
    result = {
        "changed": False,
        "response": None,
        "ext_id": None,
        "task_ext_id": None,
    }
    replication_policies_api = get_replication_policies_api_instance(module)
    perform_ad_dns_failover(module, result, replication_policies_api)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
