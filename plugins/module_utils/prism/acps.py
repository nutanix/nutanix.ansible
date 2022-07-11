# This file is part of Ansible
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

from copy import deepcopy

from .prism import Prism


class ACP(Prism):
    def __init__(self, module):
        resource_type = "/access_control_policies"
        super(ACP, self).__init__(module, resource_type=resource_type)
        self.build_spec_methods = {
            # Step 2. This is a Map of
            # ansible attirbute and corresponding API spec generation method
            # Example: method name should start with _build_spec_<method_name>
            # name: _build_spec_name
        }

    def _get_default_spec(self):
        return deepcopy(
            {
                # Step 3: Default API spec
            }
        )
