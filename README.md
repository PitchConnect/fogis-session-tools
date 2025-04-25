# Fogis Session Tools

A collection of tools for managing persistent sessions with the Fogis API (Svenska Fotbollförbundet).

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Features

* **Session Management**: Maintain persistent sessions with the Fogis API
* **Cookie Management**: Save and load session cookies
* **Session Monitoring**: Track session status and activity
* **Timeout Testing**: Test how long sessions remain valid
* **Docker Support**: Run as a containerized service
* **Interactive GUI**: Text-based menu interface for all tools

## Installation

### Using pip

```bash
pip install fogis-session-tools
```

### From Source

```bash
git clone https://github.com/YOUR_USERNAME/fogis-session-tools.git
cd fogis-session-tools
pip install -e .
```

### Using Docker

```bash
# Pull the Docker image
docker pull YOUR_USERNAME/fogis-session-tools:latest

# Run the interactive GUI
docker run -it --rm -v $(pwd)/data:/app/data YOUR_USERNAME/fogis-session-tools
```

## Quick Start

### Interactive GUI

```bash
# Run the interactive menu interface
fogis-tools
```

### Session Keeper

```bash
# Save cookies from a Fogis login
fogis-save-cookies --username YOUR_USERNAME --password YOUR_PASSWORD

# Start the session keeper with those cookies
fogis-session-keeper --cookies-file fogis_cookies.json --interval 1800 --monitor
```

### Docker

```bash
# Navigate to the repository directory
cd fogis-session-tools

# Run the helper script
./run_docker.sh help
```

## Documentation

For detailed documentation, see:

* [Session Keeper](docs/session_keeper.md)
* [Docker Usage](docs/docker.md)
* [API Reference](docs/api_reference.md)

## Dependencies

* [fogis-api-client-timmybird](https://pypi.org/project/fogis-api-client-timmybird/): Python client for the Fogis API
* [python-dotenv](https://pypi.org/project/python-dotenv/): For loading environment variables

## Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
