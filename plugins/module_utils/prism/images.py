# This file is part of Ansible
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function
from copy import deepcopy
from distutils.command.upload import upload

from .clusters import Cluster
from .projects import Project
from .users import get_user_uuid
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
        super(Image, self).__init__(module, resource_type=resource_type, additional_headers=additional_headers)
        self.build_spec_methods = {
            "name": self._build_spec_name,
            "description": self._build_spec_desc,
            "categories": self._build_spec_categories,
            "project": self._build_spec_project,
            "owner": self._build_spec_owner,
            "source_uri": self._build_spec_source_uri,
            "checksum": self._build_spec_checksum,
            "image_type": self._build_spec_image_type,
            "clusters": self._build_spec_clusters,
            "version": self._build_spec_version,
        }
        self.build_update_spec_methods = {
            "name": self._build_spec_name,
            "description": self._build_spec_desc,
            "categories": self._build_spec_categories,
            "project": self._build_spec_project,
            "owner": self._build_spec_owner,
            "checksum": self._build_spec_checksum,
            "image_type": self._build_spec_image_type,
            "version": self._build_spec_version,
        }

    def upload_image(self, image_uuid, source_path, timeout = 600, raise_error=True):
        endpoint = "{}/file".format(image_uuid)
        return self.upload(source_path, endpoint=endpoint, method="PUT", timeout=timeout, no_response=True, raise_error=raise_error)

    def _get_default_spec(self):
        return deepcopy(
            {
                "api_version": "3.1.0",
                "metadata": {"kind": "image",},
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
        payload["spec"]["metadata"]["categories"] = categories
        return payload, None
    
    def _build_spec_project(self, payload, param):
        if "name" in param:
            project = Project(self.module)
            name = param["name"]
            uuid = project.get_uuid(name)
            if not uuid:

                error = "Project {0} not found.".format(name)
                return None, error

        elif "uuid" in param:
            uuid = param["uuid"]

        payload["metadata"]["project_reference"] = {"uuid": uuid, "kind": "project"}
        return payload, None
    
    def _build_spec_owner(self, payload, param):
        uuid = get_user_uuid(param, self.module)
        payload["metadata"]["owner_reference"] = {"uuid": uuid, "kind": "user"}
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
    
    def _build_spec_clusters(self, payload, param):
        custer_references = []
        for cluster_ref in param["clusters"]:
            if "name" in cluster_ref:
                cluster = Cluster(self.module)
                name = cluster_ref["name"]
                uuid = cluster.get_uuid(name)
                if not uuid:
                    error = "Cluster {0} not found.".format(name)
                    return None, error

            elif "uuid" in cluster_ref:
                uuid = cluster_ref["uuid"]

            custer_references.append({"uuid": uuid, "kind": "cluster"})

        payload["resources"]["initial_placement_ref_list"] = custer_references
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