FROM python:3.9-slim

WORKDIR /app

# Install system dependencies for Playwright and Chromium
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    libnss3 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libcups2 \
    libdrm2 \
    libxcomposite1 \
    libxdamage1 \
    libxrandr2 \
    libgbm1 \
    libasound2 \
    libpangocairo-1.0-0 \
    libxshmfence1 \
    libx11-xcb1 \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install Playwright and chromium dependencies
RUN playwright install chromium --with-deps

# Copy the rest of the application
COPY . .

# Hugging Face exposes port 7860
ENV PORT=7860
EXPOSE 7860

# Start the Flask server
CMD ["python", "server.py"]
