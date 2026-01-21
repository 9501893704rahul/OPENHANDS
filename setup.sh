#!/bin/bash

# =============================================================================
# OpenHands GPU Setup Script
# =============================================================================
# This script sets up OpenHands with GPU support on your local machine
# =============================================================================

set -o pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Print functions
print_header() {
    echo -e "\n${BLUE}============================================${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}============================================${NC}\n"
}

print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ $1${NC}"
}

# Check if running as root
check_root() {
    if [[ $EUID -eq 0 ]]; then
        print_warning "Running as root. Some commands will be executed without sudo."
        SUDO=""
    else
        SUDO="sudo"
    fi
}

# Check system requirements
check_system() {
    print_header "Checking System Requirements"
    
    # Check OS
    if [[ -f /etc/os-release ]]; then
        . /etc/os-release
        print_info "Operating System: $NAME $VERSION"
    fi
    
    # Check architecture
    ARCH=$(uname -m)
    print_info "Architecture: $ARCH"
    
    if [[ "$ARCH" != "x86_64" && "$ARCH" != "aarch64" ]]; then
        print_warning "Architecture $ARCH may not be fully supported"
    fi
    
    # Check memory
    TOTAL_MEM=$(free -g | awk '/^Mem:/{print $2}')
    print_info "Total Memory: ${TOTAL_MEM}GB"
    
    if [[ $TOTAL_MEM -lt 8 ]]; then
        print_warning "Less than 8GB RAM detected. OpenHands may run slowly."
    fi
}

# Check and install Docker
check_docker() {
    print_header "Checking Docker Installation"
    
    if command -v docker &> /dev/null; then
        DOCKER_VERSION=$(docker --version)
        print_success "Docker is installed: $DOCKER_VERSION"
    else
        print_warning "Docker is not installed. Installing..."
        install_docker
    fi
    
    # Check if Docker daemon is running
    if docker info &> /dev/null; then
        print_success "Docker daemon is running"
    else
        print_error "Docker daemon is not running"
        print_info "Starting Docker daemon..."
        $SUDO systemctl start docker || $SUDO service docker start
    fi
    
    # Check Docker Compose
    if docker compose version &> /dev/null; then
        COMPOSE_VERSION=$(docker compose version --short)
        print_success "Docker Compose is installed: $COMPOSE_VERSION"
    else
        print_warning "Docker Compose plugin not found. Installing..."
        install_docker_compose
    fi
}

# Install Docker
install_docker() {
    print_info "Installing Docker..."
    
    # Remove old versions
    $SUDO apt-get remove -y docker docker-engine docker.io containerd runc 2>/dev/null || true
    
    # Install prerequisites
    $SUDO apt-get update
    $SUDO apt-get install -y \
        apt-transport-https \
        ca-certificates \
        curl \
        gnupg \
        lsb-release
    
    # Add Docker's official GPG key
    $SUDO mkdir -p /etc/apt/keyrings
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | $SUDO gpg --dearmor -o /etc/apt/keyrings/docker.gpg
    
    # Set up repository
    echo \
        "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
        $(lsb_release -cs) stable" | $SUDO tee /etc/apt/sources.list.d/docker.list > /dev/null
    
    # Install Docker
    $SUDO apt-get update
    $SUDO apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
    
    # Add current user to docker group
    $SUDO usermod -aG docker $USER
    
    print_success "Docker installed successfully"
    print_warning "You may need to log out and back in for group changes to take effect"
}

# Install Docker Compose
install_docker_compose() {
    print_info "Installing Docker Compose plugin..."
    $SUDO apt-get update
    $SUDO apt-get install -y docker-compose-plugin
    print_success "Docker Compose installed successfully"
}

# Check NVIDIA GPU and drivers
check_nvidia() {
    print_header "Checking NVIDIA GPU Setup"
    
    # Check for NVIDIA GPU
    if lspci | grep -i nvidia &> /dev/null; then
        print_success "NVIDIA GPU detected"
        lspci | grep -i nvidia | while read line; do
            print_info "  $line"
        done
    else
        print_error "No NVIDIA GPU detected"
        print_info "This setup requires an NVIDIA GPU for GPU acceleration"
        return 1
    fi
    
    # Check NVIDIA driver
    if command -v nvidia-smi &> /dev/null; then
        print_success "NVIDIA driver is installed"
        nvidia-smi --query-gpu=name,driver_version,memory.total --format=csv,noheader | while read line; do
            print_info "  GPU: $line"
        done
    else
        print_warning "NVIDIA driver not found. Installing..."
        install_nvidia_driver
    fi
    
    # Check NVIDIA Container Toolkit
    if command -v nvidia-container-cli &> /dev/null || dpkg -l | grep -q nvidia-container-toolkit; then
        print_success "NVIDIA Container Toolkit is installed"
    else
        print_warning "NVIDIA Container Toolkit not found. Installing..."
        install_nvidia_container_toolkit
    fi
}

# Install NVIDIA driver
install_nvidia_driver() {
    print_info "Installing NVIDIA driver..."
    
    $SUDO apt-get update
    $SUDO apt-get install -y ubuntu-drivers-common
    $SUDO ubuntu-drivers autoinstall
    
    print_success "NVIDIA driver installed"
    print_warning "A system reboot may be required"
}

# Install NVIDIA Container Toolkit
install_nvidia_container_toolkit() {
    print_info "Installing NVIDIA Container Toolkit..."
    
    # Add NVIDIA Container Toolkit repository
    distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
    curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | $SUDO gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg
    curl -s -L https://nvidia.github.io/libnvidia-container/$distribution/libnvidia-container.list | \
        sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' | \
        $SUDO tee /etc/apt/sources.list.d/nvidia-container-toolkit.list
    
    # Install toolkit
    $SUDO apt-get update
    $SUDO apt-get install -y nvidia-container-toolkit
    
    # Configure Docker to use NVIDIA runtime
    $SUDO nvidia-ctk runtime configure --runtime=docker
    $SUDO systemctl restart docker
    
    print_success "NVIDIA Container Toolkit installed and configured"
}

# Test GPU in Docker
test_gpu_docker() {
    print_header "Testing GPU Access in Docker"
    
    print_info "Running nvidia-smi in Docker container..."
    if docker run --rm --gpus all nvidia/cuda:12.0-base nvidia-smi &> /dev/null; then
        print_success "GPU is accessible from Docker containers"
        docker run --rm --gpus all nvidia/cuda:12.0-base nvidia-smi
    else
        print_error "GPU is not accessible from Docker containers"
        print_info "Please ensure NVIDIA Container Toolkit is properly configured"
        return 1
    fi
}

# Setup environment
setup_environment() {
    print_header "Setting Up Environment"
    
    # Create directories
    mkdir -p workspace openhands-state ollama-models localai-models
    print_success "Created required directories"
    
    # Create .env file if it doesn't exist
    if [[ ! -f .env ]]; then
        cp .env.example .env
        print_success "Created .env file from template"
        print_warning "Please edit .env file to add your API keys"
    else
        print_info ".env file already exists"
    fi
    
    # Set permissions
    chmod 755 workspace openhands-state ollama-models localai-models
    print_success "Set directory permissions"
}

# Pull Docker images
pull_images() {
    print_header "Pulling Docker Images"
    
    print_info "Pulling OpenHands image..."
    docker pull docker.all-hands.dev/all-hands-ai/openhands:main
    print_success "OpenHands image pulled"
    
    print_info "Pulling OpenHands runtime image..."
    docker pull docker.all-hands.dev/all-hands-ai/runtime:main
    print_success "Runtime image pulled"
}

# Start services
start_services() {
    print_header "Starting OpenHands"
    
    local profile=""
    
    # Ask about Ollama
    read -p "Do you want to start Ollama for local LLM? (y/n): " start_ollama
    if [[ "$start_ollama" =~ ^[Yy]$ ]]; then
        profile="--profile ollama"
    fi
    
    docker compose $profile up -d
    
    print_success "OpenHands is starting..."
    print_info "Web interface will be available at: http://localhost:${OPENHANDS_PORT:-3000}"
    
    if [[ "$start_ollama" =~ ^[Yy]$ ]]; then
        print_info "Ollama API available at: http://localhost:${OLLAMA_PORT:-11434}"
    fi
}

# Show status
show_status() {
    print_header "Service Status"
    docker compose ps
}

# Main menu
show_menu() {
    echo ""
    echo "OpenHands GPU Setup"
    echo "==================="
    echo "1) Full Setup (recommended for first time)"
    echo "2) Check System Requirements"
    echo "3) Install/Check Docker"
    echo "4) Install/Check NVIDIA GPU Support"
    echo "5) Test GPU in Docker"
    echo "6) Setup Environment"
    echo "7) Pull Docker Images"
    echo "8) Start OpenHands"
    echo "9) Stop OpenHands"
    echo "10) Show Status"
    echo "11) View Logs"
    echo "0) Exit"
    echo ""
}

# Full setup
full_setup() {
    check_root
    check_system
    check_docker
    check_nvidia
    test_gpu_docker
    setup_environment
    pull_images
    
    print_header "Setup Complete!"
    print_info "Next steps:"
    echo "  1. Edit .env file to add your LLM API key"
    echo "  2. Run './setup.sh' and select option 8 to start OpenHands"
    echo "  3. Open http://localhost:3000 in your browser"
}

# Main
main() {
    cd "$(dirname "$0")"
    
    if [[ $# -eq 0 ]]; then
        while true; do
            show_menu
            read -p "Select option: " choice
            case $choice in
                1) full_setup ;;
                2) check_root; check_system ;;
                3) check_root; check_docker ;;
                4) check_root; check_nvidia ;;
                5) test_gpu_docker ;;
                6) setup_environment ;;
                7) pull_images ;;
                8) start_services ;;
                9) docker compose down ;;
                10) show_status ;;
                11) docker compose logs -f ;;
                0) exit 0 ;;
                *) print_error "Invalid option" ;;
            esac
        done
    else
        case $1 in
            --full) full_setup ;;
            --start) start_services ;;
            --stop) docker compose down ;;
            --status) show_status ;;
            --logs) docker compose logs -f ;;
            *) echo "Usage: $0 [--full|--start|--stop|--status|--logs]" ;;
        esac
    fi
}

main "$@"
