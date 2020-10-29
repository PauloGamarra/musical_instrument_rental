from .base import BasePackage
from .models import Users
from sqlalchemy import or_

class Auth(BasePackage):
    def create_user(self, name, email, password):
        """
        This function inserts a new user in users table on database.

        Args:
            name: The user's name.
            email: The user's email.
            password: The user's password.

        Returns:
            TODO: check what happens if already exists an user with this email
        """
        try:
            with self.session_scope() as session:
                user = Users(name=name, email=email, password=password)
                session.add(user)
                session.commit()

            return 0
        except Exception as err:
            print(f'Error: {err}')

            return -1

    def get_user(self, name = None, email = None):
        """
        This function gets an user from users table on database.

        Args:
            name: The user's name.
            email: The user's email.

        Returns:
            None, -1: If name and email are None, then returns.
            None, -2: If some exception was raised querying in database.
            user, 0: Otherwise, with 'user' being None if the user is not in database or being an object of Users if it is.
        """
        if name == None and email == None:
            return None, -1
        else:
            try:
                with self.session_scope() as session:
                    user = session.query(Users).filter(or_(Users.name == name, Users.email == email)).first()

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

            return True if user else False, 0
        except Exception as err:
            print(f'Error: {err}')

            return None, -1