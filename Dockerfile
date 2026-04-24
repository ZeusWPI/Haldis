# syntax=docker/dockerfile:1
FROM python:3.12.4-slim AS build

WORKDIR /

RUN apt update -y && apt install -y build-essential curl git
RUN curl https://sh.rustup.rs -sSf | sh -s -- -y
ENV PATH="/root/.cargo/bin:${PATH}"

COPY pyproject.toml uv.lock .
RUN pip install uv
ENV UV_PROJECT_ENVIRONMENT="/usr/local/"
RUN uv sync --locked

RUN git clone https://git.zeus.gent/Haldis/menus.git menus

FROM python:3.12.4-slim AS development

WORKDIR /src

COPY --from=build menus menus

COPY --from=build /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages

COPY --from=build /usr/local/bin /usr/local/bin

COPY . .

WORKDIR /src/app
CMD python -m flask --app migrate_app db upgrade && \
    flask run --port=8000 --debug --host=0.0.0.0

FROM development AS production  

RUN pip install waitress

CMD flask --app migrate_app db upgrade && \
    cd .. && \
    python waitress_wsgi.py
