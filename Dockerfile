FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

ADD https://netfree.link/dl/unix-ca.sh /home/netfree-unix-ca.sh
RUN cat  /home/netfree-unix-ca.sh | sh
ENV NODE_EXTRA_CA_CERTS=/etc/ca-bundle.crt
ENV SSL_CERT_FILE=/etc/ca-bundle.crt
ENV REQUESTS_CA_BUNDLE=/etc/ssl/certs/ca-certificates.crt

RUN pip install --no-cache-dir -r requirements.txt

COPY src/main.py .

CMD ["pytest", "src/main.py"]
