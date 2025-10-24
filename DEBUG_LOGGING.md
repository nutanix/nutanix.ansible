# Nutanix Ansible Collection - Debug Logging

This document explains how to enable detailed API call logging in the Nutanix Ansible collection for debugging purposes.

## Overview

The Nutanix Ansible collection now includes comprehensive API call logging that can be enabled to help with debugging and troubleshooting. When enabled, the logger will capture:

- All HTTP requests (method, URL, headers, body)
- All HTTP responses (status code, headers, body)
- Request/response timing
- Error details
- Sensitive data is automatically redacted

## Enabling Debug Logging

### Method 1: Environment Variable (Recommended)

Set the `NUTANIX_DEBUG_LOGGING` environment variable to `true`:

```bash
export NUTANIX_DEBUG_LOGGING=true
```

### Method 2: Module Parameter

Add the `debug_logging` parameter to your Ansible tasks:

```yaml
- name: Create VM with debug logging
  nutanix.ncp.nutanix_vm:
    name: "test-vm"
    debug_logging: true
    # ... other parameters
```

### Method 3: Custom Log File Location

By default, logs are written to `/tmp/nutanix_api_debug.log`. You can specify a custom location:

```bash
export NUTANIX_DEBUG_LOG_FILE=/path/to/your/custom.log
```

## Log Format

The logs are written in JSON format with the following structure:

### Request Log Entry
```json
{
  "request_id": 1,
  "timestamp": "2024-01-15T10:30:45.123456",
  "type": "REQUEST",
  "method": "POST",
  "url": "https://10.0.0.1:9440/api/nutanix/v3/vms",
  "headers": {
    "Content-Type": "application/json",
    "Authorization": "[REDACTED]"
  },
  "data": {
    "name": "test-vm",
    "description": "Test VM"
  },
  "timeout": 30
}
```

### Response Log Entry
```json
{
  "request_id": 1,
  "timestamp": "2024-01-15T10:30:45.456789",
  "type": "RESPONSE",
  "status_code": 200,
  "headers": {
    "Content-Type": "application/json"
  },
  "body": {
    "status": {
      "state": "COMPLETE"
    }
  },
  "duration_ms": 1234
}
```

### Error Log Entry
```json
{
  "request_id": 2,
  "timestamp": "2024-01-15T10:31:00.789012",
  "type": "ERROR",
  "error_message": "HTTP 400 Bad Request",
  "exception": "HTTPError: 400 Client Error: Bad Request"
}
```

## Security Features

The logger automatically redacts sensitive information:

- **Headers**: `Authorization`, `X-API-Key`, `Cookie`, `Set-Cookie`
- **Data Fields**: Any field containing `password`, `token`, `secret`, `key`, `credential`, or `auth`
- **Large Responses**: Truncated to prevent log file bloat

## Usage Examples

### Basic Playbook with Debug Logging

```yaml
---
- name: Create VM with API logging
  hosts: localhost
  gather_facts: false
  vars:
    NUTANIX_DEBUG_LOGGING: true
    NUTANIX_DEBUG_LOG_FILE: /tmp/nutanix_debug.log
  
  tasks:
    - name: Create VM
      nutanix.ncp.nutanix_vm:
        name: "test-vm"
        nutanix_host: "{{ nutanix_host }}"
        nutanix_username: "{{ nutanix_username }}"
        nutanix_password: "{{ nutanix_password }}"
        debug_logging: true
```

### Using Environment Variables

```bash
# Enable debug logging
export NUTANIX_DEBUG_LOGGING=true
export NUTANIX_DEBUG_LOG_FILE=/var/log/nutanix_ansible_debug.log

# Run your playbook
ansible-playbook -i inventory playbook.yml
```

### Per-Task Debug Logging

```yaml
- name: Create VM with debug logging
  nutanix.ncp.nutanix_vm:
    name: "test-vm"
    debug_logging: true
    # ... other parameters

- name: Create another VM without debug logging
  nutanix.ncp.nutanix_vm:
    name: "test-vm-2"
    # ... other parameters (no debug_logging parameter)
```

## Log Analysis

### Viewing Logs

```bash
# View the log file
cat /tmp/nutanix_api_debug.log

# Follow logs in real-time
tail -f /tmp/nutanix_api_debug.log

# Filter by request ID
grep '"request_id": 1' /tmp/nutanix_api_debug.log
```

### Common Use Cases

1. **API Call Debugging**: See exactly what requests are being made
2. **Performance Analysis**: Check request/response timing
3. **Error Investigation**: Understand why API calls are failing
4. **Integration Testing**: Verify API interactions during development

## Performance Considerations

- Debug logging adds minimal overhead when disabled
- When enabled, there is a small performance impact due to I/O operations
- Large response bodies are truncated to prevent excessive disk usage
- Consider the log file size when running long playbooks

## Troubleshooting

### Log File Not Created
- Check file permissions for the log directory
- Ensure the `NUTANIX_DEBUG_LOGGING` environment variable is set correctly
- Verify the module parameter is set to `true`

### Missing Log Entries
- Ensure you're using modules from the Nutanix collection
- Check that the module is making API calls (some modules may not make calls in certain scenarios)
- Verify the logging is enabled at the right level (environment variable vs module parameter)

### Large Log Files
- Use log rotation to manage file size
- Consider using the `NUTANIX_DEBUG_LOG_FILE` environment variable to specify a different location
- Monitor disk space when running long playbooks with debug logging enabled

## Integration with CI/CD

For automated testing and debugging in CI/CD pipelines:

```yaml
# GitHub Actions example
- name: Run Ansible with debug logging
  run: |
    export NUTANIX_DEBUG_LOGGING=true
    export NUTANIX_DEBUG_LOG_FILE=/tmp/ansible_debug.log
    ansible-playbook playbook.yml
    
- name: Upload debug logs
  uses: actions/upload-artifact@v2
  if: always()
  with:
    name: nutanix-debug-logs
    path: /tmp/ansible_debug.log
```

This debug logging feature provides comprehensive visibility into API interactions, making it easier to troubleshoot issues and understand the behavior of the Nutanix Ansible collection.



