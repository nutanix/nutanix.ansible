#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_vcenter_extension_v2
short_description: Register or unregister vCenter Server extension in Nutanix Prism Central
version_added: 2.7.0
description:
  - This module allows you to register (C(state=present)) or unregister
    (C(state=absent)) a vCenter Server extension for an ESXi cluster attached
    to a Nutanix Prism Central.
  - The vCenter Server extension is what allows Nutanix Prism to perform VM
    management and other operations on an ESXi based Nutanix cluster via the
    vCenter that manages it.
  - The vCenter extension objects are discovered by Prism Central for every
    ESXi cluster it manages. An C(ext_id) that identifies the extension must
    be supplied for every register / unregister call; you can obtain the
    C(ext_id) using M(nutanix.ncp.ntnx_vcenter_extensions_info_v2).
  - This module uses PC v4 APIs based SDKs.
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
      The required roles depend on the operation being performed.
    - >-
      B(Register a vCenter Server extension) -
      Required Roles: Prism Admin, Super Admin
    - >-
      B(Unregister a vCenter Server extension) -
      Required Roles: Prism Admin, Super Admin
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=clustermgmt)"
options:
  state:
    description:
      - If C(state) is set to C(present), the vCenter Server extension identified
        by C(ext_id) will be registered using the supplied credentials.
      - If C(state) is set to C(absent), the vCenter Server extension identified
        by C(ext_id) will be unregistered using the supplied credentials.
    type: str
    required: false
    choices:
      - present
      - absent
    default: present
  ext_id:
    description:
      - The globally unique identifier of the vCenter Server extension instance
        (UUID). It should match the C(ext_id) returned by the
        M(nutanix.ncp.ntnx_vcenter_extensions_info_v2) list operation.
      - Required for register and unregister operations.
    type: str
    required: false
  username:
    description:
      - Username of a vCenter Server administrator account that can register or
        unregister the Nutanix Prism vCenter extension.
      - Required for register and unregister operations.
    type: str
    required: false
  password:
    description:
      - Password associated with C(username) used to register or unregister the
        Nutanix Prism vCenter extension.
      - Required for register and unregister operations.
    type: str
    required: false
  port:
    description:
      - Port used to reach the vCenter Server API for registering or
        unregistering the Nutanix Prism vCenter extension.
    type: int
    required: false
    default: 443
extends_documentation_fragment:
  - nutanix.ncp.ntnx_credentials
  - nutanix.ncp.ntnx_operations_v2
  - nutanix.ncp.ntnx_logger
  - nutanix.ncp.ntnx_proxy_v2
author:
  - Abhinav Bansal (@abhinavbansal29)
  - George Ghawali (@george-ghawali)
"""

EXAMPLES = r"""
- name: Register vCenter Server extension
  nutanix.ncp.ntnx_vcenter_extension_v2:
    state: present
    ext_id: "00061c8b-2f6e-4a1c-8b41-abc123abc123"
    username: "administrator@vsphere.local"
    password: "vcenter-admin-password"
    port: 443
  register: register_result

- name: Unregister vCenter Server extension
  nutanix.ncp.ntnx_vcenter_extension_v2:
    state: absent
    ext_id: "00061c8b-2f6e-4a1c-8b41-abc123abc123"
    username: "administrator@vsphere.local"
    password: "vcenter-admin-password"
    port: 443
  register: unregister_result
"""

RETURN = r"""
response:
  description:
    - Response for registering or unregistering a vCenter Server extension.
    - If the operation is register and C(wait) is true, it will return the
      refreshed vCenter Server extension details.
    - If the operation is register and C(wait) is false, it will return the
      task details.
    - If the operation is unregister, it will return the task details.
  returned: always
  type: dict
  sample:
    {
      "cluster_ext_id": "0006555e-4e63-4a5e-185b-ac1f6b6f97e2",
      "ext_id": "00061c8b-2f6e-4a1c-8b41-abc123abc123",
      "ip_address": "10.10.10.20",
      "is_registered": true,
      "links": null,
      "tenant_id": null
    }

task_ext_id:
  description:
    - The external ID of the task.
  returned: always
  type: str
  sample: "ZXJnb24=:90458bc7-a12b-4616-ac66-562fdb00c209"

ext_id:
  description:
    - The external ID of the vCenter Server extension.
  returned: always
  type: str
  sample: "00061c8b-2f6e-4a1c-8b41-abc123abc123"

changed:
  description: This indicates whether the task resulted in any changes
  returned: always
  type: bool
  sample: true

skipped:
  description: This indicates whether the task was skipped
  returned: always
  type: bool
  sample: false

error:
  description: This indicates the error message if any error occurred
  returned: When an error occurs
  type: str

failed:
  description: This indicates whether the task failed
  returned: always
  type: bool
  sample: false

msg:
  description: This indicates the message if any message occurred
  returned: When there is an error, module is idempotent or check mode (in delete operation)
  type: str
  sample: "vCenter extension with ext_id '00061c8b-2f6e-4a1c-8b41-abc123abc123' is already registered. Skipping registration."
"""

import traceback  # noqa: E402
import warnings  # noqa: E402

from ansible.module_utils.basic import missing_required_lib  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_module_v4 import BaseModuleV4  # noqa: E402
from ..module_utils.v4.clusters_mgmt.api_client import (  # noqa: E402
    get_etag,
    get_vcenter_extensions_api_instance,
)
from ..module_utils.v4.clusters_mgmt.helpers import get_vcenter_extension  # noqa: E402
from ..module_utils.v4.prism.tasks import wait_for_completion  # noqa: E402
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
    validate_required_params,
)

SDK_IMP_ERROR = None
try:
    import ntnx_clustermgmt_py_client as cluster_management_sdk  # noqa: E402
except ImportError:

    from ..module_utils.v4.sdk_mock import (  # noqa: E402
        mock_sdk as cluster_management_sdk,
    )

    SDK_IMP_ERROR = traceback.format_exc()

warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    """
    Return the argument spec for the ntnx_vcenter_extension_v2 module.

    Fields:
        ext_id:    vCenter extension UUID (required for register/unregister).
        username:  vCenter admin username used for the register/unregister API.
        password:  vCenter admin password (secret, ``no_log=True``).
        port:      vCenter Server API port (defaults to 443).
    """
    module_args = dict(
        ext_id=dict(type="str"),
        username=dict(type="str"),
        password=dict(type="str", no_log=True),
        port=dict(type="int", default=443),
    )
    return module_args


def _build_credentials_spec(module, result, operation):
    """Build a ``VcenterCredentials`` SDK spec from module.params.

    Args:
        module: Ansible module.
        result: Module result dict (populated on failure).
        operation: Human readable operation name (used in error msg).

    Returns:
        object: populated ``VcenterCredentials`` SDK object.
    """
    sg = SpecGenerator(module)
    default_spec = cluster_management_sdk.VcenterCredentials()
    spec, err = sg.generate_spec(obj=default_spec)
    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed generating {0} vCenter extension spec".format(operation),
            **result,
        )
    return spec


def _register_vcenter_extension(module, result, api_instance):
    """Register the vCenter Server extension identified by ``ext_id``.

    This is the core implementation shared by the ``create`` and ``update``
    dispatch entry points. The vCenter extension SDK exposes only register
    (create) and unregister (delete) actions; both require an ``ext_id``
    that already exists on the Prism Central, so registration is treated
    as an idempotent action on a discovered extension.
    """
    validate_required_params(module, ["ext_id", "username", "password"])
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id

    current = get_vcenter_extension(module, api_instance, ext_id)
    etag = get_etag(data=current)

    if getattr(current, "is_registered", False):
        result["skipped"] = True
        result["response"] = strip_internal_attributes(current.to_dict())
        module.exit_json(
            msg=(
                "vCenter extension with ext_id '{0}' is already registered. "
                "Skipping registration."
            ).format(ext_id),
            **result,
        )

    spec = _build_credentials_spec(module, result, "register")

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        return

    kwargs = {"if_match": etag} if etag else {}
    try:
        resp = api_instance.register_vcenter_extension(
            extId=ext_id, body=spec, **kwargs
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while registering vCenter extension",
        )

    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())

    if task_ext_id and module.params.get("wait"):
        wait_for_completion(module, task_ext_id)
        refreshed = get_vcenter_extension(module, api_instance, ext_id)
        result["response"] = strip_internal_attributes(refreshed.to_dict())
    result["changed"] = True


def create_VcenterExtension(module, result, api_instance):
    """Create dispatch entry point.

    The vCenter extension SDK exposes only a ``register`` action and always
    requires an existing ``ext_id``; therefore ``state=present`` without an
    ``ext_id`` is not a supported workflow. This function is retained to
    match the standard v2 module layout and delegates to the shared
    register implementation.
    """
    _register_vcenter_extension(module, result, api_instance)


def update_VcenterExtension(module, result, api_instance):
    """Update dispatch entry point — mapped to the SDK register action.

    Because the vCenter extension SDK does not expose a discrete update
    action, ``state=present`` with an ``ext_id`` maps to the register API.
    Idempotency is preserved via a pre-check of ``is_registered``.
    """
    _register_vcenter_extension(module, result, api_instance)


def delete_VcenterExtension(module, result, api_instance):
    """Delete dispatch entry point — mapped to the SDK unregister action.

    ``state=absent`` with an ``ext_id`` calls the unregister API using the
    supplied vCenter credentials. Idempotency is preserved via a pre-check
    of ``is_registered``.
    """
    validate_required_params(module, ["ext_id", "username", "password"])
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id

    current = get_vcenter_extension(module, api_instance, ext_id)
    etag = get_etag(data=current)

    if not getattr(current, "is_registered", True):
        result["skipped"] = True
        result["response"] = strip_internal_attributes(current.to_dict())
        module.exit_json(
            msg=(
                "vCenter extension with ext_id '{0}' is already unregistered. "
                "Skipping unregistration."
            ).format(ext_id),
            **result,
        )

    if module.check_mode:
        result["msg"] = (
            "vCenter extension with ext_id:{0} will be unregistered.".format(ext_id)
        )
        return

    spec = _build_credentials_spec(module, result, "unregister")

    kwargs = {"if_match": etag} if etag else {}
    try:
        resp = api_instance.unregister_vcenter_extension(
            extId=ext_id, body=spec, **kwargs
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while unregistering vCenter extension",
        )

    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        task_status = wait_for_completion(module, task_ext_id)
        result["response"] = strip_internal_attributes(task_status.to_dict())
    result["changed"] = True


def run_module():
    module = BaseModuleV4(
        argument_spec=get_module_spec(),
        supports_check_mode=True,
        required_if=[
            ("state", "present", ("ext_id",)),
            ("state", "absent", ("ext_id",)),
        ],
        required_together=[
            ("username", "password"),
        ],
    )
    if SDK_IMP_ERROR:
        module.fail_json(
            msg=missing_required_lib("ntnx_clustermgmt_py_client"),
            exception=SDK_IMP_ERROR,
        )

    remove_param_with_none_value(module.params)
    result = {
        "changed": False,
        "response": None,
        "failed": False,
        "ext_id": None,
    }
    api_instance = get_vcenter_extensions_api_instance(module)
    state = module.params.get("state")
    if state == "present":
        if module.params.get("ext_id"):
            update_VcenterExtension(module, result, api_instance)
        else:
            create_VcenterExtension(module, result, api_instance)
    else:
        delete_VcenterExtension(module, result, api_instance)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
