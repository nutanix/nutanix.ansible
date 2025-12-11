#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2024, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_categories_v2
short_description: Manage categories in Nutanix Prism Central
version_added: "2.0.0"
description:
    - This module allows you to create, update, and delete categories in Nutanix Prism Central.
    - This module uses PC v4 APIs based SDKs
options:
  ext_id:
    description:
      - The external ID of the category.
    required: false
    type: str
  key:
    description:
      - The key of the category.
    required: false
    type: str

  value:
    description:
      - The value of the category.
    required: false
    type: str
  type:
    description:
      - The type of the category.
    required: false
    choices: ['USER']
    default: 'USER'
    type: str
  owner_uuid:
    description:
      - The owner UUID of the category.
    required: false
    type: str
  description:
    description:
      - The description of the category.
    required: false
    type: str
extends_documentation_fragment:
      - nutanix.ncp.ntnx_credentials
      - nutanix.ncp.ntnx_operations_v2
      - nutanix.ncp.ntnx_logger
author:
 - Gevorg Khachatryan (@Gevorg-Khachatryan-97)
 - Alaa Bishtawi (@alaa-bish)
"""

EXAMPLES = r"""
- name: Create category key & value
  nutanix.ncp.ntnx_categories_v2:
    nutanix_host: <pc_ip>
    nutanix_username: <user>
    nutanix_password: <pass>
    key: "key1"
    value: "val1"
    description: "ansible test"

- name: Update category value and description
  nutanix.ncp.ntnx_categories_v2:
    nutanix_host: <pc_ip>
    nutanix_username: <user>
    nutanix_password: <pass>
    ext_id: "<ext_id>"
    key: "key1"
    value: "val2"
    description: "ansible test New value"

- name: Delete created category key value pair
  nutanix.ncp.ntnx_categories_v2:
    nutanix_host: <pc_ip>
    nutanix_username: <user>
    nutanix_password: <pass>
    ext_id: "<ext_id>"
    state: absent
"""

RETURN = r"""
response:
  description:
    - when wait is false, the response will be task status.
    - Else The response from the Nutanix PC category v4 API.
  type: dict
  returned: always
  sample:
    {
                "associations": [
                    {
                        "category_id": null,
                        "count": 18,
                        "resource_group": "ENTITY",
                        "resource_type": "VM"
                    }
                ],
                "description": "Created by CALM",
                "detailed_associations": null,
                "ext_id": "cc16efb4-6591-4b89-a643-8c835f035393",
                "key": "OSType",
                "links": [
                    {
                        "href": "https://00.00.00.00:9440/api/prism/v4.0.b1/config/categories/cc16efb4-6591-4b89-a643-8c835f035393",
                        "rel": "self"
                    }
                ],
                "owner_uuid": null,
                "tenant_id": null,
                "type": "USER",
                "value": "Linux"
            }
msg:
    description: This indicates the message if any message occurred
    returned: When there is an error, module is idempotent or check mode (in delete operation)
    type: str
    sample: "Api Exception raised while fetching category info using ext_id"
error:
  description: The error message if an error occurs.
  type: str
  returned: when an error occurs
ext_id:
    description:
        - The external ID of the category is fetched.
    type: str
    returned: always
    sample: "dded1b87-e566-419a-aac0-fb282792fb83"
changed:
    description: Indicates whether the resource has changed.
    type: bool
    returned: always
    sample: true
"""

import traceback  # noqa: E402
import warnings  # noqa: E402
from copy import deepcopy  # noqa: E402

from ansible.module_utils.basic import missing_required_lib  # noqa: E402

from ..module_utils.base_module import BaseModule  # noqa: E402
from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.prism.pc_api_client import (  # noqa: E402
    get_etag,
    get_pc_api_client,
)
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
        ext_id=dict(type="str"),
        key=dict(type="str", no_log=False),
        value=dict(type="str"),
        type=dict(type="str", choices=["USER"], default="USER"),
        owner_uuid=dict(type="str"),
        description=dict(type="str"),
    )

    return module_args


_PRISM_SDK = None


def get_category_api_instance(module):
    global _PRISM_SDK
    if not _PRISM_SDK:
        api_client = get_pc_api_client(module)
        _PRISM_SDK = prism_sdk.CategoriesApi(api_client=api_client)

    return _PRISM_SDK


def get_category(module, ext_id):
    categories = get_category_api_instance(module)
    try:
        return categories.get_category_by_id(extId=ext_id).data
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching category info using ext_id",
        )


def create_category(module, result):
    categories = get_category_api_instance(module)

    sg = SpecGenerator(module)
    default_spec = prism_sdk.Category()
    spec, err = sg.generate_spec(obj=default_spec)

    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating create categories Spec", **result)

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        return

    resp = None
    try:
        resp = categories.create_category(body=spec)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while creating category",
        )

    result["ext_id"] = resp.data.ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    result["changed"] = True


def check_categories_idempotency(old_spec, update_spec):
    old_spec = deepcopy(old_spec)
    update_spec = deepcopy(update_spec)
    strip_internal_attributes(old_spec)
    strip_internal_attributes(update_spec)
    if old_spec != update_spec:
        return False

    return True


def update_category(module, result):
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id

    current_spec = get_category(module, ext_id=ext_id)
    sg = SpecGenerator(module)
    update_spec, err = sg.generate_spec(obj=deepcopy(current_spec))

    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating categories update spec", **result)

    # check for idempotency
    if check_categories_idempotency(current_spec.to_dict(), update_spec.to_dict()):
        result["skipped"] = True
        module.exit_json(msg="Nothing to change.", **result)

    if module.check_mode:
        result["response"] = strip_internal_attributes(update_spec.to_dict())
        return

    resp = None
    categories = get_category_api_instance(module)
    try:
        resp = categories.update_category_by_id(extId=ext_id, body=update_spec)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while updating category",
        )
    result["response"] = strip_internal_attributes(resp.data[0].to_dict())

    try:
        resp = categories.get_category_by_id(ext_id)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching category info",
        )
    result["response"] = strip_internal_attributes(resp.to_dict()).get("data")
    result["changed"] = True


def delete_category(module, result):
    categories = get_category_api_instance(module)
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id

    if module.check_mode:
        result["msg"] = "Category with ext_id:{0} will be deleted.".format(ext_id)
        return

    current_spec = get_category(module, ext_id=ext_id)

    etag = get_etag(data=current_spec)
    if not etag:
        return module.fail_json("Unable to fetch etag for deleting category", **result)

    kwargs = {"if_match": etag}

    try:
        resp = categories.delete_category_by_id(extId=ext_id, **kwargs)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while deleting category",
        )

    result["response"] = strip_internal_attributes(resp)
    result["changed"] = True


def run_module():
    module = BaseModule(
        argument_spec=get_module_spec(),
        supports_check_mode=True,
        required_if=[
            ("state", "present", ("ext_id", "key", "value"), True),
            ("state", "absent", ("ext_id",)),
        ],
    )
    if SDK_IMP_ERROR:
        module.fail_json(
            msg=missing_required_lib("ntnx_prism_py_client"), exception=SDK_IMP_ERROR
        )

    remove_param_with_none_value(module.params)
    result = {
        "changed": False,
        "error": None,
        "response": None,
        "ext_id": None,
    }
    state = module.params["state"]
    if state == "present":
        if module.params.get("ext_id"):
            update_category(module, result)
        else:
            create_category(module, result)
    else:
        delete_category(module, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
