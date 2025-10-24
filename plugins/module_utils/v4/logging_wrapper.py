# Copyright: (c) 2024, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

from ..api_logger import get_logger


class LoggingApiClientWrapper:
    """
    A wrapper around the API client that adds logging functionality.
    This can be used with any v4 API client.
    """

    def __init__(self, client, module):
        self._client = client
        self._module = module
        self._logger = get_logger(module)

    def __getattr__(self, name):
        """Delegate all attribute access to the wrapped client."""
        return getattr(self._client, name)

    def call_api(self, *args, **kwargs):
        """Override call_api to add logging."""
        # Log the API call
        method = kwargs.get("method", "UNKNOWN")
        resource_path = kwargs.get("resource_path", "UNKNOWN")
        url = f"{self._client.configuration.host}{resource_path}"

        self._logger.log_request(
            method=method,
            url=url,
            headers=kwargs.get("header_params", {}),
            data=kwargs.get("body"),
            timeout=kwargs.get("_request_timeout"),
        )

        try:
            # Call the original method
            result = self._client.call_api(*args, **kwargs)

            # Log successful response
            self._logger.log_response(
                request_id=self._logger.request_id,
                status_code=200,  # Assuming success if no exception
                headers={},
                body=str(result)[:1000] if result else None,  # Truncate large responses
            )

            return result

        except Exception as e:
            # Log the error
            self._logger.log_error(
                request_id=self._logger.request_id, error_message=str(e), exception=e
            )
            raise


def add_logging_to_client(client, module):
    """
    Add logging functionality to an API client if debug logging is enabled.

    Args:
        client: The API client instance
        module: The Ansible module instance

    Returns:
        The client with logging wrapper if enabled, otherwise the original client
    """
    logger = get_logger(module)
    if logger.enabled:
        return LoggingApiClientWrapper(client, module)
    return client



