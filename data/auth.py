from .base import BasePackage
from .models import Users
from sqlalchemy import or_
from sqlalchemy.exc import IntegrityError
from psycopg2.errors import UniqueViolation

class UserAlreadyExists(Exception):
    def __init__(self, message = 'Error: already exists an user with this e-mail.'):
        self.__message = message

        super().__init__(self.__message)

class Auth(BasePackage):
    def create_user(self, name, email, password):
        """
        This function inserts a new user in users table on database.

        Args:
            name: The user's name.
            email: The user's email.
            password: The user's password.

        Returns:
            None, -1: If some exception was raised querying in database.
            user, 0: Otherwise, with user being the user inserted in database.

        Raises:
            UserAlreadyExists: If already exists an user with this e-mail
        """
        try:
            with self.session_scope() as session:
                user = Users(name=name, email=email, password=password)
                session.add(user)
                session.commit()

            return user, 0
        except IntegrityError as e:
            if isinstance(e.orig, UniqueViolation):
                raise UserAlreadyExists()
            else:
                print(f'Error: {err}')
                return None, -1
        except Exception as err:
            print(f'Error: {err}')

            return None, -1

    def get_user(self, name = None, email = None, user_id = None):
        """
        This function gets an user from users table on database.

        Args:
            name: The user's name.
            email: The user's email.
            user_id: The user's id.

        Returns:
            None, -1: If name, email and user_id are None, then returns.
            None, -2: If some exception was raised querying in database.
            user, 0: Otherwise, with 'user' being None if the user is not in database or being an object of Users if it is.
        """
        if name == None and email == None and user_id == None:
            return None, -1
        else:
            try:
                with self.session_scope() as session:
                    user = session.query(Users).filter(or_(Users.id == user_id, Users.name == name, Users.email == email)).first()

                return user, 0
            except Exception as err:
                print(f'Error: {err}')

                return None, -2

    def check_password(self, user, password):
        """
        This function checks if the password is correct according to the user.

        Args:
            user: The user's name or e-mail.
            password: The user's password.

        Returns:
            None, -1: If some exception was raised querying in database.
            bool, 0: Otherwise, with 'bool' being False if the password is wrong or True if the password is the same in the database.
        """
        try:
            with self.session_scope() as session:
                user = session.query(Users).filter(or_(Users.name == user, Users.email == user), Users.password == password).first()

            return True, 0 if user else False, 0
        except Exception as err:
            print(f'Error: {err}')

            return None, -1