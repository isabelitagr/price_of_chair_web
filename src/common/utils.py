from passlib.hash import pbkdf2_sha512
import re

class Utils(object):


    @staticmethod
    def email_is_valid(email):
        email_address_matcher = re.compile('^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*$')  # ('^[\w-]+@+([w-]+\.)+[\w]+$')
        return True if email_address_matcher.match(email) else False


    @staticmethod
    def hash_password(password):
        '''
        Hashes a password using pbkdf2_sha512
        :param password: The sha512 password from the login/register form
        :return: A sha512-> pbkdf2_sha512 encrypted password
        '''
        return pbkdf2_sha512.encrypt(password)


    @staticmethod
    def check_hashed_password(password, hashed_password):
        '''
        Checks that the oassword the user sent matches the one in the password.
        The database password is ecrypted more than the users password at this stage
        :param password: sha512-hashed password
        :param hashed_password:  pbkdf2_sha512 encrypted password
        :return: True if password match, False otherwise
        '''
        return pbkdf2_sha512.verify(password, hashed_password)

