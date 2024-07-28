FROM python:3.9-slim

WORKDIR /app

COPY insert_to_redis.py ./
RUN pip install redis

CMD ["python", "insert_to_redis.py"]
