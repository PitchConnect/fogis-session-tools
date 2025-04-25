FROM python:3.9-slim

WORKDIR /app

# Install dependencies
RUN pip install --no-cache-dir fogis-api-client-timmybird python-dotenv

# Copy the package files
COPY . /app/

# Install the package
RUN pip install -e .

# Create data directory for persistence
RUN mkdir -p /app/data

# Volume for persistent data
VOLUME /app/data

# Set working directory to data for file outputs
WORKDIR /app/data

# Default command shows help
ENTRYPOINT ["fogis-tools"]
