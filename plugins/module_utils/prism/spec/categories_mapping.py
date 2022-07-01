# Copyright: 2021, Ansible Project
# Simplified BSD License (see licenses/simplified_bsd.txt or https://opensource.org/licenses/BSD-2-Clause )
from __future__ import absolute_import, division, print_function

__metaclass__ = type


class CategoriesMapping:
    """ Categories mapping related helpers and spec"""

    @staticmethod
    def build_categories_mapping_spec(payload, categories_mapping):
        """
        This routine overrides categories mapping in a pc v3 api input payload
        Args:
            payload(dict): api payload
            categories(dict): categories to override in payload
        """
        if not payload.get("metadata"):
            error = "metadata missing in payload for building categories mapping spec"
            return None, error
        if payload["metadata"].get("categories_mapping") != categories_mapping:
            payload["metadata"]["use_categories_mapping"] = True
            payload["metadata"]["categories_mapping"] = categories_mapping
        return payload, None

    @staticmethod
    def build_remove_all_categories_spec(payload, remove_categories):
        """
        This routine removes all categories from pc v3 api input payload
        Args:
            payload(dict): api payload
            remove_categories(dict): flag to remove all categories from payload
        """
        if not payload.get("metadata"):
            error = "metadata missing in payload for removing all categories"
            return None, error
        if remove_categories and payload["metadata"].get("categories_mapping"):
            payload["metadata"]["use_categories_mapping"] = True
            payload["metadata"]["categories_mapping"] = {}
        return payload, None
