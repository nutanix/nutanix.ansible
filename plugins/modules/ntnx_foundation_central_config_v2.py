#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_foundation_central_config_v2
short_description: Update Foundation Central configuration on FCVM/Foundation
description:
    - This module updates Foundation Central configuration.
    - Foundation Central config is a singleton; there is no create or delete API.
    - C(state=present) without C(ext_id) applies the desired configuration (update).
    - C(state=present) with C(ext_id) also updates the configuration.
    - C(state=absent) is not supported and will fail.
    - This module talks to B(Foundation Central / FCVM), not Prism Central.
      Set C(nutanix_host) / C(nutanix_port) to the FCVM endpoint
      (for example C(FOUNDATION_ENDPOINT) / C(FOUNDATION_PORT)).
version_added: 2.6.0
author:
    - Abhinav Bansal (@abhinavbansal29)
    - George Ghawali (@george-ghawali)
notes:
    - >-
      This module requires Admin role on Foundation Central / FCVM for the user
      performing the operation.
    - >-
      Target host is Foundation Central / FCVM (lifecycle Foundation Central
      Config API), not Prism Central.
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=lifecycle)"
options:
    state:
        description:
            - If C(state) is C(present) and C(ext_id) is not provided, apply
              (update) the Foundation Central configuration.
            - If C(state) is C(present) and C(ext_id) is provided, update the
              Foundation Central configuration.
            - If C(state) is C(absent), the module fails because delete is not
              supported for this singleton resource.
        type: str
        choices:
            - present
            - absent
        default: present
    ext_id:
        description:
            - Optional external ID accepted for update dispatch compatibility.
            - Foundation Central config is a singleton and does not use ext_id
              in the API; the value is ignored for the update call.
        type: str
        required: false
    version:
        description:
            - Foundation Central Version.
            - Typically returned by the GET API and is read-only.
        type: str
        required: false
    commit_id:
        description:
            - Foundation Central Commit ID.
            - Typically returned by the GET API and is read-only.
        type: str
        required: false
    tls_certificate_fingerprint:
        description:
            - SHA-256 fingerprint of the TLS certificate used by Foundation
              Central service.
            - Typically returned by the GET API and is read-only.
        type: str
        required: false
    aos_download_timeout_minutes:
        description:
            - Timeout in minutes for AOS download.
        type: int
        required: false
    ahv_installation_timeout_minutes:
        description:
            - Timeout in minutes for AHV installation.
        type: int
        required: false
extends_documentation_fragment:
    - nutanix.ncp.ntnx_credentials
    - nutanix.ncp.ntnx_operations_v2
    - nutanix.ncp.ntnx_logger
    - nutanix.ncp.ntnx_proxy_v2
"""

EXAMPLES = r"""
- name: Update Foundation Central config timeouts on FCVM
  nutanix.ncp.ntnx_foundation_central_config_v2:
    nutanix_host: "<foundation_central_ip>"
    nutanix_port: 9440
    nutanix_username: "<user>"
    nutanix_password: "<pass>"
    validate_certs: false
    aos_download_timeout_minutes: 60
    ahv_installation_timeout_minutes: 50
  register: fcc_config_update
"""

RETURN = r"""
response:
    description:
        - The Foundation Central configuration after the update operation.
    type: dict
    returned: always
    sample:
        {
            "ahv_installation_timeout_minutes": 50,
            "aos_download_timeout_minutes": 60,
            "commit_id": "8701b044",
            "tls_certificate_fingerprint": "0789169a1c913336750712ad51ce22a27abcb6ba3a1bbce8a3155decf53c8757",
            "version": "2.2"
        }
changed:
    description: Whether the module made any changes
    type: bool
    returned: always
    sample: true
ext_id:
    description:
        - External ID of the resource.
        - Always null for this singleton Foundation Central config.
    type: str
    returned: always
    sample: null
task_ext_id:
    description: The task external ID returned by the update API
    type: str
    returned: always
    sample: "ZXJnb24=:04b8f6c2-80b0-5149-9e63-1077d02ae92e"
skipped:
    description: Indicates if the operation was skipped due to idempotency
    type: bool
    returned: when applicable
    sample: true
msg:
    description: Status or error message
    type: str
    returned: when applicable
    sample: "Nothing to change for Foundation Central config. Skipping update."
error:
    description: Error details
    type: str
    returned: always
    sample: null
failed:
    description: Whether the module failed
    type: bool
    returned: when something fails
    sample: false
"""


import traceback  # noqa: E402
import warnings  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_module_v4 import BaseModuleV4  # noqa: E402
from ..module_utils.v4.lcm.api_client import (  # noqa: E402
    get_etag,
    get_foundation_central_config_api_instance,
)
from ..module_utils.v4.lcm.helpers import get_foundation_central_config  # noqa: E402
from ..module_utils.v4.prism.tasks import wait_for_completion  # noqa: E402
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
)

SDK_IMP_ERROR = None
try:
    import ntnx_lifecycle_py_client as lifecycle_sdk  # noqa: E402
except ImportError:

    from ..module_utils.v4.sdk_mock import mock_sdk as lifecycle_sdk  # noqa: E402

    SDK_IMP_ERROR = traceback.format_exc()
# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")

CONFIG_FIELDS = (
    "version",
    "commit_id",
    "tls_certificate_fingerprint",
    "aos_download_timeout_minutes",
    "ahv_installation_timeout_minutes",
)


def get_module_spec():

    module_args = dict(
        state=dict(type="str", default="present", choices=["present", "absent"]),
        ext_id=dict(type="str", required=False),
        version=dict(type="str", required=False),
        commit_id=dict(type="str", required=False),
        tls_certificate_fingerprint=dict(type="str", required=False),
        aos_download_timeout_minutes=dict(type="int", required=False),
        ahv_installation_timeout_minutes=dict(type="int", required=False),
    )
    return module_args


def check_foundation_central_config_idempotency(current_spec, update_spec):
    """
    Return True when none of the provided update fields differ from current.
    """
    for field in CONFIG_FIELDS:
        new_val = getattr(update_spec, field, None)
        if new_val is None:
            continue
        if getattr(current_spec, field, None) != new_val:
            return False
    return True


def _build_update_spec(module, result):
    sg = SpecGenerator(module)
    default_spec = lifecycle_sdk.FoundationCentralConfig()
    update_spec, err = sg.generate_spec(obj=default_spec)
    if err:
        result["error"] = err
        result["failed"] = True
        module.fail_json(
            msg="Failed creating spec for updating Foundation Central config", **result
        )
    return update_spec


def _ensure_at_least_one_config_field(module, result):
    """
    Fail when no Foundation Central config attributes are provided.
    """
    provided = [
        field for field in CONFIG_FIELDS if module.params.get(field) is not None
    ]
    if not provided:
        result["failed"] = True
        result["error"] = "Missing Foundation Central config fields"
        module.fail_json(
            msg="Provide at least one of: {0}".format(", ".join(CONFIG_FIELDS)),
            **result,
        )


def _apply_foundation_central_config(module, result, api_instance):
    """
    Apply desired Foundation Central config via Update API (singleton).
    """
    _ensure_at_least_one_config_field(module, result)

    current_spec = get_foundation_central_config(module, api_instance)
    etag_value = get_etag(current_spec)
    if not etag_value:
        result["failed"] = True
        module.fail_json(
            msg="Failed to get etag value from the current Foundation Central config",
            **result,
        )

    update_spec = _build_update_spec(module, result)

    if module.check_mode:
        result["response"] = strip_internal_attributes(update_spec.to_dict())
        result["ext_id"] = None
        return

    if check_foundation_central_config_idempotency(current_spec, update_spec):
        result["skipped"] = True
        result["response"] = strip_internal_attributes(current_spec.to_dict())
        result["ext_id"] = None
        module.exit_json(
            msg="Nothing to change for Foundation Central config. Skipping update.",
            **result,
        )

    resp = None
    try:
        resp = api_instance.update_foundation_central_config(
            body=update_spec, if_match=etag_value
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while updating Foundation Central config",
        )

    task_ext_id = None
    if resp and getattr(resp, "data", None) is not None:
        task_ext_id = getattr(resp.data, "ext_id", None)
    result["task_ext_id"] = task_ext_id
    result["ext_id"] = None

    if task_ext_id and module.params.get("wait"):
        wait_for_completion(module, task_ext_id)

    resp = get_foundation_central_config(module, api_instance)
    result["response"] = strip_internal_attributes(resp.to_dict())
    result["changed"] = True


def create_foundation_central_config(module, result, api_instance):
    """
    Ensure Foundation Central config matches desired state.

    There is no Create API for this singleton; this applies an update.
    """
    _apply_foundation_central_config(module, result, api_instance)


def update_foundation_central_config(module, result, api_instance):
    """
    Update Foundation Central configuration using the Update API.
    """
    _apply_foundation_central_config(module, result, api_instance)


def delete_foundation_central_config(module, result, api_instance):
    """
    Delete is not supported for Foundation Central config singleton.
    """
    result["failed"] = True
    result["error"] = "Delete is not supported for Foundation Central config"
    module.fail_json(
        msg="Delete is not supported for Foundation Central config. "
        "This resource is a singleton managed only via Get/Update APIs. "
        "API client type: {0}".format(type(api_instance).__name__),
        **result,
    )


def run_module():
    module = BaseModuleV4(
        argument_spec=get_module_spec(),
        supports_check_mode=True,
    )

    if SDK_IMP_ERROR:
        module.fail_json(
            msg="Missing required library ntnx_lifecycle_py_client",
            exception=SDK_IMP_ERROR,
        )

    remove_param_with_none_value(module.params)
    result = {
        "changed": False,
        "response": None,
        "ext_id": None,
        "task_ext_id": None,
        "error": None,
    }
    api_instance = get_foundation_central_config_api_instance(module)

    state = module.params.get("state")
    if state == "present":
        if module.params.get("ext_id"):
            update_foundation_central_config(module, result, api_instance)
        else:
            create_foundation_central_config(module, result, api_instance)
    else:
        delete_foundation_central_config(module, result, api_instance)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
