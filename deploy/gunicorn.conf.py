bind = f"0.0.0.0:{__import__('os').getenv('PORT', '5000')}"
workers = 3
threads = 2
timeout = 120
accesslog = "-"
errorlog = "-"
graceful_timeout = 30
