# Copyright: 2021, Ansible Project
# Simplified BSD License (see licenses/simplified_bsd.txt or https://opensource.org/licenses/BSD-2-Clause )
from __future__ import absolute_import, division, print_function

from ansible.module_utils.basic import AnsibleModule, env_fallback
from ansible_collections.nutanix.ncp.plugins.module_utils.base_module import (  # noqa: E402
    BaseModule,
)

__metaclass__ = type


class FoundationBaseModule(BaseModule):
    support_base_module_keys = ["nutanix_host", "nutanix_port"]
    include_wait_key="include_wait"


    def __init__(self, **kwargs):
        if kwargs.get(self.include_wait_key,False):
            self.support_base_module_keys.append("wait")
            kwargs.pop(self.include_wait_key)
        self._remove_unsupported_attributes()
        self.argument_spec["nutanix_port"]["default"] = "8000"
        super(FoundationBaseModule, self).__init__(**kwargs)
        
    def _remove_unsupported_attributes(self):
        new_arg_spec = {}
        for k in self.argument_spec.keys():
            if k in self.support_base_module_keys:
                new_arg_spec[k] = self.argument_spec[k]
        self.argument_spec = new_arg_spec
