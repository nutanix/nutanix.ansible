# Integration test target (V2)

References (copy structure from these, adapted to your entity):

- CRUD + info in one flow: `tests/integration/targets/ntnx_address_groups_v2/`
- Heavier CRUD + info + negatives: `tests/integration/targets/ntnx_virtual_switches_v2/`
- Info-only: `tests/integration/targets/ntnx_stigs_info_v2/`

**Always WRITE the test target.** After static verification (formatters / sanity),
**also RUN** the integration target against a live Prism Central when a PC IP is
available — either already set in
`tests/integration/targets/prepare_env/vars/main.yml` **or** provided by the
user in the chat — see [Running live integration tests](#running-live-integration-tests)
and the Verification section in `SKILL.md`. If neither source has a PC IP, only
write the tests; do not invent an IP or run live.

## Directory layout

```
tests/integration/targets/ntnx_<entity>_v2/
├── aliases            # single word: disabled
├── meta/main.yml      # dependencies: [prepare_env]
├── tasks/main.yml     # module_defaults block -> import_tasks
└── tasks/<entity>.yml # the actual scenarios
```

Info-only modules use `ntnx_<entity>_info_v2/` the same way
(e.g. `ntnx_stigs_info_v2`).

### aliases

```
disabled
```

### meta/main.yml

```yaml
dependencies:
  - prepare_env
```

### tasks/main.yml

```yaml
---
- name: Set module defaults
  module_defaults:
    group/nutanix.ncp.ntnx:
      nutanix_host: "{{ ip }}"
      nutanix_username: "{{ username | default(omit) }}"
      nutanix_password: "{{ password | default(omit) }}"
      nutanix_api_key: "{{ nutanix_api_key | default(omit) }}"
      validate_certs: "{{ validate_certs }}"
      nutanix_debug: "{{ nutanix_debug | default(omit) }}"
      nutanix_log_file: "{{ nutanix_log_file | default(omit) }}"
  block:
    - name: Import <entity>.yml
      ansible.builtin.import_tasks: <entity>.yml
```

## Design rules (mandatory)

1. **Self-contained / independent target.** Do not rely on leftover entities from
   other test targets. Create any prerequisite entities the scenarios need
   (parent VM, subnet, category, certificate, etc.) **inside this target**, then
   delete them in cleanup at the end.
2. **Create what you need, delete what you create.** Track created `ext_id`s in a
   `todelete` list (or dedicated facts) and always tear them down, even after
   failed asserts where practical (`ignore_errors: true` + final cleanup loop).
3. **One assert per operation.** Every module call is followed by an
   `ansible.builtin.assert` with `fail_msg` / `success_msg`.
4. **Always** `register: result` (or a clear name) + `ignore_errors: true` on
   module tasks. Never use `ignore_errors: true` without `register:`.
5. **Check-mode dummies stay inline.** In `check_mode: true` tasks, hardcode
   dummy UUIDs / IPs / names **in the task**. Do not put check-mode-only
   references in `vars/` or `set_fact`. Live tasks use registered values.
6. **Filter fields must be API-supported.** Info `$filter` examples use only
   fields listed under the list endpoint’s supported filter fields in the API
   docs (camelCase). Never invent fields.
7. **Keep physical lines ≤ 160 characters** (ansible-lint / yamllint).

## CRUD module scenario order (V2)

Mirror `ntnx_address_groups_v2` / `ntnx_virtual_switches_v2`. Cover **all**
operations the module supports (omit update/delete sections if the API has no
update/delete).

```
1.  Debug "Start <entity> tests"
2.  set_fact random_name (community.general.random_string) + derived names
3.  set_fact todelete: []
4.  Create prerequisite entities (if needed) -> assert -> append to todelete / facts
5.  Create <entity> with check_mode: true     -> assert changed == false, response matches input
6.  Create <entity> (live)                   -> assert changed == true, capture ext_id
7.  set_fact / append ext_id to todelete
8.  Update <entity> with check_mode: true    -> assert changed == false (if update exists)
9.  Update <entity> (live)                   -> assert changed == true
10. Idempotency: same update values again    -> assert changed == false, msg == "Nothing to change."
11. Negative cases (as applicable):
      - missing required args
      - duplicate name
      - invalid / non-existent ext_id
      - unsupported update field
12. Info coverage for the companion *_info_v2 (when shipped with this target):
      - get by ext_id
      - list all
      - list with limit
      - list with filter (API-supported field)
      - fetch_all: true when supported -> assert
        (response | length) == (total_available_results | int)
      - negative get (wrong ext_id) when useful
13. Delete <entity> with check_mode: true    -> assert changed == false,
      msg matches "<Entity> with ext_id:{{ id }} will be deleted."
14. Delete <entity> (live)                   -> assert changed == true
      (and response.status == "SUCCEEDED" when wait returns a task)
15. Delete / clean prerequisites; reset todelete
```

### Check-mode create example

```yaml
- name: Create <entity> with check mode enabled
  nutanix.ncp.ntnx_<entity>_v2:
    state: present
    name: "{{ ag1 }}"
    description: test-ansible-<entity>-desc
    project_ext_id: "83083083-0000-0000-0000-000000000000"   # inline dummy UUID
    ipv4_addresses:
      - value: 10.1.1.0
        prefix_length: 24
  register: result
  ignore_errors: true
  check_mode: true

- name: Create <entity> with check mode enabled status
  ansible.builtin.assert:
    that:
      - result.response is defined
      - result.changed == false
      - result.failed == false
      - result.response.name == "{{ ag1 }}"
    fail_msg: Create <entity> with check mode enabled failed
    success_msg: Create <entity> with check mode enabled passed
```

### Idempotency example

```yaml
- name: Test idempotency by updating <entity> with same values
  nutanix.ncp.ntnx_<entity>_v2:
    state: present
    ext_id: "{{ todelete }}"
    name: "{{ ag1 }}"
    # same fields as the previous live update
  register: result
  ignore_errors: true

- name: Idempotency check status
  ansible.builtin.assert:
    that:
      - result.changed == false
      - result.failed == false
      - result.msg == "Nothing to change."
    fail_msg: Idempotency check failed
    success_msg: Idempotency check passed
```

## Info module scenario order (V2)

For a dedicated `*_info_v2` target (or the info section of a CRUD target),
mirror `ntnx_stigs_info_v2` / the info blocks in `ntnx_address_groups_v2` and
`ntnx_virtual_switches_v2`:

```
1.  Debug start
2.  If get-by-id / filter needs a known entity: create one (or use a prerequisite
    created earlier in this same target), track for cleanup
3.  List all                         -> assert response length > 0,
      total_available_results defined / > 0
4.  Get by ext_id                    -> assert response.ext_id matches
5.  List with limit: 1               -> assert response | length == 1
6.  List with filter                 -> assert length / field match
      (filter field from API docs only)
7.  fetch_all: true (when supported) -> assert
      (response | length) == (total_available_results | int)
8.  Negative: invalid filter / wrong ext_id when useful
9.  Delete any entities this target created
```

Info modules do **not** use `check_mode` (BaseInfoModule typically
`supports_check_mode=False`).

## Action / download / one-shot modules

Adapt the CRUD skeleton:

- Check mode (inline dummies) → live action → optional idempotency/skip →
  negatives → cleanup of any prerequisites.
- File-download modules: cover with and without optional `dest`, `stat` the
  file, assert `response.path`, then delete the downloaded file.

## Running live integration tests

**Trigger:** a Prism Central IP is available from **either**:
- `tests/integration/targets/prepare_env/vars/main.yml` (uncommented `ip:` in
  the managed block / vars already defined there), **or**
- the user provided a PC IP (or hostname) in the chat.

Always **read** `prepare_env/vars/main.yml` and consider variables already
defined there before inventing or overwriting connection settings.

When that happens, after formatters / sanity pass:

1. **Confirm / wire credentials in**
   `tests/integration/targets/prepare_env/vars/main.yml`:
   - Prefer an `ip:` already present in `main.yml`.
   - If the user gave a PC IP in chat, set/update `ip:` to that value.
   - **Default credentials** when username/password are missing (unless the user
     provided different ones in chat): `username: admin`,
     `password: Nutanix.123`.
   - If the user gave a different username/password in chat, use those instead.
   - Set `validate_certs: false` unless the user specified otherwise.
2. Work from the **installed** collection path (same build/install used for
   sanity), or re-build/install so the test target files are current.
3. Run only the new/changed target(s), with `--allow-disabled` because aliases
   are `disabled`:

```bash
# from collection repo root
PY="${ANSIBLE_TEST_PYTHON:-$(command -v python3.10 || command -v python3)}"
PY_VERSION="${ANSIBLE_TEST_PYTHON_VERSION:-$("$PY" -c 'import sys; print("%d.%d" % sys.version_info[:2])')}"
ansible-galaxy collection build -f
version=$(grep '^version:' galaxy.yml | awk '{print $2}' | tr -d '"')
ansible-galaxy collection install -f "./nutanix-ncp-${version}.tar.gz"
cd "${HOME}/.ansible/collections/ansible_collections/nutanix/ncp"

# ensure prepare_env vars in THIS installed tree have ip/username/password
# (copy or edit tests/integration/targets/prepare_env/vars/main.yml here)

ansible-test integration --allow-disabled --python "$PY_VERSION" \
  --python-interpreter "$PY" ntnx_<entity>_v2
# also run ntnx_<entity>_info_v2 when that target exists separately
```

4. **Fix every failure** (module or test) and re-run until the target passes.
5. Do **not** leave orphaned entities — the playbook cleanup section must delete
   what it created. If a run aborts mid-way, clean up manually or re-run after
   fixing so delete tasks execute.

If **neither** `main.yml` nor chat has a PC IP: write the tests only; do
**not** run `ansible-test integration` or live playbooks.

Do **not** edit the collection `requirements.txt` as part of this workflow.
