#!/bin/bash

# =============================================================================
# GPU Verification Script for OpenHands
# =============================================================================

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}============================================${NC}"
echo -e "${BLUE}   GPU Verification for OpenHands Setup    ${NC}"
echo -e "${BLUE}============================================${NC}"
echo ""

# Check for NVIDIA GPU hardware
echo -e "${BLUE}[1/6] Checking for NVIDIA GPU hardware...${NC}"
if lspci | grep -i nvidia &> /dev/null; then
    echo -e "${GREEN}✓ NVIDIA GPU detected:${NC}"
    lspci | grep -i nvidia | sed 's/^/  /'
else
    echo -e "${RED}✗ No NVIDIA GPU detected${NC}"
    echo "  This setup requires an NVIDIA GPU"
    exit 1
fi
echo ""

# Check NVIDIA driver
echo -e "${BLUE}[2/6] Checking NVIDIA driver...${NC}"
if command -v nvidia-smi &> /dev/null; then
    DRIVER_VERSION=$(nvidia-smi --query-gpu=driver_version --format=csv,noheader | head -1)
    echo -e "${GREEN}✓ NVIDIA driver installed: $DRIVER_VERSION${NC}"
else
    echo -e "${RED}✗ NVIDIA driver not found${NC}"
    echo "  Install with: sudo apt install nvidia-driver-535"
    exit 1
fi
echo ""

# Check GPU details
echo -e "${BLUE}[3/6] GPU Information:${NC}"
nvidia-smi --query-gpu=name,memory.total,memory.free,compute_cap --format=csv,noheader | while read line; do
    echo -e "  ${GREEN}$line${NC}"
done
echo ""

# Check CUDA version
echo -e "${BLUE}[4/6] Checking CUDA version...${NC}"
if nvidia-smi | grep -i "CUDA Version" &> /dev/null; then
    CUDA_VERSION=$(nvidia-smi | grep "CUDA Version" | awk '{print $9}')
    echo -e "${GREEN}✓ CUDA Version: $CUDA_VERSION${NC}"
else
    echo -e "${YELLOW}⚠ CUDA version not detected in nvidia-smi${NC}"
fi
echo ""

# Check Docker
echo -e "${BLUE}[5/6] Checking Docker setup...${NC}"
if command -v docker &> /dev/null; then
    echo -e "${GREEN}✓ Docker is installed${NC}"
    
    # Check NVIDIA Container Toolkit
    if docker info 2>/dev/null | grep -i "nvidia" &> /dev/null || \
       command -v nvidia-container-cli &> /dev/null || \
       dpkg -l 2>/dev/null | grep -q nvidia-container-toolkit; then
        echo -e "${GREEN}✓ NVIDIA Container Toolkit detected${NC}"
    else
        echo -e "${YELLOW}⚠ NVIDIA Container Toolkit may not be installed${NC}"
        echo "  Install with: sudo apt install nvidia-container-toolkit"
    fi
else
    echo -e "${RED}✗ Docker not installed${NC}"
    exit 1
fi
echo ""

# Test GPU in Docker
echo -e "${BLUE}[6/6] Testing GPU access in Docker...${NC}"
if docker run --rm --gpus all nvidia/cuda:12.0-base nvidia-smi &> /dev/null; then
    echo -e "${GREEN}✓ GPU is accessible from Docker containers${NC}"
    echo ""
    echo -e "${BLUE}Docker GPU Test Output:${NC}"
    docker run --rm --gpus all nvidia/cuda:12.0-base nvidia-smi 2>/dev/null | head -20
else
    echo -e "${RED}✗ GPU is NOT accessible from Docker${NC}"
    echo ""
    echo "  Troubleshooting steps:"
    echo "  1. Install NVIDIA Container Toolkit:"
    echo "     sudo apt install nvidia-container-toolkit"
    echo "  2. Configure Docker runtime:"
    echo "     sudo nvidia-ctk runtime configure --runtime=docker"
    echo "  3. Restart Docker:"
    echo "     sudo systemctl restart docker"
    exit 1
fi

echo ""
echo -e "${GREEN}============================================${NC}"
echo -e "${GREEN}   All GPU checks passed! Ready to go.     ${NC}"
echo -e "${GREEN}============================================${NC}"
echo ""
echo "Next steps:"
echo "  1. Copy .env.example to .env and configure"
echo "  2. Run: docker compose --profile ollama up -d"
echo "  3. Pull DeepSeek model: docker exec -it ollama ollama pull deepseek-coder-v2:16b"
echo "  4. Open http://localhost:3000"
