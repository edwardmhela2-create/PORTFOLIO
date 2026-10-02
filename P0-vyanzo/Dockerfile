FROM python:3.12-slim

WORKDIR /app

RUN pip install --no-cache-dir flask

COPY app.py benki.db ./

EXPOSE 5000

CMD ["python", "app.py"]
