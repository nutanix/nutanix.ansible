#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2025, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_license_seamless_action_v2
short_description: Perform Seamless Licensing Action
description:
    - This module performs seamless licensing action.
    - Seamless licensing actions like post the cluster summary file, apply license file, and others.
    - This module uses PC v4 APIs based SDKs.
version_added: 2.4.0
author:
    - Abhinav Bansal (@abhinavbansal29)
options:
    operation:
        description:
            - The operation to perform.
            - APPLY_LICENSE_SUMMARY -> Operation type for fetching the license summary file from licensing portal and applying the same to the cluster.
            - RECLAIM_FOR_DESTROYED_CLUSTER -> Reclaims all licenses for the destroyed cluster.
            - UPLOAD_CLUSTER_SUMMARY -> Operation type for posting the cluster summary file to the licensing portal.
            - UPDATE_METADATA -> Operation type for updating metadata like enforcement policy and cluster type.
            - RECLAIM -> Reclaims licenses for the provided list of clusters.
            - APPLY_LICENSE_SUMMARY_WITH_METADATA -> Fetch latest license summary and metadata(like enforcement policy, cluster type) from licensing portal and apply the same to cluster.
            - RENEW -> Operation type for renewing the licenses.
            - REBALANCE -> Operation type for rebalance the licenses which is required when cluster has been expanded or downsized.
        type: str
        choices:
            - APPLY_LICENSE_SUMMARY
            - RECLAIM_FOR_DESTROYED_CLUSTER
            - UPLOAD_CLUSTER_SUMMARY
            - UPDATE_METADATA
            - RECLAIM
            - APPLY_LICENSE_SUMMARY_WITH_METADATA
            - RENEW
            - REBALANCE
    cluster_ext_ids:
        description:
            - The list of cluster external IDs.
        type: list
        elements: str
    entitlement_names:
        description:
            - The list of entitlement names.
        type: list
        elements: str
extends_documentation_fragment:
    - nutanix.ncp.ntnx_credentials
    - nutanix.ncp.ntnx_operations_v2
"""

EXAMPLES = r"""
"""

RETURN = r"""
response:
    description: Task response for performing seamless licensing action
    type: dict
    returned: always
    sample:
        
task_ext_id:
    description: The task external ID
    type: str
    returned: always
    sample: "00061de6-4a87-6b06-185b-ac1f6b6f97e2"
changed:
    description: Whether the module made any changes
    type: bool
    returned: always
    sample: false
"""

import traceback  # noqa: E402
import warnings  # noqa: E402

from ..module_utils.base_module import BaseModule  # noqa: E402
from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.lcm.api_client import get_inventory_api_instance  # noqa: E402
from ..module_utils.v4.prism.tasks import wait_for_completion  # noqa: E402
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
)

SDK_IMP_ERROR = None
try:
    import ntnx_licensing_py_client as licensing_sdk  # noqa: E402
except ImportError:

    from ..module_utils.v4.sdk_mock import mock_sdk as licensing_sdk  # noqa: E402

    SDK_IMP_ERROR = traceback.format_exc()

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    module_args = dict(
        operation=dict(
            type="str",
            choices=[
                "APPLY_LICENSE_SUMMARY",
                "RECLAIM_FOR_DESTROYED_CLUSTER",
                "UPLOAD_CLUSTER_SUMMARY",
                "UPDATE_METADATA",
                "RECLAIM",
                "APPLY_LICENSE_SUMMARY_WITH_METADATA",
                "RENEW",
                "REBALANCE",
            ],
        ),
        cluster_ext_ids=dict(type="list", elements="str"),
        entitlement_names=dict(type="list", elements="str"),
    )
    return module_args


def license_seamless_action(module, api_instance, result):
    sg = SpecGenerator(module)
    default_spec = licensing_sdk.LicenseStateSyncSpec()
    spec, err = sg.generate_spec(obj=default_spec)
    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed generating seamless licensing action Spec", **result
        )

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        return
    resp = None

    try:
        resp = api_instance.perform_seamless_action(spec)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while performing seamless licensing action",
        )
    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        resp = wait_for_completion(module, task_ext_id)
        result["response"] = strip_internal_attributes(resp.to_dict())

    result["changed"] = True


def run_module():
    module = BaseModule(
        argument_spec=get_module_spec(),
        supports_check_mode=True,
    )

    remove_param_with_none_value(module.params)
    result = {
        "changed": False,
        "response": None,
        "task_ext_id": None,
    }
    api_instance = get_inventory_api_instance(module)
    license_seamless_action(module, api_instance, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
