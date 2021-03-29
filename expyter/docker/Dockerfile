FROM python:3.10-rc-slim-buster

ADD . .
RUN pip install -r requirements.txt

WORKDIR /src
ENV PYTHONPATH '/src/'

CMD ["python", "/src/exporter.py"]