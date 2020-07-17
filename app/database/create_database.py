"Script for interaction and changes to the database"
import add_admins
from app import db, app_manager

entry_sets = {
    "admins": add_admins.add,
}

yes = ["yes", "y"]
no = ["no", "n"]


def commit() -> None:
    "Commit all the things to the database"
    db.session.commit()
    print("Committing successful")


def check_if_overwrite() -> bool:
    "Check if the user wants to overwrite the previous database"
    answer = input("Do you want to overwrite the previous database? (y/N) ")
    return answer.lower() in yes


def add_all() -> None:
    "Add all possible entries in the entry_sets to the database"
    for entry_set, function in entry_sets.items():
        print("Adding {}.".format(entry_set))
        function()


def recreate_from_scratch() -> None:
    "Recreate a completely new database"
    confirmation = "Are you very very sure? (Will delete previous entries!) (y/N) "
    if input(confirmation).lower() in yes:
        print("Resetting the database!")
        db.drop_all()
        db.create_all()
        add_to_current()
    else:
        print("You cancelled.")


def add_to_current() -> None:
    "Add things to the current database"
    available = [entry_set for entry_set in entry_sets]

    def add_numbers() -> str:
        return "  ".join(
            ["{}({}), ".format(loc, i) for i, loc in enumerate(available)]
        ).rstrip(", ")

    while input("Do you still want to add something? (Y/n) ").lower() not in no:
        print(
            "What do you want to add? (Use numbers, or A for all, or C for cancel)   "
        )
        answer = input("Available: {}  : ".format(add_numbers()))
        if answer.lower() == "a":
            add_all()
            available = []
        elif answer.lower() == "c":
            pass
        elif answer.isnumeric() and answer in [str(x) for x in range(len(available))]:
            answer_index = int(answer)
            print("Adding {}.".format(available[answer_index]))
            entry_sets[str(available[answer_index])]()
            del available[answer_index]
        else:
            print("Not a valid answer.")
    print("Thank you for adding, come again!")


@app_manager.command
def setup_database():  # type: None
    "Start the database interaction script"
    print("Database modification script!")
    print("=============================\n\n")
    if check_if_overwrite():
        recreate_from_scratch()
    else:
        add_to_current()
    commit()


app_manager.run()
