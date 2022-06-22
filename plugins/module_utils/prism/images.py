# This file is part of Ansible
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

from copy import deepcopy

from .clusters import Cluster
from .prism import Prism

__metaclass__ = type


class Image(Prism):
    def __init__(self, module, upload_image=False):
        additional_headers = None
        if upload_image:
            additional_headers = {
                "Content-Type": "application/octet-stream",
                "Accept": "application/json",
            }
        resource_type = "/images"
        super(Image, self).__init__(
            module, resource_type=resource_type, additional_headers=additional_headers
        )
        self.build_spec_methods = {
            "name": self._build_spec_name,
            "desc": self._build_spec_desc,
            "remove_categories": self._build_spec_remove_categories,
            "categories": self._build_spec_categories,
            "source_uri": self._build_spec_source_uri,
            "checksum": self._build_spec_checksum,
            "image_type": self._build_spec_image_type,
            "clusters": self._build_spec_clusters,
            "version": self._build_spec_version,
        }

    def upload_image(self, image_uuid, source_path, timeout=600, raise_error=True):
        endpoint = "{0}/file".format(image_uuid)
        return self.upload(
            source_path,
            endpoint=endpoint,
            method="PUT",
            timeout=timeout,
            no_response=True,
            raise_error=raise_error,
        )

    def _get_default_spec(self):
        return deepcopy(
            {
                "api_version": "3.1.0",
                "metadata": {
                    "kind": "image",
                },
                "spec": {
                    "name": None,
                    "resources": {
                        "architecture": "X86_64",
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
        if flag and payload["metadata"]["categories_mapping"]:
            payload["metadata"]["use_categories_mapping"] = True
            payload["metadata"]["categories_mapping"] = {}
        return payload, None

    def _build_spec_source_uri(self, payload, source_uri):
        payload["spec"]["resources"]["source_uri"] = source_uri
        return payload, None

    def _build_spec_checksum(self, payload, checksum):
        payload["spec"]["resources"]["checksum"] = checksum
        return payload, None

    def _build_spec_image_type(self, payload, image_type):
        payload["spec"]["resources"]["image_type"] = image_type
        return payload, None

    def _build_spec_clusters(self, payload, clusters):
        cluster_references = []
        for cluster_ref in clusters:
            if "name" in cluster_ref:
                cluster = Cluster(self.module)
                name = cluster_ref["name"]
                uuid = cluster.get_uuid(name)
                if not uuid:
                    error = "Cluster {0} not found.".format(name)
                    return None, error

            elif "uuid" in cluster_ref:
                uuid = cluster_ref["uuid"]

            cluster_references.append({"uuid": uuid, "kind": "cluster"})

        payload["spec"]["resources"]["initial_placement_ref_list"] = cluster_references
        return payload, None

    def _build_spec_version(self, payload, version):
        payload["spec"]["resources"]["version"] = version
        return payload, None


def get_image_uuid(config, module):
    if "name" in config:
        image = Image(module)
        name = config["name"]
        uuid = image.get_uuid(name)
        if not uuid:
            error = "Image {0} not found.".format(name)
            return None, error
    elif "uuid" in config:
        uuid = config["uuid"]

    return uuid, None
