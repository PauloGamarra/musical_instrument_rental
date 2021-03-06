from .base import BasePackage
from .models import Records, Loans, AdvertsData
from hashlib import sha1
from enum import Enum
from typing import Tuple, List, Optional

class UserTypeLoan(Enum):
    Lessee = Loans.lessee
    Locator = AdvertsData.locator

class HistoricalRecords(BasePackage):
    def upsert(self, loan: str, rating: int) -> Tuple[Optional[Records], Optional[Exception]]:
        """
        This function upserts an historical record in the records table.

        Args:
            loan: The id of the loan.
            rating: An integer in [0, 10] which rates the loan.

        Returns:
            None, err: If some exception was raised querying in database, where err is an exception.
            obj, None: Otherwise, with 'obj' being the row inserted in the table.
        """
        return self.upsert_object(table=Records, loan=loan, rating=rating)

    def get_all_records(self) -> Tuple[Optional[List[Records]], Optional[Exception]]:
        """
        This function gets all the records in the records table.

        Returns:
            None, err: If some exception was raised querying in database, where err is an exception.
            list, None: Otherwise, with 'list' being a list with all the rows in the records table.
        """
        return self.get_all_objects(Records)

    def get_by_email(self, email: str, user_type: UserTypeLoan = UserTypeLoan.Lessee) -> Tuple[Optional[List[Records]], Optional[Exception]]:
        """
        This function gets all the objects whose attr is in values list.

        Args:
            email: An email.
            user_type: An enum setting the user type (locator/lessee)

        Returns:
            None, err: If some exception was raised querying in database, where err is an exception.
            records, None: Otherwise, with 'records' being a list with all the rows that have this e-mail for its lessee.
        """
        email = sha1(f'{email}'.encode()).hexdigest()

        try:
            with self.session_scope() as session:
                records = session.query(Records, Loans, AdvertsData).filter(user_type == email).all()

            return records, None
        except Exception as err:
            print(f'Error: {err}')

            return None, err