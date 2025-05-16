# This file is part of Ansible
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

from .prism import Prism


class Account(Prism):
    kind = "account"

    def __init__(self, module):
        resource_type = "/accounts"
        super(Account, self).__init__(module, resource_type=resource_type)

    @classmethod
    def build_account_reference_spec(cls, uuid):
        spec = {"kind": cls.kind, "uuid": uuid}
        return spec


# Helper functions


def get_account_uuid(config, module):
    if "name" in config:
        accounts = Account(module)
        name = config["name"]
        uuid = accounts.get_uuid(name)
        if not uuid:
            error = "Account {0} not found.".format(name)
            return None, error
    elif "uuid" in config:
        uuid = config["uuid"]
    else:
        error = "Config {0} doesn't have name or uuid key".format(config)
        return None, error

    return uuid, None
