import os

# Gunicorn configuration file

# Server socket
# Use PORT environment variable if available, otherwise default to 8000
bind = f"0.0.0.0:{os.getenv('PORT', '8000')}"

# Worker processes
# Use WEB_CONCURRENCY if set, otherwise default to a sensible value (e.g., 2)
workers = int(os.getenv('WEB_CONCURRENCY', 2))
worker_class = "uvicorn.workers.UvicornWorker"

# Logging
# Set log level from environment or default to 'info'
loglevel = os.getenv('GUNICORN_LOG_LEVEL', 'info')
accesslog = "-"  # Log access logs to stdout
errorlog = "-"   # Log error logs to stderr

# Performance
timeout = int(os.getenv('GUNICORN_TIMEOUT', 120))
keepalive = int(os.getenv('GUNICORN_KEEPALIVE', 5))

# For reloading in development if needed, though uvicorn --reload is preferred
reload = bool(os.getenv('GUNICORN_RELOAD', False))
