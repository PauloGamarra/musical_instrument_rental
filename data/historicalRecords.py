from .base import BasePackage
from .models import Records, Loans, AdvertsData

class HistoricalRecords(BasePackage):
    def insert(self, loan, rating):
        return self.insert_object(table=Records, loan=loan, rating=rating)

    def get_by_email(self, email):
        try:
            with self.session_scope() as session:
                records = session.query(Records, Loans, AdvertsData).filter(Loans.lessee == email).all()

            return records, None
        except Exception as err:
            print(f'Error: {err}')

            return None, err