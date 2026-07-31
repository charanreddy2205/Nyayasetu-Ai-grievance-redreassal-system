import multiprocessing
import os

# Server Socket
bind = os.getenv("GUNICORN_BIND", "0.0.0.0:8000")
backlog = 2048

# Worker Processes
# Recommended formula: 2 * num_cores + 1
workers = int(os.getenv("GUNICORN_WORKERS", multiprocessing.cpu_count() * 2 + 1))
worker_class = 'gthread'
threads = int(os.getenv("GUNICORN_THREADS", 4))
worker_connections = 1000
timeout = int(os.getenv("GUNICORN_TIMEOUT", 30))
keepalive = 2

# Process Management
pidfile = '/tmp/gunicorn.pid'
daemon = False


# Logging
errorlog = '-'
loglevel = os.getenv("GUNICORN_LOG_LEVEL", "info")
accesslog = '-'
access_log_format = '{"remote_ip":"%(h)s","request_id":"%({X-Request-Id}i)s","response_code":"%(s)s","request_method":"%(m)s","request_path":"%(U)s","request_querystring":"%(q)s","request_timetaken":"%(M)s","response_length":"%(B)s"}'

# Server Mechanics
graceful_timeout = int(os.getenv("GUNICORN_GRACEFUL_TIMEOUT", 30))
max_requests = 1000
max_requests_jitter = 50
