# This file is part of Ansible
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

from .prism import Prism


class Image(Prism):
    def __init__(self, module):
        resource_type = "/images"
        super(Image, self).__init__(module, resource_type=resource_type)


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
