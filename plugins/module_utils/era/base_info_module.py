# Copyright: 2021, Ansible Project
# Simplified BSD License (see licenses/simplified_bsd.txt or https://opensource.org/licenses/BSD-2-Clause )
from __future__ import absolute_import, division, print_function

from ..base_info_module import BaseInfoModule

__metaclass__ = type


class BaseEraInfoModule(BaseInfoModule):
    def __init__(self, **kwargs):
        super(BaseEraInfoModule, self).__init__(**kwargs)
        self.argument_spec.pop("nutanix_port")
