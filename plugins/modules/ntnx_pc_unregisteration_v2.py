#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Prem Karat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
module: ntnx_pc_unregisteration_v2
short_description: Unregister a registered remote cluster from the local cluster.
version_added: 2.1.0
description:
    - Unregister a registered remote cluster from the local cluster.
options:
    wait:
        description:
            - Wait for the task to complete.
        type: bool
        required: False
    pc_ext_id:
        description:
            - External ID of the remote cluster.
        type: str
        required: True
    cluster_ext_id:
        description:
            - External ID of the local cluster.
        type: str
        required: True
extends_documentation_fragment:
    - nutanix.ncp.ntnx_credentials
    - nutanix.ncp.ntnx_operations_v2
author:
    - Prem Karat (@premkarat)
    - Abhinav Bansal (@abhinavbansal29)
"""

EXAMPLES = r"""
"""

RETURN = r"""
"""

import traceback  # noqa: E402
import warnings  # noqa: E402

from ansible.module_utils.basic import missing_required_lib  # noqa: E402

from ..module_utils.base_module import BaseModule  # noqa: E402
from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.prism.pc_api_client import (  # noqa: E402
    get_domain_manager_api_instance,
    get_etag,
)
from ..module_utils.v4.prism.helpers import get_pc_config  # noqa: E402
from ..module_utils.v4.prism.tasks import wait_for_completion  # noqa: E402
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
)

SDK_IMP_ERROR = None
try:
    import ntnx_prism_py_client as prism_sdk  # noqa: E402
except ImportError:
    from ..module_utils.v4.sdk_mock import mock_sdk as prism_sdk  # noqa: E402

    SDK_IMP_ERROR = traceback.format_exc()

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    module_args = dict(
        pc_ext_id=dict(type="str", required=True),
        cluster_ext_id=dict(type="str", required=True),
    )
    return module_args

def unregister_cluster(module, domain_manager_api, result):
    pc_ext_id = module.params.get("pc_ext_id")
    sg = SpecGenerator(module)
    default_spec = prism_sdk.ClusterUnregistrationSpec()
    spec, err = sg.generate_spec(obj=default_spec)
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating unregistering cluster spec", **result)

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        return

    current_spec = get_pc_config(module, domain_manager_api, pc_ext_id)
    etag_value = get_etag(data=current_spec)
    if not etag_value:
        module.fail_json(msg="Failed to get etag value for the PC", **result)

    resp = None
    try:
        resp = domain_manager_api.unregister(
            extId=pc_ext_id, body=spec, if_match=etag_value
        )
        result["changed"] = True
    except prism_sdk.rest.ApiException as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="API Exception raised while unregistering cluster",
        )
    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        task_status = wait_for_completion(module, task_ext_id)
        result["response"] = strip_internal_attributes(task_status.to_dict())
    result["changed"] = True


def run_module():
    module = BaseModule(
        argument_spec=get_module_spec(),
        supports_check_mode=True,
    )
    if SDK_IMP_ERROR:
        module.fail_json(
            msg=missing_required_lib("ntnx_prism_py_client"),
            exception=SDK_IMP_ERROR,
        )

    remove_param_with_none_value(module.params)
    result = {
        "changed": False,
        "error": None,
        "response": None,
        "ext_id": None,
    }
    domain_manager_api = get_domain_manager_api_instance(module)
    unregister_cluster(module, domain_manager_api, result)
    module.exit_json(**result)
