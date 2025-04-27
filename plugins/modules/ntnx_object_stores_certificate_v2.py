#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2025, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
module: ntnx_object_stores_certificate_v2
short_description: Create SSL certificate for a Nutanix object store
version_added: 2.2.0
description:
    - Create SSL certificate for a Nutanix object store.
options:
    object_store_ext_id:
        description:
            - External ID of the object store to which the SSL certificate will be added.
        type: str
        required: true
    wait:
        description:
            - Wait for the task to complete.
        type: bool
        required: false

extends_documentation_fragment:
    - nutanix.ncp.ntnx_credentials
    - nutanix.ncp.ntnx_operations_v2
author:
    - George Ghawali (@george-ghawali)
"""

EXAMPLES = r"""
"""

RETURN = r"""
response:
    description: Task status for Creating SSL certificate for the object store
    type: dict
    returned: always
    sample:

task_ext_id:
    description: Task ID for Creating SSL certificate for the object store.
    type: str
    returned: always
    sample: "ZXJnb24=:5f63a855-6b6e-4aca-4efb-159a35ce0e52"

ext_id:
    description: External ID of the SSL certificate
    type: str
    returned: always
    sample: "00062c47-ac15-ee40-185b-ac1f6b6f97e2"

changed:
    description: This indicates whether the task resulted in any changes
    returned: always
    type: bool
    sample: true

error:
    description: This field typically holds information about if the task have errors that occurred during the task execution
    returned: When an error occurs
    type: str

failed:
    description: This field typically holds information about if the task have failed
    returned: always
    type: bool
    sample: false
"""

from pathlib import Path
import traceback  # noqa: E402
import warnings  # noqa: E402
from copy import deepcopy  # noqa: E402

from ansible.module_utils.basic import missing_required_lib  # noqa: E402

from ..module_utils.base_module import BaseModule  # noqa: E402
from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.objects.helpers import get_object_store  # noqa: E402
from ..module_utils.v4.objects.api_client import (  # noqa: E402
    get_objects_api_instance,
    get_etag,
)
from ..module_utils.v4.objects.spec.objects import (
    ObjectsSpecs as objects_specs,
)  # noqa: E402
from ..module_utils.v4.prism.tasks import wait_for_completion  # noqa: E402
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
)

SDK_IMP_ERROR = None
try:
    import ntnx_objects_py_client as objects_sdk  # noqa: E402
except ImportError:

    from ..module_utils.v4.sdk_mock import mock_sdk as objects_sdk  # noqa: E402

    SDK_IMP_ERROR = traceback.format_exc()

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    module_args = dict(
        object_store_ext_id=dict(type="str", required=True),
        path=dict(
            type="str",
            required=True,
            description="Path to a JSON file containing certificate details.",
        ),
    )
    return module_args


def create_certificate(module, object_stores_api, result):
    """
    This method will create SSL certificate for object store.
    Args:
        module (object): Ansible module object
        object_stores_api (object): ObjectStoresApi instance
        result (dict): Result object
    """
    object_store_ext_id = module.params.get("object_store_ext_id")
    path = module.params.get("path")
    path = Path(path)

    current_spec = get_object_store(module, object_stores_api, object_store_ext_id)
    etag_value = get_etag(data=current_spec)
    if not etag_value:
        return module.fail_json(
            "Unable to fetch etag for creating certificate", **result
        )
    kwargs = {"if_match": etag_value}
    try:
        resp = object_stores_api.create_certificate(
            objectStoreExtId=object_store_ext_id, path=path, **kwargs
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Failed to create SSL certificate",
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
            msg=missing_required_lib("ntnx_objects_py_client"), exception=SDK_IMP_ERROR
        )

    remove_param_with_none_value(module.params)
    result = {
        "changed": False,
        "response": None,
        "ext_id": None,
    }
    object_stores_api = get_objects_api_instance(module)
    create_certificate(module, object_stores_api, result)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
