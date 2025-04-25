# Session Keeper

The Session Keeper is a tool for maintaining persistent sessions with the Fogis API.

## Overview

The Session Keeper makes periodic requests to the Fogis API to keep your session active. This is useful for:

- Long-running applications that need to maintain authentication
- Automated systems that need to interact with the Fogis API
- Avoiding frequent re-authentication

## Usage

### Basic Usage

```bash
# Save cookies from a Fogis login
fogis-save-cookies --username YOUR_USERNAME --password YOUR_PASSWORD

# Start the session keeper with those cookies
fogis-session-keeper --cookies-file fogis_cookies.json --interval 1800 --monitor --log-file fogis_session.log
```

### Command-Line Options

#### fogis-save-cookies

```
--username USERNAME     Fogis username
--password PASSWORD     Fogis password
--output FILE           Output file path (default: fogis_cookies.json)
```

#### fogis-session-keeper

```
--cookies-file FILE     Path to cookies JSON file
--interval SECONDS      Time between session checks in seconds (default: 300)
--monitor               Monitor and log cookie changes
--log-file FILE         Path to log file
```

### Checking Session Status

You can check the status of a running session keeper:

```bash
fogis-check-status
```

This will show:
- Whether the session keeper is running
- Number of successful checks
- Number of failed checks
- Number of relogins
- Runtime
- Last activity time

## Advanced Usage

### Using Environment Variables

You can use environment variables instead of command-line options:

```bash
export FOGIS_USERNAME=your_username
export FOGIS_PASSWORD=your_password

fogis-save-cookies
```

### Long-Running Sessions

For long-running sessions, you can:

1. Use a terminal multiplexer like `screen` or `tmux`:
   ```bash
   screen -S fogis-session
   fogis-session-keeper --cookies-file fogis_cookies.json --interval 1800 --monitor
   # Press Ctrl+A followed by D to detach
   ```

2. Use Docker (see [Docker Usage](docker.md))

3. Use a system service (systemd, etc.)

## Session Timeout Testing

You can test how long a session remains valid without activity:

```bash
# Test with standard intervals
python -m fogis_session_tools.test_session_timeout --cookies-file fogis_cookies.json

# Test with adaptive intervals
python -m fogis_session_tools.auto_test_session_timeout --cookies-file fogis_cookies.json --adaptive
```

This will help you determine the optimal interval for session checks.
