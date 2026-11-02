# Example playbooks

Scope: WRITE the example playbook files only. Do NOT run them with
`ansible-playbook` — they target a live Prism Central. Generating correct,
readable examples is the deliverable.

Place examples under `examples/<area>_v2/<entity>.yml` (e.g.
`examples/networks_v2/`, `examples/iam_v2/`). Group related CRUD + info calls in
one playbook that demonstrates the full lifecycle.

**Reuse an existing related example when one already exists.** Before creating
`examples/<area>_v2/<new_entity>.yml`, check for a playbook for the parent /
same-area entity (e.g. VM startup policy compliance info →
`examples/vm_startup_policies_v2/vm_startup_policies_v2.yml`). If found, **append**
the new module tasks there (before cleanup/delete) and update the Summary
list — do **not** add a separate playbook file. Only create a new file when no
suitable related example exists.

## EXAMPLES block (inside the module)

Keep concise, runnable snippets in the module's `EXAMPLES = r"""..."""`. Show
the common operations with the credential params inline:

```yaml
- name: Create <entity>
  nutanix.ncp.ntnx_<entity>_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    state: present
    name: "example-<entity>"
    # ... entity fields ...

- name: Delete <entity>
  nutanix.ncp.ntnx_<entity>_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    state: absent
    ext_id: "{{ <entity>_ext_id }}"
```

Info module EXAMPLES: show get-by-ext_id, list all, and — when `fetch_all` is
supported (standard `ntnx_info_v2` list modules) — **must** include a
`fetch_all: true` example. The same `fetch_all` task is required in the
standalone example playbook under `examples/`.

**Filter examples must use API-supported fields only.** When adding a
`filter:` example (module `EXAMPLES`, standalone `examples/` playbook, or
integration tests), open the list endpoint’s `$filter` parameter in the API
docs and use a field from **“The filter can be applied to the following
fields”** (camelCase as documented, e.g. `recoveryPointType`, `vmExtId`).
Do **not** invent fields that are not on that list (e.g. do not use `name`
for AHV VM recovery points — it is not a supported filter field).

## Standalone example playbook (examples/<area>_v2/<entity>.yml)

```yaml
- name: <Entity> CRUD playbook. Create, update, read and delete the <entity>.
  hosts: localhost
  gather_facts: false
  module_defaults:
    group/nutanix.ncp.ntnx:
      nutanix_host: <pc_ip>
      nutanix_username: <user>
      nutanix_password: <pass>
      validate_certs: false
  tasks:
    # Hard rule: when the playbook needs user-supplied IDs / inputs (vm_ext_id,
    # parent ext_ids, device UUIDs, etc.), always introduce them in a Set
    # variables set_fact task with "<placeholder>" values, then reference
    # "{{ var_name }}" in later tasks. Do not inline "<vm_ext_id>" repeatedly
    # in module args. See examples/vmm_v2/vm_pcie_device_v2.yml.
    - name: Set variables
      ansible.builtin.set_fact:
        vm_ext_id: "<vm_ext_id>"
        # ... other required placeholders ...

    - name: Create <entity>
      nutanix.ncp.ntnx_<entity>_v2:
        state: present
        name: example-<entity>
        # ... entity fields ...
        # vm_ext_id: "{{ vm_ext_id }}"
      register: created

    - name: Update <entity>
      nutanix.ncp.ntnx_<entity>_v2:
        state: present
        ext_id: "{{ created.ext_id }}"
        name: example-<entity>-updated
      register: updated

    - name: Fetch the <entity>
      nutanix.ncp.ntnx_<entity>_info_v2:
        ext_id: "{{ updated.ext_id }}"
      register: info

    - name: Print <entity> details
      ansible.builtin.debug:
        msg: "{{ info }}"

    - name: Delete the <entity>
      nutanix.ncp.ntnx_<entity>_v2:
        state: absent
        ext_id: "{{ updated.ext_id }}"
      register: deleted
```

Conventions:
- `hosts: localhost`, `gather_facts: false`.
- Use `module_defaults: group/nutanix.ncp.ntnx` for shared connection params;
  use placeholders `<pc_ip>/<user>/<pass>` in standalone examples.
- **Always `set_fact` user-supplied variables** when the example needs IDs or
  other inputs the reader must fill in (`vm_ext_id`, parent `ext_id`,
  `device_ext_id`, cluster IDs, etc.). First task:
  `name: Set variables` / `ansible.builtin.set_fact:` with `"<placeholder>"`
  values; later tasks use `"{{ var_name }}"`. Do **not** scatter raw
  `"<vm_ext_id>"` strings across module arguments. Values produced by prior
  tasks (`register` → `created.ext_id`) stay as Jinja from the register —
  only pre-existing external inputs go in `set_fact`.
- Chain tasks with `register` + `ext_id` (do not hardcode real UUIDs here).
- **Never** add `ignore_errors: true` without a matching `register:` on the
  same task (including cleanup). `ignore_errors` alone hides failures with no
  result to inspect.
- Always include **real** (non-`dryrun`) operation examples for every module
  action. Optional `dryrun: true` tasks may be added in addition, never as the
  only example of that operation.
