# Copyright: 2021, Ansible Project
# Simplified BSD License (see licenses/simplified_bsd.txt or https://opensource.org/licenses/BSD-2-Clause )
from __future__ import absolute_import, division, print_function

from ansible.module_utils.basic import AnsibleModule, env_fallback

__metaclass__ = type


class EraBaseModule(AnsibleModule):
    argument_spec = dict(
        era_host=dict(type="str", required=True, fallback=(env_fallback, ["ERA_HOST"])),
        era_username=dict(
            type="str", fallback=(env_fallback, ["ERA_USERNAME"]), required=True
        ),
        era_password=dict(
            type="str",
            no_log=True,
            fallback=(env_fallback, ["ERA_PASSWORD"]),
            required=True,
        ),
        validate_certs=dict(
            type="bool", default=True, fallback=(env_fallback, ["VALIDATE_CERTS"])
        ),
        state=dict(type="str", choices=["present", "absent"], default="present"),
        timeout=dict(type="int", required=False, default=60),
        wait=dict(type="bool", default=True),
    )

    def __init__(self, **kwargs):
        if kwargs.get("argument_spec"):
            kwargs["argument_spec"].update(self.argument_spec)
        else:
            kwargs["argument_spec"] = self.argument_spec

        if not kwargs.get("supports_check_mode"):
            kwargs["supports_check_mode"] = True

        super(EraBaseModule, self).__init__(**kwargs)
