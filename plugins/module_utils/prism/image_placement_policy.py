# This file is part of Ansible
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

from copy import deepcopy

from .prism import Prism

__metaclass__ = type


class ImagePlacementPolicy(Prism):
    def __init__(self, module):
        resource_type = "/images/placement_policies"
        super(ImagePlacementPolicy, self).__init__(module, resource_type=resource_type)
        self.build_spec_methods = {
            "name": self._build_spec_name,
            "desc": self._build_spec_desc,
            "categories": self._build_spec_categories,
            "remove_categories": self._build_spec_remove_categories,
            "placement_type": self._build_spec_placement_type,
            "image_categories": self._build_spec_image_categories,
            "cluster_categories": self._build_spec_cluster_categories,
        }

    def _get_default_spec(self):
        return deepcopy(
            {
                "api_version": "3.1.0",
                "metadata": {
                    "kind": "image_placement_policy",
                },
                "spec": {
                    "name": None,
                    "resources": {
                        "image_entity_filter": {
                            "params": {},
                            "type": "CATEGORIES_MATCH_ANY",
                        },
                        "cluster_entity_filter": {
                            "params": {},
                            "type": "CATEGORIES_MATCH_ANY",
                        },
                    },
                },
            }
        )

    def _build_spec_name(self, payload, name):
        payload["spec"]["name"] = name
        return payload, None

    def _build_spec_desc(self, payload, desc):
        payload["spec"]["description"] = desc
        return payload, None

    def _build_spec_categories(self, payload, categories):
        if payload["metadata"].get("categories_mapping") != categories:
            payload["metadata"]["use_categories_mapping"] = True
            payload["metadata"]["categories_mapping"] = categories
        return payload, None

    def _build_spec_remove_categories(self, payload, flag):
        if flag and payload["metadata"].get("categories_mapping"):
            payload["metadata"]["use_categories_mapping"] = True
            payload["metadata"]["categories_mapping"] = {}
        return payload, None

    def _build_spec_placement_type(self, payload, type):
        if type == "hard":
            payload["spec"]["resources"]["placement_type"] = "EXACTLY"
        else:
            payload["spec"]["resources"]["placement_type"] = "AT_LEAST"
        return payload, None

    def _build_spec_image_categories(self, payload, category_mappings):
        payload["spec"]["resources"]["image_entity_filter"][
            "params"
        ] = category_mappings
        return payload, None

    def _build_spec_cluster_categories(self, payload, category_mappings):
        payload["spec"]["resources"]["cluster_entity_filter"][
            "params"
        ] = category_mappings
        return payload, None
