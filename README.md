Haldis
=======

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

    python haldis.py db upgrade
    
You can now still seed the database by running

    ./populate-db.sh
    
in the root folder of the project.
    
## Development

### Changing the database

1. Update models located in 'app/models.py'
2. Run `python haldis.py db migrate` to create a new migration.
3. Apply the changes to the database using `python haldis.py db upgrade`
