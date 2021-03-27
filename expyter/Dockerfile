FROM python:3.10-rc-slim-buster

RUN pip install prometheus-client atlassian-python-api

COPY ./src/exporter.py .

CMD ["python", "exporter.py"]