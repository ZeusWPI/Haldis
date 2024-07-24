# syntax=docker/dockerfile:1
FROM python:3.12.4-slim AS development

WORKDIR /src

RUN pip install pymysql

ADD https://git.zeus.gent/Haldis/menus/archive/master.tar.gz /tmp
RUN mkdir menus && \
	tar --directory=menus --extract --strip-components=1 --file=/tmp/master.tar.gz

# install cargo
RUN apt-get -y update; apt-get -y install curl build-essential
RUN curl https://sh.rustup.rs -sSf | sh -s -- -y
ENV PATH="/root/.cargo/bin:${PATH}"

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

WORKDIR /src/app
CMD flask --app migrate_app db upgrade && \
    flask run -h 0.0.0.0 -p 8000

FROM development AS production

RUN pip install waitress

CMD flask --app migrate_app db upgrade && \
    python waitress_wsgi.py
