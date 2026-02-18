Haldis
=======
[![chat mattermost](https://img.shields.io/badge/chat-mattermost-blue.svg)](https://mattermost.zeus.gent/zeus/channels/haldis)
[![Website](https://img.shields.io/website/https/haldis.zeus.gent.svg)](https://haldis.zeus.gent)
[![Mozilla HTTP Observatory Grade](https://img.shields.io/mozilla-observatory/grade-score/haldis.zeus.gent.svg?publish)](https://observatory.mozilla.org/analyze/haldis.zeus.gent)

![GitHub commit activity](https://img.shields.io/github/commit-activity/y/zeuswpi/haldis.svg)

Haldis is your friendly neighbourhood servant. He exists so lazy fucks like you and me don't need to keep tabs of who is ordering what from where.
Start an order and let people add items with a simple mouse-click!
No more calculating prices and making lists!
Be lazier today!

## Local development setup

### Using Docker

From the root of the project, run:

	docker compose up

This uses the `app/config.docker.py` file as the config.

### Manually

Install [uv](https://docs.astral.sh/uv/getting-started/installation/).

From the project root, run:

	uv sync

Make a config:

	cp app/config.example.py app/config.py

Edit the `app/config.py` file to suit your needs:
- If you are using a database other then sqlite you will first need to configure the correct URI to the database here.
- You might want to put your name in the `HALDIS_ADMINS` list.

Afterwards upgrade the database to the latest version using:

	uv run --directory=app flask --app migrate_app db upgrade

You can now seed the database by running: 

	./populate-db.sh

Finally run the webserver with:

	uv run --directory=app flask run --port=8000 --debug

Make sure to use localhost instead of 127.0.0.1 if you want to be able to login.

## Development

### Changing the database

1. Update models located in 'app/models.py'
2. Run `flask db migrate` to create a new migration.
3. Apply the changes to the database using `flask --app migrate_app db upgrade`

### Adding dependencies/libraries

1. Add new dependency by running `poetry add <package>`
2. Run `poetry install` to add the dependency to the lock file

### Updating dependencies

Run `poetry update`

### Problems

```
No module named '_sqlite3'
```
-> install `libsqlite3-dev` or equivalent

```
Error: Failed to find Flask application or factory in module 'app'. Use 'app:name' to specify one.
```
-> `cd app`


## Production

To prepare the application in a production environment, follow the same steps as for *Local setup* up to and including `./populate-db.sh`.

In `app/config.py`:
- Set DEBUG to False 
- Set REFRESH_OSM to True (to refresh all data every time the application starts)

See [Flask's deployment documentation](https://flask.palletsprojects.com/en/1.1.x/deploying/#self-hosted-options).

Set the server's Python interpreter to `/path/to/haldis/venv/bin/python`. Doing `source venv/bin/activate` is not necessary when that binary is used.
