# API Reference

This document provides a reference for the Python API of the Fogis Session Tools.

## SessionKeeper

The `SessionKeeper` class is the main component for maintaining persistent sessions with the Fogis API.

```python
from fogis_session_tools import SessionKeeper

# Create a session keeper with credentials
keeper = SessionKeeper(username="your_username", password="your_password")

# Or with existing cookies
keeper = SessionKeeper(cookies=cookies)

# Start the session keeper
keeper.start()

# Get the authenticated client
client = keeper.get_client()

# Use the client for API calls
matches = client.fetch_matches_list()

# Stop the session keeper when done
keeper.stop()
```

### Constructor

```python
SessionKeeper(
    username=None,
    password=None,
    client=None,
    cookies=None,
    check_interval=300,
    monitor_cookies=False,
    verbose=False,
    log_file=None,
    notification_email=None,
    notify_on_changes=True
)
```

Parameters:
- `username` (str, optional): Fogis username (not needed if client or cookies is provided)
- `password` (str, optional): Fogis password (not needed if client or cookies is provided)
- `client` (FogisApiClient, optional): Pre-authenticated client
- `cookies` (dict, optional): Session cookies
- `check_interval` (int): Time between session checks in seconds (default: 300)
- `monitor_cookies` (bool): Whether to monitor and log cookie changes
- `verbose` (bool): Enable verbose logging
- `log_file` (str, optional): Path to log file
- `notification_email` (str, optional): Email to send notifications to
- `notify_on_changes` (bool): Whether to send notifications on cookie changes

### Methods

#### start()

Start the session keeper thread.

```python
keeper.start()
```

#### stop()

Stop the session keeper thread.

```python
keeper.stop()
```

#### get_client()

Get the authenticated client.

```python
client = keeper.get_client()
```

Returns:
- `FogisApiClient`: The authenticated client

#### get_status()

Get the current status of the session keeper.

```python
status = keeper.get_status()
```

Returns:
- `dict`: Status information including running state, check counts, and timing

## Utility Functions

### test_session_timeout()

Test how long a session remains valid without activity.

```python
from fogis_session_tools import test_session_timeout

test_session_timeout(
    cookies_file="fogis_cookies.json",
    start_interval=300,
    max_interval=86400,
    multiplier=1.5,
    log_file="session_timeout_test.log"
)
```

Parameters:
- `cookies_file` (str): Path to the cookies JSON file
- `start_interval` (int): Starting interval in seconds (default: 300)
- `max_interval` (int): Maximum interval to test in seconds (default: 86400)
- `multiplier` (float): Factor to increase interval by each time (default: 1.5)
- `log_file` (str): Path to log file

### test_cookie_uniqueness()

Test if multiple logins generate unique cookies.

```python
from fogis_session_tools import test_cookie_uniqueness

test_cookie_uniqueness(
    username="your_username",
    password="your_password",
    delay=5
)
```

Parameters:
- `username` (str): Fogis username
- `password` (str): Fogis password
- `delay` (int): Delay between logins in seconds (default: 5)
