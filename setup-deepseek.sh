#!/bin/bash

# =============================================================================
# DeepSeek Local Setup Script for OpenHands
# =============================================================================
# This script sets up DeepSeek models to run locally with GPU acceleration
# =============================================================================

set -o pipefail

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

print_header() {
    echo -e "\n${BLUE}============================================${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}============================================${NC}\n"
}

print_success() { echo -e "${GREEN}✓ $1${NC}"; }
print_warning() { echo -e "${YELLOW}⚠ $1${NC}"; }
print_error() { echo -e "${RED}✗ $1${NC}"; }
print_info() { echo -e "${CYAN}ℹ $1${NC}"; }

# DeepSeek models available via Ollama
declare -A DEEPSEEK_MODELS=(
    ["1"]="deepseek-coder-v2:16b|9.0GB|16GB|Best balance of quality and speed"
    ["2"]="deepseek-coder-v2:236b|133GB|256GB+|Largest, highest quality (requires multi-GPU)"
    ["3"]="deepseek-coder:33b|19GB|24GB|Excellent code generation"
    ["4"]="deepseek-coder:6.7b|3.8GB|8GB|Lightweight, fast inference"
    ["5"]="deepseek-coder:1.3b|0.8GB|4GB|Smallest, for limited VRAM"
    ["6"]="deepseek-v2:16b|9.0GB|16GB|General purpose, good for chat"
    ["7"]="deepseek-v2.5:latest|varies|16GB+|Latest DeepSeek model"
)

cd "$(dirname "$0")"

# Check GPU memory
check_gpu_memory() {
    print_header "Checking GPU Memory"
    
    if ! command -v nvidia-smi &> /dev/null; then
        print_error "nvidia-smi not found. Please install NVIDIA drivers."
        return 1
    fi
    
    GPU_MEM=$(nvidia-smi --query-gpu=memory.total --format=csv,noheader,nounits | head -1)
    GPU_NAME=$(nvidia-smi --query-gpu=name --format=csv,noheader | head -1)
    
    print_info "GPU: $GPU_NAME"
    print_info "Total VRAM: ${GPU_MEM}MB ($(echo "scale=1; $GPU_MEM/1024" | bc)GB)"
    
    echo ""
    echo "Recommended DeepSeek models for your GPU:"
    echo ""
    
    if [ "$GPU_MEM" -ge 256000 ]; then
        print_success "You can run ALL DeepSeek models including the 236B!"
    elif [ "$GPU_MEM" -ge 48000 ]; then
        print_success "Recommended: deepseek-coder:33b or deepseek-coder-v2:16b"
    elif [ "$GPU_MEM" -ge 24000 ]; then
        print_success "Recommended: deepseek-coder:33b (may need quantization)"
        print_info "Alternative: deepseek-coder-v2:16b"
    elif [ "$GPU_MEM" -ge 16000 ]; then
        print_success "Recommended: deepseek-coder-v2:16b"
        print_info "Alternative: deepseek-coder:6.7b"
    elif [ "$GPU_MEM" -ge 8000 ]; then
        print_success "Recommended: deepseek-coder:6.7b"
        print_warning "Larger models may not fit in VRAM"
    else
        print_warning "Limited VRAM detected"
        print_info "Recommended: deepseek-coder:1.3b"
    fi
    
    return 0
}

# Show model selection menu
show_model_menu() {
    print_header "Available DeepSeek Models"
    
    echo "Select a DeepSeek model to install:"
    echo ""
    printf "%-4s %-25s %-10s %-10s %s\n" "#" "Model" "Size" "VRAM" "Description"
    echo "--------------------------------------------------------------------------------"
    
    for key in $(echo "${!DEEPSEEK_MODELS[@]}" | tr ' ' '\n' | sort -n); do
        IFS='|' read -r model size vram desc <<< "${DEEPSEEK_MODELS[$key]}"
        printf "%-4s %-25s %-10s %-10s %s\n" "$key)" "$model" "$size" "$vram" "$desc"
    done
    
    echo ""
    echo "0) Cancel"
    echo ""
}

# Pull DeepSeek model
pull_model() {
    local model=$1
    
    print_header "Pulling DeepSeek Model: $model"
    
    # Check if Ollama container is running
    if ! docker ps | grep -q ollama; then
        print_info "Starting Ollama container..."
        docker compose --profile ollama up -d ollama
        sleep 5
    fi
    
    # Pull the model
    print_info "Downloading model (this may take a while)..."
    docker exec -it ollama ollama pull "$model"
    
    if [ $? -eq 0 ]; then
        print_success "Model $model downloaded successfully!"
    else
        print_error "Failed to download model"
        return 1
    fi
}

# Configure .env for DeepSeek
configure_env() {
    local model=$1
    
    print_header "Configuring Environment"
    
    if [ ! -f .env ]; then
        cp .env.example .env
        print_success "Created .env from template"
    fi
    
    # Update LLM_MODEL in .env
    if grep -q "^LLM_MODEL=" .env; then
        sed -i "s|^LLM_MODEL=.*|LLM_MODEL=ollama/$model|" .env
    else
        echo "LLM_MODEL=ollama/$model" >> .env
    fi
    
    # Ensure Ollama settings
    if ! grep -q "^LLM_API_KEY=ollama" .env; then
        sed -i "s|^LLM_API_KEY=.*|LLM_API_KEY=ollama|" .env
    fi
    
    if ! grep -q "^LLM_BASE_URL=http://host.docker.internal:11434" .env; then
        sed -i "s|^LLM_BASE_URL=.*|LLM_BASE_URL=http://host.docker.internal:11434|" .env
    fi
    
    print_success "Configured .env for DeepSeek model: $model"
}

# Test the model
test_model() {
    local model=$1
    
    print_header "Testing DeepSeek Model"
    
    print_info "Sending test prompt to $model..."
    
    response=$(docker exec ollama ollama run "$model" "Write a hello world function in Python. Only output the code, nothing else." 2>/dev/null)
    
    if [ -n "$response" ]; then
        print_success "Model is working!"
        echo ""
        echo "Response:"
        echo "----------------------------------------"
        echo "$response"
        echo "----------------------------------------"
    else
        print_error "No response from model"
        return 1
    fi
}

# Start all services
start_services() {
    print_header "Starting OpenHands with DeepSeek"
    
    docker compose --profile ollama up -d
    
    print_success "Services started!"
    echo ""
    print_info "OpenHands UI: http://localhost:3000"
    print_info "Ollama API: http://localhost:11434"
    echo ""
    print_info "To view logs: docker compose logs -f"
}

# List installed models
list_models() {
    print_header "Installed Ollama Models"
    
    if docker ps | grep -q ollama; then
        docker exec ollama ollama list
    else
        print_warning "Ollama container is not running"
        print_info "Start with: docker compose --profile ollama up -d"
    fi
}

# Full setup
full_setup() {
    check_gpu_memory
    
    show_model_menu
    read -p "Select model number: " choice
    
    if [ "$choice" == "0" ]; then
        echo "Cancelled"
        return
    fi
    
    if [ -z "${DEEPSEEK_MODELS[$choice]}" ]; then
        print_error "Invalid selection"
        return 1
    fi
    
    IFS='|' read -r model size vram desc <<< "${DEEPSEEK_MODELS[$choice]}"
    
    echo ""
    print_info "Selected: $model ($size, requires $vram VRAM)"
    read -p "Continue? (y/n): " confirm
    
    if [[ ! "$confirm" =~ ^[Yy]$ ]]; then
        echo "Cancelled"
        return
    fi
    
    # Create directories
    mkdir -p workspace openhands-state ollama-models
    
    # Start Ollama
    print_info "Starting Ollama container..."
    docker compose --profile ollama up -d ollama
    sleep 5
    
    # Pull model
    pull_model "$model"
    
    # Configure environment
    configure_env "$model"
    
    # Test model
    read -p "Test the model? (y/n): " test_confirm
    if [[ "$test_confirm" =~ ^[Yy]$ ]]; then
        test_model "$model"
    fi
    
    # Start OpenHands
    read -p "Start OpenHands now? (y/n): " start_confirm
    if [[ "$start_confirm" =~ ^[Yy]$ ]]; then
        start_services
    fi
    
    print_header "Setup Complete!"
    echo "Your DeepSeek-powered OpenHands is ready!"
    echo ""
    echo "Quick commands:"
    echo "  Start:  docker compose --profile ollama up -d"
    echo "  Stop:   docker compose --profile ollama down"
    echo "  Logs:   docker compose logs -f"
    echo "  UI:     http://localhost:3000"
}

# Main menu
show_menu() {
    echo ""
    echo "DeepSeek Local Setup for OpenHands"
    echo "==================================="
    echo "1) Full Setup (recommended)"
    echo "2) Check GPU Memory"
    echo "3) Show Available Models"
    echo "4) Pull a Model"
    echo "5) Configure .env"
    echo "6) Test Model"
    echo "7) List Installed Models"
    echo "8) Start Services"
    echo "9) Stop Services"
    echo "0) Exit"
    echo ""
}

# Main
main() {
    if [[ $# -eq 0 ]]; then
        while true; do
            show_menu
            read -p "Select option: " choice
            case $choice in
                1) full_setup ;;
                2) check_gpu_memory ;;
                3) show_model_menu ;;
                4) 
                    show_model_menu
                    read -p "Select model: " m
                    if [ -n "${DEEPSEEK_MODELS[$m]}" ]; then
                        IFS='|' read -r model _ _ _ <<< "${DEEPSEEK_MODELS[$m]}"
                        pull_model "$model"
                    fi
                    ;;
                5)
                    show_model_menu
                    read -p "Select model: " m
                    if [ -n "${DEEPSEEK_MODELS[$m]}" ]; then
                        IFS='|' read -r model _ _ _ <<< "${DEEPSEEK_MODELS[$m]}"
                        configure_env "$model"
                    fi
                    ;;
                6)
                    list_models
                    read -p "Enter model name to test: " model
                    test_model "$model"
                    ;;
                7) list_models ;;
                8) start_services ;;
                9) docker compose --profile ollama down ;;
                0) exit 0 ;;
                *) print_error "Invalid option" ;;
            esac
        done
    else
        case $1 in
            --full) full_setup ;;
            --check) check_gpu_memory ;;
            --list) list_models ;;
            --start) start_services ;;
            --stop) docker compose --profile ollama down ;;
            --pull)
                if [ -n "$2" ]; then
                    pull_model "$2"
                else
                    echo "Usage: $0 --pull <model-name>"
                fi
                ;;
            *) 
                echo "Usage: $0 [--full|--check|--list|--start|--stop|--pull <model>]"
                ;;
        esac
    fi
}

main "$@"
