# Quick Start: Debug Logging for Nutanix Ansible Collection

## What is Debug Logging?

Debug logging captures detailed information about all API calls made by the Nutanix Ansible collection, including:
- HTTP requests (method, URL, headers, body)
- HTTP responses (status code, headers, body)
- Request/response timing
- Error details
- **Sensitive data is automatically redacted for security**

## Quick Start

### 1. Enable Debug Logging (Choose one method)

**Method A: Environment Variable (Global)**
```bash
export NUTANIX_DEBUG_LOGGING=true
ansible-playbook playbook.yml
```

**Method B: Module Parameter (Per-task)**
```yaml
- name: Get VM info with debug logging
  nutanix.ncp.nutanix_vm_info:
    nutanix_host: "{{ nutanix_host }}"
    nutanix_username: "{{ nutanix_username }}"
    nutanix_password: "{{ nutanix_password }}"
    debug_logging: true
```

### 2. View the Logs

By default, logs are written to `/tmp/nutanix_api_debug.log`:

```bash
# View the logs
cat /tmp/nutanix_api_debug.log

# Follow logs in real-time
tail -f /tmp/nutanix_api_debug.log

# Filter by specific request
grep '"request_id": 1' /tmp/nutanix_api_debug.log
```

### 3. Custom Log File Location

```bash
export NUTANIX_DEBUG_LOG_FILE=/path/to/your/custom.log
ansible-playbook playbook.yml
```

## Example Log Output

```json
{
  "request_id": 1,
  "timestamp": "2024-01-15T10:30:45.123456",
  "type": "REQUEST",
  "method": "GET",
  "url": "https://10.0.0.1:9440/api/nutanix/v3/vms",
  "headers": {
    "Content-Type": "application/json",
    "Authorization": "[REDACTED]"
  },
  "data": {
    "name": "test-vm"
  },
  "timeout": 30
}
```

## Common Use Cases

### 1. Debugging API Issues
```bash
# Enable logging and run your playbook
export NUTANIX_DEBUG_LOGGING=true
ansible-playbook debug_playbook.yml

# Check what API calls were made
cat /tmp/nutanix_api_debug.log | grep "REQUEST"
```

### 2. Performance Analysis
```bash
# Check request timing
cat /tmp/nutanix_api_debug.log | grep "duration_ms"
```

### 3. Error Investigation
```bash
# Find failed requests
cat /tmp/nutanix_api_debug.log | grep "ERROR"
```

## Security Features

- **Automatic Redaction**: Sensitive headers and data fields are automatically redacted
- **No Performance Impact**: When disabled, logging adds zero overhead
- **Configurable**: Can be enabled/disabled per task or globally

## Troubleshooting

### Log File Not Created
- Check if `NUTANIX_DEBUG_LOGGING=true` is set
- Verify file permissions for the log directory
- Ensure you're using Nutanix collection modules

### Missing Log Entries
- Some modules may not make API calls in certain scenarios
- Check that the module is actually executing (not skipped)
- Verify the module parameter or environment variable is set correctly

## Advanced Usage

### Per-Task Control
```yaml
- name: Task with debug logging
  nutanix.ncp.nutanix_vm_info:
    debug_logging: true
    # ... other parameters

- name: Task without debug logging  
  nutanix.ncp.nutanix_cluster_info:
    # ... other parameters (no debug_logging)
```

### CI/CD Integration
```yaml
# GitHub Actions example
- name: Run with debug logging
  run: |
    export NUTANIX_DEBUG_LOGGING=true
    ansible-playbook playbook.yml
    
- name: Upload debug logs
  uses: actions/upload-artifact@v2
  with:
    name: nutanix-debug-logs
    path: /tmp/nutanix_api_debug.log
```

## Test the Implementation

Run the test script to verify everything works:

```bash
cd /path/to/nutanix.ansible
python3 scripts/test_debug_logging.py
```

This will test:
- Logging when enabled
- Logging when disabled  
- Sensitive data redaction
- Log file creation

## Need Help?

- Check the full documentation: `DEBUG_LOGGING.md`
- View example playbooks in the `examples/` directory
- Run the test script to verify your setup
