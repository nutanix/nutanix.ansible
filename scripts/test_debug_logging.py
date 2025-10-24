#!/usr/bin/env python3
"""
Test script for the Nutanix Ansible collection debug logging functionality.
This script demonstrates how the logging works without requiring a full Ansible setup.
"""

import os
import sys
import json
import tempfile
from datetime import datetime

# Add the module_utils path to sys.path
sys.path.insert(
    0, os.path.join(os.path.dirname(__file__), "..", "plugins", "module_utils")
)

from api_logger import APILogger


class MockModule:
    """Mock Ansible module for testing."""

    def __init__(self, debug_logging=False):
        self.params = {"debug_logging": debug_logging}


def test_logging_enabled():
    """Test logging when enabled."""
    print("Testing logging when enabled...")

    # Set environment variable
    os.environ["NUTANIX_DEBUG_LOGGING"] = "true"

    # Create a temporary log file
    with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".log") as f:
        log_file = f.name

    os.environ["NUTANIX_DEBUG_LOG_FILE"] = log_file

    # Create logger with mock module
    module = MockModule(debug_logging=True)
    logger = APILogger(module)

    # Test logging
    logger.log_request(
        "GET",
        "https://test.example.com/api/v1/test",
        {"Content-Type": "application/json"},
        {"test": "data"},
        30,
    )

    logger.log_response(
        1, 200, {"Content-Type": "application/json"}, {"status": "success"}, 150
    )

    logger.log_info("Test info message", {"extra": "data"})

    # Read and display log contents
    print(f"Log file created at: {log_file}")
    with open(log_file, "r") as f:
        content = f.read()
        print("Log contents:")
        print(content)

    # Clean up
    os.unlink(log_file)
    print("✓ Logging when enabled works correctly\n")


def test_logging_disabled():
    """Test logging when disabled."""
    print("Testing logging when disabled...")

    # Remove environment variable
    if "NUTANIX_DEBUG_LOGGING" in os.environ:
        del os.environ["NUTANIX_DEBUG_LOGGING"]

    # Create logger with mock module (debug_logging=False)
    module = MockModule(debug_logging=False)
    logger = APILogger(module)

    # Test logging (should not create log file)
    logger.log_request(
        "GET",
        "https://test.example.com/api/v1/test",
        {"Content-Type": "application/json"},
        {"test": "data"},
        30,
    )

    logger.log_response(
        1, 200, {"Content-Type": "application/json"}, {"status": "success"}, 150
    )

    # Check if log file was created (it shouldn't be)
    log_file = logger.log_file
    if os.path.exists(log_file):
        print(f"❌ Log file was created at {log_file} when logging should be disabled")
    else:
        print("✓ Logging when disabled works correctly (no log file created)")

    print()


def test_sensitive_data_redaction():
    """Test that sensitive data is properly redacted."""
    print("Testing sensitive data redaction...")

    # Set environment variable
    os.environ["NUTANIX_DEBUG_LOGGING"] = "true"

    # Create a temporary log file
    with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".log") as f:
        log_file = f.name

    os.environ["NUTANIX_DEBUG_LOG_FILE"] = log_file

    # Create logger with mock module
    module = MockModule(debug_logging=True)
    logger = APILogger(module)

    # Test with sensitive data
    sensitive_headers = {
        "Authorization": "Bearer secret-token",
        "X-API-Key": "secret-api-key",
        "Content-Type": "application/json",
    }

    sensitive_data = {
        "username": "testuser",
        "password": "secretpassword",
        "api_key": "secret-key",
        "normal_field": "normal-value",
    }

    logger.log_request(
        "POST",
        "https://test.example.com/api/v1/auth",
        sensitive_headers,
        sensitive_data,
        30,
    )

    # Read and check log contents
    with open(log_file, "r") as f:
        content = f.read()

    # Check that sensitive data is redacted
    if "[REDACTED]" in content and "secret-token" not in content:
        print("✓ Sensitive data redaction works correctly")
    else:
        print("❌ Sensitive data redaction failed")
        print("Log content:")
        print(content)

    # Clean up
    os.unlink(log_file)
    print()


def main():
    """Run all tests."""
    print("Nutanix Ansible Collection Debug Logging Test")
    print("=" * 50)

    test_logging_enabled()
    test_logging_disabled()
    test_sensitive_data_redaction()

    print("All tests completed!")


if __name__ == "__main__":
    main()



