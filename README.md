### Python
```
apt install python3
python3 -m venv env
env/bin/python -m pip install -r requirements.txt
```

### Redis
```
brew install redis-server
brew services start redis
```

### Gunicorn
```
gunicorn src:main --bind 0.0.0.0:8000 --worker-class aiohttp.GunicornWebWorker
```
