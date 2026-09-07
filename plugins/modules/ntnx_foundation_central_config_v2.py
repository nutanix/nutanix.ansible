#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_foundation_central_config_v2
short_description: Update Foundation Central configuration
description:
    - This module updates the Foundation Central (FC) service configuration.
    - The Foundation Central configuration is a singleton resource, so only the
      update operation is supported (C(state=present)).
    - This module supports idempotency and check mode.
version_added: 2.6.0
author:
    - Abhinav Bansal (@abhinavbansal29)
    - George Ghawali (@george-ghawali)
notes:
    - This module talks to the Foundation Central VM (FCVM)/Foundation endpoint,
      B(not) Prism Central. Set C(nutanix_host)/C(nutanix_port) to the
      FCVM/Foundation endpoint (default port C(9440)).
    - >-
      B(Update the Foundation Central configuration.) -
      Requires an Admin role on the Foundation Central VM (FCVM).
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=lifecycle)"
options:
    state:
        description:
            - State of the Foundation Central configuration.
            - If C(present), the module will update the Foundation Central configuration.
        type: str
        choices:
            - present
        default: present
    tls_certificate_fingerprint:
        description:
            - The TLS certificate fingerprint used by the Foundation Central service.
        type: str
        required: false
    aos_download_timeout_minutes:
        description:
            - The timeout, in minutes, for downloading an AOS package.
        type: int
        required: false
    ahv_installation_timeout_minutes:
        description:
            - The timeout, in minutes, for installing AHV.
        type: int
        required: false
extends_documentation_fragment:
    - nutanix.ncp.ntnx_credentials
    - nutanix.ncp.ntnx_operations_v2
    - nutanix.ncp.ntnx_logger
    - nutanix.ncp.ntnx_proxy_v2
"""

EXAMPLES = r"""
- name: Update Foundation Central configuration
  nutanix.ncp.ntnx_foundation_central_config_v2:
    nutanix_host: <fcvm_ip>
    nutanix_username: <user>
    nutanix_password: <pass>
    aos_download_timeout_minutes: 60
    ahv_installation_timeout_minutes: 30
    tls_certificate_fingerprint: "AA:BB:CC:DD:EE:FF"
  register: fc_config_update
"""

RETURN = r"""
response:
    description: The response from the Nutanix Foundation Central config v4 API (served by FCVM/Foundation).
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
    description: Whether the module made any changes.
    type: bool
    returned: always
    sample: true
ext_id:
    description: The external ID of the Foundation Central configuration.
    type: str
    returned: always
    sample: null
task_ext_id:
    description: The task external ID of the update operation, if returned by the API.
    type: str
    returned: always
    sample: null
skipped:
    description: Indicates if the operation was skipped due to idempotency.
    type: bool
    returned: When the operation was skipped
    sample: true
msg:
    description: A status or informational message.
    returned: When applicable
    type: str
    sample: "Nothing to change."
error:
    description: Error details, if any error occurred during the task execution.
    type: str
    returned: When an error occurs
    sample: "Api Exception raised while updating Foundation Central config"
failed:
    description: Indicates whether the task failed.
    type: bool
    returned: When something fails
    sample: false
"""

import copy  # noqa: E402
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
    strip_users_empty_attributes,
)

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():

    module_args = dict(
        state=dict(type="str", default="present", choices=["present"]),
        tls_certificate_fingerprint=dict(type="str"),
        aos_download_timeout_minutes=dict(type="int"),
        ahv_installation_timeout_minutes=dict(type="int"),
    )
    return module_args


# Writable fields of the Foundation Central config (i.e. accepted on the
# update request body). Read-only fields such as ``version`` and ``commit_id``
# are intentionally excluded from the idempotency comparison.
WRITABLE_FIELDS = (
    "tls_certificate_fingerprint",
    "aos_download_timeout_minutes",
    "ahv_installation_timeout_minutes",
)


def check_foundation_central_config_idempotency(current_spec, update_spec):
    """Return True if the update spec introduces no changes to the current config.

    Only the writable fields are compared. Read-only/server-populated fields
    (e.g. ``version``, ``commit_id``) are ignored so an unchanged update is
    correctly detected as idempotent.
    """
    for field in WRITABLE_FIELDS:
        if getattr(current_spec, field, None) != getattr(update_spec, field, None):
            return False
    return True


def update_foundation_central_config(module, result, api_instance):
    """Update the Foundation Central configuration (singleton resource).

    The update API is a full replace (HTTP PUT), so the spec is seeded from the
    current configuration and only the fields the user provided are overridden.
    This preserves unspecified writable fields and read-only/server-populated
    fields.
    """
    current_config = get_foundation_central_config(module, api_instance)
    etag_value = get_etag(current_config)
    if not etag_value:
        module.fail_json(
            msg="Failed to get etag value from the current Foundation Central config",
            **result,
        )

    current_spec = current_config.data
    strip_users_empty_attributes(current_spec)

    # Seed the update spec from the current config so unspecified fields keep
    # their current values (the API performs a full replace).
    sg = SpecGenerator(module)
    default_spec = copy.deepcopy(current_spec)
    update_spec, err = sg.generate_spec(obj=default_spec)
    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed generating spec for updating Foundation Central config",
            **result,
        )

    if check_foundation_central_config_idempotency(current_spec, update_spec):
        result["skipped"] = True
        result["response"] = strip_internal_attributes(current_spec.to_dict())
        if module.check_mode:
            return
        module.exit_json(msg="Nothing to change.", **result)

    if module.check_mode:
        result["response"] = strip_internal_attributes(update_spec.to_dict())
        return

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

    task_ext_id = getattr(resp.data, "ext_id", None)
    result["task_ext_id"] = task_ext_id
    if task_ext_id and module.params.get("wait"):
        wait_for_completion(module, task_ext_id)

    updated_config = get_foundation_central_config(module, api_instance)
    result["response"] = strip_internal_attributes(updated_config.data.to_dict())
    result["changed"] = True


def run_module():
    module = BaseModuleV4(
        argument_spec=get_module_spec(),
        supports_check_mode=True,
    )

    remove_param_with_none_value(module.params)
    result = {
        "changed": False,
        "response": None,
        "ext_id": None,
        "task_ext_id": None,
    }
    api_instance = get_foundation_central_config_api_instance(module)
    update_foundation_central_config(module, result, api_instance)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
