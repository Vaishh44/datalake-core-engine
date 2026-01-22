FROM python:3.10-slim

# Install Java 17 for PySpark
RUN apt-get update && \
    apt-get install -y openjdk-17-jre-headless curl procps && \
    rm -rf /var/lib/apt/lists/*

ENV JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64

# Set standard generic S3 configs
ENV AWS_ACCESS_KEY_ID=any
ENV AWS_SECRET_ACCESS_KEY=any
ENV AWS_REGION=us-east-1

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
