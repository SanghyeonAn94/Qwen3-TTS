# Qwen3-TTS Fine-tuning Docker Image
# CUDA 12.8 + PyTorch nightly (RTX 5070 Ti / Blackwell sm_120 support)
FROM nvidia/cuda:12.8.1-devel-ubuntu22.04

ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1
ENV TORCH_CUDA_ARCH_LIST="8.0;8.6;8.9;9.0;12.0"

# System dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3.11 python3.11-dev python3.11-venv python3-pip \
    git wget curl sox libsox-dev libsndfile1 ffmpeg \
    build-essential ninja-build \
    && ln -sf /usr/bin/python3.11 /usr/bin/python3 \
    && ln -sf /usr/bin/python3.11 /usr/bin/python \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip
RUN python -m pip install --no-cache-dir --upgrade pip setuptools wheel

# PyTorch nightly (CUDA 12.8, Blackwell support)
RUN pip install --no-cache-dir --pre \
    torch torchaudio \
    --index-url https://download.pytorch.org/whl/nightly/cu128

# Project dependencies (using PyTorch SDPA instead of flash-attn)
RUN pip install --no-cache-dir \
    transformers==4.57.3 \
    accelerate==1.12.0 \
    librosa \
    soundfile \
    sox \
    onnxruntime \
    einops \
    safetensors \
    gradio \
    tensorboard

WORKDIR /workspace

# Install qwen-tts package (mounted at runtime)
# The source code is bind-mounted, so we install in editable mode at container start

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
CMD ["bash"]
