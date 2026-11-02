# Module anatomy (V2)

Concrete skeletons. Reference implementations:
`plugins/modules/ntnx_address_groups_v2.py` (CRUD) and
`plugins/modules/ntnx_address_groups_info_v2.py` (info).

## CRUD module skeleton

Copyright year in the file header is always `2027` (never `2026` / current year).

```python
#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2027, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_<entity>_v2
# short_description / description / state: name ONLY supported ops
# (create and/or update and/or delete). Never say an op is "not supported".
short_description: Create, Update, Delete <entity>
version_added: "2.7.0"
description:
    - Create, Update, Delete <entity>
    - This module uses PC v4 APIs based SDKs
    # Do NOT append SDK method names here, e.g. do not write
    # (C(DomainManagerApi.update_domain_manager_by_id)) or similar.
    # Do NOT mention other module names (no M(nutanix.ncp....) cross-links).
notes:
    # IAM roles block — see sdk-and-iam.md (roles only for supported ops)
options:
  state:
    description:
        # Full CRUD example — drop create/update/delete bullets that do not apply.
        - present -> Create if ext_id not provided, Update if ext_id provided.
        - absent -> Delete with the given external ID.
    type: str
    choices: ['present', 'absent']
  # Present-only modules (no delete) — use this shape instead
  # (see ntnx_foundation_central_config_v2):
  # state:
  #     description:
  #         - State of the module.
  #         - If C(state) is C(present), the module will <supported action>.
  #         - If C(state) is C(absent), the module will fail.
  #     type: str
  #     choices:
  #         - present
  #     default: present
  ext_id:
    description:
        # Only mention update/delete here if those ops exist.
        - <Entity> External ID. Required for updating or deleting.
    type: str
  # ... one entry per input field, matching get_module_spec exactly ...
  wait:
    description:
      - Wait for the task to complete
    type: bool
    default: true
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
# see examples.md
"""

RETURN = r"""
# CRUD modules MUST document the full standard return set, same as existing CRUD
# modules (e.g. ntnx_virtual_switch_v2): response, task_ext_id, ext_id, changed,
# skipped (only if the module has an idempotency check), error (if used),
# failed, msg. Do not set skipped in check_mode alone.
# Never use `sample: null` — omit `sample:` when there is no real example.
# CRUD that re-fetches the entity when wait is true:
response:
  description:
      - Response for <entity> operations.
      - <Entity> details if C(wait) is true.
      - Task details if C(wait) is false.
  returned: always
  type: dict
  sample: {}
# Task-only action modules (no entity re-fetch; both wait values return task
# details — wait=true only waits for completion). Always use this shape:
# response:
#   description:
#       - Response for <action>.
#       - If C(wait) is true, it will contain the final task payload after completion.
#       - If C(wait) is false, it will contain the initial task details.
task_ext_id:
  description:
    - The external ID of the task.
  returned: always
  type: str
  sample: "ZXJnb24=:90458bc7-a12b-4616-ac66-562fdb00c209"
ext_id:
  description:
    - The external ID of the <entity>.
  returned: always
  type: str
  sample: "63311404-8b2e-4dbf-9e33-7848cc88d330"
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
  # Only include this RETURN `error` key if the module actually sets
  # result["error"] (CRUD modules do, via SpecGenerator). If a module never
  # populates error, omit this key entirely from RETURN.
  # Hard rule: NEVER initialize `"error": None` (or any `"error"` key) in the
  # run_module `result = {...}` dict — set `result["error"] = err` only at the
  # SpecGenerator failure site before fail_json.
  # Never add sample: under error (no sample: null and no string sample either).
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
  # returned: only for paths that set msg. Mention "idempotent" ONLY if the
  # module has an idempotency check. Mention "check mode" ONLY if check mode
  # sets msg. Examples:
  #   with idempotency (+ check msg): "...error, module is idempotent or check mode"
  #   no idempotency, check sets msg: "...error or in check mode operation"
  #   no idempotency, check sets response only: "When there is an error"
  returned: When there is an error or in check mode operation
  type: str
  # sample MUST be an exact msg string from this module (fail_json / exit_json /
  # raise_api_exception / result["msg"]), not a helper-only or invented string.
  sample: "Api Exception raised while creating <entity>"
"""

import traceback  # noqa: E402
import warnings  # noqa: E402
from copy import deepcopy  # noqa: E402

from ansible.module_utils.basic import missing_required_lib  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_module_v4 import BaseModuleV4  # noqa: E402
from ..module_utils.v4.constants import Tasks as TASK_CONSTANTS  # noqa: E402
from ..module_utils.v4.<area>.api_client import (  # noqa: E402
    get_<entity>_api_instance,
    get_etag,
)
from ..module_utils.v4.<area>.helpers import get_<entity>  # noqa: E402
from ..module_utils.v4.prism.tasks import (  # noqa: E402
    get_entity_ext_id_from_task,
    wait_for_completion,
)
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    raise_unsupported_update_fields,
    strip_internal_attributes,
    validate_required_params,
)

# Hard rule: include this SDK import / SDK_IMP_ERROR block ONLY when the module
# uses SDK symbols (obj=sdk.Model, sdk.Model(), enums, SpecGenerator bodies).
# Action-only modules that never reference SDK types must omit this block —
# do not import ntnx_*_py_client just to silence missing-lib checks (api_client
# already fails if the SDK is missing). See ntnx_vm_console_token_v2.
SDK_IMP_ERROR = None
try:
    import ntnx_<ns>_py_client as sdk  # noqa: E402
except ImportError:
    from ..module_utils.v4.sdk_mock import mock_sdk as sdk  # noqa: E402
    SDK_IMP_ERROR = traceback.format_exc()

warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    # Declare nested specs inline (like ntnx_virtual_switch_v2). Do not filter
    # a shared PrismSpecs helper. Nested/list fields carry obj=sdk.<Model>.
    # ipv4_spec = dict(...)
    # nested_spec = dict(...)
    module_args = dict(
        ext_id=dict(type="str"),
        name=dict(type="str"),
        # ...
    )
    return module_args


def create_<entity>(module, result, api_instance):
    # Hard rule: for create-/update-specific required fields that are not
    # globally required=True in get_module_spec(), always use
    # validate_required_params — never hand-roll Missing required parameter
    # fail_json checks.
    validate_required_params(module, ["name"])  # adjust to create-required fields
    sg = SpecGenerator(module)
    default_spec = sdk.<Model>()
    # Hard rule: generate the request spec ONCE before check_mode. Never build
    # a different/second body inside the check_mode branch or only on the live
    # path — check_mode and the API call must reuse the same `spec` object.
    # Hard rule: call generate_spec(obj=default_spec) only — SpecGenerator reads
    # module.params and skips keys not on the SDK model via hasattr. Never
    # deepcopy/pop state/ext_id/parent ids and pass attr= manually.
    spec, err = sg.generate_spec(obj=default_spec)
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating create <entity> spec", **result)
    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        return
    resp = None
    try:
        resp = api_instance.create_<entity>(body=spec)
    except Exception as e:
        raise_api_exception(module=module, exception=e,
                            msg="Api Exception raised while creating <entity>")
    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        task_status = wait_for_completion(module, task_ext_id)
        ext_id = get_entity_ext_id_from_task(
            task_status, rel=TASK_CONSTANTS.RelEntityType.<ENTITY>)
        if ext_id:
            resp = get_<entity>(module, api_instance, ext_id)
            result["ext_id"] = ext_id
            result["response"] = strip_internal_attributes(resp.to_dict())
        else:
            # Hard rule: if create+wait cannot resolve the entity ext_id from
            # the task, always raise — never list/search as a fallback.
            raise_api_exception(
                module=module,
                exception=Exception(
                    "Failed to get entity ext_id from task for <entity>"
                ),
                msg="Failed to get entity ext_id from task for <entity>",
            )
    result["changed"] = True


def check_<entity>_idempotency(old_spec, update_spec):
    strip_internal_attributes(old_spec)
    strip_internal_attributes(update_spec)
    return old_spec == update_spec


def update_<entity>(module, result, api_instance):
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id
    current_spec = get_<entity>(module, api_instance, ext_id)
    sg = SpecGenerator(module)
    # Hard rule: generate_spec from current ONCE (same object for check_mode and
    # live). Return early only AFTER the spec is built — never regenerate later.
    update_spec, err = sg.generate_spec(obj=deepcopy(current_spec))
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating <entity> update spec", **result)
    raise_unsupported_update_fields(module, current_spec, update_spec, ["<immutable_field>"])
    if module.check_mode:
        result["response"] = strip_internal_attributes(update_spec.to_dict())
        return
    if check_<entity>_idempotency(current_spec.to_dict(), update_spec.to_dict()):
        result["skipped"] = True
        module.exit_json(msg="Nothing to change.")
    # etag / if_match only when API/SDK documents If-Match for this operation.
    # Always pass via kwargs — never bare if_match=etag on the SDK call.
    etag = get_etag(data=current_spec)
    if not etag:
        return module.fail_json("Unable to fetch etag for updating <entity>", **result)
    kwargs = {"if_match": etag}
    try:
        resp = api_instance.update_<entity>_by_id(
            extId=ext_id, body=update_spec, **kwargs
        )
    except Exception as e:
        raise_api_exception(module=module, exception=e,
                            msg="Api Exception raised while updating <entity>")
    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        wait_for_completion(module, task_ext_id)
        resp = get_<entity>(module, api_instance, ext_id)
        result["response"] = strip_internal_attributes(resp.to_dict())
    result["changed"] = True


def delete_<entity>(module, result, api_instance):
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id
    if module.check_mode:
        result["msg"] = "<Entity> with ext_id:{0} will be deleted.".format(ext_id)
        return
    # etag / if_match only when API/SDK documents If-Match for this operation.
    # Always pass via kwargs — never bare if_match=etag on the SDK call.
    current_spec = get_<entity>(module, api_instance, ext_id)
    etag = get_etag(data=current_spec)
    if not etag:
        return module.fail_json("Unable to fetch etag for deleting <entity>", **result)
    kwargs = {"if_match": etag}
    try:
        resp = api_instance.delete_<entity>_by_id(extId=ext_id, **kwargs)
    except Exception as e:
        raise_api_exception(module=module, exception=e,
                            msg="Api Exception raised while deleting <entity>")
    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        resp = wait_for_completion(module, task_ext_id)
        result["response"] = strip_internal_attributes(resp.to_dict())
    result["changed"] = True


def run_module():
    module = BaseModuleV4(
        argument_spec=get_module_spec(),
        supports_check_mode=True,
        required_if=[("state", "present", ("name", "ext_id"), True)],
    )
    if SDK_IMP_ERROR:
        module.fail_json(msg=missing_required_lib("ntnx_<ns>_py_client"),
                         exception=SDK_IMP_ERROR)
    remove_param_with_none_value(module.params)
    result = {"changed": False, "response": None, "failed": False, "ext_id": None}
    # Create the API client once in run_module and pass it into create/update/
    # delete (and info helpers). Do NOT call get_<entity>_api_instance inside
    # those operation functions.
    api_instance = get_<entity>_api_instance(module)
    state = module.params.get("state")
    if state == "present":
        if module.params.get("ext_id"):
            update_<entity>(module, result, api_instance)
        else:
            create_<entity>(module, result, api_instance)
    else:
        delete_<entity>(module, result, api_instance)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
```

## Info module skeleton

Differences from CRUD:

- `extends_documentation_fragment` uses `ntnx_info_v2` (not operations).
- Uses `BaseInfoModule`, `supports_check_mode=False`,
  `mutually_exclusive=[("ext_id", "filter")]`.
- Two functions: `get_<entity>_using_ext_id` and `get_<entity>s` (list).
- List **must** use `SpecGenerator.get_info_spec` then
  `list_entities(api.list_<entity>s, kwargs=kwargs, ...)` from
  `module_utils.v4.utils` — never call `api.list_*(**kwargs)` directly.
  **Hard rule:** always `list_entities` for list paths whether
  `skip_info_args` is `True` or `False`. Parent/path IDs go as fixed kwargs to
  `list_entities`. After a successful list, unwrap the response **exactly**
  like `ntnx_virtual_switches_info_v2` (do not read totals from the raw SDK
  object before strip):

```python
try:
    resp = list_entities(
        api_instance.list_<entity>s,
        kwargs=kwargs,
    )
except Exception as e:
    raise_api_exception(
        module=module,
        exception=e,
        msg="Api Exception raised while fetching <entity>s info",
    )

resp = strip_internal_attributes(resp.to_dict())
total_available_results = resp.get("metadata").get("total_available_results")
result["total_available_results"] = total_available_results
resp = resp.get("data")

if not resp:
    resp = []
result["response"] = resp
```
- `result = {"changed": False, "response": None, "failed": False}`.
- `ntnx_info_v2` provides `filter`, `limit`, `page`, `orderby`, `select`,
  `fetch_all`, and `read_timeout` — do not redeclare them in
  `get_module_spec()`; only add `ext_id` and any entity-specific list params.
- **Hard rule — list API missing some info query params:** if the endpoint does
  not support the full set (e.g. only `page`/`limit`, no `$filter`/`$orderby`/
  `$select`), use `BaseInfoModule(skip_info_args=True, ...)`, **omit**
  `ntnx_info_v2` from `extends_documentation_fragment`, and add only the
  supported params (+ `read_timeout`) under `DOCUMENTATION.options` and in
  `get_module_spec()`. Never keep `ntnx_info_v2` / default info args and then
  pop unsupported keys from `get_info_spec` kwargs. See
  `ntnx_vm_host_affinity_policy_compliance_info_v2` /
  `ntnx_vm_pcie_devices_info_v2`.
- **Always document `read_timeout` for every info module** (same as existing
  modules such as `ntnx_vm_anti_affinity_policy_compliance_info_v2`).
  `BaseModuleV4` always injects `read_timeout` (type `int`, default `30000`)
  into the argument_spec. Standard info modules get the docs from
  `ntnx_info_v2`. If the module does **not** extend `ntnx_info_v2` (e.g.
  `skip_info_args=True` compliance-style modules), add it explicitly under
  `DOCUMENTATION.options`:

```yaml
  read_timeout:
    description: Read timeout in milliseconds for API calls.
    type: int
    required: false
    default: 30000
```

  Omitting it fails `validate-modules` (`undocumented-parameter` /
  `doc-default-does-not-match-spec`). Do not add `read_timeout` to
  `get_module_spec()`.

Info module RETURN block documents the standard set, same as existing info
modules (e.g. ntnx_address_groups_info_v2): `response`, `changed`, `msg`,
`failed`, and `total_available_results` (for list results). Do not omit
`changed`/`failed`/`msg`.

`error` is conditional: include it in RETURN below ONLY if the module sets
`result["error"]` (list info modules using `SpecGenerator.get_info_spec` do). A
simple get-by-ext_id info module that never sets `error` (e.g.
`ntnx_security_policy_preview_info_v2`) must OMIT the `error` return key.
**Hard rule for every module:** never initialize `"error"` in the `result`
dict in `run_module` — no `"error": None`. Set `result["error"] = err` only at
the SpecGenerator failure site. `total_available_results` applies only to list
results — omit it for a single-entity-only info module.

```yaml
RETURN = r"""
response:
  description:
      - Response for fetching <entity> info.
      - One <entity> if C(ext_id) is provided.
      - List of multiple <entity>s if C(ext_id) is not provided.
  returned: always
  type: dict
  sample: {}
changed:
  description: This indicates whether the task resulted in any changes
  returned: always
  type: bool
  sample: false
error:
  description: This field typically holds information about if the task have errors that occurred during the task execution
  returned: always
  type: bool
  sample: false
failed:
  description: This field typically holds information about if the task have failed
  returned: always
  type: bool
  sample: false
msg:
  description: This indicates the message if any message occurred
  returned: When there is an error
  type: str
  # sample MUST be an exact msg string from this module (fail_json / exit_json /
  # raise_api_exception / result["msg"]), not a helper-only or invented string.
  sample: "Failed generating <entity> info Spec"
total_available_results:
  description: The total number of available <entity>s in PC.
  returned: when all <entity>s are fetched
  type: int
  sample: 125
"""
```

## api_client.py and helpers.py additions

Placement rule: ALWAYS append new functions at the END of the file. Do not
insert them between existing functions, even if a related function lives in the
middle. For example new methods like `get_policy_preview` or
`get_dry_run_summary` go at the bottom of `api_client.py` / `helpers.py`, not
next to similar existing ones. This keeps diffs minimal and reviewable.

In `plugins/module_utils/v4/<area>/api_client.py` add (at the end of the file):

```python
def get_<entity>_api_instance(module):
    client = get_api_client(module)
    return ntnx_<ns>_py_client.<Entity>Api(client)
```

Reuse the existing `get_api_client` and `get_etag` in that file (one per area).
If the area folder does not exist yet, create `api_client.py` and `helpers.py`
by copying `plugins/module_utils/v4/flow/` and swapping the SDK import.

In `plugins/module_utils/v4/<area>/helpers.py` add (at the end of the file):

```python
def get_<entity>(module, api_instance, ext_id):
    """Return <entity> info using external ID."""
    try:
        # Always return .data from helpers — never the raw API response envelope.
        return api_instance.get_<entity>_by_id(extId=ext_id).data
    except Exception as e:
        raise_api_exception(
            module=module, exception=e,
            msg="Api Exception raised while fetching <entity> info using ext_id")
```

**Helpers always return `.data`.** Every `get_*` helper in
`helpers.py` must end with `.data` (same as existing helpers in the file). Do
**not** return the raw SDK response object. Callers then use
`strip_internal_attributes(resp.to_dict())` with **no** `.get("data")`.

Because this helper already wraps the SDK call with `raise_api_exception`, call
it directly from the module WITHOUT another `try/except`, e.g.:

```python
# correct — no redundant try/except around the helper
resp = get_<entity>(module, api_instance, ext_id)
result["response"] = strip_internal_attributes(resp.to_dict())
```

Only direct `api_instance.create_*/update_*/delete_*/list_*` calls (not routed
through a helper) need their own `try/except` + `raise_api_exception`.

Method names (`create_<entity>`, `update_<entity>_by_id`,
`get_<entity>_by_id`, `delete_<entity>_by_id`, `list_<entity>s`) must match the
SDK `Api` class exactly — confirm with `grep "def " <SDK>/api/<entity>_api.py`.
