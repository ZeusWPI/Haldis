"""Script for interaction and changes to the database"""

from app.add_admins import add

from app.app import create_app, db

from sqlalchemy import inspect

app = create_app()

entry_sets = {
    "admins": add,
}

yes = ["yes", "y"]
no = ["no", "n"]


def commit() -> None:
    """Commit all the things to the database"""
    db.session.commit()
    print("Committing successful")


def check_if_overwrite() -> bool:
    """Check if the user wants to overwrite the previous database"""
    answer = input("Do you want to overwrite the previous database? (y/N) ")
    return answer.lower() in yes


def add_all() -> None:
    "Add all possible entries in the entry_sets to the database"
    for entry_set, function in entry_sets.items():
        print(f"Adding {entry_set}.")
        function()


def recreate_from_scratch() -> None:
    """Recreate a completely new database"""
    print("Resetting the database!")
    db.drop_all()
    db.create_all()
    add_to_current()


def add_to_current() -> None:
    """Add things to the current database"""
    available = list(entry_sets)

    def add_numbers() -> str:
        return "  ".join(
            [f"{loc}({i}), " for i, loc in enumerate(available)]
        ).rstrip(", ")

    while input("Do you still want to add something? (Y/n) ").lower() not in no:
        print(
            "What do you want to add? (Use numbers, or A for all, or C for cancel)   "
        )
        answer = input(f"Available: {add_numbers()}  : ")
        if answer.lower() == "a":
            add_all()
            available = []
        elif answer.lower() == "c":
            pass
        elif answer.isnumeric() and answer in [str(x) for x in range(len(available))]:
            answer_index = int(answer)
            print(f"Adding {available[answer_index]}.")
            entry_sets[str(available[answer_index])]()
            del available[answer_index]
        else:
            print("Not a valid answer.")
    print("Thank you for adding, come again!")


with app.app_context():
    """Start the database interaction script"""
    print("Database modification script!")
    print("=============================\n\n")
    if (not inspect(db.engine).get_table_names()) or check_if_overwrite():
        recreate_from_scratch()
    else:
        add_to_current()
    commit()

