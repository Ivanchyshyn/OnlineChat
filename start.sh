echo "====== RUN APP ======"
gunicorn src:main --bind 0.0.0.0:8000 --worker-class aiohttp.GunicornWebWorker