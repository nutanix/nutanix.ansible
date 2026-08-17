#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_files_ad_dns_failover_v2
short_description: Perform Nutanix Files AD-DNS failover
version_added: 2.7.0
description:
    - Trigger an AD/DNS failover between two Nutanix Files servers so that
      SMB / DNS clients are redirected to the recovery site.
    - This action is typically used after a data-replication failover to
      switch service principal names (SPNs) and DNS host records to point
      at the recovery file server.
    - This module uses PC v4 APIs based SDKs
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to
      the user performing the operation.
    - >-
      B(AD-DNS Failover) -
      Required Roles: Prism Admin, Super Admin
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=files)"
options:
    state:
        description:
            - State of the module.
            - Only C(present) is supported since this is an action module.
        type: str
        choices:
            - present
        default: present
    primary_file_server_ext_id:
        description:
            - External ID of the primary file server.
        type: str
        required: true
    secondary_file_server_ext_id:
        description:
            - External ID of the secondary file server.
        type: str
        required: true
    type:
        description:
            - Failover type context for the AD/DNS switch.
        type: str
        required: true
        choices:
            - PLANNED
            - UNPLANNED
            - FAILBACK
    active_directory:
        description:
            - Active Directory credentials used for the SPN switch.
        type: dict
        required: false
        suboptions:
            preferred_domain_controller:
                description: FQDN or IP of the preferred domain controller.
                type: str
                required: false
            credential:
                description:
                    - Credentials for the Active Directory user with rights
                      to update SPNs.
                type: dict
                required: false
                suboptions:
                    username:
                        description: AD username.
                        type: str
                        required: false
                    password:
                        description: AD password.
                        type: str
                        required: false
    dns:
        description:
            - DNS record update spec used to point clients at the recovery
              file server.
        type: dict
        required: false
        suboptions:
            preferred_name_server:
                description: Preferred DNS server the failover will target.
                type: str
                required: false
            action:
                description:
                    - Whether the failover should ADD or REMOVE the DNS
                      record for the file server.
                type: str
                required: false
                choices:
                    - ADD
                    - REMOVE
            credential:
                description: Credentials used to update DNS records.
                type: dict
                required: false
                suboptions:
                    username:
                        description: DNS admin username.
                        type: str
                        required: false
                    password:
                        description: DNS admin password.
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
- name: Perform AD-DNS failover between two file servers
  nutanix.ncp.ntnx_files_ad_dns_failover_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    primary_file_server_ext_id: "a4b02ea9-6a56-4c1b-9d0b-6bdf7bf67e11"
    secondary_file_server_ext_id: "b7d84e21-3a45-47dc-a1c8-4bcf6a24fa19"
    type: PLANNED
    dns:
      preferred_name_server: "10.1.1.10"
      action: ADD
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
    description: Task response returned by the SDK.
    returned: always
    type: dict
    sample:
        {
            "ext_id": "ZXJnb24=:0e040d14-5dcf-5302-8b48-d3c6cf115cd1",
            "operation": "AdDnsFailover",
            "operation_description": "AD/DNS failover for Files",
            "progress_percentage": 100,
            "status": "SUCCEEDED"
        }

changed:
    description: Whether any change was made.
    returned: always
    type: bool
    sample: true

msg:
    description: Status/error message.
    returned: When there is an error
    type: str
    sample: "Api Exception raised while performing AD-DNS failover"

error:
    description: Error details.
    returned: when an error occurs
    type: str

failed:
    description: Whether the module failed.
    returned: always
    type: bool
    sample: false

task_ext_id:
    description: External ID of the task.
    returned: always
    type: str
    sample: "ZXJnb24=:0e040d14-5dcf-5302-8b48-d3c6cf115cd1"

ext_id:
    description: External ID of the primary file server the failover targeted.
    returned: always
    type: str
    sample: "a4b02ea9-6a56-4c1b-9d0b-6bdf7bf67e11"
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
        username=dict(type="str", required=False),
        password=dict(type="str", required=False, no_log=True),
    )

    ad_server_spec = dict(
        preferred_domain_controller=dict(type="str", required=False),
        credential=dict(
            type="dict",
            options=credential_spec,
            required=False,
            obj=files_sdk.Credential,
        ),
    )

    dns_record_spec = dict(
        preferred_name_server=dict(type="str", required=False),
        action=dict(
            type="str",
            choices=["ADD", "REMOVE"],
            required=False,
            obj=files_sdk.DnsActionType,
        ),
        credential=dict(
            type="dict",
            options=credential_spec,
            required=False,
            obj=files_sdk.Credential,
        ),
    )

    module_args = dict(
        state=dict(type="str", default="present", choices=["present"]),
        primary_file_server_ext_id=dict(type="str", required=True),
        secondary_file_server_ext_id=dict(type="str", required=True),
        type=dict(
            type="str",
            required=True,
            choices=["PLANNED", "UNPLANNED", "FAILBACK"],
            obj=files_sdk.FailoverType,
        ),
        active_directory=dict(
            type="dict",
            options=ad_server_spec,
            required=False,
            obj=files_sdk.ADServerSpec,
        ),
        dns=dict(
            type="dict",
            options=dns_record_spec,
            required=False,
            obj=files_sdk.DnsRecordSpec,
        ),
    )
    return module_args


def perform_ad_dns_failover(module, api_instance, result):
    """Perform the AD-DNS failover using the AdDnsFailoverSpec body."""
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
        resp = api_instance.ad_dns_failover(body=spec)
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
        "failed": False,
    }
    api_instance = get_replication_policies_api_instance(module)
    perform_ad_dns_failover(module, api_instance, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
