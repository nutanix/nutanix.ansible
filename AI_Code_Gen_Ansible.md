# AI-Assisted Code Generation for Ansible Collection Development

## The Problem

Every new Nutanix API entity requires **the same set of deliverables** for Ansible collection support:

| Deliverable | Description |
|---|---|
| CRUD Module | Ansible module with Create, Read, Update, Delete + idempotency + check_mode |
| Info Module | Ansible module for Get (by ext_id) and List (with pagination) |
| API Client Function | New API instance factory in `api_client.py` |
| Helper Functions | Get-by-ID helper in `helpers.py` |
| Integration Tests | Full test playbook — CRUD, info, check_mode, negative scenarios |
| Examples | Working Ansible playbooks in `examples/` |
| Provider Registration | Wire modules into `meta/runtime.yml` action groups |
| Automated Validation | Examples run against real PC, tests executed and logs stored, linting passed |

This work is **repetitive, pattern-driven, and error-prone** — the perfect candidate for automation.

---

## Case Study: Entity Group (Flow / Microseg)

We used the AI-assisted code generation pipeline to implement complete Ansible support for the **Entity Group** entity in the Flow (Microseg) namespace.

### What Was Generated

| File | Lines | Category |
|---|---|---|
| `ntnx_entity_group_v2.py` | 622 | CRUD Module (Create/Read/Update/Delete) |
| `ntnx_entity_groups_info_v2.py` | 233 | Info Module (Get/List) |
| `api_client.py` (updated) | +15 | SDK client — new `get_entity_group_api_instance()` |
| `helpers.py` (updated) | +19 | Helper — new `get_entity_group()` |
| `entity_groups.yml` (tests) | 771 | Integration tests (CRUD + info + check_mode + negative) |
| `entity_groups_v2.yml` (examples) | 86 | Working playbook examples |
| `runtime.yml` (updated) | +2 | Action group registration |
| `example_logs_*.txt` | — | Logs of successfully running examples |
| `test_logs_*.txt` | — | Logs of successfully running tests |

**Total: 7+ files created/updated | ~1,748 lines of production-ready code**

---

## Time Comparison

### Manual Development (Traditional Approach)

| Task | Estimated Time | Notes |
|---|---|---|
| Read SDK source code & understand API | 1–2 hours | Navigate installed package, understand request/response models, enums, OneOf types |
| Design Ansible module spec | 1–1.5 hours | Map SDK fields to Ansible argument_spec types, decide required/optional/mutually_exclusive |
| Write CRUD module | 2–3 hours | DOCUMENTATION + EXAMPLES + RETURN + get_module_spec + create/update/delete + idempotency + check_mode |
| Write info module | 1–1.5 hours | DOCUMENTATION + EXAMPLES + RETURN + get/list with pagination + strip_internal_attributes |
| Write helper functions | 0.5 hour | get_entity_by_id helper, API client instance factory |
| Write integration tests | 2–3 hours | CRUD tests, check_mode tests, info tests, negative scenarios, assertions |
| Run tests and debug failures | 1–2 hours | Execute against real PC, fix assertion mismatches |
| Update runtime.yml | 5 minutes | Add module names to action_groups |
| Write examples and run them | 0.5–1 hour | Working playbooks with variables, verify against real PC |
| Debugging / fixing lint errors | 1–2 hours | black, isort, flake8, ansible-lint, ansible-test sanity |
| **Total** | **~10–16 hours** | **~2–3 full working days** |

### AI-Assisted Approach (With Code Gen Pipeline)

| Task | Estimated Time | Notes |
|---|---|---|
| Run `generate_ansible_modules.py` | 1 minute | Introspects SDK, builds prompt, launches agent session |
| AI generates all code | 5–10 minutes | All files generated in a single session |
| AI runs examples against real PC | Automated | Examples executed, logs captured — no manual step |
| AI runs integration tests against real PC | Automated | Tests executed, assertions validated, logs stored — no manual step |
| AI runs linters (black, isort, flake8, ansible-lint, sanity) | Automated | Fixes any lint issues in-place — no manual step |
| Review & validate generated code | 30–120 minutes | Verify module spec correctness, review test logs |
| Fix edge cases | 15–30 minutes | OneOf types, enum handling, SDK quirks |
| **Total** | **~1–3 hours** | **Same working day** |

### Time Saved

| Metric | Value |
|---|---|
| Manual effort | 10–16 hours (2–3 days) |
| AI-assisted effort | 1–3 hours (same day) |
| **Time saved per entity** | **~9–13 hours (80–90%)** |
| **Speedup factor** | **~5–10x faster** |

---

## How the Pipeline Works

### Architecture

```
┌──────────────────┐     ┌──────────────────┐     ┌───────────────────────┐     ┌───────────────────────┐
│  1. SDK Discovery │ ──▶ │  2. Introspection │ ──▶ │  3. Prompt Assembly   │ ──▶ │  4. Agent Session     │
│  (namespace →     │     │  (API classes,    │     │  (only the sections   │     │                       │
│   ntnx_*_py_client│     │   models, fields, │     │   you asked for are   │     │  Interactive (def)    │
│   auto-import)    │     │   method sigs)    │     │   included)           │     │  or headless / manual │
└──────────────────┘     └──────────────────┘     └───────────────────────┘     └───────────────────────┘
```

### Step-by-Step

```
Step 1: SDK Discovery & Introspection
  python generate_ansible_modules.py iam \
    --crud ntnx_scope_template_v2 \
    --info ntnx_scope_templates_info_v2 \
    --pc-ip 10.104.16.34
                |
                v
      Maps "iam" → ntnx_iam_py_client (from 21 namespace mappings)
      Uses Python `inspect` to extract:
        - All API service classes (e.g. ScopeTemplatesApi, RolesApi)
        - Every public method with full parameter signatures
        - All model/data classes with field names, SDK names, and types
          (via attribute_map + openapi_types)
        - SDK version

Step 2: Context-Aware Prompt Assembly
                |
                v
      Composes prompt from 7 independent sections:
        ┌─────────────────────────────────────────────────┐
        │ 1. Preamble — role, SDK reference, repo pointers│
        │ 2. CRUD requirements (if --crud)                │
        │ 3. Info requirements (if --info)                │
        │ 4. Helpers & API client patterns                │
        │ 5. Examples — with PC IP for live execution     │
        │ 6. Tests — with run & store-logs instructions   │
        │ 7. Code quality — lint checks to run            │
        └─────────────────────────────────────────────────┘

Step 3: Agent Invocation (auto-starts generation)
                |
                v
      Cursor Agent (claude-4.6-opus-high-thinking) generates:
        - CRUD module + Info module
        - API client updates + Helper updates
        - Integration tests → runs them against PC → stores logs
        - Examples → runs them against PC → stores logs
        - Linting → runs black/isort/flake8/ansible-lint/sanity → fixes issues
        - runtime.yml registration

Step 4: Developer Review — Human involvement
  - Review generated code and test logs
  - Verify module spec design
  - Fix any remaining edge cases
  - Submit for code review
```

---

## What the Script Does (Under the Hood)

### 1. SDK Discovery (`discover_sdk`)

Maps the namespace argument to the correct `ntnx_*_py_client` package already installed in the active venv. Supports **21 SDK packages** with alias support (e.g. `flow` → `ntnx_microseg_py_client`, `clustermgmt` → `ntnx_clustermgmt_py_client`).

### 2. Runtime Introspection (Python `inspect`)

The pipeline uses **runtime introspection** — it imports the SDK and programmatically inspects it:

| What's Extracted | How | Example Output |
|---|---|---|
| API service classes | `dir(sdk)` filtered by `*Api` suffix | `ScopeTemplatesApi`, `RolesApi`, `UsersApi` |
| Method signatures | `inspect.signature()` on each method | `create_scope_template(body, kwargs)` |
| Model classes | `dir(sdk)` filtered by non-Api, uppercase | `ScopeTemplate`, `ScopeTemplateNameValues` |
| Field names & types | `attribute_map` + `openapi_types` dicts | `name: str`, `description: str`, `scope: Scope` |
| SDK version | `sdk.__version__` | `17.6.0.18369` |

This context is embedded directly into the prompt so the AI knows every API method, parameter, model class, and field type — no guessing.

### 3. Modular Prompt Assembly

The prompt is assembled from **7 independent sections**. Only the sections matching your `--crud` / `--info` selection are included:

| Section | `--crud` only | `--info` only | Both | Key Instructions |
|---|:---:|:---:|:---:|---|
| Preamble + SDK reference | Yes | Yes | Yes | Role, SDK context, repo patterns, copyright year |
| CRUD module requirements | Yes | — | Yes | Idempotency, check_mode, etag, return params, file structure |
| Info module requirements | — | Yes | Yes | Get/list, pagination, strip_internal_attributes |
| Helpers & API client | Yes | Yes | Yes | Create/update helper & api_client with docstrings |
| Examples | Yes | Yes | Yes | **Run against PC IP**, store execution logs |
| Tests | Yes | Yes | Yes | check_mode + CRUD + info + negative, **run & store logs** |
| Code quality | Yes | Yes | Yes | **Run** black, isort, flake8, ansible-lint, ansible-test sanity |

### 4. Three Invocation Modes

| Mode | Flag | How It Works |
|---|---|---|
| **Interactive** (default) | *(none)* | `os.execvp` seamlessly replaces the Python process with a live `agent` session — no copy-paste needed |
| **Headless** | `--headless` | Pipes prompt via stdin to `agent -p --force`, logs all output to file, requires `CURSOR_API_KEY` |
| **Prompt-only** | `--prompt-only` | Saves prompt file, prints manual instructions — no agent invocation |

Fallback: if the `agent` CLI is not installed, the script tries to open the prompt file in the running Cursor IDE window.

### 5. Optional Design Document Support

Pass `--design-doc path/to/design.md` and its contents are embedded in the prompt preamble, giving the AI additional context about the entity's design decisions and constraints.

---

## What the AI Agent Does Automatically

This is the key differentiator — the pipeline doesn't just generate code, it **validates everything against a real Prism Central**:

### Auto-Executed Examples
- The prompt instructs the agent to **run all examples** against the provided PC IP (using `--pc-ip`)
- Credentials are provided inline: `Username: admin, Password: Nutanix.123`
- A **separate log file** (`example_logs_*.txt`) is created with the output of successfully running examples
- For response samples: if the example runs successfully, actual API responses are captured; if it fails, `<Need to add sample>` is used as placeholder

### Auto-Executed Integration Tests
- All tests are **run against the real PC** automatically
- The agent stores test execution logs in a file (`test_logs_*.txt`)
- Assertions are added **after running** — the agent first runs the test, then adds proper assertions based on actual results
- Test coverage includes:
  - **CRUD operations**: create, update, delete with all required fields
  - **check_mode**: every field tested for create, update, and delete
  - **Info operations**: get-by-ext_id and list with pagination
  - **Negative scenarios**: with assertions for expected error messages
  - **Assertions**: `changed` and `failed` checked first in every test, then field-level assertions

### Auto-Executed Linting
- The agent runs **all 5 linters** and fixes any issues:
  - `black` — code formatting
  - `isort` — import sorting
  - `flake8` — style and error checks
  - `ansible-lint` — Ansible-specific best practices
  - `ansible-test sanity` — Ansible collection sanity checks

---

## CRUD Module: What Gets Generated

Every CRUD module follows this exact file structure (enforced by the prompt):

```
1. Documentation (DOCUMENTATION, EXAMPLES, RETURN)
2. All Imports (SDK + mock fallback)
3. get_module_spec()
4. create_<resource>(module, result)
5. Idempotency check method
6. update_<resource>(module, result)
7. delete_<resource>(module, result)
8. run_module()
9. main()
```

Key requirements enforced:
- **Idempotency + check_mode** support matching existing v2 modules
- **Etag** handling for Update and Delete via `if_match`
- **Return params**: `response`, `changed`, `ext_id`, `task_ext_id`, `skipped`, `msg`, `error`, `failed`
- **SDK mock import** for sanity test compatibility
- **InsecureRequestWarning suppression**
- API instance defined once in `run_module()` and passed to all methods

## Info Module: What Gets Generated

- Get (by ext_id) and List (with pagination) operations
- Pagination uses `total_available_results` from `resp.metadata`
- `strip_internal_attributes` applied to list responses
- **Return params**: `response`, `changed`, `ext_id`, `msg`, `error`, `failed`

---

## Advantages

### 1. Speed
- **5–10x faster** development per entity
- Same-day delivery instead of multi-day effort
- Faster time-to-market for new Ansible modules

### 2. Consistency
- Every module follows the **exact same patterns** (module_spec, DOCUMENTATION format, error handling, return values)
- No more "this module does it one way, that module does it another"
- Uniform test structure across all modules

### 3. Completeness
- **Nothing gets forgotten** — tests, examples, helpers, runtime.yml registration all generated together
- Every module ships with full inline documentation from day one
- Integration tests include CRUD, check_mode, info, and negative scenarios

### 4. Automated Validation
- Examples **actually run** against a real Prism Central — not just written
- Tests **actually execute** with real assertions — not just placeholders
- Linting **actually passes** — issues fixed before the developer even looks at the code

### 5. Lower Review Burden
- Generated code follows established patterns, making reviews faster
- Reviewers focus on **business logic correctness** rather than boilerplate structure
- Less back-and-forth on code style or missing files

---

## What Still Needs Human Judgment

The AI-assisted pipeline is not fully autonomous. Developers still need to:

- **Review**: Review the code in detail — verify module_spec correctness, SDK field mappings, and idempotency logic
- **Dev testing**: Validate edge cases the automated run might miss (e.g. concurrent operations, unusual input values)
- **Test correction**: Fix any assertion mismatches from test execution logs

**The pipeline handles the 70–80% of boilerplate. The developer focuses on the 20–30% that requires expertise.**

---

## Investment Required

The code gen pipeline is already built and operational:

| Component | Lines of Code | Status |
|---|---|---|
| `generate_ansible_modules.py` | 862 | Complete |
| `GENERATE_MODULES_README.md` | 264 | Complete |
| **Total** | **1,126** | **Ready to use** |

No additional infrastructure, CI/CD changes, or tool installations required. It runs locally with `python` and the Cursor `agent` CLI.

---

## Supported Namespaces (21 SDKs)

| Namespace | Alias(es) | SDK Package |
|---|---|---|
| `vmm` | — | `ntnx_vmm_py_client` |
| `iam` | — | `ntnx_iam_py_client` |
| `networking` | `network` | `ntnx_networking_py_client` |
| `clusters_mgmt` | `clustermgmt` | `ntnx_clustermgmt_py_client` |
| `prism` | — | `ntnx_prism_py_client` |
| `volumes` | — | `ntnx_volumes_py_client` |
| `security` | — | `ntnx_security_py_client` |
| `objects` | — | `ntnx_objects_py_client` |
| `lcm` | `lifecycle` | `ntnx_lifecycle_py_client` |
| `licensing` | — | `ntnx_licensing_py_client` |
| `data_protection` | `dataprotection` | `ntnx_dataprotection_py_client` |
| `data_policies` | `datapolicies` | `ntnx_datapolicies_py_client` |
| `flow` | `microseg` | `ntnx_microseg_py_client` |
| `aiops` | — | `ntnx_aiops_py_client` |
| `files` | — | `ntnx_files_py_client` |
| `monitoring` | — | `ntnx_monitoring_py_client` |
| `opsmgmt` | — | `ntnx_opsmgmt_py_client` |
| `devops` | — | `ntnx_devops_py_client` |

---

## Cost Efficiency: Real Usage Data

The Entity Group implementation was generated in **1 Cursor AI request**.

| Metric | Value |
|---|---|
| Date | Apr 2026 |
| Model | claude-4.6-opus-high-thinking |
| Requests | **1** |
| Tokens used | **~1M** |
| Output | 7+ files, ~1,748 lines of production code |

### What This Means

- **1 request** = 1 CRUD module + 1 info module + tests + examples + helpers + API client + registration + execution logs
- No additional API costs — this runs within the existing Cursor Business license
- A developer writing the same code manually would spend **2–3 days** and still need review cycles for consistency and completeness
- The AI produced **review-ready code** in one shot that followed existing patterns, passed linting, and was validated against a real PC

---

## Quick Start

```bash
# 1. Activate venv with the target SDK installed
source venv_projects_3.12/bin/activate

# 2. Run the pipeline — interactive agent session (default)
python generate_ansible_modules.py iam \
    --crud ntnx_scope_template_v2 \
    --info ntnx_scope_templates_info_v2 \
    --pc-ip 10.104.16.34

# The script:
#   - Discovers ntnx_iam_py_client, introspects all API classes & models
#   - Builds a context-aware prompt with SDK reference
#   - Launches an interactive agent session
#   - Agent generates modules, tests, examples
#   - Agent runs examples against 10.104.16.34 and stores logs
#   - Agent runs tests against 10.104.16.34 and stores logs
#   - Agent runs black, isort, flake8, ansible-lint, ansible-test sanity
```

### Other Modes

```bash
# Headless — non-interactive, logs everything to file
export CURSOR_API_KEY=<your-key>
python generate_ansible_modules.py iam \
    --crud ntnx_scope_template_v2 \
    --info ntnx_scope_templates_info_v2 \
    --pc-ip 10.104.16.34 \
    --headless

# Prompt only — generate prompt file, no agent invocation
python generate_ansible_modules.py iam \
    --crud ntnx_scope_template_v2 \
    --pc-ip 10.104.16.34 \
    --prompt-only

# With design document
python generate_ansible_modules.py iam \
    --crud ntnx_scope_template_v2 \
    --info ntnx_scope_templates_info_v2 \
    --pc-ip 10.104.16.34 \
    --design-doc docs/scope_template_design.md
```

For full options and troubleshooting see the [README](GENERATE_MODULES_README.md).

---

## Conclusion

**Bottom line: A one-time investment of ~1,100 lines of tooling code saves 9–13 hours per entity. The entire Entity Group module set — 7+ files, ~1,748 lines — was generated in a single AI request at zero incremental cost. The code was not just generated but automatically tested against a real Prism Central and lint-checked before the developer even reviewed it.**

This approach helps us ship new Ansible modules faster, with greater consistency, and with less manual toil.

**Note:** ~80% of the boilerplate is automated — the developer focuses on the 20% that matters.

* Important to note: Used claude-4.6-opus-high-thinking agent consumed only 1 Request (~1M tokens) to generate the production-ready code.

### Future Plan
1. Currently we run this pipeline locally, not pushed to any code base. Find a solution for it.
2. Build Agent skill for streamlined invocation.
