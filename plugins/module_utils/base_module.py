# Copyright: 2021, Ansible Project
# Simplified BSD License (see licenses/simplified_bsd.txt or https://opensource.org/licenses/BSD-2-Clause )
from __future__ import absolute_import, division, print_function

from copy import deepcopy

from ansible.module_utils.basic import AnsibleModule, env_fallback

__metaclass__ = type


class BaseModule(AnsibleModule):
    """Basic module with common arguments"""

    unsupported_spec_keys = ["obj"]
    argument_spec = dict(
        nutanix_host=dict(
            type="str", fallback=(env_fallback, ["NUTANIX_HOST"]), required=True
        ),
        nutanix_port=dict(
            default="9440", type="str", fallback=(env_fallback, ["NUTANIX_PORT"])
        ),
        nutanix_username=dict(
            type="str", fallback=(env_fallback, ["NUTANIX_USERNAME"]), required=True
        ),
        nutanix_password=dict(
            type="str",
            no_log=True,
            fallback=(env_fallback, ["NUTANIX_PASSWORD"]),
            required=True,
        ),
        validate_certs=dict(
            type="bool", default=True, fallback=(env_fallback, ["VALIDATE_CERTS"])
        ),
        state=dict(type="str", choices=["present", "absent"], default="present"),
        wait=dict(type="bool", default=True),
        enable_debug_logging=dict(
            type="bool", default=False, fallback=(env_fallback, ["NUTANIX_DEBUG"])
        ),
    )

    def __init__(self, **kwargs):
        argument_spec = deepcopy(self.argument_spec)
        if kwargs.get("argument_spec"):
            argument_spec.update(deepcopy(kwargs["argument_spec"]))
        self.argument_spec_with_extra_keys = deepcopy(argument_spec)
        self.strip_extra_attributes(argument_spec)
        kwargs["argument_spec"] = argument_spec

        if not kwargs.get("supports_check_mode"):
            kwargs["supports_check_mode"] = True

        super(BaseModule, self).__init__(**kwargs)

    def strip_extra_attributes(self, argument_spec):
        """
        This recursive method checks argument spec and remove extra spec definations which are not allowed in ansible
        """
        for spec in argument_spec.values():
            for k in self.unsupported_spec_keys:
                spec.pop(k, None)
            if spec.get("options"):
                self.strip_extra_attributes(spec["options"])
