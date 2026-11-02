---
name: module-development
description: >-
  Develop new nutanix.ansible V2 modules, examples, and integration tests that
  match the existing repository schema and structure. Use when asked to add a
  new ntnx_*_v2 module (CRUD and/or info), its example playbook, or its
  integration test target for the nutanix.ansible collection. Builds the module
  argument spec from the ntnx_*_py_client SDK models, writes V2-style integration
  tests (CRUD: create/update check-mode + live, idempotency, delete, negatives;
  info: get, list, limit, filter, fetch_all), and documents required IAM roles
  plus option/suboption attribute descriptions from the developers.nutanix.com
  API reference, using existing V2 modules only as a formatting reference. After
  generation, run black, isort, flake8, ansible-lint, and ansible-test sanity and
  fix every failure. Never edit requirements.txt. Run live ansible-test
  integration when a Prism Central IP is available (already set in
  prepare_env/vars/main.yml, or provided by the user in the chat) and fix until
  green.
---

# Nutanix Ansible V2 Module Development

Generate new `ntnx_*_v2` modules, examples, and integration tests for the
`nutanix.ansible` collection (`nutanix.ncp`) that are indistinguishable in
structure from the existing code.

**Repository root:** the `nutanix.ansible` collection checkout (directory that
contains `galaxy.yml` and `plugins/`). Resolve it from the workspace / git root
or current working directory — do **not** hardcode a machine-specific path.
All relative paths below (`plugins/`, `examples/`, `tests/`, …) are from that
root. SDK packages: `ntnx_*_py_client` (installed in the active Python
site-packages).

## Golden rule: copy an existing V2 module, don't invent

Always start from an existing V2 module of the **same shape** and adapt it.
Never design a new pattern. Pick a reference:

- CRUD entity (create/update/delete + task waiting): `ntnx_address_groups_v2.py`
- Info entity (get-by-id + list with filters): `ntnx_address_groups_info_v2.py`
- Their helpers/client: `plugins/module_utils/v4/flow/{helpers.py,api_client.py}`
- Their test target: `tests/integration/targets/ntnx_address_groups_v2/`
- For a namespace closer to your entity, find the matching `module_utils/v4/<ns>/`
  folder and reuse its `api_client.py` + `helpers.py`.

## Workflow

Copy this checklist and track progress:

```
- [ ] 1. Identify the SDK namespace + entity (which ntnx_*_py_client, which Api class)
- [ ] 2. Read the SDK model(s) to extract the API schema -> module spec
- [ ] 3. Read the API docs for the endpoint: IAM roles + attribute/sub-attribute descriptions
- [ ] 4. Diff SDK vs API request schema; exhaustive writable checklist (nested) vs get_module_spec — no missing attrs
- [ ] 5. Pick the closest existing V2 module(s) as reference
- [ ] 6. Add/extend api_client.py (api instance + get_etag) and helpers.py (get_<entity>)
- [ ] 7. Write the CRUD module and/or the info module
- [ ] 8. Fill DOCUMENTATION options descriptions + notes (roles) from the API docs
- [ ] 9. Write EXAMPLES and RETURN blocks
- [ ] 10. Example playbook: append to related existing examples/<area>_v2/ file if one exists; else create new
- [ ] 11. Create the integration test target (V2 schema — see tests.md; check-mode uses inline dummy values; self-contained create/cleanup)
- [ ] 12. Register modules in meta/runtime.yml action_groups (append at end); append any constants at end. Do **not** add changelog fragments.
- [ ] 13. Verify (formatters, linters, sanity) then clear pycache — see Verification; fix every failure
- [ ] 14. If a PC IP is available (in prepare_env/vars/main.yml or provided in chat): wire/confirm prepare_env vars and run ansible-test integration for the new target(s); fix until green. Do **not** edit requirements.txt
- [ ] 15. At the end of the chat, print any SDK vs API docs schema differences for the user
```

### Step 1 — Identify SDK namespace + entity

Each `module_utils/v4/<area>/` maps to one SDK package. Common mappings:

| module_utils/v4 area | SDK package                  |
|----------------------|------------------------------|
| flow                 | ntnx_microseg_py_client      |
| network              | ntnx_networking_py_client    |
| iam                  | ntnx_iam_py_client           |
| vmm                  | ntnx_vmm_py_client           |
| volumes              | ntnx_volumes_py_client       |
| clusters_mgmt        | ntnx_clustermgmt_py_client   |
| prism                | ntnx_prism_py_client         |
| data_protection      | ntnx_dataprotection_py_client|
| data_policies        | ntnx_datapolicies_py_client  |
| security             | ntnx_security_py_client      |
| lcm                  | ntnx_lcm_py_client / lifecycle|
| objects              | ntnx_objects_py_client       |
| multidomain          | ntnx_multidomain_py_client   |
| licensing            | ntnx_licensing_py_client     |

Find the entity's `Api` class and CRUD methods:

```bash
SDK=$(python3 -c "import ntnx_microseg_py_client,os;print(os.path.dirname(ntnx_microseg_py_client.__file__))")
ls "$SDK/api"                 # *_api.py files => Api classes
grep -n "def " "$SDK/api/address_groups_api.py" | grep -iE "create|update|delete|get|list"
```

### Step 2 — API docs decide fields; SDK supplies types/schema

**Which fields to expose:** match the API docs **request** schema for the
operation. That is the source of truth for the module argspec / DOCUMENTATION
options. Do **not** expose a field only because it exists on the SDK model.

**How to type each field:** use the SDK model (`openapi_types`, nesting, enums,
`obj=`) so `SpecGenerator` builds the correct SDK objects. See
[sdk-and-iam.md](sdk-and-iam.md).

Key points:

- Model fields live in `<SDK>/models/<ns>/v4/config/<Model>.py`.
- Use the snake_case keys from `openapi_types`/`attribute_map` as Ansible arg
  names (the SDK and modules use snake_case; the wire format is camelCase).
- **Intersect SDK ∩ API request schema.** Start from the SDK model for
  structure/types, then keep only fields present on the API docs request body.
  SDK-only fields are often read-only even when the SDK does **not** say
  `readOnly` (example: `bootstrap_config` on Domain Manager update).
- **Exhaustive writable coverage (do not skip attributes).** Before writing
  `get_module_spec()`, download the OpenAPI YAML and walk the **create** (and
  **update**, if any) request body schema end-to-end — including every nested
  `$ref` / `allOf` / `oneOf` property. Build a complete checklist of every
  property that is **not** `readOnly: true`. Every item on that checklist
  **must** appear in `get_module_spec()` and `DOCUMENTATION.options`
  (with full nested `suboptions`). Do **not** omit a field because:
  - it “looks like” response/metadata (e.g. `sourceLocation` /
    `DisasterRecoveryLocation` on VM recovery point create)
  - it is uncommon, optional, DR-only, or nested deep
  - codegen / a first draft already left it out
  - the description sounds past-tense / informational
  Only omit when a read-only rule below applies. After the module is written,
  re-diff the checklist against `get_module_spec()` keys (recursively) and
  fix any gaps before finishing. Report any still-omitted API request fields
  in the final **SDK vs API docs** section (with the reason, or treat as a
  bug to fix).
- **Never add read-only fields as module inputs** (not in `get_module_spec()`
  and not in `DOCUMENTATION.options`). Prefer the OpenAPI/API docs request
  schema over the SDK. Treat as read-only when any of these apply:
  - OpenAPI property has `readOnly: true` (download
    `https://developers.nutanix.com/api/v1/namespaces/<ns>/versions/<ver>/yaml`
    and check the schema) — authoritative even when the Python SDK omits
    “readOnly” wording (example: `DomainManagerNetwork.fqdn`)
  - Absent from the API docs **request** schema (even if present on the SDK)
  - Common server fields: `ext_id`, `links`, `tenant_id`, `created_by`,
    `*_time`, `_reserved`, `_object_type`, `_unknown_fields`
  - The SDK `:param` / property docstring says `readOnly`, `read-only`,
    “used for readOnly purposes”, or otherwise marks the field as output-only
- **Do not mention omitted read-only fields in DOCUMENTATION** (no “X/Y/Z are
  read-only and not accepted” notes). Document only the writable options that
  remain.
- Nested model/list fields get `obj=<SDK>.<Model>` so `SpecGenerator` can build
  the nested SDK object recursively.

### Step 3 — API docs for roles + attribute / sub-attribute descriptions

**Required for every module.** Open the Nutanix API reference for the endpoint
you are wrapping:

`https://developers.nutanix.com/api-reference?namespace=<namespace>`

From that endpoint (and its request/response schemas), obtain **all** of:

1. **IAM roles** per operation → `DOCUMENTATION.notes`
2. **Attribute descriptions** for every module option → `DOCUMENTATION.options`
3. **Sub-attribute descriptions** for every nested `suboptions` field → nested
   `options:` under each dict/list arg

Do **not** invent, paraphrase from memory, or copy descriptions from another
module. The API docs (and the matching SDK `:param` lines as a secondary check)
are the source of truth for wording. Existing V2 modules are only a formatting
reference. Full procedure in [sdk-and-iam.md](sdk-and-iam.md).

### Step 4 — Diff SDK spec vs API docs (required)

After extracting the SDK model and reading the API request schema, compare them
field-by-field (presence, requiredness, types/enums, nesting).

- **Field set / requiredness:** follow the **API docs request** schema (do not
  expose SDK-only fields).
- **Types, nesting, enums, `obj=`:** follow the **SDK** so SpecGenerator works.
- **Descriptions:** follow the **API docs**.
- **Completeness gate:** list every non-`readOnly` property from the API
  request schema (nested included) and confirm each is in `get_module_spec()`.
  A missing writable field (e.g. forgetting `source_location` on VM recovery
  point) is a skill failure — add it before finishing, do not rationalize the
  omission.

**If there is any difference between the SDK spec and the API spec the AI should
print differences at the end here in the chat so that user can see them.**

Include at least: fields only in SDK (omit from module), fields only in API docs,
required mismatches, type/enum mismatches, which source you followed, and the
writable-API-field ↔ module-spec completeness result. If there are no
differences and coverage is complete, say so explicitly at the end of the chat.

### Step 5–8 — Write the module(s)

Follow [module-anatomy.md](module-anatomy.md) for the exact file skeleton of
both a CRUD module and an info module, including imports, `get_module_spec`,
the create/update/delete functions, idempotency, check-mode handling, and
`run_module`.

When filling `DOCUMENTATION`:
- `options` / nested `suboptions` descriptions must come from the API docs
  (step 3), matching field meaning. Put only the semantic description text —
  do **not** add min/max value, min/max length, maxItems, or similar constraint
  lines in `description` (e.g. no `Minimum value is 1.`, no
  `Maximum length is 32000 characters.`). Express requiredness via Ansible
  `required:` and enums via `choices:` when needed; leave numeric/length
  bounds to the API.
- `notes` must contain **only** the IAM roles block (intro line, per-operation
  `B(...)` role lines, and the Ref URL) — same pattern as other V2 modules.
  Do not put behavioral tips, host requirements, or other prose in `notes`.
- End `notes` with
  `"Ref: U(https://developers.nutanix.com/api-reference?namespace=<namespace>)"`.
- If the API docs do **not** list IAM roles for the endpoint, omit the `notes`
  section entirely (do not invent roles).
- IAM `Required Roles:` lists must be **sorted alphabetically by role name**
  (A–Z), matching the API docs presentation. Do not leave codegen / arbitrary
  order. Keep `(deprecated)` on deprecated role names while sorting on the
  bare name (e.g. `…, Self-Service Admin (deprecated), Super Admin, …`).
- In `description`, use exactly `This module uses PC v4 APIs based SDKs`.
  Do **not** mention SDK class/method names there (e.g. do not write
  `(C(DomainManagerApi.update_domain_manager_by_id))`).
- Do **not** mention any other module names in DOCUMENTATION (`description`,
  `notes`, or `options`) — no `M(nutanix.ncp....)` cross-links to sibling
  modules.
- **Only document operations the API actually supports.** In
  `short_description`, `description`, `options.state`, `notes` role lines,
  EXAMPLES, and RETURN wording, mention create / update / delete **only** when
  that method exists. If update is missing (create+delete only), do **not**
  write that update is unsupported, do **not** describe
  `present`+`ext_id` as a fetch/update fallback, and do **not** say
  “update is not supported by the API”. Same rule if create or delete is
  missing — omit that operation entirely from docs (no “X is not supported”
  notes). Tailor `short_description` / `state` bullets to the supported set
  only (e.g. create+delete → “Create or delete …”; create-only → create only).
- **Present-only `state` (choices: present only).** When the module has a single
  `state` choice `present` (update/action modules with no delete), document
  `options.state` exactly like `ntnx_foundation_central_config_v2`:

```yaml
    state:
        description:
            - State of the module.
            - If C(state) is C(present), the module will <do the supported action>.
            - If C(state) is C(absent), the module will fail.
        type: str
        choices:
            - present
        default: present
```

  Replace `<do the supported action>` with the real verb (e.g. “update the
  Foundation Central configuration”, “compute LCM recommendations”). Keep
  `choices: [present]` and `default: present`. Do **not** add `absent` to
  `choices`.

### Step 9 — Example playbook

Follow [examples.md](examples.md). If an example already exists for the parent /
related entity in the same area (e.g. compliance info for a VM startup policy →
`examples/vm_startup_policies_v2/vm_startup_policies_v2.yml`), **append** the new
tasks to that playbook instead of creating a new file. Only create
`examples/<area>_v2/<entity>.yml` when no suitable related example exists.
Always show **real** (non-`dryrun`) operations; `dryrun` may be extra, never the
only example of an action.

### Step 10 — Integration test target

Create `tests/integration/targets/ntnx_<entity>_v2/` (and/or
`ntnx_<entity>_info_v2/`) following [tests.md](tests.md). Copy the V2 schema
from `ntnx_address_groups_v2`, `ntnx_virtual_switches_v2`, and
`ntnx_stigs_info_v2` — do not invent a new layout.

**Required coverage:**

- **CRUD:** create with/without check mode → update with/without check mode →
  idempotency (`Nothing to change.`) → delete with/without check mode →
  negatives (missing args, bad ext_id, duplicate name, etc. as applicable).
- **Info:** get by `ext_id` → list all → list with `limit` → list with `filter`
  (API-supported fields only) → `fetch_all` when supported → useful negatives.
- **Independence:** the target creates any prerequisite entities it needs and
  deletes them (and the entity under test) at the end. Do not depend on leftover
  state from other targets.

**Hard rule for check-mode tests:** in any task with `check_mode: true`, put
dummy values (names, UUIDs, IPs, ext_ids) **inline in the playbook task**. Do
NOT define them in `vars/` or via `set_fact`. Real (non-check-mode) tasks use
values registered from prior create tasks. Example:

```yaml
- name: Create <entity> with check mode enabled
  nutanix.ncp.ntnx_<entity>_v2:
    state: present
    name: "{{ ag1 }}"
    project_ext_id: "83083083-0000-0000-0000-000000000000"   # inline dummy
  register: result
  check_mode: true
  ignore_errors: true
```

### Step 11 — Register (no changelog fragments)

- Add the new module name(s) to `meta/runtime.yml` under `action_groups.ntnx`
  (both the CRUD and the `_info` module). APPEND them at the END of the list —
  do not insert in the middle or re-sort existing entries.
- If you need to add anything to a constants file (e.g.
  `plugins/module_utils/v4/constants.py` — new `RelEntityType`, task type, etc.),
  APPEND the new entries at the END of the relevant class/section. Do not insert
  in the middle or reorder existing constants.
- Do **not** create or edit `changelogs/fragments/*.yml`.

General placement rule: any new addition to shared files (`api_client.py`,
`helpers.py`, `meta/runtime.yml`, `constants.py`) goes at the END of its file /
list / class — never inserted between existing items.

## Verification (after modules, examples, and tests are written)

After generating the modules, example playbooks, and integration tests, **always**
run the checks below and **fix any failure** before finishing (re-run the failing
check until it passes). Adjust paths to every new/changed file. Run every
command from the collection repository root (the directory with `galaxy.yml`).

**Always** run formatters, linters, and `ansible-test sanity` as below.

**Live integration tests (conditional):** a Prism Central IP may come from
**either** `tests/integration/targets/prepare_env/vars/main.yml` (check the
`# BEGIN ANSIBLE MANAGED BLOCK insertion 0` section for an uncommented `ip:`)
**or** the user providing a PC IP/hostname **in this chat**. If either source
has an IP, you **must** run `ansible-test integration` for the new/changed
target(s) after sanity is green — confirm/wire
`tests/integration/targets/prepare_env/vars/main.yml`, use `--allow-disabled`,
fix failures, and re-run until pass. Full procedure is in
[tests.md](tests.md#running-live-integration-tests). If **neither** source has
a PC IP, only write the integration tests; do **not** invent an IP or run live
playbooks / `ansible-test integration`.

**Hard rule — never edit `requirements.txt`.** Do not change, pin, unpin, add,
or remove lines in the collection `requirements.txt` (including SDK package
versions such as `ntnx-*-py-client==...`). Leave that file untouched.

### 1. Quick static checks

```bash
# from collection repo root (directory containing galaxy.yml)
python3 -m py_compile plugins/modules/ntnx_<entity>_v2.py plugins/modules/ntnx_<entity>_info_v2.py
ansible-doc -M plugins/modules ntnx_<entity>_v2 >/dev/null && echo "doc OK"
yamllint examples/<area>_v2/<entity>.yml tests/integration/targets/ntnx_<entity>_v2/
```

### 2. black, isort, flake8, ansible-lint

Run these on the new/changed Python and YAML (repo configs apply —
`pyproject.toml` / `setup.cfg`). Fix every reported issue.

```bash
# from collection repo root
# Format / sort imports on new or changed Python files
black plugins/modules/ntnx_<entity>_v2.py plugins/modules/ntnx_<entity>_info_v2.py \
  plugins/module_utils/v4/<area>/api_client.py plugins/module_utils/v4/<area>/helpers.py
isort plugins/modules/ntnx_<entity>_v2.py plugins/modules/ntnx_<entity>_info_v2.py \
  plugins/module_utils/v4/<area>/api_client.py plugins/module_utils/v4/<area>/helpers.py
# Lint Python
flake8 plugins/modules/ntnx_<entity>_v2.py plugins/modules/ntnx_<entity>_info_v2.py \
  plugins/module_utils/v4/<area>/api_client.py plugins/module_utils/v4/<area>/helpers.py
# Lint Ansible content (modules, examples, tests as applicable)
ansible-lint plugins/modules/ntnx_<entity>_v2.py plugins/modules/ntnx_<entity>_info_v2.py \
  examples/<area>_v2/ tests/integration/targets/ntnx_<entity>_v2/
```

Include every other new/changed `.py` file in the `black` / `isort` / `flake8`
lists. If a tool is missing, install it (same tools CI uses) and re-run.

### 3. ansible-test sanity

Always run sanity after the formatters/linters above. Build and install the
collection, then run `ansible-test sanity` from the installed collection path.
Pass the new module paths so checks focus on what you added; omit path args
only if you need a full-collection sanity run:

```bash
# from collection repo root
PY="${ANSIBLE_TEST_PYTHON:-$(command -v python3.10 || command -v python3)}"
PY_VERSION="${ANSIBLE_TEST_PYTHON_VERSION:-$("$PY" -c 'import sys; print("%d.%d" % sys.version_info[:2])')}"
ansible-galaxy collection build -f
version=$(grep '^version:' galaxy.yml | awk '{print $2}' | tr -d '"')
ansible-galaxy collection install -f "./nutanix-ncp-${version}.tar.gz"
cd "${HOME}/.ansible/collections/ansible_collections/nutanix/ncp"
ansible-test sanity --python "$PY_VERSION" --python-interpreter "$PY" \
  plugins/modules/ntnx_<entity>_v2.py plugins/modules/ntnx_<entity>_info_v2.py
```

If a local wrapper script that performs the same build/install/sanity steps
exists in the environment, you may use it instead — the steps above are the
portable source of truth.

If sanity fails because cached ansible-test venvs point at a removed Python,
clear them and retry:

```bash
rm -rf "${HOME}/.ansible/test/venv"
# re-run the build / install / ansible-test sanity steps above
```

### 4. Clear pycache

After the checks pass, remove generated Python cache files under the collection
repo so they do not show up as untracked noise:

```bash
# from collection repo root
find . -type d -name '__pycache__' -prune -exec rm -rf {} +
find . -type f \( -name '*.pyc' -o -name '*.pyo' \) -delete
```

### 5. Live integration tests (if PC IP is in main.yml or provided in chat)

**Always inspect** `tests/integration/targets/prepare_env/vars/main.yml` first
(especially the managed block around `ip:` / `username:` / `password:` /
`validate_certs:`). Treat variables already defined there as valid PC
connection settings.

Run live integration when **either**:
- `ip:` is already set (uncommented) in that `main.yml`, **or**
- the user gave a PC IP/hostname in the chat.

Then:

1. Ensure `tests/integration/targets/prepare_env/vars/main.yml` has the PC
   `ip` and credentials. Prefer values already present in `main.yml`. If the
   user supplied an IP (and optionally credentials) in chat, update the managed
   block with those values. **Default credentials** when wiring or filling
   missing username/password (unless the user provided different ones in chat):
   `username: admin`, `password: Nutanix.123`. Set `validate_certs: false`
   unless the user specified otherwise. Do not invent an IP when neither
   `main.yml` nor chat provides one.
2. Build/install the collection (same as sanity) so the installed tree has the
   new tests and vars (and the same prepare_env `ip`/credentials).
3. From the installed collection path, run:

```bash
ansible-test integration --allow-disabled --python "$PY_VERSION" \
  --python-interpreter "$PY" ntnx_<entity>_v2
# plus ntnx_<entity>_info_v2 when that target exists
```

4. Fix module or test failures and re-run until the target passes. The playbook
   must create its own prerequisites and delete everything it created.

If neither `main.yml` nor chat has a PC IP: skip this step.

### 6. Fix failures, then finish

Fix **any** failure from py_compile, ansible-doc, yamllint, black, isort,
flake8, ansible-lint, sanity, or (when applicable) live integration before
finishing. DOCUMENTATION `options` must match `get_module_spec()` exactly
(names, types, suboptions) — sanity tests enforce this. Also keep every
physical line in docs/examples/tests ≤ 160 characters (ansible-lint / yamllint).

After verification, end the chat response with an **SDK vs API docs** section:
list every schema difference found (or state that none were found). Do not omit
this section.

## Conventions summary (do not deviate)

- File header: shebang, coding, Nutanix copyright, GPLv3, `from __future__ ...`,
  `__metaclass__ = type`.
- Copyright year is always `2027` for every new or rewritten module header:
  `# Copyright: (c) 2027, Nutanix`. Never use `2025`, `2026`, or the current
  calendar year — codegen often emits the wrong year; fix it to `2027`.
- `version_added` for new modules is `"2.7.0"` (quoted) in DOCUMENTATION.
- `description` ends with `This module uses PC v4 APIs based SDKs` only — never
  append SDK method names such as `(C(SomeApi.some_method))`.
- Never mention other module names in DOCUMENTATION (no `M(nutanix.ncp....)`).
- Never document unsupported CRUD operations (no “update not supported”, no
  create/update/delete wording for methods the API does not provide). Exception:
  present-only modules still document `If C(state) is C(absent), the module will
  fail.` under `options.state` (see present-only `state` rule above /
  `ntnx_foundation_central_config_v2`).
- Never ship a module with missing writable API request fields — walk the full
  OpenAPI create/update/action body (nested) and match `get_module_spec()` **and**
  `DOCUMENTATION.options` 1:1. Include **every** writable attribute and nested
  object from the API docs / SDK model (including all `oneOf` / discriminator
  variants such as `nic_backing_info.virtual_ethernet_nic` /
  `sriov_nic` / `dp_offload_nic` / `pcie_passthrough_nic`). Do not document or
  wire only the first variant. Skip read-only response fields only.
- **Never exceed 160 characters on any physical line** in module
  `DOCUMENTATION` / `EXAMPLES` / `RETURN` YAML (inside the `.py`), example
  playbooks under `examples/`, or integration tests under
  `tests/integration/targets/`. Ansible lint / yamllint fail on lines longer
  than 160. Wrap long descriptions, `msg:` strings, and Jinja expressions
  across multiple lines (folded scalars `>-` / `|` are fine; each physical
  line must still be ≤ 160).
- **Never** add `ignore_errors: true` without a matching `register:` on the
  same task in examples or tests (including cleanup).
- **Always generate the request spec before `check_mode`.** Build the body once
  (prefer `SpecGenerator.generate_spec`) upstream of `if module.check_mode:`;
  reuse that same object for the live API call. Never build a different/second
  spec inside the check-mode branch or only on the non-check-mode path.
- **Hard rule — `check_mode` before idempotency.** When a module has an
  idempotency / skip path (`result["skipped"] = True` /
  `exit_json(msg="Nothing to change.")`), always handle
  `if module.check_mode:` **before** that skip. Check mode must return the
  would-be request in `response` (from the already-built spec) and must not
  short-circuit as skipped. Order: build spec → `check_mode` return →
  idempotency skip (if any) → live API.
- **Hard rule — never edit `requirements.txt`.** Leave the collection
  `requirements.txt` unchanged. Do not modify SDK pins or other dependency
  lines while developing or fixing modules.
- **Hard rule — V2 integration tests + live run when a PC IP is available.**
  Write targets like `ntnx_address_groups_v2` / `ntnx_virtual_switches_v2` /
  `ntnx_stigs_info_v2` (CRUD: create/update check+live, idempotency, delete,
  negatives; info: get, list, limit, filter, fetch_all). Targets must be
  self-contained: create prerequisites, delete them after. Always check
  `tests/integration/targets/prepare_env/vars/main.yml` for an existing `ip:`
  (and related vars). If `ip` is already in `main.yml` **or** the user provided
  a PC IP in the chat, after sanity run `ansible-test integration
  --allow-disabled` for those targets (confirm/wire `prepare_env/vars/main.yml`)
  and fix until green. If neither source has an IP, write tests only — never
  invent an IP.
- **Hard rule — default PC credentials for live tests.** When wiring
  `prepare_env/vars/main.yml` (or otherwise authenticating for live integration),
  keep any credentials already defined there; when filling missing
  username/password, always use `username: admin` and `password: Nutanix.123`
  unless the user explicitly provided different credentials in the chat.
- **Never initialize `"error"` in the `result` dict.** Use
  `result = {"changed": False, "response": None, "failed": False, ...}` only —
  do **not** add `"error": None`. If SpecGenerator fails, set
  `result["error"] = err` at that failure site before `fail_json`; still never
  pre-seed `error` in `run_module`.
- **Always use `validate_required_params` for operation-specific required
  fields.** When create/update/delete needs params that are not globally
  `required=True` in `get_module_spec()` (e.g. create needs `backing_info`),
  call `validate_required_params(module, ["field", ...])` at the start of that
  operation function. Import it from `..module_utils.v4.utils`. Never hand-roll
  `if not module.params.get(...): module.fail_json(msg="Missing required...")`.
- **Never deepcopy/pop `module.params` for create `generate_spec`.** Call
  `sg.generate_spec(obj=default_spec)` only. SpecGenerator already deep-copies
  `module.params` and only applies keys that exist on the SDK model (`hasattr`).
  Do not pop `state` / `ext_id` / parent path ids and pass `attr=...`.
- **Always raise if create+wait cannot get `ext_id` from the task.** After
  `get_entity_ext_id_from_task`, if `ext_id` is missing, call
  `raise_api_exception(...)` with
  `"Failed to get entity ext_id from task for <Entity>"`. Never list/search as
  a fallback to invent the new entity id.
- **Partial info list support → `skip_info_args=True`.** If the list API does
  not support all of `filter`/`orderby`/`select`/`page`/`limit`/`fetch_all`,
  omit `ntnx_info_v2` from docs, set `skip_info_args=True`, and declare only
  the supported query params (+ `read_timeout`) manually. Never pop unsupported
  keys from `get_info_spec` kwargs.
- **Always use `list_entities` for info list paths** — whether
  `skip_info_args` is `True` or `False`. Never call `api.list_*(**kwargs)`
  directly.
- **Always `set_fact` user-supplied IDs in standalone examples.** When an
  `examples/<area>_v2/*.yml` playbook needs inputs the reader must fill in
  (`vm_ext_id`, parent/device UUIDs, etc.), start with
  `ansible.builtin.set_fact` (`name: Set variables`) and reference
  `"{{ var }}"` afterward — do not inline `"<vm_ext_id>"` in every task
  (see `examples/vmm_v2/vm_pcie_device_v2.yml` / [examples.md](examples.md)).
- **Hard rule — always remove unused imports.** Do not leave imports that are
  never referenced in the module. Never silence unused imports with
  `# noqa: F401` / `# pylint: disable=unused-import` — delete them instead.
  Also drop now-unused helpers pulled in only for those imports (e.g.
  `traceback`, `missing_required_lib`) when the SDK import block is removed.
- **Only import `ntnx_*_py_client` when the module uses SDK symbols.** Add the
  `SDK_IMP_ERROR` / `import ntnx_<ns>_py_client as sdk` (+ mock_sdk) block when
  the module references SDK models (`obj=sdk.Model`, `sdk.Model()`,
  SpecGenerator bodies, enums). If the module only calls `api_instance` methods
  and never uses SDK types, do **not** import the client (no
  `F401` / `pylint: disable=unused-import` stubs). Missing-SDK fail is already
  handled in `get_*_api_instance` / `api_client` (see
  `ntnx_vm_console_token_v2` / `ntnx_foundation_central_config_v2`).
- **Hard rule — file-download modules expose optional `dest`.** Whenever a
  module downloads a file (octet-stream / binary / metadata) and returns a
  local path under `response.path`, always add an optional `dest` arg
  (`type: path`) so the user can choose where to save it. Document that the
  parent directory is created if missing, and that omitting `dest` leaves the
  file at the SDK default download location (that path is returned). Implement
  like `ntnx_object_stores_certificate_download_v2` / `ntnx_image_download_v2`:
  if `dest` is set, set
  `api_instance.api_client.configuration.download_directory` to the parent
  dir (create it), call the download API, then `shutil.move` the SDK file to
  `dest` when the paths differ. For APIs that return bytes instead of a file
  path, still accept optional `dest` and persist via `save_bytes_to_file`
  (see `ntnx_saml_identity_providers_sp_metadata_download_v2`). Cover both
  with- and without-`dest` in EXAMPLES, the standalone example playbook, and
  integration tests (stat the file, assert `response.path`, clean up). In
  check mode with `dest`, set `result["response"] = {"path": dest}` and a
  msg that mentions the destination path.
- **Docs + argspec must cover all API objects/attributes.** For every request
  body field in the API docs (e.g.
  [crossClusterMigrateVm](https://developers.nutanix.com/api-reference?namespace=vmm&version=v4.3#tag/Vm/operation/crossClusterMigrateVm)),
  mirror nested objects and `oneOf` variants in both `DOCUMENTATION` and
  `get_module_spec()` (shared helpers like `VmSpecs.nic_spec` must also expose
  every variant). Never leave sibling oneOf types undocumented/unwired.
- `notes` is roles-only (+ Ref URL). If API docs have no IAM roles, omit `notes`.
- `Required Roles:` always alphabetical (A–Z), same as the API docs.
- Order inside the module: `DOCUMENTATION`, `EXAMPLES`, `RETURN`, imports,
  `get_module_spec`, operation functions, `run_module`, `main`.
- CRUD modules: `BaseModuleV4`, `supports_check_mode=True`. Info modules:
  `BaseInfoModule`, `supports_check_mode=False`.
- **Info module file names must include `_info`.** Any read-only module that
  gets by id, lists, or does both is an info module and must be named
  `ntnx_<entity>_info_v2` (e.g. `ntnx_esxi_vm_stats_info_v2`,
  `ntnx_esxi_vm_disk_stats_info_v2`). Do **not** ship get/list-only modules as
  `ntnx_<entity>_v2` / `ntnx_<entity>_stat_v2` without `_info`.
- **ESXi-only APIs must include `esxi` in the module name.** If the endpoint /
  SDK is ESXi-specific (e.g. `EsxiStatsApi`, `/vmm/.../esxi/...`), name modules
  with `esxi` (e.g. `ntnx_esxi_vm_stats_info_v2`,
  `ntnx_esxi_vm_disk_stats_info_v2`, `ntnx_esxi_vm_nic_stats_info_v2`). Do **not**
  use a generic `ntnx_vm_*` name for an ESXi-only module.
- **One info module per distinct get/list resource.** If the API exposes
  multiple get (or list) operations for different resources — e.g. get VM
  stats, get VM disk stats, get VM NIC stats — do **not** combine them in one
  module with mutually exclusive selectors. Put shared list+get for the same
  resource in one `*_info_v2` module; put each other resource’s get/list in its
  own `*_info_v2` module (e.g. `ntnx_esxi_vm_stats_info_v2` +
  `ntnx_esxi_vm_disk_stats_info_v2` + `ntnx_esxi_vm_nic_stats_info_v2`).
- **Hard rule — always `list_entities` for listing.** Info modules that list
  entities **must** call `list_entities(api.list_<...>, kwargs=kwargs, ...)`
  from `module_utils.v4.utils` (see `ntnx_virtual_switches_info_v2` /
  `ntnx_vm_pcie_devices_info_v2`). This applies for **both**
  `skip_info_args=False` (full `ntnx_info_v2`) and `skip_info_args=True`
  (partial query params). Do **not** call the SDK `list_*` method directly
  with `api.list_*(**kwargs)` or `api.list_*(vmExtId=..., **kwargs)`. Pass any
  parent/path IDs as fixed kwargs to `list_entities` (e.g. `vmExtId=...`,
  `domainManagerExtId=...`, `taskExtId=...`). Singleton / get-by-id-only info
  modules that have no list API are exempt.
- After `list_entities` succeeds, always unwrap the list response exactly like
  `ntnx_virtual_switches_info_v2` — strip internals on the full response dict,
  then take `metadata.total_available_results` and `data` (default `[]`). Do
  **not** read `total_available_results` from the raw SDK object before
  `strip_internal_attributes`:

```python
resp = strip_internal_attributes(resp.to_dict())
total_available_results = resp.get("metadata").get("total_available_results")
result["total_available_results"] = total_available_results
resp = resp.get("data")

if not resp:
    resp = []
result["response"] = resp
```
- Info modules **must always document `read_timeout`** (type `int`, default
  `30000`, description: "Read timeout in milliseconds for API calls.") the same
  way existing modules do (e.g. `ntnx_vm_anti_affinity_policy_compliance_info_v2`).
  `BaseModuleV4` always adds `read_timeout` to the argument_spec; omitting it
  from docs fails `validate-modules` (`undocumented-parameter` /
  `doc-default-does-not-match-spec`). Prefer covering it via the
  `ntnx_info_v2` fragment for standard list/get info modules. When the info
  module does **not** extend `ntnx_info_v2` (e.g. `skip_info_args=True`
  compliance-style modules that only use credentials / logger / proxy), declare
  `read_timeout` explicitly under `DOCUMENTATION.options`. Do **not** redeclare
  it in `get_module_spec()` — it already comes from `BaseModuleV4`.
- **Hard rule — partial list query support → `skip_info_args=True`.** If the
  list API does **not** support the full `ntnx_info_v2` set (`filter`,
  `orderby`, `select`, `page`, `limit`, `fetch_all`), do **not** extend
  `ntnx_info_v2` in DOCUMENTATION (that would document unused params). Call
  `BaseInfoModule(skip_info_args=True, ...)`, then declare **only** the
  supported query params in `get_module_spec()` and document them under
  `options` (plus explicit `read_timeout`). Never accept unsupported args and
  strip them from kwargs (no `kwargs.pop("_filter", None)` hacks). Pattern:
  `ntnx_vm_host_affinity_policy_compliance_info_v2` /
  `ntnx_vm_pcie_devices_info_v2` (page/limit/fetch_all only).
- When the info module supports `fetch_all` (via `ntnx_info_v2` /
  `list_entities`), you **must** cover it in: the module `EXAMPLES` block, the
  standalone example playbook under `examples/`, and the integration tests.
  Assert `response|length == total_available_results` (see
  `ntnx_pcie_devices_info_v2` / `ntnx_stigs_info_v2`).
- Info `filter:` examples (module EXAMPLES, `examples/` playbooks, and
  integration tests) must use only fields listed under the list endpoint’s
  `$filter` “The filter can be applied to the following fields” in the API
  docs (camelCase). Never invent unsupported fields (e.g. `name` is invalid
  for AHV VM recovery points — use `recoveryPointType`, `vmExtId`, etc.).
- Always `remove_param_with_none_value(module.params)` and
  `strip_internal_attributes(...)` on responses.
- Build request specs with `SpecGenerator` (`sg.generate_spec(obj=sdk.<Model>())`)
  driven by `obj=` in the argument spec. Do NOT manually instantiate SDK models
  and assign fields one-by-one with `if module.params.get(...)` blocks (as in the
  non-standard `ntnx_config_upgrade_v2.build_upgrade_spec`). For polymorphic
  (`oneOf`) bodies use `SpecGenerator`'s dynamic `obj={...}` mechanism (see
  `ntnx_vm_startup_policy_v2.py`). See [sdk-and-iam.md](sdk-and-iam.md).
- RETURN block must document the return keys consistent with existing modules,
  but only document keys the module can actually return. Always include
  `response`, `changed`, `failed`, `msg` (plus `ext_id` for CRUD and
  single-entity info; `total_available_results` for list info).
- For **task-only action modules** (share/unshare, migrate, etc.) where
  `wait=true` only waits for task completion and does **not** re-fetch an
  entity, both wait values return task details. Always document `response`
  like `ntnx_vm_profile_share_v2`:

```yaml
response:
  description:
      - Response for <action>.
      - If C(wait) is true, it will contain the final task payload after completion.
      - If C(wait) is false, it will contain the initial task details.
```

  Do **not** claim wait=true returns entity details unless the module actually
  re-fetches the entity after `wait_for_completion` (CRUD create/update style).
- Match standard RETURN field **descriptions** to existing CRUD modules such as
  `ntnx_virtual_switch_v2` when the field exists there, e.g.:
  - `task_ext_id`: "The external ID of the task."
  - `ext_id`: "The external ID of the \<entity\>."
  - `changed`: "This indicates whether the task resulted in any changes"
  - `skipped`: "This indicates whether the task was skipped" — document and set
    `skipped` **only** when the module has an idempotency check (e.g.
    `check_<entity>_idempotency` → `result["skipped"] = True` /
    `exit_json(msg="Nothing to change.")`). Do **not** set `skipped` in
    `check_mode` alone, and omit `skipped` from RETURN when there is no
    idempotency method (e.g. one-shot actions like scale-up).
  - `error`: "This indicates the error message if any error occurred"
  - `failed`: "This indicates whether the task failed"
  - `msg`: "This indicates the message if any message occurred"
    - Document `returned:` based on when the module **actually** sets `msg`
      (e.g. `fail_json(msg=...)`, `exit_json(msg=...)`, or `result["msg"] = ...`).
    - With idempotency that exits with a message (e.g. `Nothing to change.`):
      `returned: When there is an error, module is idempotent or check mode`
      — only include "check mode" if check mode also sets `msg`.
    - Without idempotency: if check mode sets `msg`, use
      `returned: When there is an error or in check mode operation`;
      if check mode does **not** set `msg` (typical: only `response` + return),
      use `returned: When there is an error` — do **not** mention check mode.
    - Never write "module is idempotent" in `returned:` when the module has no
      idempotency check.
    - RETURN `msg.sample` must be an **exact** string that the module itself
      sets via `fail_json(msg=...)`, `exit_json(msg=...)`,
      `raise_api_exception(..., msg=...)`, or `result["msg"] = ...` in that
      module file. Do **not** invent samples or copy helper-only messages that
      are not passed from the module.
- **Never** put `sample: null` (or any null sample) in RETURN. If there is no
  useful sample, omit the `sample:` key entirely.
- **Never** add a `sample:` under RETURN `error` — omit `sample:` for `error`
  entirely (no string samples either).
- `error` is conditional: document `error` in RETURN ONLY if the module actually
  populates `result["error"]` (e.g. `SpecGenerator` error handling in
  `ntnx_address_groups_v2` / `ntnx_address_groups_info_v2`). If the module never
  sets `error` (e.g. a simple get-by-ext_id info module like
  `ntnx_security_policy_preview_info_v2`), do NOT mention `error` in the docs at
  all.
- The initial `result` dict in `run_module` must match existing modules — do
  **not** pre-seed `error` or `task_ext_id` (set those only when assigned later):
  - CRUD: `{"changed": False, "response": None, "failed": False, "ext_id": None}`
    (see `ntnx_virtual_switch_v2`)
  - Info: `{"changed": False, "response": None, "failed": False}`
- **Hard rule — use `validate_required_params` for op-specific required attrs.**
  At the top of create/update/delete (or other action helpers), when that path
  needs fields that are optional in the shared argspec, call
  `validate_required_params(module, ["name", "vm_ext_id", ...])` (see
  `ntnx_vm_recovery_point_v2` / `ntnx_virtual_switch_v2`). Do **not** write
  manual missing-param `fail_json` checks. `required_if` in `BaseModuleV4` may
  still apply for state routing; the helper is the in-function validation.
- **Hard rule — `generate_spec(obj=default_spec)` only on create.** Do not
  `deepcopy(module.params)`, pop Ansible/control fields, and pass `attr=`.
  SpecGenerator skips non-model keys via `hasattr(obj, key)` (see
  `ntnx_virtual_switch_v2` / `ntnx_vms_serial_port_v2`).
- **Hard rule — missing post-create `ext_id` from task → raise.** On create with
  `wait`, after `get_entity_ext_id_from_task`, if there is no `ext_id`, always
  `raise_api_exception` (see `ntnx_virtual_switch_v2` /
  `ntnx_vms_serial_port_v2`). Do **not** fall back to list/filter/search helpers
  to recover the id.
- **Hard rule — generate the request spec once, before `check_mode`.** Always
  build the request body **before** the `if module.check_mode:` early return —
  same path for check mode and live runs (see `ntnx_virtual_switch_v2` /
  `ntnx_address_groups_v2`). Prefer `SpecGenerator.generate_spec(...)`; if the
  body is built another way, still construct it **once** upstream of check mode
  and reuse that same object for the live API call. Do **not**:
  - short-circuit check mode with a separate / different `sdk.Model()` build
  - regenerate or rebuild the body after the check-mode branch for the live path
  - put a second `Update*Params(...)` / `generate_spec(...)` only on the
    non-check-mode path
  Pattern: fetch current (update / idempotent action) or build default (create)
  → build/`generate_spec` → if `check_mode`: set `response` from that spec and
  return → else idempotency skip (if any) → API with the **same** spec.
  Never run the idempotency/`Nothing to change.` exit before the `check_mode`
  branch (see `ntnx_esxi_vms_categories_v2`).
- Declare `get_module_spec()` **inline** like `ntnx_virtual_switch_v2`: local
  nested `*_spec = dict(...)` helpers, then `module_args = dict(...)`. Do **not**
  build the argspec by filtering/mutating a shared helper (e.g.
  `PrismSpecs.get_prism_spec()`) and selecting allowed keys.
- On update, strip read-only fields **only at the top-level entity** with
  `strip_read_only_fields(update_spec, fields=(...))` (see `ntnx_product_v2`).
  Do **not** walk nested objects to strip nested read-only attributes — keep
  those fields out of the argspec instead.
- Create the API client **once** in `run_module` via
  `api_instance = get_<entity>_api_instance(module)` (or the area-specific
  getter) **before** dispatching to create/update/delete/info helpers, and
  **pass `api_instance` as an argument** into those functions. Do **not** call
  `get_*_api_instance(module)` inside create/update/delete/list operation
  functions (see `ntnx_virtual_switch_v2` / `ntnx_vm_to_host_migration_v2`).
- Create/update/delete go through a task: capture `task_ext_id`, and when
  `wait` is true call `wait_for_completion` then re-fetch the entity.
- Use `get_etag(...)` + `if_match` **only when the API docs / SDK require or
  document `If-Match` for that operation** (typical for update/delete). Check
  the OpenAPI parameters and the SDK method signature/docstring first. If
  `If-Match` is not listed as a parameter for the endpoint (e.g. many `$actions`
  like migrate-to-host), do **not** fetch an etag, call `get_<entity>`, or pass
  `if_match` — call the SDK with only the documented required args.
- When `If-Match` **is** required, always pass it via a `kwargs` dict — never as
  a bare `if_match=etag` keyword on the SDK call. Same pattern as existing CRUD
  modules (e.g. `ntnx_vm_anti_affinity_policy_v2`, `ntnx_vms_disks_v2`):

```python
etag = get_etag(data=current_spec)
if not etag:
    return module.fail_json(
        "Unable to fetch etag for updating <entity>", **result
    )
kwargs = {"if_match": etag}
resp = api_instance.update_<entity>_by_id(
    extId=ext_id, body=update_spec, **kwargs
)
```
- Do not double-handle exceptions. Helper functions (`get_<entity>` in
  `helpers.py`) already wrap their SDK call with `raise_api_exception`, so call
  them directly — never wrap a call to a `get_<entity>` helper in another
  `try/except`. Only direct `api_instance.create/update/delete/list_*` calls made
  in the module (which are not wrapped elsewhere) get their own `try/except` +
  `raise_api_exception`.
- **Helpers always return `.data`.** In `helpers.py`, every get helper must
  return `api_instance.get_*(...).data` (never the raw response envelope). In
  the module, serialize with `strip_internal_attributes(resp.to_dict())` — do
  **not** call `.get("data")` again after a helper.
- Doc fragments: CRUD uses `ntnx_credentials`, `ntnx_operations_v2`,
  `ntnx_logger`, `ntnx_proxy_v2`; info uses `ntnx_credentials`, `ntnx_info_v2`,
  `ntnx_logger`, `ntnx_proxy_v2`.
- Author list: always include both of these (and keep any other existing authors):
  - `Abhinav Bansal (@abhinavbansal29)`
  - `George Ghawali (@george-ghawali)`
