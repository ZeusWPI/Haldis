# syntax=docker/dockerfile:1
FROM python:3.9.2-slim AS development

WORKDIR /src

RUN pip install pymysql

ADD https://git.zeus.gent/haldis/menus/-/archive/master/menus-master.tar /tmp
RUN mkdir menus && \
	tar --directory=menus --extract --strip-components=1 --file=/tmp/menus-master.tar

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

WORKDIR /src/app
CMD python app.py db upgrade && \
    python app.py runserver -h 0.0.0.0 -p 8000

FROM development AS production

RUN pip install waitress

CMD python app.py db upgrade && \
    python waitress_wsgi.py
