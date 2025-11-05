FROM python:3.11-slim

WORKDIR /app

COPY app/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY app/ .

EXPOSE 5000

ENV DB_HOST=postgres-service
ENV DB_PORT=5432
ENV DB_NAME=webapp_db
ENV DB_USER=webapp_user
ENV DB_PASSWORD=webapp_password

CMD ["python", "app.py"]
