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


def get_esxi_vm_stats(
    module,
    api_instance,
    ext_id,
    start_time,
    end_time,
    sampling_interval=None,
    stat_type=None,
    select=None,
):
    """
    Get ESXi VM stats by VM ext_id.

    Args:
        module: Ansible module
        api_instance: EsxiStatsApi instance from ntnx_vmm_py_client sdk
        ext_id: ext_id of ESXi VM
        start_time: ISO-8601 start time
        end_time: ISO-8601 end time
        sampling_interval: sampling interval in seconds
        stat_type: down-sampling operator (SUM/AVG/...)
        select: OData $select projection

    Returns:
        response: raw SDK response object
    """
    try:
        return api_instance.get_vm_stats_by_id(
            extId=ext_id,
            _startTime=start_time,
            _endTime=end_time,
            _samplingInterval=sampling_interval,
            _statType=stat_type,
            _select=select,
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching ESXi VM stats using ext_id",
        )


def get_esxi_vm_disk_stats(
    module,
    api_instance,
    vm_ext_id,
    ext_id,
    start_time,
    end_time,
    sampling_interval=None,
    stat_type=None,
    select=None,
):
    """
    Get ESXi VM disk stats by VM ext_id and disk ext_id.

    Args:
        module: Ansible module
        api_instance: EsxiStatsApi instance from ntnx_vmm_py_client sdk
        vm_ext_id: ext_id of the parent ESXi VM
        ext_id: ext_id of the ESXi VM disk

    Returns:
        response: raw SDK response object
    """
    try:
        return api_instance.get_disk_stats_by_id(
            vmExtId=vm_ext_id,
            extId=ext_id,
            _startTime=start_time,
            _endTime=end_time,
            _samplingInterval=sampling_interval,
            _statType=stat_type,
            _select=select,
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching ESXi VM disk stats using ext_id",
        )


def get_esxi_vm_nic_stats(
    module,
    api_instance,
    vm_ext_id,
    ext_id,
    start_time,
    end_time,
    sampling_interval=None,
    stat_type=None,
    select=None,
):
    """
    Get ESXi VM NIC stats by VM ext_id and NIC ext_id.

    Args:
        module: Ansible module
        api_instance: EsxiStatsApi instance from ntnx_vmm_py_client sdk
        vm_ext_id: ext_id of the parent ESXi VM
        ext_id: ext_id of the ESXi VM NIC

    Returns:
        response: raw SDK response object
    """
    try:
        return api_instance.get_nic_stats_by_id(
            vmExtId=vm_ext_id,
            extId=ext_id,
            _startTime=start_time,
            _endTime=end_time,
            _samplingInterval=sampling_interval,
            _statType=stat_type,
            _select=select,
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching ESXi VM NIC stats using ext_id",
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
