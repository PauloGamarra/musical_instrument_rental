from .base import BasePackage, RowAlreadyExists, BadRequestForQuery
from .models import Users
from sqlalchemy import or_
from sqlalchemy.exc import IntegrityError
from psycopg2.errors import UniqueViolation
from hashlib import sha1

class UserAlreadyExists(RowAlreadyExists):
    def __init__(self):
        super().__init__(table='Users')

class Auth(BasePackage):
    def create_user(self, name, email, password, admin=False):
        """
        This function inserts a new user in users table on database.

        Args:
            name: The user's name.
            email: The user's email.
            password: The user's password.

        Returns:
            None, err: If some exception was raised querying in database, where err is an exception.
            Users, None: Otherwise, with user being the user inserted in database.

        Raises:
            UserAlreadyExists: If already exists an user with this e-mail
        """
        user_id = sha1(f'{email}'.encode()).hexdigest()

        try:
            with self.session_scope() as session:
                user = Users(id=user_id, name=name, email=email, password=password, admin=admin)
                session.add(user)
                session.commit()

            return user, None
        except IntegrityError as err:
            if isinstance(err.orig, UniqueViolation):
                raise UserAlreadyExists()
            else:
                print(f'Error: {err}')
                return None, err
        except Exception as err:
            print(f'Error: {err}')

            return None, err

    def get_user(self, name = None, email = None, user_id = None):
        """
        This function gets an user from users table on database.

        Args:
            name: The user's name.
            email: The user's email.
            user_id: The user's id.

        Returns:
            None, BadRequestForQuery: If name, email and user_id are None, then returns None and an exception explaining the necessary args.
            None, err: If some exception was raised querying in database, where err is an exception.
            user, None: Otherwise, with 'user' being None if the user is not in database or being an object of Users if it is.
        """
        if name == None and email == None and user_id == None:
            return None, BadRequestForQuery('Users', ['name', 'email', 'user_id'])
        else:
            try:
                with self.session_scope() as session:
                    user = session.query(Users).filter(or_(Users.id == user_id, Users.name == name, Users.email == email)).first()

                return user, None
            except Exception as err:
                print(f'Error: {err}')

                return None, err

    def get_all_users(self):
        """
        This function gets all the users in the users table.

        Returns:
            None, err: If some exception was raised querying in database, where err is an exception.
            list, None: Otherwise, with 'list' being a list with all the rows in the users table.
        """
        return self.get_all_objects(Users)

    def check_password(self, user, password):
        """
        This function checks if the password is correct according to the user.

        Args:
            user: The user's name or e-mail.
            password: The user's password.

        Returns:
            None, err: If some exception was raised querying in database.
            bool, None: Otherwise, with 'bool' being False if the password is wrong or True if the password is the same in the database.
        """
        try:
            with self.session_scope() as session:
                user = session.query(Users).filter(or_(Users.name == user, Users.email == user), Users.password == password).first()

            return True, None if user else False, None
        except Exception as err:
            print(f'Error: {err}')

            return None, err