FROM python:3.12.2-alpine

WORKDIR /Internship_frontend

ADD . /Internship_frontend/

RUN python3 -m pip install -r requirements.txt

ENV FLASK_APP=Internship_frontend
ENV FLASK_ENV=development

CMD flask run --host 0.0.0.0

EXPOSE 5000


