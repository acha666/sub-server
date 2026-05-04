FROM mcr.microsoft.com/devcontainers/python:3.13

# Install system dependencies if needed
# RUN apt-get update && apt-get install -y \
#     some-package && \
#     rm -rf /var/lib/apt/lists/*

# Install Python development tools
RUN pip install --no-cache-dir \
    build \
    twine

# Optional: pre-install common Python tools
# RUN pip install --no-cache-dir ipython jupyter
