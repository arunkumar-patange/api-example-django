FROM python:2.7


COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

ADD . /drchrono/src
WORKDIR /drchrono/src

CMD ["python", "manage.py", "runserver", "0.0.0.0:80"]
