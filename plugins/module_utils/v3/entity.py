# This file is part of Ansible
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

import copy
import json
import os
from base64 import b64encode

from ansible.module_utils._text import to_text
from ansible.module_utils.urls import fetch_url

from .. import utils

try:
    from urllib.parse import parse_qsl, urlencode, urlparse, urlunparse
except ImportError:
    from urlparse import urlparse  # python2


class Entity(object):
    entities_limitation = 20
    entity_type = "entities"

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
        method="POST",
        raise_error=True,
        no_response=False,
        timeout=30,
    ):
        url = self.base_url + "/{0}".format(endpoint) if endpoint else self.base_url
        if query:
            url = self._build_url_with_query(url, query)
        return self._fetch_url(
            url,
            method=method,
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
        method="GET",
        **kwargs  # fmt: skip
    ):
        url = self.base_url + "/{0}".format(uuid) if uuid else self.base_url
        if endpoint:
            url = url + "/{0}".format(endpoint)
        if query:
            url = self._build_url_with_query(url, query)
        return self._fetch_url(
            url,
            method=method,
            raise_error=raise_error,
            no_response=no_response,
            timeout=timeout,
            **kwargs  # fmt: skip
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
        method="PUT",
        **kwargs  # fmt: skip
    ):
        url = self.base_url + "/{0}".format(uuid) if uuid else self.base_url
        if endpoint:
            url = url + "/{0}".format(endpoint)
        if query:
            url = self._build_url_with_query(url, query)
        return self._fetch_url(
            url,
            method=method,
            data=data,
            raise_error=raise_error,
            no_response=no_response,
            timeout=timeout,
            **kwargs  # fmt: skip
        )

    # source is the file path of resource where ansible yaml runs
    def upload(
        self,
        source,
        endpoint=None,
        method="POST",
        query=None,
        raise_error=True,
        no_response=False,
        timeout=30,
    ):
        url = self.base_url + "/{0}".format(endpoint) if endpoint else self.base_url
        if query:
            url = self._build_url_with_query(url, query)
        return self._upload_file(
            url,
            source,
            method=method,
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
        data=None,
    ):
        url = self.base_url + "/{0}".format(uuid) if uuid else self.base_url
        if endpoint:
            url = url + "/{0}".format(endpoint)
        if query:
            url = self._build_url_with_query(url, query)
        return self._fetch_url(
            url,
            method="DELETE",
            data=data,
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

        resp = self._fetch_url(
            url,
            method="POST",
            data=data,
            raise_error=False,
            no_response=no_response,
            timeout=timeout,
        )
        if resp:
            custom_filters = self.module.params.get("custom_filter")

            if custom_filters:
                entities_list = self._filter_entities(
                    resp[self.entity_type], custom_filters
                )
                entities_count = len(entities_list)

                resp[self.entity_type] = entities_list
                resp["metadata"]["length"] = entities_count

            return resp
        entities_list = []
        main_length = data.get("length")
        main_offset = data.get("offset", 0)
        data["length"] = self.entities_limitation
        while True:
            resp = self._fetch_url(
                url,
                method="POST",
                data=data,
                raise_error=raise_error,
                no_response=no_response,
                timeout=timeout,
            )
            if self.entity_type not in resp:
                return resp
            entities_list.extend(resp[self.entity_type])
            entities_count = len(entities_list)
            data["offset"] = main_offset + entities_count
            if (
                len(resp[self.entity_type]) != self.entities_limitation
                or entities_count == main_length
            ):
                break
        custom_filters = self.module.params.get("custom_filter")
        if custom_filters:
            entities_list = self._filter_entities(entities_list, custom_filters)
            entities_count = len(entities_list)

        resp[self.entity_type] = entities_list
        resp["metadata"]["offset"] = main_offset
        resp["metadata"]["length"] = entities_count

        return resp

    # "params" can be used to override module.params to create spec by other modules backened
    def get_spec(self, old_spec=None, params=None, **kwargs):
        spec = copy.deepcopy(old_spec) or self._get_default_spec()

        ansible_params = None
        if params:
            ansible_params = params
        else:
            ansible_params = self.module.params

        for ansible_param, ansible_config in ansible_params.items():
            build_spec_method = self.build_spec_methods.get(ansible_param)
            if build_spec_method and ansible_config:
                spec, error = build_spec_method(spec, ansible_config)
                if error:
                    return None, error
        return spec, None

    def get_uuid(
        self,
        value,
        key="name",
        data=None,
        entity_type=None,
        raise_error=True,
        no_response=False,
    ):
        filter_spec = (
            data if data else {"filter": "{0}=={1}".format(key, value), "length": 1}
        )

        resp = self.list(
            data=filter_spec, raise_error=raise_error, no_response=no_response
        )
        entities = resp.get("entities") if resp else None
        if entities:
            for entity in entities:

                name = ""
                if entity.get("spec", {}).get("name"):
                    name = entity["spec"]["name"]
                elif entity.get("status", {}).get("name"):
                    name = entity["status"]["name"]
                else:
                    continue

                if name == value:
                    return entity["metadata"]["uuid"]
        return None

    @staticmethod
    def update_entity_spec_version(spec):
        spec["metadata"]["entity_version"] = str(
            int(spec["metadata"]["entity_version"]) + 1
        )

    def get_info_spec(self):
        params = self.module.params
        spec = {
            "kind": None,
            "offset": None,
            "length": None,
            "filter": None,
            "sort_order": None,
            "sort_attribute": None,
        }

        for key in spec.copy().keys():
            if params.get(key):
                spec[key] = params[key]
            else:
                spec.pop(key)

        if params.get("filter"):
            if params.get("filter", {}).get("name") and params.get("kind") == "vm":
                spec["filter"]["vm_name"] = spec["filter"].pop("name")

            spec["filter"] = self._parse_filters(params.get("filter", {}))

        elif params.get("filter_string"):
            spec["filter"] = params["filter_string"]

        return spec, None

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
        self,
        url,
        method,
        data=None,
        raise_error=True,
        no_response=False,
        timeout=30,
        **kwargs  # fmt: skip
    ):
        # only jsonify if content-type supports, added to avoid incase of form-url-encodeded type data
        if self.headers["Content-Type"] == "application/json" and data is not None:
            data = self.module.jsonify(data)

        headers = copy.deepcopy(self.headers)
        if kwargs.get("additional_headers"):
            headers.update(kwargs.get("additional_headers"))

        resp, info = fetch_url(
            self.module,
            url,
            data=data,
            method=method,
            headers=headers,
            cookies=self.cookies,
            timeout=timeout,
        )

        status_code = info.get("status")

        body = None

        # buffer size with ref. to max read size of http.client.HTTPResponse.read() defination
        buffer_size = 65536

        # From ansible-core>=2.13, incase of http error, urllib.HTTPError object is returned in resp
        # as per the docs of ansible we need to use body in that case.
        if not resp or status_code >= 400:
            # get body containing error
            body = info.get("body")
        else:
            # For case when response body size is > 65536, read() will fail due to http.client.IncompleteRead exception
            # This eventually closes connection and can't read response further.
            # So here we read all content in chunks (of size < 65536) and combine data at last to get final response.
            resp_chunk = None
            resp_chunks = []
            while True:
                resp_chunk = resp.read(buffer_size)
                if resp_chunk:
                    resp_chunks.append(to_text(resp_chunk.decode("utf-8")))
                else:
                    break

            body = "".join(resp_chunks)

        try:
            resp_json = json.loads(to_text(body)) if body else None
        except ValueError:
            resp_json = None

        if not raise_error:
            return resp_json

        if status_code >= 300:
            if (
                resp_json and isinstance(resp_json, dict) and resp_json.get("message")
            ):  # for ndb apis
                err = resp_json["message"]
            elif info.get("msg"):
                err = info["msg"]
            else:
                err = "Status code != 2xx"
            self.module.fail_json(
                msg="Failed fetching URL: {0}".format(url),
                status_code=status_code,
                error=err,
                response=resp_json,
            )

        if no_response:
            return {"status_code": status_code}

        if resp_json is None:
            if info.get("msg"):
                resp_json_msg = "{}".format(info.get("msg"))
            else:
                resp_json_msg = "Failed to convert API response to json"

            self.module.fail_json(
                msg=resp_json_msg,
                status_code=status_code,
                error=body,
                response=resp_json,
            )

        if kwargs.get("include_etag"):
            resp_json["etag"] = info.get("etag")
        return resp_json

    # upload file in chunks to the given url
    def _upload_file(
        self, url, source, method, raise_error=True, no_response=False, timeout=30
    ):
        file_chunks_iterator = FileChunksIterator(source)
        headers = copy.deepcopy(self.headers)
        headers["Content-Length"] = file_chunks_iterator.length
        resp, info = fetch_url(
            self.module,
            url,
            data=file_chunks_iterator,
            method=method,
            headers=headers,
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
            # Add error details and status details if any
            if not resp_json:
                resp_json = {}
            if status_code >= 300:
                resp_json["error"] = body
            resp_json["status_code"] = status_code
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

    @staticmethod
    def _parse_filters(filters):
        return ";".join(map(lambda i: "{0}=={1}".format(i[0], i[1]), filters.items()))

    @staticmethod
    def _filter_entities(entities, custom_filters):
        filtered_entities = []
        for entity in entities:
            if utils.intersection(entity, custom_filters.copy()):
                filtered_entities.append(entity)
        return filtered_entities


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
