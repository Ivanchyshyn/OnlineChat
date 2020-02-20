echo "====== RUN APP ======"
gunicorn main:app --bind 0.0.0.0:8000 --worker-class aiohttp.GunicornWebWorker