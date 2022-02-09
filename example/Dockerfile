#FROM python:3.6
#FROM python:3.7
#FROM python:3.8
#FROM python:3.9
FROM python:3.10

WORKDIR ./

COPY . .

RUN pip install multirunnable

CMD [ "python3", "./<Program Under Test>.py" ]
