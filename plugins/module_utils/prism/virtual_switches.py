# This file is part of Ansible
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

from .groups import Groups

# Helper functions


def get_dvs_uuid(config, module):
    if "name" in config["virtual_switch"]:
        groups = Groups(module)
        name = config["virtual_switch"]["name"]
        uuid = groups.get_uuid("distributed_virtual_switch", "name=={0}".format(name))
        if not uuid:
            error = "Virtual Switch {0} not found.".format(name)
            return None, error
    elif "uuid" in config["virtual_switch"]:
        uuid = config["virtual_switch"]["uuid"]
    return uuid, None
