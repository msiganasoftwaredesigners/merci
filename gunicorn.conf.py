# gunicorn.conf.py
import multiprocessing

workers = multiprocessing.cpu_count() * 2 + 1  # Optimal worker count
worker_class = 'gevent'  # Async workers for Django
timeout = 120            # Worker timeout (seconds)
keepalive = 65           # Keep-alive for connections
bind = '0.0.0.0:8000'    # Binding address
max_requests = 1000      # Restart workers after N requests (prevents memory leaks)
max_requests_jitter = 50 # Randomize worker recycling