import multiprocessing

# Jumlah worker berdasarkan jumlah core CPU
workers = multiprocessing.cpu_count() * 2 + 1
# Worker class menggunakan uvicorn
worker_class = "uvicorn.workers.UvicornWorker"
# Bind ke semua IP di port 8000
bind = "0.0.0.0:8000"
# Aktifkan reload otomatis
reload = True
# Log level
loglevel = "info"
# Access log
accesslog = "./access.log"
# Error log
errorlog = "./error.log" 