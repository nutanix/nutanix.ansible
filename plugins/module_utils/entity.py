# This file is part of Ansible
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import json
from ansible.module_utils.urls import fetch_url
from ansible.module_utils._text import to_text
from base64 import b64encode

# from urllib.parse import urlparse, parse_qsl, urlencode, urlunparse
try:
    from urllib.parse import urlparse, parse_qsl, urlencode, urlunparse
except ImportError:
    from urlparse import urlparse  # python2


class Entity(object):
    def __init__(
        self,
        module,
        resource_type,
        scheme="https",
        cookies=None,
        additional_headers=None,
    ):
        self.module = module
        self.base_url = self._build_url(module, scheme, resource_type)
        self.headers = self._build_headers(module, additional_headers)
        self.cookies = cookies

    def create(self, data=None, endpoint=None, query=None, timeout=30):
        url = self.base_url + "/{0}".format(endpoint) if endpoint else self.base_url
        if query:
            url = self._build_url_with_query(url, query)
        return self._fetch_url(url, method="POST", data=data, timeout=timeout)

    def read(self, uuid=None, endpoint=None, query=None, timeout=30):
        url = self.base_url + "/{0}".format(uuid) if uuid else self.base_url
        if endpoint:
            url = url + "/{0}".format(endpoint)
        if query:
            url = self._build_url_with_query(url, query)
        return self._fetch_url(url, method="GET", timeout=timeout)

    def update(self, data=None, uuid=None, endpoint=None, query=None, timeout=30):
        url = self.base_url + "/{0}".format(uuid) if uuid else self.base_url
        if endpoint:
            url = url + "/{0}".format(endpoint)
        if query:
            url = self._build_url_with_query(url, query)
        return self._fetch_url(url, method="PUT", data=data, timeout=timeout)

    def delete(self, uuid=None, endpoint=None, query=None, timeout=30):
        url = self.base_url + "/{0}".format(uuid) if uuid else self.base_url
        if endpoint:
            url = url + "/{0}".format(endpoint)
        if query:
            url = self._build_url_with_query(url, query)
        return self._fetch_url(url, method="DELETE", timeout=timeout)

    def list(self, data=None, endpoint=None, use_base_url=False, timeout=30):
        url = self.base_url if use_base_url else self.base_url + "/list"
        if endpoint:
            url = url + "/{0}".format(endpoint)
        return self._fetch_url(url, method="POST", data=data, timeout=timeout)

    def get_uuid(self, name):
        data = {"filter": "name=={0}".format(name), "length": 1}
        resp, _ = self.list(data)
        if resp.get("entities"):
            return resp["entities"][0]["metadata"]["uuid"]
        return None

    def _build_url(self, module, scheme, resource_type):
        host = module.params.get("nutanix_host")
        url = "{proto}://{host}".format(proto=scheme, host=host)
        port = module.params.get("nutanix_port")
        if port:
            url += ":{port}".format(port=port)
        if resource_type.startswith("/"):
            url += resource_type
        else:
            url += "/{resource_type}".format(resource_type=resource_type)
        return url

    def _build_headers(self, module, additional_headers):
        headers = {"Content-Type": "application/json", "Accept": "application/json"}
        if additional_headers:
            headers.update(additional_headers)
        usr = module.params.get("nutanix_username")
        pas = module.params.get("nutanix_password")
        if usr and pas:
            cred = "{0}:{1}".format(usr, pas)
            try:
                encoded_cred = b64encode(bytes(cred, encoding="ascii")).decode("ascii")
            except BaseException:
                encoded_cred = b64encode(bytes(cred).encode("ascii")).decode("ascii")
            auth_header = "Basic " + encoded_cred
            headers.update({"Authorization": auth_header})
        return headers

    def _build_url_with_query(self, url, query):
        url = urlparse(url)
        query_ = dict(parse_qsl(url.query))
        query_.update(query)
        query_ = urlencode(query_)
        url = url._replace(query=query_)
        return urlunparse(url)

    def _fetch_url(self, url, method, data=None, timeout=30):
        data = self.module.jsonify(data) if data else None
        resp, info = fetch_url(
            self.module,
            url,
            data=data,
            method=method,
            headers=self.headers,
            cookies=self.cookies,
            timeout=timeout,
        )

        status_code = info.get("status")
        body = resp.read() if resp else info.get("body")
        try:
            resp_json = json.loads(to_text(body)) if body else None
        except ValueError:
            resp_json = None

        if 199 < status_code < 300:
            err = None
        else:
            err = info.get("msg", "Refer error detail in response")
        status = {"error": err, "code": status_code}
        return resp_json, status
