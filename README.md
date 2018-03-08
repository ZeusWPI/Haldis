Haldis
=======

Haldis is your friendly neighbourhood servant. He exists so lazy fucks like you and me don't need to keep tabs of who is ordering what from where.
Start an order and let people add items with a simple mouse-click!
No more calculating prices and making lists!
Be lazier today!

Local hosting steps
===================
1. Run `pip install -r requirements.txt`
2. Copy `config.example.py` to `config.py` and fill in random values for the `ZEUS_KEY` and `ZEUS_SECRET` 
3. Copy the python files from `database/` to `app/` (yes, it's sad, I know)
4. Run `python database.py` in `app/`
5. Run `rm -f add_admins.pyc? add_oceans_garden.pyc? add_simpizza.pyc? create_database.pyc?` in `app/`
6. Run `python haldis.py runserver`
