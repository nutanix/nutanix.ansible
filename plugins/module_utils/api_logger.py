# Copyright: (c) 2024, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import json
import os
import sys
import time
from datetime import datetime


class APILogger:
    """
    A centralized logging utility for Nutanix Ansible collection API calls.
    Can be enabled by setting NUTANIX_DEBUG_LOGGING environment variable to 'true'.
    """

    def __init__(self, module=None):
        self.module = module
        self.enabled = self._is_logging_enabled()
        self.log_file = self._get_log_file_path()
        self.request_id = 0

    def _is_logging_enabled(self):
        """Check if API logging is enabled via environment variable or module parameter."""
        # Check environment variable first
        if os.getenv("NUTANIX_DEBUG_LOGGING", "").lower() in ["true", "1", "yes"]:
            return True

        # Check module parameter if module is available
        if self.module and hasattr(self.module, "params"):
            return self.module.params.get("debug_logging", False)

        return False

    def _get_log_file_path(self):
        """Get the log file path. Defaults to /tmp/nutanix_api_debug.log"""
        log_file = os.getenv("NUTANIX_DEBUG_LOG_FILE", "/tmp/nutanix_api_debug.log")
        return log_file

    def _sanitize_headers(self, headers):
        """Remove sensitive information from headers."""
        if not headers:
            return headers

        sanitized = dict(headers)
        sensitive_headers = ["authorization", "x-api-key", "cookie", "set-cookie"]

        for header in sensitive_headers:
            if header in sanitized:
                sanitized[header] = "[REDACTED]"
            if header.upper() in sanitized:
                sanitized[header.upper()] = "[REDACTED]"
            # Also check for case variations
            for key in list(sanitized.keys()):
                if key.lower() == header.lower():
                    sanitized[key] = "[REDACTED]"

        return sanitized

    def _sanitize_data(self, data):
        """Remove sensitive information from request/response data."""
        if not data:
            return data

        try:
            if isinstance(data, str):
                # Try to parse as JSON
                json_data = json.loads(data)
                return self._sanitize_json_data(json_data)
            elif isinstance(data, dict):
                return self._sanitize_json_data(data)
            else:
                return str(data)
        except (json.JSONDecodeError, TypeError):
            # If not JSON, return as string but truncate if too long
            data_str = str(data)
            if len(data_str) > 1000:
                return data_str[:1000] + "... [TRUNCATED]"
            return data_str

    def _sanitize_json_data(self, data):
        """Recursively sanitize JSON data to remove sensitive fields."""
        if not isinstance(data, dict):
            return data

        sensitive_fields = ["password", "token", "secret", "key", "credential", "auth"]
        sanitized = {}

        for key, value in data.items():
            key_lower = key.lower()
            if any(sensitive in key_lower for sensitive in sensitive_fields):
                sanitized[key] = "[REDACTED]"
            elif isinstance(value, dict):
                sanitized[key] = self._sanitize_json_data(value)
            elif isinstance(value, list):
                sanitized[key] = [
                    self._sanitize_json_data(item) if isinstance(item, dict) else item
                    for item in value
                ]
            else:
                sanitized[key] = value

        return sanitized

    def _write_log(self, log_entry):
        """Write log entry to file."""
        if not self.enabled:
            return

        try:
            with open(self.log_file, "a", encoding="utf-8") as f:
                f.write(
                    json.dumps(log_entry, indent=2, default=str)
                    + "\n"
                    + "=" * 80
                    + "\n"
                )
        except Exception as e:
            # If we can't write to log file, print to stderr
            print(f"Failed to write to log file {self.log_file}: {e}", file=sys.stderr)

    def log_request(self, method, url, headers=None, data=None, timeout=None):
        """Log an API request."""
        if not self.enabled:
            return

        self.request_id += 1
        timestamp = datetime.now().isoformat()

        log_entry = {
            "request_id": self.request_id,
            "timestamp": timestamp,
            "type": "REQUEST",
            "method": method,
            "url": url,
            "headers": self._sanitize_headers(headers),
            "data": self._sanitize_data(data),
            "timeout": timeout,
        }

        self._write_log(log_entry)

    def log_response(
        self, request_id, status_code, headers=None, body=None, duration=None
    ):
        """Log an API response."""
        if not self.enabled:
            return

        timestamp = datetime.now().isoformat()

        log_entry = {
            "request_id": request_id,
            "timestamp": timestamp,
            "type": "RESPONSE",
            "status_code": status_code,
            "headers": self._sanitize_headers(headers),
            "body": self._sanitize_data(body),
            "duration_ms": duration,
        }

        self._write_log(log_entry)

    def log_error(self, request_id, error_message, exception=None):
        """Log an API error."""
        if not self.enabled:
            return

        timestamp = datetime.now().isoformat()

        log_entry = {
            "request_id": request_id,
            "timestamp": timestamp,
            "type": "ERROR",
            "error_message": str(error_message),
            "exception": str(exception) if exception else None,
        }

        self._write_log(log_entry)

    def log_info(self, message, extra_data=None):
        """Log general information."""
        if not self.enabled:
            return

        timestamp = datetime.now().isoformat()

        log_entry = {
            "timestamp": timestamp,
            "type": "INFO",
            "message": message,
            "extra_data": extra_data,
        }

        self._write_log(log_entry)


# Global logger instance
_global_logger = None


def get_logger(module=None):
    """Get the global logger instance."""
    global _global_logger
    if _global_logger is None:
        _global_logger = APILogger(module)
    return _global_logger


def log_api_call(
    method,
    url,
    headers=None,
    data=None,
    timeout=None,
    status_code=None,
    response_headers=None,
    response_body=None,
    error=None,
    module=None,
):
    """
    Convenience function to log a complete API call.
    This can be used as a wrapper around existing API calls.
    """
    logger = get_logger(module)

    if not logger.enabled:
        return

    start_time = time.time()
    request_id = logger.request_id + 1

    # Log request
    logger.log_request(method, url, headers, data, timeout)

    # If this is a synchronous call, we can log the response immediately
    if status_code is not None:
        duration = (time.time() - start_time) * 1000  # Convert to milliseconds
        logger.log_response(
            request_id, status_code, response_headers, response_body, duration
        )

    if error is not None:
        logger.log_error(request_id, str(error), error)

    return request_id
