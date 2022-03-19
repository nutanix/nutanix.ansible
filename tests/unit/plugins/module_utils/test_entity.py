from __future__ import absolute_import, division, print_function

import json
from base64 import b64encode

from ansible.module_utils.six.moves.urllib.parse import urlparse
from ansible_collections.nutanix.ncp.plugins.module_utils.entity import Entity
from ansible_collections.nutanix.ncp.tests.unit.plugins.modules.utils import (
    AnsibleExitJson,
    AnsibleFailJson,
    ModuleTestCase,
)

__metaclass__ = type

try:
    from unittest.mock import MagicMock
except Exception:
    from mock import MagicMock


class Module:
    def __init__(self):
        self.params = {
            "nutanix_host": "99.99.99.99",
            "nutanix_port": "9999",
            "nutanix_username": "username",
            "nutanix_password": "password",
        }
        self.tmpdir = "/tmp"

    def jsonify(self, data):
        return json.dumps(data)


def _fetch_url(url, method, data=None, **kwargs):
    """Mock send_request"""
    response = {
        "status": {"state": "succeeded"},
        "status_code": 200,
        "request": {"method": method, "url": url, "data": data},
        "entities": [
            {"spec": {"name": "test_name"}, "metadata": {"uuid": "test_uuid"}}
        ],
    }

    return response


def exit_json(*args, **kwargs):
    if "changed" not in kwargs:
        kwargs["changed"] = False
    raise AnsibleExitJson(kwargs)


def fail_json(*args, **kwargs):
    kwargs["failed"] = True
    raise AnsibleFailJson(kwargs)


class TestEntity(ModuleTestCase):
    def setUp(self):
        self.module = Module()
        Entity._fetch_url = MagicMock(side_effect=_fetch_url)
        Entity._get_default_spec = MagicMock(side_effect=lambda: {})
        Entity.build_spec_methods = {
            "test_param": lambda s, v: ({"test_param": v}, None)
        }
        self.entity = Entity(self.module, resource_type="/test")
        self.module.exit_json = MagicMock(side_effect=exit_json)
        self.module.fail_json = MagicMock(side_effect=fail_json)

    def test_create_action(self):
        data = {}
        req = {"method": "POST", "url": "https://99.99.99.99:9999/test", "data": data}
        result = self.entity.create(data)
        self.assertEqual(result["request"], req)

    def test_negative_create_action(self):
        data = {}
        self.module.params = {}
        entity = Entity(self.module, resource_type="")

        req = {"method": "POST", "url": "https://None/", "data": data}
        result = entity.create(data)
        self.assertEqual(result["request"], req)
        self.assertEqual(entity.headers.get("Authorization"), None)

    def test_update_action(self):
        data = {}
        req = {"method": "PUT", "url": "https://99.99.99.99:9999/test", "data": data}
        result = self.entity.update(data)
        self.assertEqual(result["request"], req)

    def test_negative_update_action(self):
        data = {}
        self.module.params = {}
        entity = Entity(self.module, resource_type="")

        req = {"method": "PUT", "url": "https://None/", "data": data}
        result = entity.update(data)
        self.assertEqual(result["request"], req)
        self.assertEqual(entity.headers.get("Authorization"), None)

    def test_list_action(self):
        data = {}
        req = {
            "method": "POST",
            "url": "https://99.99.99.99:9999/test/list",
            "data": data,
        }
        result = self.entity.list(data)
        self.assertEqual(result["request"], req)

    def test_negative_list_action(self):
        data = {}
        self.module.params = {}
        entity = Entity(self.module, resource_type="")

        req = {"method": "POST", "url": "https://None//list", "data": data}
        result = entity.list(data)
        self.assertEqual(result["request"], req)
        self.assertEqual(entity.headers.get("Authorization"), None)

    def test_raed_action(self):
        uuid = "test_uuid"
        req = {
            "method": "GET",
            "url": "https://99.99.99.99:9999/test/{0}".format(uuid),
            "data": None,
        }
        result = self.entity.read(uuid=uuid)
        self.assertEqual(result["request"], req)

    def test_negative_read_action(self):
        data = None
        self.module.params = {}
        entity = Entity(self.module, resource_type="")

        req = {"method": "GET", "url": "https://None/", "data": data}
        result = entity.read(data)
        self.assertEqual(result["request"], req)
        self.assertEqual(entity.headers.get("Authorization"), None)

    def test_delete_action(self):
        uuid = "test_uuid"
        req = {
            "method": "DELETE",
            "url": "https://99.99.99.99:9999/test/{0}".format(uuid),
            "data": None,
        }
        result = self.entity.delete(uuid=uuid)
        self.assertEqual(result["request"], req)

    def test_negative_delete_action(self):
        data = None
        self.module.params = {}
        entity = Entity(self.module, resource_type="")

        req = {"method": "DELETE", "url": "https://None/", "data": data}
        result = entity.delete(data)
        self.assertEqual(result["request"], req)
        self.assertEqual(entity.headers.get("Authorization"), None)

    def test_build_url(self):
        module_name = "test"
        actual = self.entity._build_url(self.module, "https", "/test")
        actual = urlparse(actual)
        path = "/" + module_name
        self.assertTrue("http" in actual.scheme)
        self.assertEqual(path, actual.path)

    def test_build_url_with_query(self):
        query = {"some_id": "1234"}
        url = "https://99.99.99.99:9999/test"
        generated_url = self.entity._build_url_with_query(url, query)
        url_with_query = "https://99.99.99.99:9999/test?some_id=1234"
        self.assertEqual(url_with_query, generated_url)

    def test_build_headers(self):
        actual_headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

        usr = self.module.params.get("nutanix_username")
        pas = self.module.params.get("nutanix_password")

        cred = "{0}:{1}".format(usr, pas)
        try:
            encoded_cred = b64encode(bytes(cred, encoding="ascii")).decode("ascii")
        except BaseException:
            encoded_cred = b64encode(bytes(cred).encode("ascii")).decode("ascii")
        auth_header = "Basic " + encoded_cred

        actual_headers.update({"Authorization": auth_header})
        additional_headers = {"some_header": "test"}

        actual_headers.update(additional_headers)

        generated_headers = self.entity._build_headers(self.module, additional_headers)

        self.assertEqual(actual_headers, generated_headers)

    def test_get_uuid(self):
        name = "test_name"
        result = self.entity.get_uuid(value=name)
        self.assertEqual(result, "test_uuid")

    def test_negative_get_uuid(self):
        name = "wrong_test_name"
        result = self.entity.get_uuid(value=name)
        self.assertEqual(result, None)

    def test_get_spec(self):
        result = self.entity.get_spec()
        self.assertEqual(result, ({}, None))

    def test_build_spec_methods(self):
        self.module.params = {"test_param": "test_value"}
        entity = Entity(self.module, resource_type="/test")
        result = entity.get_spec()
        self.assertEqual(result, ({"test_param": "test_value"}, None))

    def test_negative_build_spec_methods(self):
        self.module.params = {"wrong_param": "test_value"}
        entity = Entity(self.module, resource_type="/test")
        result = entity.get_spec()
        self.assertNotEqual(result, ({"wrong_param": "test_value"}, None))
