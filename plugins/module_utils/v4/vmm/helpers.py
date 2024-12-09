from __future__ import absolute_import, division, print_function

__metaclass__ = type

from ..utils import raise_api_exception  # noqa: E402


def get_vm(module, api_instance, ext_id):
    try:
        return api_instance.get_vm_by_id(extId=ext_id).data
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching Vms info using ext_id",
        )


def get_nic(module, api_instance, ext_id, vm_ext_id):
    try:
        return api_instance.get_nic_by_id(vmExtId=vm_ext_id, extId=ext_id).data
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching vm nic info using ext_id",
        )


def get_ngt_status(module, api_instance, vm_ext_id):
    try:
        return api_instance.get_guest_tools_by_id(extId=vm_ext_id).data
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching NGT info for given vm",
        )


def get_disk(module, api_instance, ext_id, vm_ext_id):
    try:
        return api_instance.get_disk_by_id(vmExtId=vm_ext_id, extId=ext_id).data
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching vm disk info using ext_id",
        )


def get_serial_port(module, api_instance, ext_id, vm_ext_id):
    try:
        return api_instance.get_serial_port_by_id(vmExtId=vm_ext_id, extId=ext_id).data
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching vm serial port info using ext_id",
        )


def get_template(module, api_instance, ext_id):
    try:
        return api_instance.get_template_by_id(extId=ext_id).data
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching template info using ext_id",
        )


def get_cd_rom(module, api_instance, ext_id, vm_ext_id):
    try:
        return api_instance.get_cd_rom_by_id(vmExtId=vm_ext_id, extId=ext_id).data
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching vm cd rom info using ext_id",
        )


def get_gpu(module, api_instance, ext_id, vm_ext_id):
    try:
        return api_instance.get_gpu_by_id(vmExtId=vm_ext_id, extId=ext_id).data
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching GPU info using ext_id",
        )
