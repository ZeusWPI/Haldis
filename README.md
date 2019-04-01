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
2. `cd app`
3. Copy `config.example.py` to `config.py`
4. Copy the python files from `database/` to `app/` (yes, it's sad, I know)
5. Run `python create_database.py` in `app/` (if you want to fill the DB with sample data be sure to answer `Y` to `Do you still want to add something?`)
6. Run `rm -f add_* create_database.py*` in `app/`
7. Run `python haldis.py runserver`

---
Or run `./first-setup.sh` in the root of the git folder (in linux)
