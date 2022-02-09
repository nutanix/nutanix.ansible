# This file is part of Ansible
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

from copy import deepcopy

from .prism import Prism


class Vpc(Prism):
    def __init__(self, module):
        resource_type = "/vpcs"
        super(Vpc, self).__init__(module, resource_type=resource_type)
        self.build_spec_methods = {
            # TODO. This is a Map of
            # ansible attirbute and corresponding API spec generation method
            # Example: method name should start with _build_spec_<method_name>
            # name: _build_spec_name
        }

    def _get_default_spec(self):
        return deepcopy(
            {
                # TODO: Default API spec
            }
        )


# Helper functions


def get_vpc_uuid(config, module):
    if "name" in config["vpc"]:
        vpc = Vpc(module)
        name = config["vpc"]["name"]
        uuid = vpc.get_uuid(name)
        if not uuid:
            error = "VPC {0} not found.".format(name)
            return None, error
    elif "uuid" in config["vpc"]:
        uuid = config["vpc"]["uuid"]
    return uuid, None