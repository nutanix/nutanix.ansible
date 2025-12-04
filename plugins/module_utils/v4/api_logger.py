# Copyright: (c) 2025, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import json
import os
import sys
import time
import warnings
from datetime import datetime


class APILogger:
    """
    Logger utility to intercept and log all API calls made through the SDK.
    This logger captures detailed information about API requests and responses.
    """

    def __init__(self, module):
        """
        Initialize the API logger.
        Args:
            module: Ansible module instance
        """
        self.module = module
        self.enabled = (
            module.params.get("nutanix_debug", False)
            or os.environ.get("NUTANIX_DEBUG", "false").lower() == "true"
        )

    def log_api_call(
        self,
        method,
        url,
        query_params=None,
        headers=None,
        body=None,
        response=None,
        status_code=None,
        elapsed_time=None,
        error=None,
    ):
        """
        Log detailed information about an API call.
        Args:
            method (str): HTTP method (GET, POST, PUT, DELETE, etc.)
            url (str): Full URL of the API endpoint
            query_params (dict): Query parameters
            headers (dict): Request headers
            body: Request body (can be dict, string, or bytes)
            response: Response body
            status_code (int): HTTP status code
            elapsed_time (float): Time taken for the request in seconds
            error (Exception): Any exception that occurred
        """
        if not self.enabled:
            return

        # Build the log message
        log_lines = []
        log_lines.append("=" * 80)
        log_lines.append("{}".format(datetime.now().isoformat()))
        log_lines.append("=" * 80)

        # Request details
        log_lines.append("METHOD: {}".format(method))
        log_lines.append("URL: {}".format(url))

        # Add query parameters
        self._log_query_params(log_lines, query_params)

        # Add headers
        self._log_headers(log_lines, headers)

        # Add request body
        self._log_request_body(log_lines, body)

        # Add response details
        self._log_response(log_lines, response, status_code, elapsed_time)

        # Add error details
        self._log_error(log_lines, error)

        log_lines.append("=" * 80)
        log_lines.append("")  # Empty line for readability

        # Write log message to all outputs
        self._write_log("\n".join(log_lines))

    def _log_query_params(self, log_lines, query_params):
        """Add query parameters to log lines."""
        if not query_params:
            return

        log_lines.append("QUERY PARAMETERS:")
        if isinstance(query_params, dict):
            for key, value in query_params.items():
                log_lines.append("  {}: {}".format(key, value))
        elif isinstance(query_params, list):
            for entry in query_params:
                if isinstance(entry, (list, tuple)) and len(entry) == 2:
                    log_lines.append("  {}: {}".format(entry[0], entry[1]))
                else:
                    log_lines.append("  {}".format(entry))
        else:
            log_lines.append("  {}".format(str(query_params)))

    def _log_headers(self, log_lines, headers):
        """Add headers to log lines."""
        if not headers:
            return

        sanitized_headers = self._sanitize_headers(headers)
        log_lines.append("HEADERS:")
        if isinstance(sanitized_headers, dict):
            for key, value in sanitized_headers.items():
                log_lines.append("  {}: {}".format(key, value))
        elif isinstance(sanitized_headers, list):
            for entry in sanitized_headers:
                if isinstance(entry, (list, tuple)) and len(entry) == 2:
                    log_lines.append("  {}: {}".format(entry[0], entry[1]))
                else:
                    log_lines.append("  {}".format(entry))
        else:
            log_lines.append("  {}".format(str(sanitized_headers)))

    def _log_request_body(self, log_lines, body):
        """Add request body to log lines."""
        log_lines.append("REQUEST BODY:")
        if body is not None:
            formatted_body = self._format_body(body)
            log_lines.append(formatted_body)
        else:
            log_lines.append("  (empty)")

    def _log_response(self, log_lines, response, status_code, elapsed_time):
        """Add response details to log lines."""
        if status_code is not None:
            log_lines.append("STATUS CODE: {}".format(status_code))

        if elapsed_time is not None:
            log_lines.append("ELAPSED TIME: {:.1f} seconds".format(elapsed_time))

        if response is not None:
            # Check if this is a task status response
            task_summary = self._get_task_summary(response)
            if task_summary:
                log_lines.append("")
                log_lines.append(task_summary)
                log_lines.append("=" * 80)

            log_lines.append("RESPONSE BODY:")
            formatted_response = self._format_body(response)
            log_lines.append(formatted_response)
        else:
            log_lines.append("RESPONSE BODY:")
            log_lines.append("  (no response data)")

    def _log_error(self, log_lines, error):
        """Add error details to log lines."""
        if not error:
            return

        log_lines.append("")
        log_lines.append("ERROR:")
        log_lines.append("  Type: {}".format(type(error).__name__))

        # Extract error details from ApiException
        if hasattr(error, "status"):
            log_lines.append("  Status Code: {}".format(error.status))
        if hasattr(error, "reason"):
            log_lines.append("  Reason: {}".format(error.reason))

        # Format error body if available
        if hasattr(error, "body") and error.body:
            log_lines.append("")
            log_lines.append("  Error Response:")
            try:
                # Try to parse and format as JSON
                if isinstance(error.body, str):
                    error_json = json.loads(error.body)
                    formatted_error = self._format_body(error_json)
                else:
                    formatted_error = self._format_body(error.body)
                log_lines.append(formatted_error)
            except Exception:
                # If parsing fails, just show as string
                log_lines.append("    {}".format(error.body))

        # Fallback to string representation if no specific attributes
        elif not any(hasattr(error, attr) for attr in ["status", "reason", "body"]):
            log_lines.append("  Message: {}".format(str(error)))

    def _write_log(self, log_message):
        """Write log message to all outputs."""
        self.module.log(log_message)

        log_file = self.module.params.get("nutanix_log_file") or os.environ.get("NUTANIX_LOG_FILE", "/tmp/nutanix_ansible_debug.log")
        if log_file:
            try:
                with open(log_file, "a") as f:
                    f.write(log_message + "\n")
            except Exception as e:
                warnings.warn(
                    "Failed to write to API log file '{}': {}".format(log_file, str(e)),
                    RuntimeWarning,
                )

        # Write to stderr for visibility during execution
        try:
            sys.stderr.write(log_message + "\n")
            sys.stderr.flush()
        except Exception:
            pass

    def _sanitize_headers(self, headers):
        """
        Sanitize headers to remove or mask sensitive information.
        Args:
            headers (dict or list): Request headers
        Returns:
            dict or list: Sanitized headers
        """
        sensitive_keys = [
            "authorization",
            "password",
            "token",
            "api-key",
            "api_key",
            "secret",
        ]
        # Defensive: handle dict or list header formats
        if isinstance(headers, dict):
            sanitized = {}
            for key, value in headers.items():
                key_lower = str(key).lower()
                if any(sensitive in key_lower for sensitive in sensitive_keys):
                    sanitized[key] = "***REDACTED***"
                else:
                    sanitized[key] = value
            return sanitized
        elif isinstance(headers, list):
            sanitized = []
            for entry in headers:
                if isinstance(entry, (list, tuple)) and len(entry) == 2:
                    key_lower = str(entry[0]).lower()
                    if any(sensitive in key_lower for sensitive in sensitive_keys):
                        sanitized.append((entry[0], "***REDACTED***"))
                    else:
                        sanitized.append((entry[0], entry[1]))
                else:
                    sanitized.append(entry)
            return sanitized
        else:
            return headers

    def _format_body(self, body):
        """
        Format request or response body for logging.
        Args:
            body: Body content (dict, string, bytes, list, or object)
        Returns:
            str: Formatted body string
        """
        if body is None:
            return "  (empty)"

        # Handle dict
        if isinstance(body, dict):
            try:
                return self._indent_json(json.dumps(body, indent=2, default=str))
            except Exception:
                return "  {}".format(str(body))

        # Handle list
        elif isinstance(body, list):
            try:
                return self._indent_json(json.dumps(body, indent=2, default=str))
            except Exception:
                return "  {}".format(str(body))

        # Handle string - try to parse as JSON first
        elif isinstance(body, str):
            try:
                # Try to parse as JSON and pretty print
                parsed = json.loads(body)
                return self._indent_json(json.dumps(parsed, indent=2, default=str))
            except (json.JSONDecodeError, ValueError):
                # Not JSON, return as plain text
                return "  {}".format(body)

        # Handle other types
        else:
            return "  {}".format(str(body))

    def _indent_json(self, json_str):
        """Add indentation to each line of JSON string."""
        lines = json_str.split("\n")
        return "\n".join(["  " + line for line in lines])

    def _get_task_summary(self, response):
        """
        Check if response is a task status and return a summary line.
        Args:
            response: Response body (string or dict)
        Returns:
            str: Task summary line, or None if not a task response
        """
        # Parse response if it's a string
        response_dict = response
        if isinstance(response, str):
            try:
                response_dict = json.loads(response)
            except (json.JSONDecodeError, ValueError):
                return None

        if not isinstance(response_dict, dict):
            return None

        # Check if this is a task response (has data.status)
        data_obj = response_dict.get("data")
        if not isinstance(data_obj, dict):
            return None

        status = data_obj.get("status")
        if not status:
            return None

        # This is a task status response, extract key info
        operation = data_obj.get("operation", "")
        task_id = data_obj.get("extId", "")

        # Build summary line - Operation first, then Status
        summary_parts = []
        if operation:
            summary_parts.append("Operation: {}".format(operation))
        summary_parts.append("Task Status: {}".format(status))
        if task_id:
            summary_parts.append("ID: {}".format(task_id))

        return " | ".join(summary_parts)


class LoggedRequestHandler:
    """Handler class to wrap API requests with logging."""

    def __init__(self, logger, original_request):
        """
        Initialize the handler.

        Args:
            logger: APILogger instance
            original_request: Original request function to wrap
        """
        self.logger = logger
        self.original_request = original_request

    def __call__(
        self,
        method,
        url,
        query_params=None,
        headers=None,
        body=None,
        post_params=None,
        _preload_content=True,
        _request_timeout=None,
    ):
        """
        Execute the API request with logging.

        Args:
            method: HTTP method
            url: Request URL
            query_params: Query parameters
            headers: Request headers
            body: Request body
            post_params: POST parameters
            _preload_content: Whether to preload content
            _request_timeout: Request timeout

        Returns:
            Response object
        """
        start_time = time.time()

        try:
            # Make the actual API call
            response = self.original_request(
                method=method,
                url=url,
                query_params=query_params,
                headers=headers,
                body=body,
                post_params=post_params,
                _preload_content=_preload_content,
                _request_timeout=_request_timeout,
            )

            elapsed = time.time() - start_time

            # Try to get response data (handle different response types)
            response_data = None
            if hasattr(response, "data"):
                response_data = response.data
                # If data is bytes, try to decode it
                if isinstance(response_data, bytes):
                    try:
                        response_data = response_data.decode("utf-8")
                    except Exception:
                        pass
                # If data is still None, try to read from urllib3_response
                if response_data is None and hasattr(response, "urllib3_response"):
                    try:
                        response_data = response.urllib3_response.data
                        if isinstance(response_data, bytes):
                            response_data = response_data.decode("utf-8")
                    except Exception:
                        pass
            elif hasattr(response, "text"):
                response_data = response.text
            elif hasattr(response, "content"):
                try:
                    response_data = response.content.decode("utf-8")
                except Exception:
                    response_data = str(response.content)

            # Log the successful call
            self.logger.log_api_call(
                method=method,
                url=url,
                query_params=query_params,
                headers=headers,
                body=body,
                response=response_data,
                status_code=response.status if hasattr(response, "status") else None,
                elapsed_time=elapsed,
            )

            return response

        except Exception as e:
            elapsed = time.time() - start_time

            # Log the failed call
            self.logger.log_api_call(
                method=method,
                url=url,
                query_params=query_params,
                headers=headers,
                body=body,
                status_code=getattr(e, "status", None),
                elapsed_time=elapsed,
                error=e,
            )

            # Re-raise the original exception to preserve error details
            raise


def setup_api_logging(module, api_client):
    """
    Setup API logging using the SDK's REST client.
    Args:
        module: Ansible module instance
        api_client: SDK API client instance

    Returns:
        APILogger: Logger instance
    """
    logger = APILogger(module)

    if not logger.enabled:
        return logger

    # Get the REST client from the API client
    if not hasattr(api_client, "rest_client"):
        return logger

    rest_client = api_client.rest_client
    original_request = rest_client.request

    # Use the handler class to wrap the request
    rest_client.request = LoggedRequestHandler(logger, original_request)

    return logger
