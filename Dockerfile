FROM python:3.6-alpine

RUN apk --update add bash nano

COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip install -r requirements.txt

COPY . /app

HEALTHCHECK CMD curl --fail http://localhost:3000 || exit 1

ENTRYPOINT [ "python" ]

CMD [ "contact/views.py" ]
