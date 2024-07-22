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

## Local setup

### Docker
From the root of the project, run:

	docker compose up

This uses the `config.docker.py` file as the config.

### Manual

There is a special script to get started with the project. Just run it in the root of the project.
Note: this script might require you to install a certain python version, you can do this using your favorite tool e.g. [pyenv](https://github.com/pyenv/pyenv#simple-python-version-management-pyenv)

	./first-setup.sh

This will create a virtual environment, install the necessary dependencies and will give you the option to seed the database.

If you are using a database other then sqlite you will first need to configure the correct URI to the database in the generated 'config.py' file.
Afterwards upgrade the database to the latest version using

	cd app
	flask db upgrade

You can now still seed the database by running, note that you might want to put your name in the `HALDIS_ADMINS` in `app/config.py`

	./populate-db.sh

in the root folder of the project.


Activate the virtual environment using

	source venv/bin/activate

Finally run the webserver with

	`flask run --port=8000 --debug`

Make sure to use localhost instead of 127.0.0.1 if you want to be able to login.

## Development

### Changing the database

1. Update models located in 'app/models.py'
2. Run `flask db migrate` to create a new migration.
3. Apply the changes to the database using `flask db upgrade`

### Adding dependencies/libraries

1. Add new dependency to the `requirements.in` file
2. Run `pip-compile` to freeze the dependency into the `requirements.txt` file together with its own deps
3. Run `pip-sync` to download frozen deps

### Updating dependencies
Run `pip-compile --upgrade`

For more information about managing the dependencies see [jazzband/pip-tools: A set of tools to keep your pinned Python dependencies fresh.](https://github.com/jazzband/pip-tools)

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

Set DEBUG to False in `app/config.py`.

See [Flask's deployment documentation](https://flask.palletsprojects.com/en/1.1.x/deploying/#self-hosted-options).

Set the server's Python interpreter to `/path/to/haldis/venv/bin/python`. Doing `source venv/bin/activate` is not necessary when that binary is used.
