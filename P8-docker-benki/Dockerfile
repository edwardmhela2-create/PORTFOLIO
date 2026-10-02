FROM python:3.12-slim

WORKDIR /app

COPY P6-benki-app/ ./

RUN pip install --no-cache-dir flask

RUN useradd -m -u 1001 mtumiaji \
    && mkdir -p /data \
    && chown -R mtumiaji:mtumiaji /app /data

USER mtumiaji

ENV BENKI_DB=/data/benki.db

EXPOSE 5000

HEALTHCHECK --interval=30s --timeout=3s --start-period=10s --retries=3 \
    CMD python -c "import urllib.request; \
urllib.request.urlopen('http://localhost:5000/ingia', timeout=2)"

CMD ["python", "app.py"]
