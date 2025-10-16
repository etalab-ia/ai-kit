# Platform-Specific Setup Guide

Setup instructions for different operating systems and environments.

## Table of Contents

- [macOS](#macos)
- [Linux](#linux)
- [Windows](#windows)
- [Docker](#docker)
- [Edge Cases](#edge-cases)

## macOS

### Prerequisites

```bash
# Install Homebrew (if not installed)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install just
brew install just

# Install uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install Volta
curl https://get.volta.sh | bash
```

### Setup

```bash
cd ai-kit
just setup
```

### Common Issues

#### Older Python Version
**Issue**: System Python is older than 3.12

**Solution**: uv will automatically install Python 3.12.10
```bash
uv python install 3.12.10
```

#### Tool Conflicts (pip/virtualenv vs uv)
**Issue**: Conflicts with existing pip or virtualenv

**Solution**: uv manages its own environment
```bash
# Remove conflicting tools (optional)
pip uninstall virtualenv

# uv handles everything
uv sync
```

## Linux

### Ubuntu/Debian

```bash
# Update package list
sudo apt-get update

# Install curl and build essentials
sudo apt-get install -y curl build-essential

# Install just
curl --proto '=https' --tlsv1.2 -sSf https://just.systems/install.sh | bash -s -- --to ~/bin
echo 'export PATH="$HOME/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc

# Install uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install Volta
curl https://get.volta.sh | bash
```

### Fedora/RHEL/CentOS

```bash
# Install development tools
sudo dnf groupinstall "Development Tools"

# Install just
curl --proto '=https' --tlsv1.2 -sSf https://just.systems/install.sh | bash -s -- --to ~/bin
echo 'export PATH="$HOME/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc

# Install uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install Volta
curl https://get.volta.sh | bash
```

### Arch Linux

```bash
# Install just
sudo pacman -S just

# Install uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install Volta
curl https://get.volta.sh | bash
```

### Common Issues

#### Binary Dependencies
**Issue**: Missing system libraries for Python packages

**Solution**: Install development headers
```bash
# Ubuntu/Debian
sudo apt-get install -y python3-dev libffi-dev libssl-dev

# Fedora/RHEL
sudo dnf install python3-devel libffi-devel openssl-devel
```

## Windows

### Prerequisites

**Option 1: WSL2 (Recommended)**

```powershell
# Install WSL2
wsl --install

# Then follow Linux instructions inside WSL
```

**Option 2: Native Windows**

```powershell
# Install Scoop (package manager)
irm get.scoop.sh | iex

# Install just
scoop install just

# Install uv
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# Install Volta
# Download installer from https://volta.sh/
```

### Setup

```powershell
cd ai-kit
just setup
```

### Common Issues

#### Line Endings (CRLF vs LF)
**Issue**: Git converts line endings causing pre-commit failures

**Solution**: Configure git
```bash
git config --global core.autocrlf input
git config --global core.eol lf

# Fix existing files
uv run pre-commit run --all-files
```

#### Path Length Limit
**Issue**: Windows MAX_PATH limit (260 characters)

**Solution**: Enable long paths
```powershell
# Run as Administrator
New-ItemProperty -Path "HKLM:\SYSTEM\CurrentControlSet\Control\FileSystem" -Name "LongPathsEnabled" -Value 1 -PropertyType DWORD -Force
```

#### PowerShell Execution Policy
**Issue**: Scripts blocked by execution policy

**Solution**: Allow scripts
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

## Docker

### Development Container

```dockerfile
# Dockerfile.dev
FROM python:3.12.10-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    build-essential \
    git \
    && rm -rf /var/lib/apt/lists/*

# Install just
RUN curl --proto '=https' --tlsv1.2 -sSf https://just.systems/install.sh | bash -s -- --to /usr/local/bin

# Install uv
RUN curl -LsSf https://astral.sh/uv/install.sh | sh
ENV PATH="/root/.cargo/bin:$PATH"

# Install Volta
RUN curl https://get.volta.sh | bash
ENV VOLTA_HOME="/root/.volta"
ENV PATH="$VOLTA_HOME/bin:$PATH"

WORKDIR /workspace

# Copy project files
COPY . .

# Setup
RUN just setup

CMD ["/bin/bash"]
```

### Usage

```bash
# Build image
docker build -f Dockerfile.dev -t ai-kit-dev .

# Run container
docker run -it --rm -v $(pwd):/workspace ai-kit-dev

# Inside container
just test
```

### Docker Compose

```yaml
# docker-compose.yml
version: '3.8'

services:
  dev:
    build:
      context: .
      dockerfile: Dockerfile.dev
    volumes:
      - .:/workspace
      - /workspace/.venv  # Don't sync .venv
      - /workspace/node_modules  # Don't sync node_modules
    command: /bin/bash
```

## Edge Cases

### Older Python Version on System

**Issue**: System has Python older than 3.12

**Solution**: uv installs Python 3.12.10 automatically
```bash
# uv will download and use Python 3.12.10
uv python install 3.12.10
uv sync
```

### Tool Conflicts (pip/virtualenv vs uv)

**Issue**: Existing pip or virtualenv interferes

**Solution**: uv is self-contained
```bash
# uv doesn't conflict with pip
# It manages its own environments in .venv/
uv sync
```

### Platform-Specific Binary Dependencies

**Issue**: Python packages with C extensions fail to build

**Solution**: Install development headers

**macOS**:
```bash
xcode-select --install
```

**Linux**:
```bash
# Ubuntu/Debian
sudo apt-get install python3-dev

# Fedora/RHEL
sudo dnf install python3-devel
```

**Windows**:
```powershell
# Install Visual Studio Build Tools
# https://visualstudio.microsoft.com/downloads/
```

### Proxy/Firewall Issues

**Issue**: Corporate proxy blocks downloads

**Solution**: Configure proxy
```bash
# Set proxy environment variables
export HTTP_PROXY=http://proxy.example.com:8080
export HTTPS_PROXY=http://proxy.example.com:8080

# For uv
export UV_HTTP_PROXY=http://proxy.example.com:8080

# For pnpm
pnpm config set proxy http://proxy.example.com:8080
pnpm config set https-proxy http://proxy.example.com:8080
```

### Disk Space Issues

**Issue**: Not enough disk space for dependencies

**Solution**: Clean caches
```bash
# Clean all caches
just clean

# Clean uv cache
uv cache clean

# Clean pnpm cache
pnpm store prune
```

## Verification

After setup, verify everything works:

```bash
# Check tool versions
python --version  # 3.12.10
node --version    # v22.14.0
pnpm --version    # 10.18.2

# Run tests
just test

# Run linting
just lint
```

## Getting Help

If you encounter issues not covered here:

1. Check [CONTRIBUTING.md](../CONTRIBUTING.md) troubleshooting section
2. Search [GitHub Issues](https://github.com/your-org/ai-kit/issues)
3. Ask in [GitHub Discussions](https://github.com/your-org/ai-kit/discussions)
