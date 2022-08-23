#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Prem Karat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type


DOCUMENTATION = r"""
---
module: ntnx_recovery_plan_jobs_info
short_description: recovery plan jobs info module
version_added: 1.5.0
description: 'Get recovery plan jobs info'
options:
    kind:
      description:
        - The kind name
      type: str
      default: recovery_plan_job
    job_uuid:
        description:
            - recovery plan job  UUID
        type: str
extends_documentation_fragment:
      - nutanix.ncp.ntnx_credentials
      - nutanix.ncp.ntnx_info
author:
 - Prem Karat (@premkarat)
 - Pradeepsingh Bhati (@bhati-pradeep)
"""
EXAMPLES = r"""
"""
RETURN = r"""
"""

from ..module_utils.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.prism.recovery_plan_jobs import RecoveryPlanJob  # noqa: E402
from ..module_utils.utils import remove_param_with_none_value  # noqa: E402


def get_module_spec():

    module_args = dict(
        job_uuid=dict(type="str"),
        kind=dict(type="str", default="recovery_plan_job"),
        sort_order=dict(type="str", choices=["ASCENDING", "DESCENDING"]),
        sort_attribute=dict(type="str"),
    )

    return module_args


def get_recovery_plan_job(module, result):
    recovery_plan_job = RecoveryPlanJob(module)
    uuid = module.params.get("recovery_plan_uuid")
    resp = recovery_plan_job.read(uuid)

    result["response"] = resp


def get_recovery_plan_jobs(module, result):
    recovery_plan_job = RecoveryPlanJob(module)
    spec, error = recovery_plan_job.get_info_spec()
    if error:
        result["error"] = error
        module.fail_json(msg="Failed generating recovery plan job info spec", **result)
    resp = recovery_plan_job.list(spec)

    result["response"] = resp


def run_module():
    module = BaseInfoModule(
        argument_spec=get_module_spec(),
        supports_check_mode=False,
        required_together=[("sort_order", "sort_attribute")],
    )
    remove_param_with_none_value(module.params)
    result = {"changed": False, "error": None, "response": None}
    if module.params.get("job_uuid"):
        get_recovery_plan_job(module, result)
    else:
        get_recovery_plan_jobs(module, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
