# -*- coding: utf-8 -*-
# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

from ansible_collections.nutanix.ncp.plugins.module_utils.v4.utils import (
    ListEntitiesResponse,
    list_entities,
)


class _FakeMeta(object):
    def __init__(self, total):
        self.total_available_results = total


class _FakeResp(object):
    def __init__(self, data, total):
        self.data = data
        self.metadata = _FakeMeta(total)

    def to_dict(self):
        return {
            "data": self.data,
            "metadata": {"total_available_results": self.metadata.total_available_results},
        }


def test_list_entities_default_returns_raw_response():
    calls = []

    def list_fn(**kwargs):
        calls.append(kwargs)
        return _FakeResp(["a", "b"], 100)

    resp = list_entities(list_fn, kwargs={"_page": 0, "_limit": 50}, fetch_all=False)

    assert len(calls) == 1
    assert calls[0] == {"_page": 0, "_limit": 50}
    assert not isinstance(resp, ListEntitiesResponse)
    assert resp.data == ["a", "b"]


def test_list_entities_fetch_all_paginates():
    calls = []

    def list_fn(**kwargs):
        calls.append(dict(kwargs))
        page = kwargs["_page"]
        limit = kwargs["_limit"]
        total = 120
        start = page * limit
        end = min(start + limit, total)
        data = ["item-{0}".format(i) for i in range(start, end)]
        return _FakeResp(data, total)

    resp = list_entities(
        list_fn,
        kwargs={"_filter": "name eq 'x'"},
        fetch_all=True,
        default_page_size=50,
    )

    assert isinstance(resp, ListEntitiesResponse)
    assert len(calls) == 3
    assert calls[0]["_page"] == 0 and calls[0]["_limit"] == 50
    assert calls[1]["_page"] == 1
    assert calls[2]["_page"] == 2
    assert all(c.get("_filter") == "name eq 'x'" for c in calls)
    assert len(resp.data) == 120
    assert resp.metadata.total_available_results == 120
    assert len(resp.to_dict()["data"]) == 120


def test_list_entities_fetch_all_uses_limit_as_page_size():
    calls = []

    def list_fn(**kwargs):
        calls.append(dict(kwargs))
        page = kwargs["_page"]
        limit = kwargs["_limit"]
        total = 25
        start = page * limit
        end = min(start + limit, total)
        return _FakeResp(["i{0}".format(i) for i in range(start, end)], total)

    resp = list_entities(
        list_fn,
        kwargs={"_limit": 10, "_page": 99},
        fetch_all=True,
    )

    assert len(calls) == 3
    assert all(c["_limit"] == 10 for c in calls)
    # page from kwargs must be ignored when fetch_all is true
    assert calls[0]["_page"] == 0
    assert len(resp.data) == 25


def test_list_entities_passes_fixed_kwargs():
    calls = []

    def list_fn(**kwargs):
        calls.append(dict(kwargs))
        return _FakeResp(["x"], 1)

    list_entities(
        list_fn,
        kwargs={},
        fetch_all=False,
        vmExtId="vm-1",
    )

    assert calls[0]["vmExtId"] == "vm-1"
