# Copyright: 2021, Ansible Project
# Simplified BSD License (see licenses/simplified_bsd.txt or https://opensource.org/licenses/BSD-2-Clause )
from __future__ import absolute_import, division, print_function

from ansible.module_utils.basic import AnsibleModule

__metaclass__ = type


class BaseModule(AnsibleModule):
    """Basic module with common arguments"""

    argument_spec = dict(
        action=dict(type="str", required=True, aliases=["state"]),
        auth=dict(type="dict", required=True),
        data=dict(type="dict", required=False),
        operations=dict(type="list", required=False),
        wait=dict(type="bool", required=False, default=True),
        wait_timeout=dict(type="int", required=False, default=300),
        validate_certs=dict(type="bool", required=False, default=False),
    )

    def __init__(self, **kwargs):
        if not kwargs.get("argument_spec"):
            kwargs["argument_spec"] = self.argument_spec
        else:
            kwargs["argument_spec"].update(self.argument_spec)
        kwargs["supports_check_mode"] = True
        super(BaseModule, self).__init__(**kwargs)
