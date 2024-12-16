# This file is part of Ansible
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type


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
