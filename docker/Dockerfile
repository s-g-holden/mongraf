FROM python:3.10-rc-slim-buster

RUN pip install prometheus-client

COPY ./exporter.py .

CMD ["python", "exporter.py"]