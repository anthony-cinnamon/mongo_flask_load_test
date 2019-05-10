FROM ubuntu:18.04

RUN apt-get update \
    && apt-get install -y curl python3 python3-distutils

RUN update-alternatives --install /usr/bin/python python /usr/bin/python3.6 99

RUN curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py \
  && python get-pip.py

COPY requirements.txt /tmp/requirements.txt

RUN pip install -r /tmp/requirements.txt

COPY config/config.json /etc/config.json
COPY . /code

WORKDIR /code

CMD [ "gunicorn", "-w", "3", "--bind", "0.0.0.0:5000", "--capture-output", "flaskr:application" ]