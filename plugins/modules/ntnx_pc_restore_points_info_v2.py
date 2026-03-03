#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2025, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type
DOCUMENTATION = r"""
module: ntnx_pc_restore_points_info_v2
short_description: Fetch pc restore points info
version_added: 2.1.0
description:
    - Fetch specific restore point info for a given restore source.
    - Fetch list of multiple restore points for a given restore source.
    - Please provide Prism Element IP address here in C(nutanix_host)
options:
    restore_source_ext_id:
        description:
            - External ID of the restore source.
        required: true
        type: str
    restorable_domain_manager_ext_id:
        description:
            - External ID of the restorable domain manager(PC).
        required: true
        type: str
    ext_id:
        description:
            - External ID of the restore point.
        type: str
    nutanix_host:
        description:
            - The Nutanix Prism Element IP address.
        required: true
        type: str
    nutanix_username:
        description:
            - The username to authenticate with the Nutanix Prism Element.
        required: true
        type: str
    nutanix_password:
        description:
            - The password to authenticate with the Nutanix Prism Element.
        required: true
        type: str
extends_documentation_fragment:
    - nutanix.ncp.ntnx_credentials
    - nutanix.ncp.ntnx_info_v2
    - nutanix.ncp.ntnx_logger
    - nutanix.ncp.ntnx_proxy_v2
author:
    - Abhinav Bansal (@abhinavbansal29)
    - George Ghawali (@george-ghawali)
"""

EXAMPLES = r"""
- name: Get restore point info
  nutanix.ncp.ntnx_pc_restore_points_info_v2:
      nutanix_host: <pe_ip>
      nutanix_username: <user>
      nutanix_password: <pass>
      restore_source_ext_id: "d4e44c2b-944c-48b0-8de1-b0adae3d54c6"
      restorable_domain_manager_ext_id: "cfddac63-ffdb-4d9c-9a8c-54abf89ce234"
      ext_id: "cda893b8-2aee-34bf-817d-d2ee6026790b"
  register: result

- name: List all restore points
  nutanix.ncp.ntnx_pc_restore_points_info_v2:
      nutanix_host: <pe_ip>
      nutanix_username: <user>
      nutanix_password: <pass>
      restore_source_ext_id: "d4e44c2b-944c-48b0-8de1-b0adae3d54c6"
      restorable_domain_manager_ext_id: "cfddac63-ffdb-4d9c-9a8c-54abf89ce234"
  register: result

- name: List all restore points with filter
  nutanix.ncp.ntnx_pc_restore_points_info_v2:
      nutanix_host: <pe_ip>
      nutanix_username: <user>
      nutanix_password: <pass>
      restore_source_ext_id: "d4e44c2b-944c-48b0-8de1-b0adae3d54c6"
      restorable_domain_manager_ext_id: "cfddac63-ffdb-4d9c-9a8c-54abf89ce234"
      filter: extId eq "cda893b8-2aee-34bf-817d-d2ee6026790b"
  register: result

- name: List all restore points with limit
  nutanix.ncp.ntnx_pc_restore_points_info_v2:
      nutanix_host: <pe_ip>
      nutanix_username: <user>
      nutanix_password: <pass>
      restore_source_ext_id: "d4e44c2b-944c-48b0-8de1-b0adae3d54c6"
      restorable_domain_manager_ext_id: "cfddac63-ffdb-4d9c-9a8c-54abf89ce234"
      limit: 1
  register: result
"""

RETURN = r"""
response:
    description:
        - Response for fetching restore points info
        - Restore point info if external ID is provided
        - List of multiple restore points info if external ID is not provided
    type: dict
    returned: always
    sample:
        {
            "creation_time": "2025-01-30T05:37:49.340219+00:00",
            "domain_manager": null,
            "ext_id": "8545bc57-7719-3273-a837-5aeb5f2c64b5",
            "links": null,
            "tenant_id": null
        }

ext_id:
    description: External ID of the restore point
    returned: always
    type: str
    sample: "cda893b8-2aee-34bf-817d-d2ee6026790b"

changed:
    description: This indicates whether the task resulted in any changes
    returned: always
    type: bool
    sample: true

msg:
    description: This indicates the message if any message occurred
    returned: When there is an error
    type: str
    sample: "Api Exception raised while fetching restore points info"

error:
    description: This field typically holds information about if the task have errors that occurred during the task execution
    returned: When an error occurs
    type: str
    sample: false

failed:
    description: This field typically holds information about if the task have failed
    returned: always
    type: bool
    sample: false

total_available_results:
    description:
        - The total number of available restore points in the PC.
    type: int
    returned: when all restore points are fetched
    sample: 125
"""

import warnings  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.prism.helpers import get_restore_point  # noqa: E402
from ..module_utils.v4.prism.pc_api_client import (  # noqa: E402
    get_domain_manager_backup_api_instance,
)
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
)

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    module_args = dict(
        restore_source_ext_id=dict(type="str", required=True),
        restorable_domain_manager_ext_id=dict(type="str", required=True),
        ext_id=dict(type="str"),
    )
    return module_args


def get_restore_points(module, domain_manager_backups_api, result):
    restore_source_ext_id = module.params.get("restore_source_ext_id")
    restorable_domain_manager_ext_id = module.params.get(
        "restorable_domain_manager_ext_id"
    )
    sg = SpecGenerator(module)
    kwargs, err = sg.get_info_spec(attr=module.params)
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating restore points info Spec", **result)
    try:
        resp = domain_manager_backups_api.list_restore_points(
            restoreSourceExtId=restore_source_ext_id,
            restorableDomainManagerExtId=restorable_domain_manager_ext_id,
            **kwargs  # fmt: skip
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching restore points info",
        )

    total_available_results = resp.metadata.total_available_results
    result["total_available_results"] = total_available_results

    resp = strip_internal_attributes(resp.to_dict()).get("data")
    if not resp:
        resp = []
    result["response"] = resp


def get_restore_points_with_ext_id(module, domain_manager_backups_api, result):
    restore_source_ext_id = module.params.get("restore_source_ext_id")
    restorable_domain_manager_ext_id = module.params.get(
        "restorable_domain_manager_ext_id"
    )
    ext_id = module.params.get("ext_id")
    resp = get_restore_point(
        module,
        domain_manager_backups_api,
        ext_id,
        restore_source_ext_id,
        restorable_domain_manager_ext_id,
    )
    result["ext_id"] = ext_id
    result["response"] = strip_internal_attributes(resp.to_dict())


def run_module():
    module = BaseInfoModule(
        argument_spec=get_module_spec(),
        supports_check_mode=False,
        mutually_exclusive=[
            ("ext_id", "filter"),
        ],
    )
    remove_param_with_none_value(module.params)
    result = {"changed": False, "response": None}
    domain_manager_backups_api = get_domain_manager_backup_api_instance(module)
    if module.params.get("ext_id"):
        get_restore_points_with_ext_id(module, domain_manager_backups_api, result)
    else:
        get_restore_points(module, domain_manager_backups_api, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
