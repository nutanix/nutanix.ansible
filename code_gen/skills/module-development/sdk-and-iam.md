# SDK schema extraction + API docs (roles and attribute descriptions)

## Build the module spec from SDK models

Always build the request body with `SpecGenerator`, NOT by hand. This is the
single most important structural rule for matching the repo.

DO (standard pattern — every module uses this):

```python
sg = SpecGenerator(module)
default_spec = sdk.<Model>()
spec, err = sg.generate_spec(obj=default_spec)
if err:
    result["error"] = err
    module.fail_json(msg="Failed generating <entity> spec", **result)
```

The mapping from `module.params` to SDK object fields is driven entirely by the
argument spec: declare `obj=sdk.<Model>` on each nested `dict`/`list` arg and
`SpecGenerator` recursively constructs the SDK objects.

DON'T (anti-pattern — do not generate code like this):

```python
# WRONG: manual construction + per-field if/assignment bypasses SpecGenerator
spec = sdk.UpgradeJob(spec=sdk.DryRunSpec())
dry_run_spec = spec.spec
if module.params.get("policy_names") is not None:
    dry_run_spec.policy_names = module.params["policy_names"]
```

For polymorphic bodies (SDK `oneOf`, e.g. a field whose object type depends on
which suboption is set), use `SpecGenerator`'s dynamic `obj` mechanism: set `obj`
to a dict mapping each selector suboption name to its SDK model class, instead of
writing if/else attribute assignments. Real examples:
`plugins/modules/ntnx_vm_startup_policy_v2.py` and
`plugins/modules/ntnx_lcm_bundle_v2.py` (search `obj={` under `plugins/modules`):

```python
power_state_criteria=dict(
    type="dict",
    options=power_state_criteria_spec,
    obj={
        "power_on": vmm_sdk.PowerStateCriteriaPowerOn,
        "guest_bootup": vmm_sdk.PowerStateCriteriaGuestBootup,
    },
    mutually_exclusive=[("power_on", "guest_bootup")],
),
```

Only fall back to manual field assignment if no `SpecGenerator` path exists for
that shape — and keep it minimal.

### Procedure

The argument spec mirrors the SDK request model. Procedure:

1. Locate the SDK package for the namespace and the request model class.

```bash
SDK=$(python3 -c "import ntnx_microseg_py_client,os;print(os.path.dirname(ntnx_microseg_py_client.__file__))")
ls "$SDK/models/microseg/v4/config" | grep -iE "<Entity>"
sed -n '1,140p' "$SDK/models/microseg/v4/config/<Entity>.py"
```

2. Read these parts of the model file:
   - The class docstring: each `:param x:` line says what the field is and
     whether it is `required` plus constraints (`max=64 chars`, enums, etc.).
     Use constraints for typing/`choices`/`required` only — do **not** put
     min/max value or length text into DOCUMENTATION `description` lines.
   - `openapi_types = {...}`: the snake_case field name -> type. Types map to
     Ansible as: `str`->`str`, `int`->`int`, `bool`->`bool`,
     `list[...]`->`list` (set `elements`), a model name -> `dict` (nested).
   - `attribute_map = {...}`: snake_case -> camelCase wire name (informational;
     the Ansible arg uses the snake_case key).

3. **Also open the API docs for the same endpoint** (required — do not skip):
   `https://developers.nutanix.com/api-reference?namespace=<namespace>`
   For the Create/Update/Get/List operation you are wrapping, read the request
   (and nested schema) property descriptions. Use those as the authoritative
   text for DOCUMENTATION `options` / nested `suboptions` `description:` lines.
   Recurse into every nested object/array item schema so **sub-attributes** get
   accurate descriptions too (e.g. `ipv4_addresses[].value`,
   `deployment.management_interface.address.ipv4.value`).
   Cross-check against the SDK `:param` lines; if they disagree, prefer the
   API docs wording. Never invent descriptions or copy them from another module.

   **SDK vs API request schema:** also compare which fields exist, which are
   required, and types/enums. Use the SDK for `get_module_spec()` structure;
   use the API docs for DOCUMENTATION wording. **If there is any difference
   between the SDK spec and the API spec the AI should print differences at the
   end here in the chat so that user can see them** (fields only on one side,
   required/type/enum mismatches, and which source was followed). If none, say
   there were no differences.

4. Translate to `get_module_spec()` (inline, like `ntnx_virtual_switch_v2`):
   - Define nested `*_spec = dict(...)` locals, then `module_args = dict(...)`.
   - Do **not** derive the module argspec by filtering a shared PrismSpecs (or
     similar) helper and picking allowed keys.
   - One arg per writable field, using the snake_case key as the arg name.
   - Scalars: `dict(type="str" | "int" | "bool")`.
   - Enums: `dict(type="str", choices=[...])` from the docstring/enum model.
   - Nested object field: `dict(type="dict", options=<sub_spec>, obj=sdk.<Model>)`.
   - List of objects: `dict(type="list", elements="dict",
     options=<sub_spec>, obj=sdk.<Model>)`.
   - List of scalars: `dict(type="list", elements="str")`.
   - `obj=` must point at the SDK model class so `SpecGenerator` can construct
     the nested SDK object.
   - For update, strip server read-only fields only on the **top-level** entity
     (`strip_read_only_fields(update_spec, fields=(...))`); do not recursively
     strip nested read-only attributes — omit those from the argspec.

5. **Module field set must match the API docs / OpenAPI request schema.** Use
   the SDK only for attribute types, nesting, enums, and `obj=` classes, then
   **intersect** with the API request body — do not expose SDK-only or
   `readOnly` fields.
   Download OpenAPI when needed:
   `https://developers.nutanix.com/api/v1/namespaces/<ns>/versions/<ver>/yaml`
   **Exhaustive coverage:** walk the full create/update request schema
   (nested `$ref` / `allOf` / `oneOf` included) and put **every** non-
   `readOnly` property into `get_module_spec()` + `DOCUMENTATION.options`.
   Do not skip optional, nested, or “metadata-looking” fields that lack
   `readOnly: true` (failure example: omitting `sourceLocation` /
   `domainManagerExtId` + `clusterExtIds` on AHV VM recovery point create).
   Re-check the module keys against that checklist before finishing.
   **Never add read-only fields as module inputs** (`get_module_spec()` or
   `DOCUMENTATION.options` / nested `suboptions`). Detect read-only via:
   - OpenAPI property `readOnly: true` (authoritative; SDK may omit the wording
     — e.g. `DomainManagerNetwork.fqdn`)
   - **Missing from the API docs request schema** (even when present on the SDK)
   - Common server-managed names: `ext_id`, `links`, `tenant_id`, `created_by`,
     `creation_time`, `last_update_time`/`*_time`, `_reserved`, `_object_type`,
     `_unknown_fields`
   - SDK docstring “readOnly” / “used for readOnly purposes” wording (example:
     `DomainManagerResourceConfig.num_vcpus` / `memory_size_bytes` /
     `data_disk_size_bytes`)
   Writable siblings on the same nested object (e.g. `container_ext_ids`) stay
   in the argspec; drop only the read-only / API-absent ones.
   **Do not mention the omitted read-only fields in DOCUMENTATION.** Describe
   only the writable fields that remain.

6. The DOCUMENTATION `options:` block must list exactly the same args
   (names, types, suboptions, choices) as `get_module_spec()`. Sanity tests
   fail on any mismatch. Every option and nested suboption must have a
   `description` taken from the API docs (step 3), not left blank or guessed.

### Example mapping (AddressGroup)

SDK `openapi_types`: `name: str`, `description: str`,
`ipv4_addresses: list[common.v1.config.IPv4Address]`,
`ip_ranges: list[microseg.v4.config.IPv4Range]`, `project_ext_id: str` ...

becomes:

```python
ip_address_sub_spec = dict(value=dict(type="str"), prefix_length=dict(type="int"))
ip_range_spec = dict(start_ip=dict(type="str"), end_ip=dict(type="str"))
module_args = dict(
    ext_id=dict(type="str"),
    project_ext_id=dict(type="str"),
    name=dict(type="str"),
    description=dict(type="str"),
    ipv4_addresses=dict(type="list", elements="dict",
                        options=ip_address_sub_spec, obj=mic_sdk.IPv4Address),
    ip_ranges=dict(type="list", elements="dict",
                   options=ip_range_spec, obj=mic_sdk.IPv4Range),
)
```

## API docs: IAM roles + attribute / sub-attribute descriptions (required)

Every module must use the Nutanix API reference for **both**:

1. **IAM roles** → `DOCUMENTATION.notes`
2. **Attribute and sub-attribute descriptions** → `DOCUMENTATION.options`
   (including every nested `suboptions` / `options` field)

The authoritative source is the Nutanix API reference at the Ref URL — NOT
another module. Existing V2 modules are only a format reference (how to phrase
docs), not a source of truth for roles or field wording.

### How to use the Ref URL

1. Resolve the **latest** docs version for the SDK namespace (do not hardcode
   version numbers — they change over time):
   `https://developers.nutanix.com/api/v1/namespaces/<namespace>/versions`
   (or the version selector on the docs UI). `<namespace>` matches the API
   group, e.g. `microseg`, `networking`, `iam`, `vmm`, `volumes`,
   `clustermgmt`, `prism`, `dataprotection`, `datapolicies`, `security`,
   `objects`, `lcm`, `licensing`.
2. Open that latest version and read the specific endpoint you are calling
   (e.g. Create / Update / Delete / Get / List):
   `https://developers.nutanix.com/api-reference?namespace=<namespace>&version=<latest>`
   Older versions can omit fields or list different roles; always gather
   roles/attributes from the latest page.
3. **Roles:** each endpoint lists its required IAM roles — copy those exact
   role names. List roles per operation, matching how the API docs break them
   down (operations are endpoint-specific, not fixed). Put roles **only** in
   `notes` (intro + `B(...)` lines + Ref). Do not add other prose to `notes`.
   If the API docs do not list roles for the endpoint, omit `notes` entirely.
   **Always list `Required Roles:` alphabetically by role name**, the same way
   the API docs present them (A–Z). Do not keep a random / codegen / YAML dump
   order. Mark deprecated roles as `Self-Service Admin (deprecated)` (or the
   docs’ deprecated name) and still sort them by the bare role name.
4. **Attributes:** for the same endpoint, open the request body / query /
   path schema. For every field that becomes a module option, copy (or closely
   adapt) the docs description into Ansible `description:`. For nested objects
   and arrays, open each child schema and do the same for **every sub-attribute**
   under `suboptions` / nested `options`.
5. Do not invent, guess, or carry over roles or descriptions from a similar
   module — if the docs and a neighboring module disagree, the API docs win.
6. In `DOCUMENTATION.notes`, the Ref URL stays unversioned (match existing
   modules):
   `"Ref: U(https://developers.nutanix.com/api-reference?namespace=<namespace>)"`

### CRUD notes template

`notes` is roles-only. Omit the whole `notes:` section if the API docs have no
roles for the operations this module covers.

```yaml
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
    - >-
      B(Create a <Entity>) -
      Required Roles: <role1>, <role2>, ...
    - >-
      B(Update a <Entity>) -
      Required Roles: <role1>, <role2>, ...
    - >-
      B(Delete a <Entity>) -
      Required Roles: <role1>, <role2>, ...
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=<namespace>)"
```

### Info notes template

Same rule: roles-only, or omit `notes` if the API docs list no roles.

```yaml
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
    - >-
      B(Get <Entity> by ext_id) -
      Required Roles: <role1>, <viewer_role>, ...
    - >-
      B(List all the <Entity>s) -
      Required Roles: <role1>, <viewer_role>, ...
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=<namespace>)"
```
