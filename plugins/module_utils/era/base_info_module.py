# Copyright: 2021, Ansible Project
# Simplified BSD License (see licenses/simplified_bsd.txt or https://opensource.org/licenses/BSD-2-Clause )
from __future__ import absolute_import, division, print_function

from copy import deepcopy

from plugins.module_utils.base_info_module import BaseInfoModule

__metaclass__ = type


class BaseEraInfoModule(BaseInfoModule):

    def __init__(self, skip_info_args=False, **kwargs):
        self.argument_spec = deepcopy(BaseInfoModule.argument_spec)
        self.argument_spec.pop("nutanix_port")
        super(BaseEraInfoModule, self).__init__(**kwargs)
