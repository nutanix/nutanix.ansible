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


def strip_extra_attrs_from_status(status, spec):
    for k, v in status.copy().items():
        if k not in spec:
            status.pop(k)
        elif isinstance(v, dict):
            strip_extra_attrs_from_status(status[k], spec[k])
        elif isinstance(v, list) and v and isinstance(v[0], dict):
            for i in range(len(v)):
                try:
                    strip_extra_attrs_from_status(status[k][i], spec[k][i])
                except IndexError:
                    status[k] = spec[k]
                    break


def check_for_idempotency(spec, resp, **kwargs):
    state = kwargs.get("state")
    if spec == resp:
        if (
            state == "present"
            or (
                state in ["soft_shutdown", "hard_poweroff", "power_off"]
                and resp["spec"]["resources"]["power_state"] == "OFF"
            )
            or (
                state == "power_on" and resp["spec"]["resources"]["power_state"] == "ON"
            )
        ):
            return True
    return False
