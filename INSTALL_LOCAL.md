# 🚀 Complete OpenHands Local Installation Guide

This guide will help you install OpenHands on your local machine with **ALL features**:
- ✅ Visual Studio Code integration
- ✅ Auto browser automation
- ✅ GPU acceleration with DeepSeek
- ✅ Full coding agent capabilities

---

## 📋 Prerequisites

### System Requirements
- **OS**: Ubuntu 20.04+, Debian 11+, Windows 10/11 (WSL2), macOS
- **RAM**: 16GB minimum (32GB recommended)
- **GPU**: NVIDIA GPU with 8GB+ VRAM (for local LLM)
- **Storage**: 50GB+ free space
- **Docker**: Docker Desktop or Docker Engine

---

## 🔧 Step 1: Install Docker

### Ubuntu/Debian
```bash
# Remove old versions
sudo apt-get remove docker docker-engine docker.io containerd runc

# Install prerequisites
sudo apt-get update
sudo apt-get install -y ca-certificates curl gnupg lsb-release

# Add Docker's official GPG key
sudo mkdir -p /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg

# Set up repository
echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# Install Docker
sudo apt-get update
sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

# Add your user to docker group (logout/login required)
sudo usermod -aG docker $USER
newgrp docker
```

### Windows
1. Download and install [Docker Desktop for Windows](https://www.docker.com/products/docker-desktop/)
2. Enable WSL2 backend in Docker Desktop settings
3. Restart your computer

### macOS
1. Download and install [Docker Desktop for Mac](https://www.docker.com/products/docker-desktop/)
2. Start Docker Desktop
3. Allocate at least 8GB RAM in Docker settings

---

## 🎮 Step 2: Install NVIDIA GPU Support (For Local LLM)

### Ubuntu/Debian
```bash
# Install NVIDIA driver
sudo apt-get update
sudo apt-get install -y ubuntu-drivers-common
sudo ubuntu-drivers autoinstall
sudo reboot

# After reboot, verify driver
nvidia-smi

# Install NVIDIA Container Toolkit
distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg
curl -s -L https://nvidia.github.io/libnvidia-container/$distribution/libnvidia-container.list | \
    sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' | \
    sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list

sudo apt-get update
sudo apt-get install -y nvidia-container-toolkit
sudo nvidia-ctk runtime configure --runtime=docker
sudo systemctl restart docker

# Test GPU in Docker
docker run --rm --gpus all nvidia/cuda:12.0-base nvidia-smi
```

### Windows (WSL2)
1. Install latest NVIDIA drivers from [nvidia.com](https://www.nvidia.com/Download/index.aspx)
2. GPU support is automatic in Docker Desktop with WSL2 backend

---

## 📦 Step 3: Install OpenHands

### Option A: Quick Start (Recommended)
```bash
# Create project directory
mkdir -p ~/openhands-local && cd ~/openhands-local

# Clone the setup files
git clone https://github.com/9501893704rahul/OPENHANDS.git .

# Or download directly
curl -O https://raw.githubusercontent.com/9501893704rahul/OPENHANDS/main/docker-compose.yml
curl -O https://raw.githubusercontent.com/9501893704rahul/OPENHANDS/main/.env.example
curl -O https://raw.githubusercontent.com/9501893704rahul/OPENHANDS/main/setup-deepseek.sh
chmod +x setup-deepseek.sh

# Run setup
./setup-deepseek.sh --full
```

### Option B: Manual Docker Run
```bash
# Create directories
mkdir -p ~/openhands-local/{workspace,openhands-state}
cd ~/openhands-local

# Run OpenHands
docker run -d \
    --name openhands \
    --gpus all \
    -p 3000:3000 \
    -v /var/run/docker.sock:/var/run/docker.sock \
    -v $(pwd)/workspace:/opt/workspace_base \
    -v $(pwd)/openhands-state:/.openhands-state \
    -e SANDBOX_RUNTIME_CONTAINER_IMAGE=docker.all-hands.dev/all-hands-ai/runtime:main \
    docker.all-hands.dev/all-hands-ai/openhands:main
```

### Option C: Using Docker Compose (Full Setup)
```bash
# Create directory
mkdir -p ~/openhands-local && cd ~/openhands-local

# Create docker-compose.yml
cat > docker-compose.yml << 'EOF'
version: '3.8'

services:
  openhands:
    image: docker.all-hands.dev/all-hands-ai/openhands:main
    container_name: openhands
    pull_policy: always
    restart: unless-stopped
    environment:
      - SANDBOX_RUNTIME_CONTAINER_IMAGE=docker.all-hands.dev/all-hands-ai/runtime:main
      - LOG_ALL_EVENTS=true
    env_file:
      - .env
    ports:
      - "3000:3000"
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
      - ./workspace:/opt/workspace_base
      - ./openhands-state:/.openhands-state
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: all
              capabilities: [gpu]
    extra_hosts:
      - "host.docker.internal:host-gateway"

  ollama:
    image: ollama/ollama:latest
    container_name: ollama
    pull_policy: always
    restart: unless-stopped
    ports:
      - "11434:11434"
    volumes:
      - ./ollama-models:/root/.ollama
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: all
              capabilities: [gpu]
    profiles:
      - ollama
EOF

# Create .env file
cat > .env << 'EOF'
# DeepSeek Local (GPU accelerated)
LLM_MODEL=ollama/deepseek-coder-v2:16b
LLM_API_KEY=ollama
LLM_BASE_URL=http://host.docker.internal:11434
EOF

# Create directories
mkdir -p workspace openhands-state ollama-models

# Start services
docker compose --profile ollama up -d

# Pull DeepSeek model (wait for download)
docker exec -it ollama ollama pull deepseek-coder-v2:16b
```

---

## 🌐 Step 4: Access OpenHands

1. Open your browser and go to: **http://localhost:3000**

2. On first launch, configure your LLM:
   - **For DeepSeek Local**: 
     - Model: `ollama/deepseek-coder-v2:16b`
     - API Key: `ollama`
     - Base URL: `http://host.docker.internal:11434`
   
   - **For OpenAI**:
     - Model: `gpt-4o`
     - API Key: Your OpenAI API key
   
   - **For Anthropic**:
     - Model: `claude-sonnet-4-20250514`
     - API Key: Your Anthropic API key

---

## 💻 Step 5: VS Code Integration

### Method 1: Open Workspace in VS Code
```bash
# Your projects are in the workspace folder
code ~/openhands-local/workspace
```

### Method 2: VS Code Dev Containers Extension
1. Install the **Dev Containers** extension in VS Code
2. Open VS Code
3. Press `Ctrl+Shift+P` → "Dev Containers: Attach to Running Container"
4. Select the `openhands` container
5. Now you can edit files directly inside the container!

### Method 3: VS Code Remote - SSH (For Remote Servers)
1. Install **Remote - SSH** extension
2. Connect to your server
3. Open the workspace folder

### Method 4: Live Sync with VS Code
```bash
# Install the OpenHands VS Code extension (if available)
# Or use the workspace folder directly - changes sync automatically
```

---

## 🌍 Step 6: Browser Automation Features

OpenHands includes **built-in browser automation**! Here's how to use it:

### Enable Browser in OpenHands
The browser is automatically available. Just ask OpenHands to:
- "Open a browser and go to google.com"
- "Search for Python documentation"
- "Take a screenshot of the current page"
- "Click on the login button"
- "Fill in the form with my details"

### Browser Capabilities
- ✅ Navigate to URLs
- ✅ Click elements
- ✅ Fill forms
- ✅ Take screenshots
- ✅ Extract text content
- ✅ Handle JavaScript-heavy sites
- ✅ Multiple tabs

### Example Prompts
```
"Open the browser, go to github.com, and search for 'openhands'"

"Navigate to stackoverflow.com and find the top Python questions"

"Go to my localhost:8080 and test if the login form works"
```

---

## 🧠 Step 7: Using DeepSeek Locally

### Pull DeepSeek Models
```bash
# Recommended model (16GB VRAM)
docker exec -it ollama ollama pull deepseek-coder-v2:16b

# Smaller model (8GB VRAM)
docker exec -it ollama ollama pull deepseek-coder:6.7b

# Larger model (24GB+ VRAM)
docker exec -it ollama ollama pull deepseek-coder:33b
```

### Test DeepSeek
```bash
# Test the model
docker exec -it ollama ollama run deepseek-coder-v2:16b "Write a Python function to sort a list"
```

### Configure in OpenHands UI
1. Go to http://localhost:3000
2. Click Settings (gear icon)
3. Set:
   - Model: `ollama/deepseek-coder-v2:16b`
   - API Key: `ollama`
   - Base URL: `http://host.docker.internal:11434`

---

## 📁 Step 8: Working with Projects

### Add Existing Projects
```bash
# Copy your project to the workspace
cp -r /path/to/your/project ~/openhands-local/workspace/

# Or create a symlink
ln -s /path/to/your/project ~/openhands-local/workspace/my-project
```

### Start a New Project
1. Open http://localhost:3000
2. Tell OpenHands: "Create a new React project called my-app"
3. OpenHands will create it in the workspace folder
4. Open in VS Code: `code ~/openhands-local/workspace/my-app`

---

## 🔧 Useful Commands

```bash
# Start OpenHands
docker compose --profile ollama up -d

# Stop OpenHands
docker compose --profile ollama down

# View logs
docker compose logs -f

# Restart OpenHands
docker compose --profile ollama restart

# Update to latest version
docker compose pull
docker compose --profile ollama up -d

# Check GPU usage
nvidia-smi -l 1

# List Ollama models
docker exec ollama ollama list

# Remove a model
docker exec ollama ollama rm model-name
```

---

## 🐛 Troubleshooting

### OpenHands won't start
```bash
# Check logs
docker logs openhands

# Ensure Docker socket is accessible
ls -la /var/run/docker.sock

# Fix permissions
sudo chmod 666 /var/run/docker.sock
```

### GPU not detected
```bash
# Verify NVIDIA driver
nvidia-smi

# Test GPU in Docker
docker run --rm --gpus all nvidia/cuda:12.0-base nvidia-smi

# Restart Docker
sudo systemctl restart docker
```

### Ollama connection failed
```bash
# Check if Ollama is running
docker ps | grep ollama

# Test Ollama API
curl http://localhost:11434/api/tags

# Restart Ollama
docker restart ollama
```

### Out of memory
```bash
# Use a smaller model
docker exec ollama ollama pull deepseek-coder:6.7b

# Update .env
echo "LLM_MODEL=ollama/deepseek-coder:6.7b" > .env

# Restart
docker compose --profile ollama restart
```

### Browser not working
- Browser automation is built into OpenHands
- Make sure you're using the latest OpenHands image
- Try: `docker compose pull && docker compose up -d`

---

## 🎯 Quick Reference

| Action | Command |
|--------|---------|
| Start | `docker compose --profile ollama up -d` |
| Stop | `docker compose --profile ollama down` |
| Logs | `docker compose logs -f` |
| Update | `docker compose pull && docker compose --profile ollama up -d` |
| Open UI | http://localhost:3000 |
| Workspace | `~/openhands-local/workspace` |

---

## 🔗 Links

- [OpenHands Documentation](https://docs.all-hands.dev/)
- [OpenHands GitHub](https://github.com/All-Hands-AI/OpenHands)
- [Ollama Models](https://ollama.ai/library)
- [DeepSeek](https://www.deepseek.com/)

---

**You're all set! 🎉**

Open http://localhost:3000 and start coding with AI assistance!
