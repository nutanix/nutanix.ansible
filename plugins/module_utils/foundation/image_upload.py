from __future__ import absolute_import, division, print_function
from copy import deepcopy

from .foundation import Foundation

__metaclass__ = type


class Image(Foundation):
    def __init__(self, module):
        resource_type = "/upload"
        super(Image, self).__init__(module, resource_type=resource_type)

    def upload(self, filename, installer_type, timeout=60):
        query = {"filename": filename, "installer_type": installer_type}
        return self.create(payload="", query=query, timeout=timeout)

    def _get_default_spec():
        raise NotImplementedError
