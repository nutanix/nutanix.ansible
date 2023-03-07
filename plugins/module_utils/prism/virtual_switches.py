# This file is part of Ansible
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

from .groups import Groups
from ..utils import create_filter_criteria_string

# Helper functions


def get_dvs_uuid(config, module, cluster_uuid=None):
    if "name" in config:
        groups = Groups(module)
        name = config["name"]
        filters = {
            "name": name,
            "cluster_configuration_list.cluster_uuid": cluster_uuid,
        }

        data = {
            "entity_type": "distributed_virtual_switch",
            "filter_criteria": create_filter_criteria_string(filters),
        }
        uuid = groups.get_uuid(data=data)
        if not uuid:
            error = "Virtual Switch {0} not found.".format(name)
            return None, error
    elif "uuid" in config:
        uuid = config["uuid"]
    else:
        error = "Config {0} doesn't have name or uuid key".format(config)
        None, error
    return uuid, None
