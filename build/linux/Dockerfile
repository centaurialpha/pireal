FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive
ENV UV_LINK_MODE=copy

RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-venv \
    patchelf \
    ccache \
    gcc \
    g++ \
    libgl1 \
    libglib2.0-0 \
    libdbus-1-3 \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

RUN pip3 install uv

WORKDIR /project

CMD ["uv", "run", "python", "build/linux/build_appimage.py"]
