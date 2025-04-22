FROM python:3.13-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy project configuration files first to leverage Docker caching
COPY pyproject.toml uv.lock ./

# Install uv for faster Python package management
RUN pip install --no-cache-dir uv

# Install dependencies using uv and python-dotenv
RUN uv pip install --no-cache-dir -e .
RUN uv pip install --no-cache-dir python-dotenv httpx

# Copy the application code
COPY . .

# Expose the port
EXPOSE 8080

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV SERVER_NAME=${SERVER_NAME:-"instalily-mcp-server"}
# Do not set sensitive env vars like API keys in the Dockerfile

# Run the application with default arguments
CMD ["python", "server.py", "--host=0.0.0.0", "--port=8080"]