FROM tiangolo/uvicorn-gunicorn:python3.8-slim
RUN pip install --no-cache-dir fastapi
COPY ./app /app