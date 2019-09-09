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
