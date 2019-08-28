class AnonymouseUser:
    id = None

    def is_active(self):
        return False

    def is_authenticated(self):
        return False

    def is_anonymous(self):
        return True

    def is_admin(self):
        return False

    def get_id(self):
        return None
