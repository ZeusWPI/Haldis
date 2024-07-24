# syntax=docker/dockerfile:1
FROM python:3.12.4-slim AS compile

RUN pip install poetry

COPY pyproject.toml poetry.lock .

RUN poetry export --without-hashes --format=requirements.txt > requirements.txt

FROM python:3.12.4-slim AS build

# install cargo
RUN apt-get -y update; apt-get -y install curl build-essential
RUN curl https://sh.rustup.rs -sSf | sh -s -- -y
ENV PATH="/root/.cargo/bin:${PATH}"

COPY --from=compile requirements.txt .

RUN pip install -r requirements.txt

FROM python:3.12.4-slim AS development

WORKDIR /src

ADD https://git.zeus.gent/Haldis/menus/archive/master.tar.gz /tmp
RUN mkdir menus && \
	tar --directory=menus --extract --strip-components=1 --file=/tmp/master.tar.gz

COPY --from=build /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages

COPY --from=build /usr/local/bin /usr/local/bin

COPY . .

WORKDIR /src/app
CMD python -m flask --app migrate_app db upgrade && \
    flask run --port=8000 --debug --host=0.0.0.0

FROM development AS production  

RUN pip install waitress

CMD python -m flask --app migrate_app db upgrade && \
    python waitress_wsgi.py
