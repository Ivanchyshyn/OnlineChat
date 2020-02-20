FROM python:3.7-alpine

WORKDIR /app
COPY requirements.txt .
RUN pip3 install -r requirements.txt

COPY . .
EXPOSE 8000

CMD ["/app/start.sh"]
