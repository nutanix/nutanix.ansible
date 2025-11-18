#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2025, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type
DOCUMENTATION = r"""
module: ntnx_object_stores_certificate_info_v2
short_description: Get Object Stores certificate info
version_added: 2.2.0
description:
    - Fetch specific object store certificate info if external ID is provided
    - Fetch list of multiple object store certificates info if external ID is not provided with optional filters
    - This module uses PC v4 APIs based GA SDKs
options:
    object_store_ext_id:
        description: object store external ID
        type: str
        required: true
    ext_id:
        description: external ID of certificate to fetch
        type: str
extends_documentation_fragment:
    - nutanix.ncp.ntnx_credentials
    - nutanix.ncp.ntnx_info_v2
    - nutanix.ncp.ntnx_logger
author:
    - George Ghawali (@george-ghawali)
"""

EXAMPLES = r"""
- name: List all certificates for an object store
  nutanix.ncp.ntnx_object_stores_certificate_info_v2:
    object_store_ext_id: "cda893b8-2aee-34bf-817d-d2ee6026790b"
  register: result
  ignore_errors: true

- name: Fetch certificate details using external ID
  nutanix.ncp.ntnx_object_stores_certificate_info_v2:
    object_store_ext_id: "cda893b8-2aee-34bf-817d-d2ee6026790b"
    ext_id: "f3197423-f486-4037-6037-95442e58484e"
  register: result
"""

RETURN = r"""
response:
    description:
        - Response for fetching object store certificate info
        - Object store certificate info if external ID is provided
        - List of multiple object store certificates info if external ID is not provided
    type: dict
    returned: always
    sample:
        {
            "alternate_fqdns": null,
            "alternate_ips": [
                {
                    "ipv4": {
                        "prefix_length": 32,
                        "value": "10.44.77.123"
                    },
                    "ipv6": null
                }
            ],
            "ca": null,
            "ext_id": "b18822e9-b417-4834-6191-986010a4ee06",
            "links": null,
            "metadata": null,
            "private_key": null,
            "public_cert": null,
            "should_generate": false,
            "tenant_id": null
        }

ext_id:
    description: External ID of the object store certificate
    returned: always
    type: str
    sample: "cda893b8-2aee-34bf-817d-d2ee6026790b"

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
total_available_results:
    description:
        - The total number of available object store certificates for the given object store
    type: int
    returned: when all object store certificates for the given object store are fetched
    sample: 125
"""

import warnings  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.objects.api_client import get_objects_api_instance  # noqa: E402
from ..module_utils.v4.objects.helpers import get_object_store_certificate  # noqa: E402
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
)

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    module_args = dict(
        object_store_ext_id=dict(type="str", required=True),
        ext_id=dict(type="str"),
    )
    return module_args


def get_object_store_certificate_with_ext_id(module, object_stores_api, result):
    ext_id = module.params.get("ext_id")
    object_store_ext_id = module.params.get("object_store_ext_id")
    resp = get_object_store_certificate(
        module, object_stores_api, ext_id, object_store_ext_id
    )
    result["ext_id"] = ext_id
    result["response"] = strip_internal_attributes(resp.to_dict())


def get_object_store_certificates(module, object_stores_api, result):
    object_store_ext_id = module.params.get("object_store_ext_id")
    sg = SpecGenerator(module)
    kwargs, err = sg.get_info_spec(attr=module.params)

    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed generating object store certificates info Spec", **result
        )
    try:
        resp = object_stores_api.list_certificates_by_objectstore_id(
            objectStoreExtId=object_store_ext_id, **kwargs
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching object store certificates info",
        )

    total_available_results = resp.metadata.total_available_results
    result["total_available_results"] = total_available_results

    resp = strip_internal_attributes(resp.to_dict()).get("data")
    if not resp:
        resp = []
    result["response"] = resp


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
    object_stores_api = get_objects_api_instance(module)
    if module.params.get("ext_id"):
        get_object_store_certificate_with_ext_id(module, object_stores_api, result)
    else:
        get_object_store_certificates(module, object_stores_api, result)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
