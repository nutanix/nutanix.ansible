# Copyright: 2021, Ansible Project
# Simplified BSD License (see licenses/simplified_bsd.txt or https://opensource.org/licenses/BSD-2-Clause )
from __future__ import absolute_import, division, print_function

from ansible.module_utils.basic import AnsibleModule, env_fallback

__metaclass__ = type


class BaseModule(AnsibleModule):
    """Basic module with common arguments"""

    argument_spec = dict(
        nutanix_host=dict(
            type="str",
            fallback=(env_fallback, ["NUTANIX_HOST"]),
            required=True,
        ),
        nutanix_port=dict(
            default="9440", type="str", fallback=(env_fallback, ["NUTANIX_PORT"])
        ),
        nutanix_username=dict(
            type="str",
            fallback=(env_fallback, ["NUTANIX_USERNAME"]),
            required=True,
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
    )

    def __init__(self, **kwargs):
        if kwargs.get("argument_spec"):
            kwargs["argument_spec"].update(self.argument_spec)
        else:
            kwargs["argument_spec"] = self.argument_spec

        if not kwargs.get("supports_check_mode"):
            kwargs["supports_check_mode"] = True

        super(BaseModule, self).__init__(**kwargs)
