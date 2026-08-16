# Copyright: (c) 2024, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

from ..utils import raise_api_exception  # noqa: E402


def get_vm(module, api_instance, ext_id):
    """
    Get VM by ext_id
    Args:
        module: Ansible module
        api_instance: VmApi instance from ntnx_vmm_py_client sdk
        ext_id: ext_id of VM
    Returns:
        vm (obj): VM info object
    """
    try:
        return api_instance.get_vm_by_id(extId=ext_id).data
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching Vms info using ext_id",
        )


def get_nic(module, api_instance, ext_id, vm_ext_id):
    """
    Get NIC by ext_id
    Args:
        module: Ansible module
        api_instance: VmApi instance from ntnx_vmm_py_client sdk
        ext_id: ext_id of NIC
        vm_ext_id: ext_id of VM
    Returns:
        nic (obj): NIC info object
    """
    try:
        return api_instance.get_nic_by_id(vmExtId=vm_ext_id, extId=ext_id).data
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching vm nic info using ext_id",
        )


def get_ngt_status(module, api_instance, vm_ext_id):
    """
    Get NGT info by vm ext_id
    Args:
        module: Ansible module
        api_instance: VmApi instance from ntnx_vmm_py_client sdk
        vm_ext_id: ext_id of VM
    Returns:
        ngt (obj): NGT info object
    """
    try:
        return api_instance.get_guest_tools_by_id(extId=vm_ext_id).data
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching NGT info for given vm",
        )


def get_disk(module, api_instance, ext_id, vm_ext_id):
    """
    Get Disk by ext_id
    Args:
        module: Ansible module
        api_instance: VmApi instance from ntnx_vmm_py_client sdk
        ext_id: ext_id of Disk
        vm_ext_id: ext_id of VM
    Returns:
        disk (obj): Disk info object
    """
    try:
        return api_instance.get_disk_by_id(vmExtId=vm_ext_id, extId=ext_id).data
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching vm disk info using ext_id",
        )


def get_serial_port(module, api_instance, ext_id, vm_ext_id):
    """
    Get Serial Port by ext_id
    Args:
        module: Ansible module
        api_instance: VmApi instance from ntnx_vmm_py_client sdk
        ext_id: ext_id of Serial Port
        vm_ext_id: ext_id of VM
    Returns:
        serial_port (obj): Serial Port info object
    """
    try:
        return api_instance.get_serial_port_by_id(vmExtId=vm_ext_id, extId=ext_id).data
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching vm serial port info using ext_id",
        )


def get_template(module, api_instance, ext_id):
    """
    Get Template by ext_id
    Args:
        module: Ansible module
        api_instance: VmApi instance from ntnx_vmm_py_client sdk
        ext_id: ext_id of Template
    Returns:
        template (obj): Template info object
    """
    try:
        return api_instance.get_template_by_id(extId=ext_id).data
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching template info using ext_id",
        )


def get_cd_rom(module, api_instance, ext_id, vm_ext_id):
    """
    Get CD ROM by ext_id
    Args:
        module: Ansible module
        api_instance: VmApi instance from ntnx_vmm_py_client sdk
        ext_id: ext_id of CD ROM
        vm_ext_id: ext_id of VM
    Returns:
        cd_rom (obj): CD ROM info object
    """
    try:
        return api_instance.get_cd_rom_by_id(vmExtId=vm_ext_id, extId=ext_id).data
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching vm cd rom info using ext_id",
        )


def get_gpu(module, api_instance, ext_id, vm_ext_id):
    """
    Get GPU by ext_id
    Args:
        module: Ansible module
        api_instance: VmApi instance from ntnx_vmm_py_client sdk
        ext_id: ext_id of GPU
        vm_ext_id: ext_id of VM
    Returns:
        gpu (obj): GPU info object
    """
    try:
        return api_instance.get_gpu_by_id(vmExtId=vm_ext_id, extId=ext_id).data
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching GPU info using ext_id",
        )


def get_ova(module, api_instance, ext_id):
    """
    Get OVA by ext_id
    Args:
        module: Ansible module
        api_instance: OvasApi instance from ntnx_vmm_py_client sdk
        ext_id: ext_id of OVA
    Returns:
        ova (obj): OVA info object
    """
    try:
        return api_instance.get_ova_by_id(extId=ext_id).data
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching OVA info using ext_id",
        )


def list_vm_host_affinity_policy_vm_compliance_states(
    module, api_instance, vm_host_affinity_policy_ext_id, page=None, limit=None
):
    """
    List the VM compliance states associated with a VM-Host Affinity policy.

    The v4 SDK exposes only a paginated list endpoint for compliance state
    entries; there is no dedicated GetById counterpart. Callers can iterate
    the result client-side to find a single entry by ``ext_id``.

    Args:
        module: Ansible module (used to raise a descriptive failure).
        api_instance: VmHostAffinityPoliciesApi instance from ntnx_vmm_py_client.
        vm_host_affinity_policy_ext_id (str): ext_id of the parent VM-Host
            Affinity policy whose compliance states must be listed.
        page (int | None): Optional 0-indexed page number.
        limit (int | None): Optional page size (SDK caps this at 100).

    Returns:
        obj: The full v4 SDK response object
        (``ListVmHostAffinityPolicyVmComplianceStatesApiResponse``).
    """
    kwargs = {}
    if page is not None:
        kwargs["_page"] = page
    if limit is not None:
        kwargs["_limit"] = limit
    try:
        return api_instance.list_vm_host_affinity_policy_vm_compliance_states(
            vmHostAffinityPolicyExtId=vm_host_affinity_policy_ext_id, **kwargs
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg=(
                "Api Exception raised while fetching VM host affinity policy "
                "VM compliance states"
            ),
        )


def get_vm_host_affinity_policy_vm_compliance_state(
    module, api_instance, vm_host_affinity_policy_ext_id, ext_id
):
    """
    Fetch a single VmHostAffinityPolicyVmComplianceState entry by iterating
    the list endpoint (the SDK has no GetById for this entity).

    Args:
        module: Ansible module.
        api_instance: VmHostAffinityPoliciesApi instance.
        vm_host_affinity_policy_ext_id (str): ext_id of the parent policy.
        ext_id (str): ext_id of the desired compliance state entry.

    Returns:
        obj | None: The matching SDK compliance state entry, or ``None`` when
        no compliance state on the policy has the provided ``ext_id``.
    """
    page = 0
    limit = 100
    while True:
        resp = list_vm_host_affinity_policy_vm_compliance_states(
            module,
            api_instance,
            vm_host_affinity_policy_ext_id,
            page=page,
            limit=limit,
        )
        entries = resp.data or []
        for entry in entries:
            if getattr(entry, "ext_id", None) == ext_id:
                return entry
        if len(entries) < limit:
            return None
        page += 1
