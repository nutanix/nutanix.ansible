#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Generate Ansible modules by introspecting installed Nutanix SDKs and delivering
a rich, context-aware prompt to Cursor.

The script:
  1. Discovers the SDK package for the given namespace from the active venv.
  2. Introspects API classes, model classes, and method signatures.
  3. Builds a comprehensive prompt (following the team's conventions).
  4. Launches an interactive ``agent`` session with the prompt (default),
     runs headless (``--headless``), or just saves the prompt (``--prompt-only``).

You can generate a CRUD module, an info module, or both in one run.

Usage:
    # Default — starts interactive agent session with the prompt
    python generate_ansible_modules.py iam --crud ntnx_directory_services_v2 --info ntnx_directory_services_info_v2 --pc-ip 10.0.0.1

    # Headless — runs standalone agent CLI non-interactively
    python generate_ansible_modules.py vmm --crud ntnx_vms_v2 --pc-ip 10.0.0.1 --headless

    # Prompt only — no Cursor invocation
    python generate_ansible_modules.py vmm --info ntnx_vms_info_v2 --pc-ip 10.0.0.1 --prompt-only
"""

from __future__ import annotations

import argparse
import importlib
import inspect
import os
import shutil
import subprocess
import sys
import textwrap
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


# ---------------------------------------------------------------------------
# Namespace → SDK package mapping (mirrors v4/*/api_client.py imports)
# ---------------------------------------------------------------------------
NAMESPACE_TO_SDK: Dict[str, str] = {
    "vmm": "ntnx_vmm_py_client",
    "iam": "ntnx_iam_py_client",
    "networking": "ntnx_networking_py_client",
    "network": "ntnx_networking_py_client",
    "clusters_mgmt": "ntnx_clustermgmt_py_client",
    "clustermgmt": "ntnx_clustermgmt_py_client",
    "prism": "ntnx_prism_py_client",
    "volumes": "ntnx_volumes_py_client",
    "security": "ntnx_security_py_client",
    "objects": "ntnx_objects_py_client",
    "lcm": "ntnx_lifecycle_py_client",
    "lifecycle": "ntnx_lifecycle_py_client",
    "licensing": "ntnx_licensing_py_client",
    "data_protection": "ntnx_dataprotection_py_client",
    "dataprotection": "ntnx_dataprotection_py_client",
    "data_policies": "ntnx_datapolicies_py_client",
    "datapolicies": "ntnx_datapolicies_py_client",
    "flow": "ntnx_microseg_py_client",
    "microseg": "ntnx_microseg_py_client",
    "aiops": "ntnx_aiops_py_client",
    "files": "ntnx_files_py_client",
    "monitoring": "ntnx_monitoring_py_client",
    "opsmgmt": "ntnx_opsmgmt_py_client",
    "devops": "ntnx_devops_py_client",
}

V4_DIR_MAP: Dict[str, str] = {
    "vmm": "vmm", "iam": "iam", "networking": "network", "network": "network",
    "clusters_mgmt": "clusters_mgmt", "clustermgmt": "clusters_mgmt",
    "prism": "prism", "volumes": "volumes", "security": "security",
    "objects": "objects", "lcm": "lcm", "lifecycle": "lcm",
    "licensing": "licensing", "data_protection": "data_protection",
    "dataprotection": "data_protection", "data_policies": "data_policies",
    "datapolicies": "data_policies", "flow": "flow", "microseg": "flow",
    "aiops": "aiops", "files": "files", "monitoring": "monitoring",
    "opsmgmt": "opsmgmt", "devops": "devops",
}

REPO_ROOT = Path(__file__).resolve().parent
COLLECTION_ROOT = REPO_ROOT / "nutanix.ansible"


# ---------------------------------------------------------------------------
# SDK introspection helpers
# ---------------------------------------------------------------------------

def discover_sdk(namespace: str) -> Tuple[str, Any]:
    """Return (sdk_package_name, imported_module) for *namespace*."""
    sdk_name = NAMESPACE_TO_SDK.get(namespace.lower())
    if not sdk_name:
        available = sorted(set(NAMESPACE_TO_SDK.values()))
        sys.exit(
            f"Unknown namespace '{namespace}'.\n"
            f"Available SDK packages: {', '.join(available)}\n"
            f"Supported namespace aliases: {', '.join(sorted(NAMESPACE_TO_SDK.keys()))}"
        )
    try:
        sdk = importlib.import_module(sdk_name)
    except ImportError:
        sys.exit(
            f"SDK '{sdk_name}' is not installed in the current environment.\n"
            f"Install it first, e.g.: pip install {sdk_name}"
        )
    return sdk_name, sdk


def get_api_classes(sdk: Any) -> List[str]:
    """Return all *Api service classes (e.g. VmApi, ImagesApi)."""
    return sorted(
        name for name in dir(sdk)
        if name.endswith("Api") and not name.startswith("_") and inspect.isclass(getattr(sdk, name, None))
    )


def get_model_classes(sdk: Any) -> List[str]:
    """Return all model / data classes (non-Api, non-private, uppercase start)."""
    return sorted(
        name for name in dir(sdk)
        if not name.startswith("_")
        and name[0].isupper()
        and not name.endswith("Api")
        and inspect.isclass(getattr(sdk, name, None))
    )


def get_api_methods(sdk: Any, api_class_name: str) -> List[Dict[str, Any]]:
    """Return public methods of an API class with their signatures."""
    cls = getattr(sdk, api_class_name, None)
    if cls is None:
        return []
    methods = []
    for name in sorted(dir(cls)):
        if name.startswith("_"):
            continue
        attr = getattr(cls, name, None)
        if callable(attr):
            try:
                sig = inspect.signature(attr)
                params = [
                    {"name": p.name, "default": repr(p.default) if p.default is not inspect.Parameter.empty else None}
                    for p in sig.parameters.values()
                    if p.name != "self"
                ]
                methods.append({"name": name, "params": params})
            except (ValueError, TypeError):
                methods.append({"name": name, "params": []})
    return methods


def get_model_fields(sdk: Any, model_name: str) -> List[Dict[str, str]]:
    """Try to extract fields from a model class via its __init__ or attribute_map."""
    cls = getattr(sdk, model_name, None)
    if cls is None:
        return []

    attribute_map = getattr(cls, "attribute_map", None)
    if attribute_map and isinstance(attribute_map, dict):
        swagger_types = getattr(cls, "openapi_types", getattr(cls, "swagger_types", {}))
        return [
            {"name": k, "sdk_name": v, "type": swagger_types.get(k, "unknown")}
            for k, v in attribute_map.items()
        ]

    try:
        sig = inspect.signature(cls.__init__)
        return [
            {"name": p.name, "type": str(p.annotation) if p.annotation != inspect.Parameter.empty else "unknown"}
            for p in sig.parameters.values()
            if p.name != "self"
        ]
    except (ValueError, TypeError):
        return []


def build_sdk_context(sdk_name: str, sdk: Any) -> str:
    """Build a detailed SDK context string for the prompt."""
    lines: List[str] = []
    lines.append(f"## SDK Package: {sdk_name}")
    lines.append(f"SDK Version: {getattr(sdk, '__version__', 'N/A')}")
    lines.append("")

    api_classes = get_api_classes(sdk)
    lines.append(f"### API Service Classes ({len(api_classes)} total)")
    for ac in api_classes:
        lines.append(f"- {ac}")
        methods = get_api_methods(sdk, ac)
        for m in methods[:30]:
            param_str = ", ".join(p["name"] for p in m["params"])
            lines.append(f"    - {m['name']}({param_str})")
    lines.append("")

    model_classes = get_model_classes(sdk)
    lines.append(f"### Model Classes ({len(model_classes)} total, showing first 50)")
    for mc in model_classes[:50]:
        fields = get_model_fields(sdk, mc)
        if fields:
            field_names = ", ".join(f["name"] for f in fields[:15])
            lines.append(f"- {mc}: [{field_names}]")
        else:
            lines.append(f"- {mc}")
    lines.append("")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _module_display_name(module_name: str) -> str:
    """ntnx_directory_services_info_v2 → directory services"""
    return (
        module_name
        .replace("ntnx_", "")
        .replace("_info_v2", "")
        .replace("_v2", "")
        .replace("_", " ")
    )


def _sdk_alias(sdk_name: str) -> str:
    """ntnx_iam_py_client → ntnx_iam"""
    return sdk_name.split("_py_")[0]


# ---------------------------------------------------------------------------
# Prompt section builders
# ---------------------------------------------------------------------------

def _section_preamble(
    sdk_name: str,
    sdk_context: str,
    v4_subdir: str,
    design_doc_content: Optional[str],
    module_count_label: str,
) -> str:
    """Shared intro: role, SDK reference, repo pointers, copyright."""
    current_year = datetime.now().year

    design_block = ""
    if design_doc_content:
        design_block = textwrap.dedent(f"""\

            ----- DESIGN DOCUMENT START -----
            {design_doc_content}
            ----- DESIGN DOCUMENT END -----
        """)

    return textwrap.dedent(f"""\
        You are an expert Ansible module developer for the Nutanix Ansible collection.
        Your task is to create {module_count_label} using the Nutanix Python SDK.
        {design_block}
        ==================== SDK REFERENCE ====================
        {sdk_context}
        ========================================================

        Refer the SDK code installed in the system (package: {sdk_name}).
        Refer to the existing modules in this repo under nutanix.ansible/plugins/modules/ — especially *_v2.py modules.
        Refer to existing helpers in nutanix.ansible/plugins/module_utils/v4/{v4_subdir}/ and the patterns in api_client.py and helpers.py there.
        Copyright should be of the current year: {current_year}.
    """)


def _section_crud(module_name: str, sdk_name: str) -> str:
    """Prompt section for the CRUD (create/update/delete) module."""
    sdk_alias = _sdk_alias(sdk_name)

    return textwrap.dedent(f"""\

        ==================== CRUD MODULE: {module_name} ====================
        Create module: {module_name}
        Version added: 2.6.0
        Author: Abhinav Bansal (@abhinavbansal29)

        Requirements:
        - Add Create, Update and Delete operations.
        - Add Idempotency and check_mode support like other v2 modules have.
        - Return params:
          * response (returned always)
          * changed (returned always)
          * ext_id (returned always)
          * task_ext_id (returned always)
          * skipped (returned when nothing to change)
          * msg (check properly where you are returning it — use for skip messages, check_mode, errors)
          * error (returned always)
          * failed (returned when something fails)
        - Make sure you check each and every parameter stated above.
        - File structure must be:
          1. Documentation (DOCUMENTATION, EXAMPLES, RETURN)
          2. All Imports
          3. get_module_spec()
          4. create_<resource>(module, result)
          5. Idempotency check method
          6. update_<resource>(module, result)
          7. delete_<resource>(module, result)
          8. run_module()
          9. main()
          Refer existing modules for the exact pattern.
        - For Update and Delete operations, don't forget to pass etag in if_match wherever applicable.
        - Use the validate_required_params method whenever needed.
        - Add this in except ImportError:
            from ..module_utils.v4.sdk_mock import mock_sdk as {sdk_alias}_sdk  # noqa: E402
            SDK_IMP_ERROR = traceback.format_exc()
        - Add this line after importing everything:
            # Suppress the InsecureRequestWarning
            warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")
        - As we need get api instance in all the methods, define it in run_module and pass to respective methods.
        - Don't add wait: True in Examples or Tests as by default it is true.
        - Don't add assertions in Examples.
        - Don't include checkmode examples in example folder and module examples.
    """)


def _section_info(module_name: str, sdk_name: str) -> str:
    """Prompt section for the info (get/list) module."""
    display = _module_display_name(module_name)
    sdk_alias = _sdk_alias(sdk_name)

    return textwrap.dedent(f"""\

        ==================== INFO MODULE: {module_name} ====================
        Create module: {module_name}
        This is an info module.
        Version added: 2.6.0
        Author: Abhinav Bansal (@abhinavbansal29)

        Requirements:
        - Description of response should be like this:
            - The response from the Nutanix PC {display} info v4 API.
            - It can be a single {display} if external ID is provided.
            - List of multiple {display} if external ID is not provided.
          Type is dict always.
        - Return params:
          * response (returned always)
          * changed (returned always)
          * ext_id (returned when single entity is fetched)
          * msg (check properly where you are returning it)
          * error (returned always)
          * failed (returned when something fails)
        - In listing method, use this snippet:
            total_available_results = resp.metadata.total_available_results
            result["total_available_results"] = total_available_results
            resp = strip_internal_attributes(resp.to_dict()).get("data")
            if not resp:
                resp = []
            result["response"] = resp
        - Add this in except ImportError:
            from ..module_utils.v4.sdk_mock import mock_sdk as {sdk_alias}_sdk  # noqa: E402
            SDK_IMP_ERROR = traceback.format_exc()
        - Add this line after importing everything:
            # Suppress the InsecureRequestWarning
            warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")
    """)


def _section_helpers(v4_subdir: str) -> str:
    return textwrap.dedent(f"""\

        ==================== HELPERS & API CLIENT ====================
        - Create or update helpers in nutanix.ansible/plugins/module_utils/v4/{v4_subdir}/helpers.py
        - Create or update API client functions in nutanix.ansible/plugins/module_utils/v4/{v4_subdir}/api_client.py
        - Use the existing helpers and libraries and create wherever required.
        - Write proper docstrings in api clients or any helper methods, refer other helpers for this.
    """)


def _section_examples(pc_ip: str, module_names: List[str], has_crud: bool) -> str:
    modules_label = " and ".join(module_names)
    crud_note = ""
    if has_crud:
        crud_note = (
            "- Don't include checkmode examples in example folder and module examples.\n"
            "        - Don't add wait: True in Examples as by default it is true.\n"
            "        - Don't add assertions in Examples."
        )

    return textwrap.dedent(f"""\

        ==================== EXAMPLES ====================
        - Write detailed Examples in the nutanix.ansible/examples/ folder, in just 1 file covering {modules_label}.
        - Make sure examples are running. PC IP for running: {pc_ip}, Username: admin, Password: Nutanix.123
        - Create a separate file where I can see the logs of successfully running Examples.
        - For response samples: If you can run any example and get the results then add in sample.
          If example fails for you, then just add "<Need to add sample>".
        {crud_note}
    """)


def _section_tests(has_crud: bool, has_info: bool) -> str:
    crud_tests = ""
    if has_crud:
        crud_tests = textwrap.dedent("""\
            - Tests should have a check_mode test where each and every field should be tested for all Create, Update and Delete.
            - Test for all the operations and required fields.
        """)
    info_tests = ""
    if has_info:
        info_tests = textwrap.dedent("""\
            - Test get-by-ext_id and list operations for the info module.
        """)

    return textwrap.dedent(f"""\

        ==================== TESTS ====================
        - Write full tests in just 1 file under nutanix.ansible/tests/integration/targets/.
        {crud_tests}{info_tests}\
        - Add negative scenarios. Add assertions for the failed message. First run the test and then add assertions.
        - Add assertions for changed and failed in every test before asserting anything else.
        - Add proper assertions for all the tests, including the check mode tests.
        - For loops, add proper assertion for every element in the loop.
        - Refer other tests file and see how we are doing testing earlier.
        - Make sure you run the tests and all tests should be running. Store the test logs in a file.
    """)


def _section_quality() -> str:
    return textwrap.dedent("""\

        ==================== CODE QUALITY ====================
        - Write clean code with full documentation.
        - Make sure black, isort, flake8, ansible-lint and ansible sanity passes. Run and check.
    """)


def _section_reminders(sdk_name: str) -> str:
    return textwrap.dedent(f"""\

        ==================== IMPORTANT REMINDERS ====================
        - Refer the SDK source code in the installed packages for exact class names, method signatures, and model fields.
        - Use the existing patterns in this repository — do NOT invent new patterns.
        - The SDK package to import is: {sdk_name}
        - All API methods, model classes, and field names must match the SDK exactly.
    """)


# ---------------------------------------------------------------------------
# Prompt assembly
# ---------------------------------------------------------------------------

def build_prompt(
    namespace: str,
    sdk_name: str,
    sdk_context: str,
    crud_module: Optional[str],
    info_module: Optional[str],
    pc_ip: str,
    design_doc_content: Optional[str],
) -> str:
    """Assemble the full prompt from composable sections."""
    v4_subdir = V4_DIR_MAP.get(namespace.lower(), namespace.lower())

    has_crud = crud_module is not None
    has_info = info_module is not None

    if has_crud and has_info:
        count_label = "two Ansible modules (a CRUD module and an info module)"
    elif has_crud:
        count_label = "one Ansible CRUD module (Create, Update, Delete)"
    else:
        count_label = "one Ansible info module (Get / List)"

    parts: List[str] = []

    # 1. Preamble (always)
    parts.append(_section_preamble(sdk_name, sdk_context, v4_subdir, design_doc_content, count_label))

    # 2. Module-specific sections (conditional)
    if has_crud:
        parts.append(_section_crud(crud_module, sdk_name))
    if has_info:
        parts.append(_section_info(info_module, sdk_name))

    # 3. Helpers & API client (always)
    parts.append(_section_helpers(v4_subdir))

    # 4. Examples
    module_names = [m for m in [crud_module, info_module] if m]
    parts.append(_section_examples(pc_ip, module_names, has_crud))

    # 5. Tests
    parts.append(_section_tests(has_crud, has_info))

    # 6. Code quality (always)
    parts.append(_section_quality())

    # 7. Reminders (always)
    parts.append(_section_reminders(sdk_name))

    return "\n".join(parts)


# ---------------------------------------------------------------------------
# Cursor invocation
# ---------------------------------------------------------------------------

def find_agent_cli() -> Optional[str]:
    """Locate the standalone ``agent`` CLI binary (NOT the IDE ``cursor`` binary)."""
    agent_path = shutil.which("agent")
    if agent_path:
        return agent_path

    home = Path.home()
    candidates = [
        home / ".cursor" / "bin" / "agent",
        home / ".local" / "bin" / "agent",
        Path("/usr/local/bin/agent"),
    ]
    for c in candidates:
        if c.exists() and os.access(str(c), os.X_OK):
            return str(c)

    return None


def find_cursor_ide_cli() -> Optional[str]:
    """Locate the Cursor IDE ``cursor`` CLI (opens files in the running IDE)."""
    return shutil.which("cursor")


def save_prompt_to_file(prompt: str, output_path: str) -> None:
    """Save the generated prompt to a file for reference or manual use."""
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(prompt)
    print(f"Prompt saved to: {output_path}")


def invoke_agent_interactive(prompt_file: str, workspace: str) -> None:
    """
    Replace the current process with an interactive ``agent`` session,
    passing the prompt file as context via ``@`` reference.

    Uses ``os.execvp`` so the terminal seamlessly transitions from the
    Python script into the live agent session — no manual copy-paste needed.

    If the ``agent`` binary is not found, falls back to opening the prompt
    file in the current Cursor IDE window with manual instructions.
    """
    agent_bin = find_agent_cli()

    if agent_bin:
        abs_prompt = str(Path(prompt_file).resolve())
        initial_msg = (
            f"Read and follow every instruction in @{abs_prompt} — "
            "generate all requested Ansible modules, tests, and examples."
        )
        print(f"\nStarting interactive agent session ...")
        print(f"  Agent  : {agent_bin}")
        print(f"  Prompt : {abs_prompt}")
        print(f"  Workspace: {workspace}\n")
        os.execvp(
            agent_bin,
            [
                agent_bin,
                "--model", "claude-4.6-opus-high-thinking",
                "--workspace", workspace,
                initial_msg,
            ],
        )
        # execvp replaces the process; code below only runs on failure
        sys.exit("ERROR: os.execvp failed")

    # --- Fallback: agent not installed ---
    print(
        "\nWARNING: Standalone 'agent' CLI not found.\n"
        "Install it for the best experience (one-time setup):\n"
        "  curl -fsSL https://cursor.com/install | bash\n",
        file=sys.stderr,
    )

    cursor_bin = find_cursor_ide_cli()
    if cursor_bin:
        cmd = [cursor_bin, "--reuse-window", prompt_file]
        print(f"Falling back: opening prompt file in Cursor IDE ...")
        try:
            subprocess.run(cmd, check=True, timeout=10)
        except (subprocess.CalledProcessError, subprocess.TimeoutExpired) as exc:
            print(f"WARNING: Could not open file in Cursor: {exc}", file=sys.stderr)

    print(
        f"\nPrompt saved to: {prompt_file}\n"
        "To start the agent manually, run:\n"
        f"  agent --model claude-4.6-opus-high-thinking --workspace {workspace} "
        f"\"Read and follow every instruction in @{prompt_file}\"\n"
    )


def invoke_agent_headless(prompt_file: str, workspace: str, output_log: str) -> int:
    """
    Run the standalone Cursor Agent CLI in headless mode, piping the
    prompt via stdin (avoids shell argument-length limits).

    Returns the process exit code.
    """
    agent_bin = find_agent_cli()
    if not agent_bin:
        return None  # signal that agent CLI is unavailable

    cmd = [
        agent_bin,
        "-p",
        "--force",
        "--model", "claude-4.6-opus-high-thinking",
        "--workspace", workspace,
    ]

    env = os.environ.copy()
    if not env.get("CURSOR_API_KEY"):
        print(
            "WARNING: CURSOR_API_KEY is not set. The agent CLI may require it for headless mode.\n"
            "Set it with:  export CURSOR_API_KEY=<your-key>",
            file=sys.stderr,
        )

    print(f"\n{'='*70}")
    print("Invoking Cursor Agent CLI (headless)")
    print(f"Binary     : {agent_bin}")
    print(f"Workspace  : {workspace}")
    print(f"Prompt file: {prompt_file}")
    print(f"Log file   : {output_log}")
    print(f"{'='*70}\n")

    prompt_text = Path(prompt_file).read_text(encoding="utf-8")

    with open(output_log, "w", encoding="utf-8") as log_f:
        log_f.write("=== Cursor Agent Invocation Log ===\n")
        log_f.write(f"Timestamp: {datetime.now().isoformat()}\n")
        log_f.write(f"Binary: {agent_bin}\n")
        log_f.write(f"Workspace: {workspace}\n")
        log_f.write(f"Prompt file: {prompt_file}\n\n")
        log_f.write("=== Agent Output ===\n")
        log_f.flush()

        proc = subprocess.Popen(
            cmd,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            env=env,
            cwd=workspace,
            text=True,
        )

        proc.stdin.write(prompt_text)
        proc.stdin.close()

        for line in proc.stdout:
            sys.stdout.write(line)
            sys.stdout.flush()
            log_f.write(line)
            log_f.flush()

        proc.wait()

        log_f.write(f"\n=== Exit Code: {proc.returncode} ===\n")

    print(f"\nAgent finished with exit code {proc.returncode}")
    print(f"Full log saved to: {output_log}")
    return proc.returncode


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate Ansible modules by introspecting Nutanix SDKs and invoking Cursor Agent CLI.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent("""\
            Examples:
              # Default — starts interactive agent session with the prompt
              python generate_ansible_modules.py iam --crud ntnx_directory_services_v2 --info ntnx_directory_services_info_v2 --pc-ip 10.0.0.1

              # Only CRUD
              python generate_ansible_modules.py vmm --crud ntnx_vms_v2 --pc-ip 10.0.0.1

              # Only info
              python generate_ansible_modules.py vmm --info ntnx_vms_info_v2 --pc-ip 10.0.0.1

              # Headless: non-interactive (logs output, no user interaction)
              python generate_ansible_modules.py vmm --crud ntnx_vms_v2 --pc-ip 10.0.0.1 --headless

              # Prompt only (no Cursor invocation)
              python generate_ansible_modules.py networking --crud ntnx_subnets_v2 --info ntnx_subnets_info_v2 --pc-ip 10.0.0.1 --prompt-only

              # With design doc
              python generate_ansible_modules.py iam --crud ntnx_roles_v2 --info ntnx_roles_info_v2 --pc-ip 10.0.0.1 --design-doc design.md
        """),
    )

    parser.add_argument(
        "namespace",
        help="SDK namespace (e.g. vmm, iam, networking, volumes, ...)",
    )

    module_group = parser.add_argument_group(
        "module selection",
        "Specify which module(s) to generate. At least one of --crud or --info is required.",
    )
    module_group.add_argument(
        "--crud",
        metavar="MODULE_NAME",
        default=None,
        help="Generate a CRUD module (create/update/delete). Example: ntnx_vms_v2",
    )
    module_group.add_argument(
        "--info",
        metavar="MODULE_NAME",
        default=None,
        help="Generate an info module (get/list). Example: ntnx_vms_info_v2",
    )

    parser.add_argument(
        "--pc-ip",
        required=True,
        dest="pc_ip",
        help="Prism Central IP for running examples/tests",
    )
    parser.add_argument(
        "--design-doc",
        dest="design_doc",
        default=None,
        help="Path to design document file",
    )
    mode_group = parser.add_argument_group(
        "invocation mode",
        "Control how the prompt is delivered to Cursor.",
    )
    mode_exclusive = mode_group.add_mutually_exclusive_group()
    mode_exclusive.add_argument(
        "--prompt-only",
        action="store_true",
        help="Only generate and save the prompt file; do not invoke Cursor at all.",
    )
    mode_exclusive.add_argument(
        "--headless",
        action="store_true",
        help=(
            "Run the 'agent' CLI in non-interactive mode (output logged to file, "
            "requires 'agent' installed and CURSOR_API_KEY set). "
            "By default the script starts an interactive agent session."
        ),
    )

    parser.add_argument(
        "--output-dir",
        default=None,
        help="Directory to store generated logs and prompt (default: repo root)",
    )

    args = parser.parse_args()

    # --- Validate: at least one module type selected ---
    if not args.crud and not args.info:
        parser.error("At least one of --crud or --info is required.")

    output_dir = Path(args.output_dir) if args.output_dir else REPO_ROOT
    output_dir.mkdir(parents=True, exist_ok=True)

    primary_module = args.crud or args.info

    # --- Step 1: Discover and introspect SDK ---
    print(f"[1/4] Discovering SDK for namespace '{args.namespace}' ...")
    sdk_name, sdk = discover_sdk(args.namespace)
    print(f"       Found SDK: {sdk_name} (version {getattr(sdk, '__version__', 'N/A')})")

    api_classes = get_api_classes(sdk)
    model_classes = get_model_classes(sdk)
    print(f"       API classes : {len(api_classes)}")
    print(f"       Model classes: {len(model_classes)}")

    # --- Step 2: Build SDK context ---
    print("[2/4] Building SDK context for prompt ...")
    sdk_context = build_sdk_context(sdk_name, sdk)

    # --- Step 3: Read design doc if provided ---
    design_doc_content = None
    if args.design_doc:
        design_path = Path(args.design_doc)
        if not design_path.exists():
            sys.exit(f"Design doc not found: {design_path}")
        design_doc_content = design_path.read_text(encoding="utf-8")
        print(f"       Design doc loaded: {design_path} ({len(design_doc_content)} chars)")

    # --- Step 4: Build the prompt ---
    generating = []
    if args.crud:
        generating.append(f"CRUD → {args.crud}")
    if args.info:
        generating.append(f"INFO → {args.info}")
    print(f"[3/4] Building prompt for: {', '.join(generating)} ...")

    prompt = build_prompt(
        namespace=args.namespace,
        sdk_name=sdk_name,
        sdk_context=sdk_context,
        crud_module=args.crud,
        info_module=args.info,
        pc_ip=args.pc_ip,
        design_doc_content=design_doc_content,
    )

    prompt_file = output_dir / f"generated_prompt_{primary_module}.md"
    save_prompt_to_file(prompt, str(prompt_file))

    # --- Step 5: Deliver the prompt ---
    if args.prompt_only:
        print("\n--prompt-only flag set. Skipping agent invocation.")
        print("You can use the prompt manually:")
        abs_pf = str(prompt_file.resolve())
        print(
            f'  1. Interactive:  agent --model claude-4.6-opus-high-thinking --workspace {REPO_ROOT} '
            f'"Read and follow every instruction in @{abs_pf}"'
        )
        print(f"  2. Headless:     agent -p --force --model claude-4.6-opus-high-thinking --workspace {REPO_ROOT} < {abs_pf}")
        return

    if args.headless:
        # --- Headless: standalone agent CLI ---
        print("[4/4] Invoking standalone Cursor Agent CLI (headless) ...")
        log_file = output_dir / f"cursor_agent_log_{primary_module}.txt"
        exit_code = invoke_agent_headless(
            prompt_file=str(prompt_file),
            workspace=str(REPO_ROOT),
            output_log=str(log_file),
        )
        if exit_code is None:
            print(
                "ERROR: Standalone 'agent' CLI not found.\n"
                "Install it:  curl https://cursor.com/install -fsS | bash\n"
                "Or omit --headless to open the prompt in your current Cursor window.",
                file=sys.stderr,
            )
            sys.exit(1)
        if exit_code == 0:
            print("\nModule generation completed successfully!")
            print("Check the following locations:")
            print(f"  Modules : {COLLECTION_ROOT / 'plugins' / 'modules'}/")
            print(f"  Utils   : {COLLECTION_ROOT / 'plugins' / 'module_utils' / 'v4'}/")
            print(f"  Examples: {COLLECTION_ROOT / 'examples'}/")
            print(f"  Tests   : {COLLECTION_ROOT / 'tests' / 'integration' / 'targets'}/")
        else:
            print(f"\nAgent exited with code {exit_code}. Check: {log_file}", file=sys.stderr)
        sys.exit(exit_code)

    # --- Default: launch interactive agent session ---
    print("[4/4] Launching interactive agent session ...")
    invoke_agent_interactive(
        prompt_file=str(prompt_file),
        workspace=str(REPO_ROOT),
    )


if __name__ == "__main__":
    main()
