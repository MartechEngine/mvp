# --- Stage 1: Builder ---
# This stage builds a virtual environment with all necessary dependencies.
FROM python:3.11-slim as builder

# Set environment variables to prevent generating .pyc files and ensure output is sent directly
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install OS-level dependencies required for compiling some Python packages
RUN apt-get update && apt-get install -y --no-install-recommends build-essential

# Create and activate a virtual environment
WORKDIR /opt/venv
RUN python -m venv .
ENV PATH="/opt/venv/bin:$PATH"

# Copy and install Python requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# --- Stage 2: Final Production Image ---
FROM python:3.11-slim

# Create a dedicated, non-root user for security
RUN addgroup --system --gid 1001 appgroup && \
    adduser --system --uid 1001 --ingroup appgroup appuser

# Set the working directory inside the app user's home
WORKDIR /home/appuser

# Copy the pre-built virtual environment from the builder stage
COPY --from=builder /opt/venv /opt/venv

# Copy the application code with ownership set to the non-root user
# This prevents the code from being owned by root
COPY --chown=appuser:appgroup ./app ./app

# Set the PATH environment variable to use the virtual environment's executables
ENV PATH="/opt/venv/bin:$PATH"

# Switch to the non-root user
USER appuser

# Expose the port the application will run on
EXPOSE 8000

# The default command to run the application in a production environment using Gunicorn.
# This will be used in production. Docker Compose will override this for local development.
CMD ["gunicorn", "-k", "uvicorn.workers.UvicornWorker", "app.main:app", "--bind", "0.0.0.0:8000"]
