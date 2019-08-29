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

    ./first-setup.sh
    
This will create a virtual environment, install the necessary dependencies and will give you the option to seed the database.

If you are using a database other then sqlite you will first need to configure the correct uri to the database in the generated 'config.py' file.
Afterwards upgrade the database to the latest version using 

    cd app
    python haldis.py db upgrade
    
You can now still seed the database by running

    ./populate-db.sh
    
in the root folder of the project.


Activate the virtual environment using

    source venv/bin/activate

Finally run the webserver with

    python app/haldis.py runserver
    
## Development

### Changing the database

1. Update models located in 'app/models.py'
2. Run `python app/haldis.py db migrate` to create a new migration.
3. Apply the changes to the database using `python app/haldis.py db upgrade`

### Adding dependencies/libraries

1. Add new dependency to the `requirements.in` file
2. Run `pip-compile` to freeze the dependency into the `requirements.txt` file together with it's own deps
3. Run `pip-sync` to download frozen deps

### Updating dependencies
Run `pip-compile --upgrade`

For more information about managing the dependencies see [jazzband/pip-tools: A set of tools to keep your pinned Python dependencies fresh.](https://github.com/jazzband/pip-tools)

## Authors

* **Feliciaan De Palmenaer** - *Initial work* - [Github](https://github.com/feliciaan)