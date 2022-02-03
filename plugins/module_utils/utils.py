# This file is part of Ansible
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type


def remove_param_with_none_value(d):
    for k, v in d.copy().items():
        if v is None:
            d.pop(k)
        elif isinstance(v, dict):
            remove_param_with_none_value(v)
        elif isinstance(v, list):
            for e in v:
                if isinstance(e, dict):
                    remove_param_with_none_value(e)
                break


def validate_spec_disks(vdisks):
    for vdisk in vdisks:
        if (
            vdisk.get("type") == "CDROM"
            and vdisk.get("size_gb")
            and not vdisk.get("clone_image")
        ):
            return True, "Size can't not be specfied for empty CDROM"
    return False, ""


def validate_spec_vcpus(value):
    if value < 1 or value > 99:
        return True, "Vcpus can't  be less than 0 or greater than 99"
    else:
        return False, ""


def validate_spec_cores(value):
    if value < 1 or value > 99:
        return True, "Cores per vcpu can't be less than 0 or greater than 99"
    else:
        return False, ""


validiate_spec_methods = {
    "disks": validate_spec_disks,
    "vcpus": validate_spec_vcpus,
    "cores_per_vcpu": validate_spec_cores,
}


def validate_spec(spec):
    for ansible_param, ansible_value in spec.items():
        validiate_spec_method = validiate_spec_methods.get(ansible_param)
        if validiate_spec_method and ansible_value:
            error, msg = validiate_spec_method(ansible_value)
            if error:
                return error, msg
    return False, ""
