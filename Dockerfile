FROM python:3.11-slim

ENV FFUF_VERSION=2.1.0

# Install ffuf binary and minimal deps
RUN apt-get update && apt-get install -y \
    curl \
    ca-certificates \
    tar \
    && rm -rf /var/lib/apt/lists/* \
    && curl -sSL "https://github.com/ffuf/ffuf/releases/download/v${FFUF_VERSION}/ffuf_${FFUF_VERSION}_linux_amd64.tar.gz" -o /tmp/ffuf.tgz \
    && tar -xzf /tmp/ffuf.tgz -C /usr/local/bin ffuf \
    && chmod +x /usr/local/bin/ffuf \
    && rm /tmp/ffuf.tgz

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV HOST=0.0.0.0
EXPOSE 8000

CMD ["python", "server.py"]
