class EmailAlreadyExists(Exception):
    def __init__(self):
        super().__init__("Email already exists")


class UserNotFound(Exception):
    def __init__(self):
        super().__init__("User not found.")


class UserIsExists(Exception):
    def __init__(self):
        super().__init__("User already exists.")


class PhoneAlreadyExists(Exception):
    def __init__(self):
        super().__init__("Phone already exists.")


class PassportNumberAlreadyExists(Exception):
    def __init__(self):
        super().__init__("Passport number already exists.")
