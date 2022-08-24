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


def strip_extra_attrs(spec1, spec2):
    for k, v in spec1.copy().items():
        if k not in spec2:
            spec1.pop(k)
        elif isinstance(v, dict):
            strip_extra_attrs(spec1[k], spec2[k])
        elif isinstance(v, list) and v and isinstance(v[0], dict):
            for i in range(len(v)):
                try:
                    strip_extra_attrs(spec1[k][i], spec2[k][i])
                except IndexError:
                    spec1[k] = spec2[k]
                    break


def check_for_idempotency(spec, resp, **kwargs):
    state = kwargs.get("state")
    if spec == resp:
        if (
            state == "present"
            # only for VMs
            or (
                state in ["soft_shutdown", "hard_poweroff", "power_off"]
                and resp["spec"]["resources"]["power_state"] == "OFF"
            )
            # only for VMs
            or (
                state == "power_on" and resp["spec"]["resources"]["power_state"] == "ON"
            )
        ):
            return True
    return False


def intersection(first_obj, second_obj):
    if isinstance(first_obj, dict):
        for key, value in first_obj.items():
            if key in second_obj and second_obj[key] == value:
                second_obj.pop(key)
            if isinstance(value, (dict, list)):
                intersection(value, second_obj)
        if not second_obj:
            return True
    elif isinstance(first_obj, list):
        for item in first_obj:
            intersection(item, second_obj)
    return False

def convert_to_secs(value, unit):
    """
    This routine converts given value to time interval into seconds as per unit
    """
    conversion_multiplier = {
        "MINUTE": 60,
        "HOUR": 3600,
        "DAY": 86400,
        "WEEK": 604800,
    }
    if unit not in conversion_multiplier:
        return None, "Invalid unit given for interval conversion to seconds"

    return value * conversion_multiplier[unit], None