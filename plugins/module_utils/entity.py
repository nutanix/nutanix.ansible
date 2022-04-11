# This file is part of Ansible
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

import json
import os
from base64 import b64encode

try:
    from urllib.parse import parse_qsl, urlencode, urlparse, urlunparse
except ImportError:
    from urlparse import urlparse  # python2

from ansible.module_utils._text import to_text
from ansible.module_utils.urls import fetch_url

__metaclass__ = type


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

    def create(
        self,
        data=None,
        endpoint=None,
        query=None,
        raise_error=True,
        no_response=False,
        timeout=30,
    ):
        url = self.base_url + "/{0}".format(endpoint) if endpoint else self.base_url
        if query:
            url = self._build_url_with_query(url, query)
        return self._fetch_url(
            url,
            method="POST",
            data=data,
            raise_error=raise_error,
            no_response=no_response,
            timeout=timeout,
        )

    def read(
        self,
        uuid=None,
        endpoint=None,
        query=None,
        raise_error=True,
        no_response=False,
        timeout=30,
    ):
        url = self.base_url + "/{0}".format(uuid) if uuid else self.base_url
        if endpoint:
            url = url + "/{0}".format(endpoint)
        if query:
            url = self._build_url_with_query(url, query)
        return self._fetch_url(
            url,
            method="GET",
            raise_error=raise_error,
            no_response=no_response,
            timeout=timeout,
        )

    def update(
        self,
        data=None,
        uuid=None,
        endpoint=None,
        query=None,
        raise_error=True,
        no_response=False,
        timeout=30,
    ):
        url = self.base_url + "/{0}".format(uuid) if uuid else self.base_url
        if endpoint:
            url = url + "/{0}".format(endpoint)
        if query:
            url = self._build_url_with_query(url, query)
        return self._fetch_url(
            url,
            method="PUT",
            data=data,
            raise_error=raise_error,
            no_response=no_response,
            timeout=timeout,
        )

    # source is the file path of resource where ansible yaml runs
    def upload(
        self,
        source,
        endpoint=None,
        query=None,
        raise_error=True,
        no_response=False,
        timeout=30,
    ):
        url = self.base_url + "/{0}".format(endpoint) if endpoint else self.base_url
        if endpoint:
            url = url + "/{0}".format(endpoint)
        if query:
            url = self._build_url_with_query(url, query)
        return self._upload_file(
            url,
            source,
            method="POST",
            raise_error=raise_error,
            no_response=no_response,
            timeout=timeout,
        )

    def delete(
        self,
        uuid=None,
        endpoint=None,
        query=None,
        raise_error=True,
        no_response=False,
        timeout=30,
    ):
        url = self.base_url + "/{0}".format(uuid) if uuid else self.base_url
        if endpoint:
            url = url + "/{0}".format(endpoint)
        if query:
            url = self._build_url_with_query(url, query)
        return self._fetch_url(
            url,
            method="DELETE",
            raise_error=raise_error,
            no_response=no_response,
            timeout=timeout,
        )

    def list(
        self,
        data=None,
        endpoint=None,
        use_base_url=False,
        raise_error=True,
        no_response=False,
        timeout=30,
    ):
        url = self.base_url if use_base_url else self.base_url + "/list"
        if endpoint:
            url = url + "/{0}".format(endpoint)
        return self._fetch_url(
            url,
            method="POST",
            data=data,
            raise_error=raise_error,
            no_response=no_response,
            timeout=timeout,
        )

    def get_spec(self):
        spec = self._get_default_spec()
        for ansible_param, ansible_config in self.module.params.items():
            build_spec_method = self.build_spec_methods.get(ansible_param)
            if build_spec_method and ansible_config:
                spec, error = build_spec_method(spec, ansible_config)
                if error:
                    return None, error
        return spec, None

    def get_uuid(self, value, key="name", raise_error=True, no_response=False):
        data = {"filter": "{0}=={1}".format(key, value), "length": 1}
        resp = self.list(data, raise_error=raise_error, no_response=no_response)
        entities = resp.get("entities") if resp else None
        if entities:
            for entity in entities:
                if entity["spec"]["name"] == value:
                    return entity["metadata"]["uuid"]
        return None

    def _build_url(self, module, scheme, resource_type):
        host = module.params.get("nutanix_host")
        url = "{proto}://{host}".format(proto=scheme, host=host)
        port = module.params.get("nutanix_port")
        if port:
            url += ":{0}".format(port)
        if resource_type.startswith("/"):
            url += resource_type
        else:
            url += "/{0}".format(resource_type)
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

    def _fetch_url(
        self, url, method, data=None, raise_error=True, no_response=False, timeout=30
    ):

        # only jsonify if content-type supports, added to avoid incase of form-url-encodeded type data
        if self.headers["Content-Type"] == "application/json":
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

        if not raise_error:
            return resp_json

        if status_code >= 300:
            err = info.get("msg", "Status code != 2xx")
            self.module.fail_json(
                msg="Failed fetching URL: {0}".format(url),
                status_code=status_code,
                error=err,
                response=resp_json,
            )

        if no_response:
            return {"status_code": status_code}

        if not resp_json:
            self.module.fail_json(
                msg="Failed to convert API response to json",
                status_code=status_code,
                error=body,
                response=resp_json,
            )

        return resp_json

    # upload file in chunks to the given url
    def _upload_file(
        self, url, source, method, raise_error=True, no_response=False, timeout=30
    ):

        resp, info = fetch_url(
            self.module,
            url,
            data=FileChunksIterator(source),
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

        if not raise_error:
            return resp_json

        if status_code >= 300:
            err = info.get("msg", "Status code != 2xx")
            self.module.fail_json(
                msg="Failed fetching URL: {0}".format(url),
                status_code=status_code,
                error=err,
                response=resp_json,
            )

        if no_response:
            return {"status_code": status_code}

        if not resp_json:
            self.module.fail_json(
                msg="Failed to convert API response to json",
                status_code=status_code,
                error=body,
                response=resp_json,
            )

        return resp_json

    def unify_spec(self, spec1, spec2):
        """
        This routine return intersection of two specs(dict) as per
        keys in first level of dictionary.
        """
        spec = {}
        for k in spec1:
            v = spec2.get(k)
            if v:
                spec[k] = v
        return spec


# Read files in chunks and yeild it
class CreateChunks(object):
    def __init__(self, filename, chunk_size=1 << 13):
        self.filename = filename
        self.chunk_size = chunk_size
        self.total_size = os.path.getsize(filename)

    def __iter__(self):
        with open(self.filename, "rb") as file:
            while True:
                data = file.read(self.chunk_size)
                if not data:
                    break
                yield data

    def __len__(self):
        return self.total_size


# to iterate over chunks of file
class FileChunksIterator(object):
    def __init__(self, filename, chunk_size=1 << 13):
        iterable = CreateChunks(filename, chunk_size)
        self.iterator = iter(iterable)
        self.length = len(iterable)

    # request lib checks for read func in iterable object
    def read(self, size=None):
        return next(self.iterator, b"")

    def __len__(self):
        return self.length
