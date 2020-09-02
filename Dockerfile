FROM tiangolo/uvicorn-gunicorn:python3.8-slim
RUN pip install --no-cache-dir fastapi google-cloud-storage google-cloud-firestore
COPY ./app /app