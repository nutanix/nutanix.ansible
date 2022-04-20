#from __future__ import absolute_import, division, print_function

from copy import deepcopy
from .fc import FoundationCentral

__metaclass__ = type


class ImagedNodes(FoundationCentral):
    def __init__(self, module):
        resource_type = "/imaged_nodes"
        super(ImagedNodes, self).__init__(
                module, resource_type=resource_type
            )




