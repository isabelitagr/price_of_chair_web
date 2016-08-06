
class UserError(Exception):
    def __init__(self, message):
        self.message = message


class UserNotExistsError(UserError): # heredo de UserError
    pass


class IncorrectPasswordError(UserError): # heredo de UserError
    pass

class UserAlreadyRegisteredError(UserError):
    pass

class InvalidEmailError(UserError):
    pass