# Copyright: (c) 2025, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import json
import os
import re
import sys
import time
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
        self.enabled = module.params.get("enable_debug_logging", False)
        self.call_count = self._get_last_call_count()

    def _get_last_call_count(self):
        """
        Get the last API call count from the debug log file.
        If the file doesn't exist or is empty, return 0.

        Returns:
            int: Last API call count from log file, or 0 if not found
        """
        try:
            log_file = os.path.expanduser("~/nutanix_ansible_debug.log")

            # If file doesn't exist, start from 0
            if not os.path.exists(log_file):
                return 0

            # Read the file and get the highest API CALL number using regex over the full content
            last_count = 0
            with open(log_file, "r") as f:
                content = f.read()
                matches = re.findall(r"API CALL #(\d+)", content)
                if matches:
                    last_count = max(int(m) for m in matches)
            return last_count

        except Exception:
            # If any error occurs, start from 0
            return 0

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

        self.call_count += 1

        # Build the log message
        log_lines = []
        log_lines.append("=" * 80)
        log_lines.append(f"API CALL #{self.call_count} - {datetime.now().isoformat()}")
        log_lines.append("=" * 80)

        # Request details
        log_lines.append(f"METHOD: {method}")
        log_lines.append(f"URL: {url}")

        # Query parameters
        if query_params:
            log_lines.append("QUERY PARAMETERS:")
            if isinstance(query_params, dict):
                for key, value in query_params.items():
                    log_lines.append(f"  {key}: {value}")
            elif isinstance(query_params, list):
                # Defensive: display as list of 2-tuples or strings
                for entry in query_params:
                    if isinstance(entry, (list, tuple)) and len(entry) == 2:
                        log_lines.append(f"  {entry[0]}: {entry[1]}")
                    else:
                        log_lines.append(f"  {entry}")
            else:
                log_lines.append(f"  {str(query_params)}")

        # Headers (sanitize sensitive information)
        if headers:
            sanitized_headers = self._sanitize_headers(headers)
            log_lines.append("HEADERS:")
            if isinstance(sanitized_headers, dict):
                for key, value in sanitized_headers.items():
                    log_lines.append(f"  {key}: {value}")
            elif isinstance(sanitized_headers, list):
                for entry in sanitized_headers:
                    if isinstance(entry, (list, tuple)) and len(entry) == 2:
                        log_lines.append(f"  {entry[0]}: {entry[1]}")
                    else:
                        log_lines.append(f"  {entry}")
            else:
                log_lines.append(f"  {str(sanitized_headers)}")

        # Request body
        if body is not None:
            log_lines.append("REQUEST BODY:")
            formatted_body = self._format_body(body)
            log_lines.append(formatted_body)
        else:
            log_lines.append("REQUEST BODY:")
            log_lines.append("  (empty)")

        # Response details
        if status_code is not None:
            log_lines.append(f"STATUS CODE: {status_code}")

        if elapsed_time is not None:
            log_lines.append(f"ELAPSED TIME: {elapsed_time:.1f} seconds")

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

        # Error details
        if error:
            log_lines.append("ERROR:")
            log_lines.append(f"  Type: {type(error).__name__}")
            log_lines.append(f"  Message: {str(error)}")

        log_lines.append("=" * 80)
        log_lines.append("")  # Empty line for readability

        # Log to Ansible's logger and stderr for visibility
        log_message = "\n".join(log_lines)
        self.module.log(log_message)

        # Also write to a dedicated log file for easy viewing
        try:
            log_file = os.path.expanduser("~/nutanix_ansible_debug.log")
            with open(log_file, "a") as f:
                f.write(log_message + "\n")
        except Exception:
            pass  # Silently fail if we can't write to log file

        # Write to stderr for remote execution visibility
        sys.stderr.write(log_message + "\n")
        sys.stderr.flush()

    def _sanitize_headers(self, headers):
        """
        Sanitize headers to remove or mask sensitive information.
        Args:
            headers (dict or list): Request headers
        Returns:
            dict or list: Sanitized headers
        """
        sensitive_keys = ["authorization", "password", "token", "api-key", "api_key"]
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
                return f"  {str(body)}"

        # Handle list
        elif isinstance(body, list):
            try:
                return self._indent_json(json.dumps(body, indent=2, default=str))
            except Exception:
                return f"  {str(body)}"

        # Handle string - try to parse as JSON first
        elif isinstance(body, str):
            try:
                # Try to parse as JSON and pretty print
                parsed = json.loads(body)
                return self._indent_json(json.dumps(parsed, indent=2, default=str))
            except (json.JSONDecodeError, ValueError):
                # Not JSON, return as plain text
                return f"  {body}"

        # Handle other types
        else:
            return f"  {str(body)}"

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
            summary_parts.append(f"Operation: {operation}")
        summary_parts.append(f"Task Status: {status}")
        if task_id:
            summary_parts.append(f"ID: {task_id}")

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

            # Re-raise the exception
            raise Exception(f"Error logging API call: {e}")


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
