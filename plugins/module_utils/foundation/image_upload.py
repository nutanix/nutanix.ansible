from __future__ import absolute_import, division, print_function

from .foundation import Foundation

__metaclass__ = type


class Image(Foundation):
    def __init__(self, module, delete_image=False):
        if delete_image:
            resource_type = "/delete"
            additional_headers = {
                "Content-Type": "application/x-www-form-urlencoded",
                "Accept": "application/json",
            }
        else:
            resource_type = "/upload"
            additional_headers = {
                "Content-Type": "application/octet-stream",
                "Accept": "application/json",
            }

        super(Image, self).__init__(
            module, resource_type=resource_type, additional_headers=additional_headers
        )

    def upload_image(self, filename, installer_type, source, timeout=600):
        query = {"filename": filename, "installer_type": installer_type}
        return self.upload(source=source, query=query, timeout=timeout)

    def delete_image(self, filename, installer_type):
        data = "installer_type={}&filename={}".format(installer_type, filename)
        return self.create(data=data, no_response=True)

    def _get_default_spec(self):
        raise NotImplementedError
