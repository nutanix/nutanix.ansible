# This file is part of Ansible
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

from .prism import Prism

__metaclass__ = type


class Image(Prism):
    kind = "image"
