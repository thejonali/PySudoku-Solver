# PySudoku Solver Dockerfile
# --------------------------
# Build a container for running the PySudoku Solver CLI and GUI

FROM python:3.11

# Install system dependencies for building Python packages
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        build-essential \
        python3-dev \
        libffi-dev \
        libssl-dev \
        libgl1-mesa-glx \
        libglib2.0-0 \
        qtbase5-dev \
        && rm -rf /var/lib/apt/lists/*

# Set workdir
WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy the rest of the code
COPY . .

# Default command
CMD ["python", "main.py"]
