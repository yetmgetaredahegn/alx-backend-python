# Use Python 3.10 slim: small-ish, Debian-based (glibc), good for mysqlclient
FROM python:3.10-slim

# Working directory inside the container
WORKDIR /app

# Make Python output immediately (no buffering) — helps logs appear in real time
ENV PYTHONUNBUFFERED=1

# Install OS packages needed to compile native Python extensions (mysqlclient)
# --no-install-recommends keeps packages minimal. Clean apt lists afterwards.
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
      build-essential \
      default-libmysqlclient-dev \
      gcc \
      libssl-dev \
      libffi-dev \
      pkg-config \
      netcat-openbsd && \
    rm -rf /var/lib/apt/lists/*



# Copy requirements.txt first so pip install can be cached by Docker layers
COPY requirements.txt .

# Upgrade pip and install Python deps (no cache to save space)
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy application source code into the image
COPY . .

# Ensure entrypoint is executable (entrypoint.sh will be created next)
RUN chmod +x ./entrypoint.sh || true

# Create a non-root user and switch to it (security best practice)
RUN useradd --create-home appuser
USER appuser
ENV HOME=/home/appuser

# Expose the port Django runs on
EXPOSE 8000

# Default command runs entrypoint which will handle migrations and start the server
CMD ["./entrypoint.sh"]
