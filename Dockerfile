# Use Python 3.11 slim image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    bluetooth \
    bluez \
    libbluetooth-dev \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libxext6 \
    libxrender1 \
    libxcb1 \
    libx11-6 \
    libxkbcommon-x11-0 \
    libxcb-icccm4 \
    libxcb-image0 \
    libxcb-keysyms1 \
    libxcb-randr0 \
    libxcb-render-util0 \
    libxcb-xinerama0 \
    libxcb-xfixes0 \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Make scripts executable
RUN chmod +x run_in_venv.sh create_venv.sh

# Create non-root user for security
RUN useradd -m -u 1000 idotmatrix && chown -R idotmatrix:idotmatrix /app
USER idotmatrix

# Expose port for potential web interface
EXPOSE 8080

# Default command
CMD ["python", "app.py", "--help"]
