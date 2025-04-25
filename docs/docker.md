# Docker Usage

This document explains how to use the Fogis Session Tools with Docker.

## Quick Start

### Prerequisites

- Docker and Docker Compose installed
- Fogis account credentials

### Setup

1. Create a `.env` file in the repository root directory:

```
FOGIS_USERNAME=your_username
FOGIS_PASSWORD=your_password
INTERVAL=1800  # Session check interval in seconds (optional, default: 1800)
```

2. Create a data directory for persistence:

```bash
mkdir -p data
```

### Running the Interactive GUI

```bash
# Using docker-compose
docker-compose run --rm session-gui

# Using the helper script
./run_docker.sh gui
```

This will start the interactive menu interface where you can:
- Login and save cookies
- Maintain a session
- Check session status
- Test session timeout
- Test cookie uniqueness

### Running the Session Keeper as a Service

```bash
# Using docker-compose
docker-compose up -d session-keeper

# Using the helper script
./run_docker.sh keeper
```

This will start a long-running service that maintains your Fogis session.

### Running a Session Timeout Test

```bash
# Using docker-compose
docker-compose up -d timeout-test

# Using the helper script
./run_docker.sh test
```

This will start a service that tests how long a session remains valid without activity.

## Container Services

The `docker-compose.yml` file defines three services:

### 1. session-gui

An interactive service that provides a text-based menu interface for all session management tools.

```bash
# Start the GUI
docker-compose run --rm session-gui
```

### 2. session-keeper

A long-running service that maintains your Fogis session by making periodic requests.

```bash
# Start the service
docker-compose up -d session-keeper

# View logs
docker-compose logs -f session-keeper

# Check status
docker-compose exec session-keeper fogis-check-status
```

### 3. timeout-test

A service that tests how long a session remains valid without activity.

```bash
# Start the test
docker-compose up -d timeout-test

# View logs
docker-compose logs -f timeout-test
```

## Helper Script

The `run_docker.sh` script provides a simple interface for common Docker operations:

```bash
# Show help
./run_docker.sh help

# Start the interactive GUI
./run_docker.sh gui

# Run the session keeper as a service
./run_docker.sh keeper

# Run a session timeout test
./run_docker.sh test

# Check the status of the session keeper
./run_docker.sh status

# View logs of the session keeper
./run_docker.sh logs

# View logs of the timeout test
./run_docker.sh logs test

# Stop all containers
./run_docker.sh stop
```

## Data Persistence

All data (cookies, logs, status files) is stored in the `data` directory, which is mounted as a volume in the containers. This ensures that your data persists across container restarts.

## Customization

### Environment Variables

You can customize the behavior of the containers by setting environment variables in the `.env` file:

- `FOGIS_USERNAME`: Your Fogis username
- `FOGIS_PASSWORD`: Your Fogis password
- `INTERVAL`: Session check interval in seconds (default: 1800)

## Troubleshooting

### Container Fails to Start

If a container fails to start, check the logs:

```bash
docker-compose logs session-keeper
```

### Session Expires Too Quickly

If your session expires too quickly, try decreasing the check interval:

```bash
# Edit .env file
INTERVAL=900  # 15 minutes

# Restart the service
docker-compose restart session-keeper
```

### Data Not Persisting

Make sure the data directory exists and has the correct permissions:

```bash
mkdir -p data
chmod 777 data
```
