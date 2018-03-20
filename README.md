Haldis
=======

Haldis is your friendly neighbourhood servant. He exists so lazy fucks like you and me don't need to keep tabs of who is ordering what from where.
Start an order and let people add items with a simple mouse-click!
No more calculating prices and making lists!
Be lazier today!

Local hosting steps
===================
0. This is a Python 3 project so make sure to use python 3 and pip3 everywhere
1. Run `pip install -r requirements.txt`
2. Copy `config.example.py` to `config.py`
3. Copy the python files from `database/` to `app/` (yes, it's sad, I know)
4. Run `python database.py` in `app/` (if you want to fill the DB with sample data be sure to answer `Y` to `Do you still want to add something?`)
5. Run `rm -f add_admins.py* add_oceans_garden.py* add_simpizza.py* create_database.py*` in `app/`
6. Run `python haldis.py runserver`
