# Copyright: 2021, Ansible Project
# Simplified BSD License (see licenses/simplified_bsd.txt or https://opensource.org/licenses/BSD-2-Clause )
from __future__ import absolute_import, division, print_function

__metaclass__ = type


class EntityReference():
    """Entity reference related helpers and spec"""

    entity_by_spec = dict(name=dict(type="str"), uuid=dict(type="str"))

    @staticmethod
    def get_entity_reference_by_uuid_module_spec(kind):
        """
        Module spec for entity reference with uuid and given kind
        """
        spec = dict(name=dict(type="str"), uuid=dict(type="str", required=False), kind=dict(type="str", default=kind))
        return spec
