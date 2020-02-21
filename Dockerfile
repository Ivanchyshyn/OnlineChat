FROM python:3.7-alpine

WORKDIR /app

RUN apk add --update bash postgresql-dev gcc python3-dev musl-dev zlib-dev

COPY requirements.txt .
RUN pip3 install -r requirements.txt

COPY . .
EXPOSE 8000

CMD ["/app/start.sh"]
