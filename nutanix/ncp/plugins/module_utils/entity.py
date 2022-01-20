# Copyright: 2021, Ansible Project
# Simplified BSD License (see licenses/simplified_bsd.txt or https://opensource.org/licenses/BSD-2-Clause )
from __future__ import absolute_import, division, print_function

__metaclass__ = type
import json
import time
import uuid
from base64 import b64encode
from copy import deepcopy

from ansible.module_utils.common.text.converters import to_text
from ansible.module_utils.urls import fetch_url

try:
    from urllib.parse import urlparse
except ImportError:
    from urlparse import urlparse


class Entity:
    """Basic functionality for Nutanix modules"""

    entity_type = "Base"
    spec_file = ""
    result = dict(changed=False, original_message="", message="")

    methods_of_actions = {
        "create": "post",
        "list": "post",
        "update": "put",
        "delete": "delete",
        "absent": "delete",
    }
    kind = ""
    api_version = "3.1.0"
    __BASEURL__ = ""

    def __init__(self, module):
        self.run_module(module)

    def parse_data(self):
        if self.action != "list":
            if self.data.get("metadata"):
                if not self.data["metadata"].get("kind"):
                    self.data["metadata"].update({"kind": self.kind})
            else:
                self.data.update({"metadata": {"kind": self.kind}})
            if not self.data.get("api_version"):
                self.data["api_version"] = self.api_version

    def check_response(self):

        if self.response.get("task_uuid") and self.wait:
            task = self.validate_request(
                self.module,
                self.response.get("task_uuid"),
                self.netloc,
                self.wait_timeout,
            )
            self.result["task_information"] = task

        if not self.response.get("status"):
            if self.response.get("api_response_list"):
                self.response["status"] = (
                    self.response.get("api_response_list")[0]
                    .get("api_response")
                    .get("status")
                )
            elif "entities" in self.response:
                if self.response["entities"]:
                    self.response["status"] = self.response.get("entities")[0].get(
                        "status"
                    )
                else:
                    self.response["status"] = {"state": "complete"}

        if self.response.get("status") and self.wait:
            state = self.response.get("status").get("state")
            if "pending" in state.lower() or "running" in state.lower():
                task = self.validate_request(
                    self.module,
                    self.response.get("status")
                    .get("execution_context")
                    .get("task_uuid"),
                    self.netloc,
                    self.wait_timeout,
                )
                self.response["status"]["state"] = task.get("status")
                self.result["task_information"] = task

        self.result["changed"] = True
        status = self.response.get("state") or self.response.get("status").get("state")
        if status and status.lower() != "succeeded" or self.action == "list":
            self.result["changed"] = False
            if status.lower() != "complete":
                self.result["failed"] = True

        self.result["response"] = self.response

    def create(self):
        pass

    def update(self):
        item_uuid = self.data["metadata"]["uuid"]
        if not self.data.get("operations"):
            self.url += "/" + str(uuid.UUID(item_uuid))
        else:
            self.url += "/" + str(uuid.UUID(item_uuid)) + "/file"
        response = self.send_request(
            self.module, "get", self.url, self.data, self.username, self.password
        )

        if response.get("state") and response.get("state").lower() == "error":
            self.result["changed"] = False
            self.result["failed"] = True
            self.result["message"] = response["message_list"]
        else:
            self.data["metadata"]["spec_version"] = response["metadata"]["spec_version"]

    def delete(self):
        item_uuid = self.data["metadata"]["uuid"]
        self.url += "/" + str(uuid.UUID(item_uuid))

    def list(self):
        self.url += "/" + self.action
        if not self.data:
            self.data = {"kind": self.kind}

    @staticmethod
    def send_request(module, method, req_url, req_data, username, password, timeout=30):
        try:
            credentials = bytes(username + ":" + password, encoding="ascii")
        except BaseException:
            credentials = bytes(username + ":" + password).encode("ascii")

        encoded_credentials = b64encode(credentials).decode("ascii")
        authorization = "Basic " + encoded_credentials
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": authorization,
            "cache-control": "no-cache",
        }
        if req_data is None:
            payload = {}
        else:
            payload = req_data
        resp, info = fetch_url(
            module=module,
            url=req_url,
            headers=headers,
            method=method,
            data=module.jsonify(payload),
            timeout=timeout,
        )
        if not 300 > info["status"] > 199:
            module.fail_json(
                msg="Fail: %s"
                % (
                    "Status: "
                    + str(info["msg"])
                    + ", Message: "
                    + str(info.get("body"))
                )
            )

        body = resp.read() if resp else info.get("body")
        try:
            resp_json = json.loads(to_text(body)) if body else None
        except ValueError:
            resp_json = None
        return resp_json

    def validate_request(self, module, task_uuid, netloc, wait_timeout):
        timer = 5
        retries = wait_timeout // timer
        response = None
        succeeded = False
        task_uuid = str(uuid.UUID(task_uuid))
        url = self.generate_url_from_operations("tasks", netloc, [task_uuid])
        while retries > 0 or not succeeded:
            response = self.send_request(
                module, "get", url, None, self.username, self.password
            )
            if response.get("status"):
                status = response.get("status")
                if "running" not in status.lower() and "queued" not in status.lower():
                    succeeded = True
                    return response
            time.sleep(timer)
            retries -= 1
        return response

    def generate_url_from_operations(self, name, netloc=None, ops=None):
        name = name.split("_")[-1]
        url = "https://" + netloc
        path = self.__BASEURL__ + "/" + name
        if ops:
            for each in ops:
                if type(each) is str:
                    path += "/" + each
                elif type(each) is dict:
                    key = list(each.keys())[0]
                    val = each[key]
                    path += "/{0}/{1}".format(key, val)
        url += path
        return self.validate_url(url, netloc, path)

    @staticmethod
    def validate_url(url, netloc, path=""):
        parsed_url = urlparse(url)
        if (
            url
            and netloc
            and "http" in parsed_url.scheme
            and netloc == parsed_url.netloc
            and path == parsed_url.path
        ):
            return url
        raise ValueError("Incorrect URL :", url)

    def get_action(self):
        if self.action in self.methods_of_actions.keys():
            self.action = self.methods_of_actions[self.action]
        elif self.action == "present":
            self.action = "update" if self.data["metadata"].get("uuid") else "create"
        else:
            raise ValueError("Wrong action: " + self.action)

    def get_spec(self):
        from os.path import join

        import yaml

        # Get the current working directory

        ncp_dir = (
            self.module.tmpdir.split("/tmp")[0]
            + "/collections/ansible_collections/nutanix/ncp/"
        )

        file_path = join(ncp_dir, self.spec_file)
        with open(file_path) as f:
            # spec = json.loads(str(f.read()))
            spec = yaml.safe_load(f.read())
        return spec

    def clean_spec(self, spec):
        for key, value in spec.copy().items():
            if isinstance(value, str):
                if value.startswith("{{") and value.endswith("}}"):
                    value = getattr(self, value[2:-2], None)
                    if value:
                        spec[key] = value
                    else:
                        spec.pop(key)

            elif isinstance(value, dict):
                value = self.clean_spec(value)
                if value:
                    spec[key] = value
                else:
                    spec.pop(key)
            elif isinstance(value, list) and key != "required":
                obj = value.pop(0)
                list_key = obj.pop("list_key")
                sub_spec_key = list_key.split("__")[-1]
                if list_key:
                    value = self.get_attr_spec(
                        sub_spec_key, getattr(self, list_key, None)
                    )
                    if value:
                        spec[key] = value
                    else:
                        spec.pop(key)
        requirements = spec.pop("required")
        # if not set(requirements) <= spec.keys() or not spec:
        #     return None
        return spec

    def build(self):

        self.username = self.credentials["username"]
        self.password = self.credentials["password"]

        self.parse_data()

        self.url = self.generate_url_from_operations(
            self.module_name, self.netloc, self.operations
        )

        self.get_action()

        getattr(self, self.action)()

        self.response = self.send_request(
            self.module,
            self.methods_of_actions[self.action],
            self.url,
            self.data,
            self.username,
            self.password,
        )

        self.check_response()

    def run_module(self, module):

        if module.check_mode:
            module.exit_json(**self.result)
        for key, value in module.params.items():
            if isinstance(value, dict):
                for k, v in value.items():
                    setattr(self, k, v)
            setattr(self, key, value)
        self.module = module

        spec = self.get_spec()
        self.clean_spec(spec)
        self.data = spec

        self.url = self.auth.get("url")
        self.credentials = self.auth.get("credentials")

        if not self.url:
            self.url = (
                str(self.auth.get("ip_address")) + ":" + str(self.auth.get("port"))
            )

        self.netloc = self.url
        self.module_name = module._name
        self.build()

        module.exit_json(**self.result)
