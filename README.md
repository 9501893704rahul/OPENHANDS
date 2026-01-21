# OpenHands GPU Setup with DeepSeek

Run OpenHands with your own GPU using **DeepSeek** models for powerful local AI coding assistance.

## 🚀 Quick Start (DeepSeek Local)

```bash
# 1. Clone this repository
git clone <your-repo-url>
cd openhands-gpu-setup

# 2. Run the DeepSeek setup script
chmod +x setup-deepseek.sh
./setup-deepseek.sh --full

# 3. Access OpenHands
# Open http://localhost:3000 in your browser
```

That's it! The script will:
- Check your GPU compatibility
- Help you select the right DeepSeek model for your VRAM
- Download and configure everything automatically

## 🧠 DeepSeek Models

| Model | Size | VRAM Required | Best For |
|-------|------|---------------|----------|
| `deepseek-coder-v2:16b` | 9GB | 16GB | ⭐ **Recommended** - Best balance |
| `deepseek-coder:33b` | 19GB | 24GB | High quality code generation |
| `deepseek-coder:6.7b` | 3.8GB | 8GB | Fast inference, limited VRAM |
| `deepseek-coder:1.3b` | 0.8GB | 4GB | Minimal resources |
| `deepseek-v2.5:latest` | varies | 16GB+ | Latest general purpose |

## 📋 Alternative Quick Start (Manual)

```bash
# Run the general setup script
chmod +x setup.sh
./setup.sh --full

# Edit your configuration
cp .env.example .env
nano .env  # Configure for DeepSeek

# Start OpenHands with Ollama
docker compose --profile ollama up -d

# Pull DeepSeek model
docker exec -it ollama ollama pull deepseek-coder-v2:16b

# Start OpenHands
./setup.sh --start
```

Then open http://localhost:3000 in your browser.

## 📋 Prerequisites

- **Operating System**: Ubuntu 20.04+ / Debian 11+ (or compatible Linux distribution)
- **GPU**: NVIDIA GPU with CUDA support (GTX 1060 or better recommended)
- **RAM**: Minimum 8GB (16GB+ recommended for local LLMs)
- **Storage**: 20GB+ free space (more for local models)
- **Docker**: Docker Engine 20.10+ with Docker Compose v2

## 📁 Project Structure

```
openhands-gpu-setup/
├── docker-compose.yml    # Main Docker Compose configuration
├── .env.example          # Environment variables template
├── .env                  # Your configuration (create from .env.example)
├── setup.sh              # General automated setup script
├── setup-deepseek.sh     # DeepSeek-specific setup script ⭐
├── verify-gpu.sh         # GPU verification script
├── README.md             # This file
├── workspace/            # Your project files (mounted to OpenHands)
├── openhands-state/      # OpenHands persistent state
├── ollama-models/        # Ollama model storage (DeepSeek models stored here)
└── localai-models/       # LocalAI model storage (if using)
```

## 🔧 Configuration

### LLM Provider Options

Edit `.env` to configure your preferred LLM provider:

#### ⭐ Option 1: DeepSeek Local (Recommended)
```env
LLM_MODEL=ollama/deepseek-coder-v2:16b
LLM_API_KEY=ollama
LLM_BASE_URL=http://host.docker.internal:11434
```

Start with Ollama profile:
```bash
docker compose --profile ollama up -d
docker exec -it ollama ollama pull deepseek-coder-v2:16b
```

#### Option 2: DeepSeek API (Cloud)
```env
LLM_MODEL=deepseek/deepseek-chat
LLM_API_KEY=your-deepseek-api-key
LLM_BASE_URL=https://api.deepseek.com/v1
```

#### Option 3: OpenAI (Cloud)
```env
LLM_MODEL=gpt-4o
LLM_API_KEY=sk-your-openai-key
LLM_BASE_URL=https://api.openai.com/v1
```

#### Option 4: Anthropic Claude (Cloud)
```env
LLM_MODEL=claude-sonnet-4-20250514
LLM_API_KEY=sk-ant-your-anthropic-key
LLM_BASE_URL=https://api.anthropic.com
```

#### Option 5: Other Ollama Models (Local GPU)
```env
LLM_MODEL=ollama/llama3.1:70b
LLM_API_KEY=ollama
LLM_BASE_URL=http://host.docker.internal:11434
```

#### Option 6: LM Studio (Local GPU)
```env
LLM_MODEL=lmstudio/your-model-name
LLM_API_KEY=lm-studio
LLM_BASE_URL=http://host.docker.internal:1234/v1
```

#### Option 7: LocalAI (Local GPU)
```env
LLM_MODEL=localai/your-model
LLM_API_KEY=localai
LLM_BASE_URL=http://localai:8080/v1
```

Start with LocalAI profile:
```bash
docker compose --profile localai up -d
```

## 🖥️ GPU Setup

### NVIDIA Driver Installation

If you don't have NVIDIA drivers installed:

```bash
# Ubuntu/Debian
sudo apt update
sudo apt install ubuntu-drivers-common
sudo ubuntu-drivers autoinstall
sudo reboot
```

### NVIDIA Container Toolkit

Required for GPU access in Docker:

```bash
# Add NVIDIA repository
distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg
curl -s -L https://nvidia.github.io/libnvidia-container/$distribution/libnvidia-container.list | \
    sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' | \
    sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list

# Install toolkit
sudo apt update
sudo apt install -y nvidia-container-toolkit

# Configure Docker
sudo nvidia-ctk runtime configure --runtime=docker
sudo systemctl restart docker
```

### Verify GPU Setup

```bash
# Check NVIDIA driver
nvidia-smi

# Test GPU in Docker
docker run --rm --gpus all nvidia/cuda:12.0-base nvidia-smi

# Or use the verification script
./verify-gpu.sh
```

## 🚀 Usage

### Starting OpenHands

```bash
# Basic start (OpenHands only)
docker compose up -d

# With Ollama for local LLM
docker compose --profile ollama up -d

# With LocalAI
docker compose --profile localai up -d

# Or use the setup script
./setup.sh --start
```

### Stopping OpenHands

```bash
docker compose down
# or
./setup.sh --stop
```

### Viewing Logs

```bash
docker compose logs -f
# or
./setup.sh --logs
```

### Checking Status

```bash
docker compose ps
# or
./setup.sh --status
```

## 🧠 Using DeepSeek with OpenHands

### Quick DeepSeek Setup

```bash
# Use the dedicated DeepSeek setup script
./setup-deepseek.sh --full
```

### Manual DeepSeek Setup

```bash
# Start Ollama with GPU support
docker compose --profile ollama up -d

# Pull DeepSeek model (choose based on your VRAM)
docker exec -it ollama ollama pull deepseek-coder-v2:16b

# List available models
docker exec -it ollama ollama list

# Test the model
docker exec -it ollama ollama run deepseek-coder-v2:16b "Write hello world in Python"
```

### DeepSeek Model Selection Guide

| Model | Size | VRAM | Speed | Quality | Best For |
|-------|------|------|-------|---------|----------|
| `deepseek-coder-v2:16b` | 9GB | 16GB | ⚡⚡⚡ | ⭐⭐⭐⭐ | **Recommended** - Best balance |
| `deepseek-coder:33b` | 19GB | 24GB | ⚡⚡ | ⭐⭐⭐⭐⭐ | High quality, slower |
| `deepseek-coder:6.7b` | 3.8GB | 8GB | ⚡⚡⚡⚡ | ⭐⭐⭐ | Fast, good for simple tasks |
| `deepseek-coder:1.3b` | 0.8GB | 4GB | ⚡⚡⚡⚡⚡ | ⭐⭐ | Minimal resources |
| `deepseek-v2.5:latest` | varies | 16GB+ | ⚡⚡⚡ | ⭐⭐⭐⭐ | Latest general purpose |

### Other Recommended Models

| Model | Size | VRAM Required | Best For |
|-------|------|---------------|----------|
| `qwen2.5-coder:32b` | 18GB | 24GB | Excellent for coding |
| `codellama:34b` | 19GB | 24GB | Code generation |
| `llama3.1:70b` | 40GB | 48GB+ | Best quality general |

## 🔒 Security Notes

- Never commit your `.env` file with API keys
- The Docker socket is mounted for container management - be aware of security implications
- Consider using Docker secrets for production deployments
- Restrict network access if running on a shared system

## 🐛 Troubleshooting

### GPU Not Detected in Docker

```bash
# Check NVIDIA driver
nvidia-smi

# Check NVIDIA Container Toolkit
nvidia-container-cli info

# Restart Docker
sudo systemctl restart docker

# Test GPU access
docker run --rm --gpus all nvidia/cuda:12.0-base nvidia-smi
```

### Out of Memory Errors

- Use a smaller model
- Reduce context length in model settings
- Close other GPU-intensive applications
- Check GPU memory usage: `nvidia-smi -l 1`

### Container Won't Start

```bash
# Check logs
docker compose logs openhands

# Verify Docker socket permissions
ls -la /var/run/docker.sock

# Add user to docker group
sudo usermod -aG docker $USER
# Then log out and back in
```

### Ollama Connection Issues

```bash
# Check if Ollama is running
docker compose ps ollama

# Test Ollama API
curl http://localhost:11434/api/tags

# Check Ollama logs
docker compose logs ollama
```

## 📊 Performance Tips

1. **Use NVMe SSD** for model storage to reduce load times
2. **Allocate sufficient VRAM** - larger models need more GPU memory
3. **Monitor GPU usage** with `nvidia-smi -l 1` or `nvtop`
4. **Use quantized models** (Q4, Q5) for better performance with less VRAM
5. **Enable GPU persistence mode** for faster model loading:
   ```bash
   sudo nvidia-smi -pm 1
   ```

## 🔄 Updating

```bash
# Pull latest images
docker compose pull

# Restart services
docker compose down
docker compose up -d
```

## 📚 Additional Resources

- [OpenHands Documentation](https://docs.all-hands.dev/)
- [Ollama Model Library](https://ollama.ai/library)
- [NVIDIA Container Toolkit](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/overview.html)
- [Docker Compose GPU Support](https://docs.docker.com/compose/gpu-support/)

## 📄 License

MIT License - Feel free to use and modify for your needs.
