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

There is a special script to get started with the project. Just run it in the root of the project.
Note: this script might require you to install a certain python version, you can do this using your favorite tool e.g. [pyenv](https://github.com/pyenv/pyenv#simple-python-version-management-pyenv)

	./first-setup.sh

This will create a virtual environment, install the necessary dependencies and will give you the option to seed the database.

If you are using a database other then sqlite you will first need to configure the correct URI to the database in the generated 'config.py' file.
Afterwards upgrade the database to the latest version using

	cd app
	python3 app.py db upgrade

You can now still seed the database by running, note that you might want to put your name in the `HALDIS_ADMIN_USERS` in `app/config.py`

	./populate-db.sh

in the root folder of the project.


Activate the virtual environment using

	source venv/bin/activate

Finally run the webserver with

	python3 app/app.py runserver

Make sure to use localhost instead of 127.0.0.1 if you want to be able to login.

## Development

### Changing the database

1. Update models located in 'app/models.py'
2. Run `python app/app.py db migrate` to create a new migration.
3. Apply the changes to the database using `python app/app.py db upgrade`

### Adding dependencies/libraries

1. Add new dependency to the `requirements.in` file
2. Run `pip-compile` to freeze the dependency into the `requirements.txt` file together with its own deps
3. Run `pip-sync` to download frozen deps

### Updating dependencies
Run `pip-compile --upgrade`

For more information about managing the dependencies see [jazzband/pip-tools: A set of tools to keep your pinned Python dependencies fresh.](https://github.com/jazzband/pip-tools)

### Github CI - WIP

CI/CD is done with the help of [dagger.io](). The tooling can easily be installed
by running the following wherever you want to install the binary (I propose
creating a `~/.local/bin` and adding it to your `PATH`). The install scripts
fetches the latest version and installs the binaries in a `./bin` folder of the
current working directory.

```
curl -L https://dl.dagger.io/dagger/install.sh | sh
```

On every push the CI will run `isort`, `black` and `pylint` against the codebase.

## Production
To prepare the application in a production environment, follow the same steps as for *Local setup* up to and including `./populate-db.sh`.

Set DEBUG to False in `app/config.py`.

See [Flask's deployment documentation](https://flask.palletsprojects.com/en/1.1.x/deploying/#self-hosted-options).

Set the server's Python interpreter to `/path/to/haldis/venv/bin/python`. Doing `source venv/bin/activate` is not necessary when that binary is used.
