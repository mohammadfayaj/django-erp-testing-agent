FROM python:3.11-slim

# Install system dependencies for Playwright
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    libnss3 \
    libatk-bridge2.0-0 \
    libdrm2 \
    libxkbcommon0 \
    libgbm1 \
    libasound2 \
    libxshmfence1 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY pyproject.toml .
RUN pip install --no-cache-dir -e ".[dev]" && \
    playwright install --with-deps chromium

COPY . .

RUN mkdir -p artifacts/runs artifacts/screenshots artifacts/traces artifacts/videos artifacts/reports

CMD ["python", "-m", "erp_test_agent", "--help"]
