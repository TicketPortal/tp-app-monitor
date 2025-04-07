FROM python:3.10-slim

WORKDIR /app

COPY exporter.py .

RUN pip install flask requests

EXPOSE 8000

CMD ["python", "exporter.py"]