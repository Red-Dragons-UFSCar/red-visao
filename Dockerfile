FROM ubuntu

ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get update \
    && apt-get -y install python pip python3-pyqt5

WORKDIR /usr/red
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
RUN pip install -e .
ENTRYPOINT python3 /usr/red/bin/main.py