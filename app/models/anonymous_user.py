"AnonymouseUser for people who are not logged in the normal way"
# pylint: disable=R0201,C0111


class AnonymouseUser:
    id = None

    def is_active(self) -> bool:
        return False

    def is_authenticated(self) -> bool:
        return False

    def is_anonymous(self) -> bool:
        return True

    def is_admin(self) -> bool:
        return False

    def get_id(self) -> None:
        return None
