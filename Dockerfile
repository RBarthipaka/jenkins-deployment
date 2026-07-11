# ---- Base image ----
FROM python:3.11-slim

# ---- Environment settings ----
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    STREAMLIT_SERVER_HEADLESS=true \
    STREAMLIT_SERVER_PORT=8501 \
    STREAMLIT_SERVER_ADDRESS=0.0.0.0

WORKDIR /app

# ---- Install OS-level deps (only what's usually needed for pandas/openpyxl etc.) ----
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# ---- Install Python deps first (better layer caching) ----
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ---- Copy app code ----
COPY . .

# ---- Expose Streamlit port ----
EXPOSE 8601

# ---- Healthcheck (optional but useful for Jenkins/monitoring) ----
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD curl -f http://localhost:8501/_stcore/health || exit 1

# ---- Run the app ----
ENTRYPOINT ["streamlit", "run", "app.py"]
