import uuid

from src.common.database import Database
from src.common.utils import Utils
import src.models.users.errors as UserErrors # importa todao el file y lo llama UserErrors
from src.models.alerts.alert import Alert
import src.models.users.constants as UserConstants

class User(object):

    def __init__(self, email, password, _id=None):
        self.email = email
        self.password = password
        self._id = uuid.uuid4().hex if _id == None else _id


    def __repr__(self):
        return "<User {}>".format(self.email)


    @staticmethod
    def is_login_valid(email, password):
        '''
        This method verifies that the email-password combo (as sent by the site forms) is valid or not
        Check that email exists, and that the password associate to that email is correct
        :param email: the user's email
        :param password: a sha512 hashed password
        :return: True if valid, False otherwise
        '''

        user_data = Database.find_one(UserConstants.COLLECTION, {'email': email}) # password in sha512 -> pbkdf2_sha512
        if user_data is None:
            #tell the user their password doesn't exists
            raise UserErrors.UserNotExistsError("Your user doesn't exists") # lo levantamos y lo podemos catchear desde donde se lo llame
        if not Utils.check_hashed_password(password, user_data['password']):
            # Tell the  user that their password is wrong
            raise UserErrors.IncorrectPasswordError("Your password was wrong")
        return True


    @staticmethod
    def register_user(email, password):
        '''
        this method register a user using email and password.
        The password already comes hashed as sha512
        :param email: user's email (might bbe invalid)
        :param password: sha512-hashed password
        :return: True if registered succefully, or False otherwise (exceptions can also be raised)
        '''

        user_data = Database.find_one(UserConstants.COLLECTION, {'email': email})
        if user_data is not None:
            raise UserErrors.UserAlreadyRegisteredError('That email already exists')
        if not Utils.email_is_valid(email):
            raise UserErrors.InvalidEmailError('The email has not the right format')

        User(email, Utils.hash_password(password)).save_to_db()

        return True


    def save_to_db(self):
        Database.insert(UserConstants.COLLECTION, self.json())

    def json(self):
        return {
            '_id': self._id,
            'email': self.email,
            'password': self.password  # la pass ya esta hasheada
        }

    @classmethod
    def find_by_email(cls, email):
        return cls(**Database.find_one(UserConstants.COLLECTION, {'email': email}))


    def  get_alerts(self):
        return Alert.find_by_user_email(self.email) # llamo desde aca porque si no la view de user tiene que tratar con dos modelos distintos (user y alert) y no esta bien