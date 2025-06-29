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
    - This module creates a new default certificate and keys.
    - It can be used to configure alternate FQDNs and alternative IPs for the Object Store.
    - The certificate can be created when the Object Store is in an OBJECT_STORE_AVAILABLE or
      OBJECT_STORE_CERT_CREATION_FAILED state.
    - If 'publicCert', 'privateKey', and 'ca' are provided in the request body, they will be used
      to create the new certificate.
    - If those values are not provided, a new certificate will be generated if 'shouldGenerate' is true.
    - If 'shouldGenerate' is false, the existing certificate will be reused as the new certificate.
    - Optionally, a list of alternate FQDNs and IPs can be provided.
    - These 'alternateFqdns' and 'alternateIps' must be included in the CA certificate if a CA is provided.
    - This module uses PC v4 APIs based GA SDKs.
options:
    object_store_ext_id:
        description:
            - External ID of the object store to which the SSL certificate will be added.
        type: str
        required: true
    path:
        description:
            - Path to a JSON file containing certificate details.
            - The JSON file can contain alternateFqdns, alternateIps, shouldGenerate, ca, publicCert, and privateKey.
            - The JSON file should be in the following format
            - |
              ```
              {
                  "alternateFqdns": [{"value": "fqdn1.nutanix.com"}, {"value": "fqdn2.nutanix.com"}],
                  "alternateIps": [{"ipv4": {"value": "92.41.252.152"}}, {"ipv4": {"value": "92.41.252.153"}}],
                  "shouldGenerate": true,
                  "ca": "-----BEGIN CERTIFICATE-----\nMIIDzTCCArWgAwIBAgIUI...\n-----END CERTIFICATE-----",
                  "publicCert": "-----BEGIN CERTIFICATE-----\nMIIDzTCCArWgAwIBAgIUI...\n-----END CERTIFICATE-----",
                  "privateKey": "-----BEGIN RSA PRIVATE KEY-----\nMIIDzTCCArWgAwIBAgIUI...\n-----END RSA PRIVATE KEY-----"
              }
              ```
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
- name: Create certificate for an object store
  nutanix.ncp.ntnx_object_stores_certificate_v2:
    object_store_ext_id: "6dd6df38-5d5c-40a8-561f-10862416c1c0"
    path: "/tmp/certificate_details.json"
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
    description: Task status for Creating SSL certificate for the object store
    type: dict
    returned: always
    sample:
        {
            "cluster_ext_ids": [
                "000633ea-e256-b6a1-185b-ac1f6b6f97e2"
            ],
            "completed_time": "2025-05-04T12:04:05.735594+00:00",
            "completion_details": null,
            "created_time": "2025-05-04T12:02:23.891449+00:00",
            "entities_affected": [
                {
                    "ext_id": "62f80159-be3b-49aa-4701-9e1e32b9c828",
                    "name": "ansible-object",
                    "rel": "objects:config:object-store"
                },
                {
                    "ext_id": "b18822e9-b417-4834-6191-986010a4ee06",
                    "name": null,
                    "rel": "objects:config:object-store:certificate"
                }
            ],
            "error_messages": null,
            "ext_id": "ZXJnb24=:a0d744cf-9686-560a-b80b-c878fdbb711d",
            "is_background_task": false,
            "is_cancelable": false,
            "last_updated_time": "2025-05-04T12:04:05.735593+00:00",
            "legacy_error_message": null,
            "number_of_entities_affected": 2,
            "number_of_subtasks": 0,
            "operation": "replace_certs_object_store",
            "operation_description": "Create Object store certificate",
            "owned_by": {
                "ext_id": "00000000-0000-0000-0000-000000000000",
                "name": "admin"
            },
            "parent_task": null,
            "progress_percentage": 100,
            "root_task": null,
            "started_time": "2025-05-04T12:02:23.921955+00:00",
            "status": "SUCCEEDED",
            "sub_steps": [
                {
                    "name": "Replace certs object store 62f80159-be3b-49aa-4701-9e1e32b9c828: Running prechecks"
                },
                {
                    "name": "Replace certs object store ansible-object: Deploying oc app"
                },
                {
                    "name": "Replace certs object store ansible-object: Deploying oc app"
                },
                {
                    "name": "Replace certs object store ansible-object: Running Object store health checks"
                }
            ],
            "sub_tasks": null,
            "warnings": null
        }

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

import traceback  # noqa: E402
import warnings  # noqa: E402

from ansible.module_utils.basic import missing_required_lib  # noqa: E402

PATHLIB_IMP_ERROR = None
try:
    import pathlib  # noqa: E402
except ImportError:

    from ..module_utils.v4.sdk_mock import mock_sdk as pathlib  # noqa: E402

    PATHLIB_IMP_ERROR = traceback.format_exc()

from ..module_utils.base_module import BaseModule  # noqa: E402
from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.objects.api_client import (  # noqa: E402
    get_etag,
    get_objects_api_instance,
)
from ..module_utils.v4.objects.helpers import get_object_store  # noqa: E402
from ..module_utils.v4.prism.tasks import wait_for_completion  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
)

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    module_args = dict(
        object_store_ext_id=dict(type="str", required=True),
        path=dict(
            type="str",
            required=True,
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
    path = pathlib.Path(path)
    if not path.is_file():
        return module.fail_json(
            "Path to the JSON file which contains the public certificates, private key, and CA certificate or chain is invalid",
            **result  # fmt: skip
        )

    if module.check_mode:
        result["object_store_ext_id"] = object_store_ext_id
        result["path"] = module.params.get("path")
        result[
            "msg"
        ] = "New certificate will be created for the object store with ext_id:{0} using the certificate details file:{1}".format(
            object_store_ext_id, path
        )
        return

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
            msg="API Exception raised while creating SSL certificate",
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
    if PATHLIB_IMP_ERROR:
        module.fail_json(
            msg=missing_required_lib("pathlib"), exception=PATHLIB_IMP_ERROR
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
