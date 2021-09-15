FROM python:3.8.0-alpine

WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN set -ex apk update \
    && apk add --no-cache postgresql-libs build-base \
    && apk add --no-cache postgresql-dev gcc python3-dev musl-dev \
    && apk add --no-cache bash git openssh \
    && apk add --no-cache fontconfig ttf-freefont font-noto terminus-font \
    && fc-cache -f \
    && fc-list | sort \
    && apk add tzdata \
    && cp /usr/share/zoneinfo/Europe/Warsaw /etc/localtime \
    && echo "Europe/Warsaw" > /etc/timezone \
    && apk del tzdata

RUN pip install --upgrade pip
COPY ./requirements.txt /usr/src/app/requirements.txt
RUN pip install -r requirements.txt

CMD [ "gunicorn", "-w", "4", "--bind", "0.0.0.0:5000", "--reload", "wsgi:app" ]