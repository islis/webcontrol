FROM python:3
WORKDIR /opt
COPY requirements.txt /opt
RUN pip3 install -r requirements.txt
COPY . /opt
WORKDIR /opt/smarthouse
CMD python3 manage.py runserver 0.0.0.0:8000 | python3 manage.py mqtt_listener
