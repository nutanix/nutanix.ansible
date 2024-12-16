from __future__ import absolute_import, division, print_function

__metaclass__ = type


class MockSDK(object):
    def __getattribute__(self, item):
        try:
            return object.__getattribute__(self, item)
        except AttributeError:
            return None


mock_sdk = MockSDK()
