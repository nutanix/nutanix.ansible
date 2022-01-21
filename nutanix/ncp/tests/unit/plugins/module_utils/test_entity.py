from __future__ import absolute_import, division, print_function

from ansible.module_utils import basic
from ansible.module_utils.six.moves.urllib.parse import urlparse
from ansible_collections.nutanix.ncp.plugins.module_utils.entity import Entity
from ansible_collections.nutanix.ncp.tests.unit.plugins.modules.utils import (
    AnsibleExitJson,
    ModuleTestCase,
)

__metaclass__ = type

try:
    from unittest.mock import MagicMock
except Exception:
    from mock import MagicMock


def send_request(module, req_verb, req_url, req_data, username, password, timeout=30):
    """Mock send_request"""
    kwargs = locals()
    status = {"state": "succeeded"}
    spec_version = None
    if req_verb == "get":
        status = "succeeded"
        spec_version = "1"
    response = {
        "status": status,
        "status_code": 200,
        "request": {
            "req_verb": req_verb,
            "req_url": req_url,
            "req_data": req_data,
            "username": username,
            "password": password,
        },
        "metadata": {"spec_version": spec_version},
    }

    return response


def exit_json(*args, **kwargs):
    if "changed" not in kwargs:
        kwargs["changed"] = False
    raise AnsibleExitJson(kwargs)


class TestEntity(ModuleTestCase):
    def setUp(self):
        module = object()
        Entity.__init__ = MagicMock(side_effect=lambda *args: None)
        self.builder = Entity(module)
        self.builder.username = "username"
        self.builder.password = "password"
        self.builder.credentials = {}
        self.builder.ip_address = "99.99.99.99"
        self.builder.port = "9999"
        self.builder.netloc = "test.com"
        self.builder.url = "https://test.com/test"
        self.builder.operations = ""
        self.builder.wait = True
        self.builder.module_name = "test"
        self.builder.module = module
        self.builder.send_request = MagicMock(side_effect=send_request)
        basic.AnsibleModule.exit_json = MagicMock(side_effect=exit_json)

    def test_create_action(self):
        action = "present"

        self.builder.data = {}
        self.builder.credentials = {
            "username": self.builder.username,
            "password": self.builder.password,
        }
        req = {
            "req_verb": "post",
            "req_url": self.builder.url,
            "req_data": self.builder.data,
        }
        req.update(self.builder.credentials)
        self.builder.action = action
        self.builder.build()
        self.assertEqual(self.builder.result["response"]["request"], req)
        self.assertEqual(self.builder.result["changed"], True)

    def test_negative_create_action(self):
        action = "present"

        self.builder.data = {}
        self.builder.credentials = {
            "username": self.builder.username,
        }
        exception = None
        try:
            self.builder.action = action
            self.builder.build()
        except Exception as e:
            exception = e
        self.assertEqual(type(exception), KeyError)
        self.assertEqual(self.builder.result["changed"], False)

    def test_update_action(self):
        action = "present"

        self.builder.data = {
            "metadata": {"uuid": "a218f559-0ec0-46d8-a876-38f7d8950098"}
        }
        self.builder.credentials = {
            "username": self.builder.username,
            "password": self.builder.password,
        }
        req = {
            "req_verb": "put",
            "req_url": self.builder.url + "/" + self.builder.data["metadata"]["uuid"],
            "req_data": self.builder.data,
        }
        req.update(self.builder.credentials)
        self.builder.action = action
        self.builder.build()
        self.assertEqual(self.builder.result["response"]["request"], req)
        self.assertEqual(self.builder.result["changed"], True)

    def test_negative_update_action(self):
        action = "present"

        self.builder.data = {}
        self.builder.credentials = {
            "username": self.builder.username,
        }
        exception = None
        try:
            self.builder.action = action
            self.builder.build()
        except Exception as e:
            exception = e
        self.assertEqual(type(exception), KeyError)
        self.assertEqual(self.builder.result["changed"], False)

    def test_list_action(self):
        action = "list"

        self.builder.data = {"kind": ""}
        self.builder.credentials = {
            "username": self.builder.username,
            "password": self.builder.password,
        }
        req = {
            "req_verb": "post",
            "req_url": self.builder.url + "/list",
            "req_data": self.builder.data,
        }
        req.update(self.builder.credentials)
        self.builder.action = action
        self.builder.build()
        self.assertEqual(self.builder.result["response"]["request"], req)
        self.assertEqual(self.builder.result["changed"], False)

    def test_delete_action(self):
        action = "absent"

        self.builder.data = {
            "metadata": {"uuid": "a218f559-0ec0-46d8-a876-38f7d8950098"}
        }
        self.builder.credentials = {
            "username": self.builder.username,
            "password": self.builder.password,
        }
        req = {
            "req_verb": "delete",
            "req_url": self.builder.url + "/" + self.builder.data["metadata"]["uuid"],
            "req_data": self.builder.data,
        }
        req.update(self.builder.credentials)
        self.builder.action = action
        self.builder.build()
        self.assertEqual(self.builder.result["response"]["request"], req)
        self.assertEqual(self.builder.result["changed"], True)

    def test_negative_delete_action(self):
        action = "delete"

        self.builder.data = {}  # testing without uuid
        self.builder.credentials = {
            "username": self.builder.username,
            "password": self.builder.password,
        }
        exception = None
        try:
            self.builder.action = action
            self.builder.build()
        except Exception as e:
            exception = e
        self.assertEqual(type(exception), KeyError)
        self.assertEqual(self.builder.result["changed"], False)

    def test_generate_url(self):
        module_name = "test"
        operations = ["update", {"clone": "test"}]
        ip = str(self.builder.ip_address)
        port = str(self.builder.port)
        netloc = self.builder.netloc or ip + ":" + port
        actual = self.builder.generate_url_from_operations(
            module_name, netloc, operations
        )
        actual = urlparse(actual)
        path = "/" + module_name
        for each in operations:
            if isinstance(each, str):
                path += "/" + each
            elif isinstance(each, dict):
                key = list(each.keys())[0]
                val = each[key]
                path += "/{0}/{1}".format(key, val)
        self.assertTrue("http" in actual.scheme)
        self.assertEqual(netloc, actual.netloc)
        self.assertEqual(path, actual.path)

    def test_negative_generate_url(self):
        operations = ["update", {"clone": "test"}]
        exception = None
        try:
            self.builder.generate_url_from_operations("", "", operations)

        except Exception as e:
            exception = e
        self.assertEqual(type(exception), ValueError)

    def test_validate_request(self):
        response = self.builder.validate_request(
            self.builder.module,
            "a218f559-0ec0-46d8-a876-38f7d8950098",
            self.builder.netloc,
            1,
        )
        self.assertEqual(response.get("status"), "succeeded")

    def test_negative_validate_request(self):
        exception = None
        try:
            self.builder.validate_request(
                self.builder.module, "wrong_uuid", self.builder.netloc, 1
            )
        except Exception as e:
            exception = e
        self.assertEqual(type(exception), ValueError)
