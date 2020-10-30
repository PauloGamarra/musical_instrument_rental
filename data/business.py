from .base import BasePackage
from .models import Instruments, Records, Loans, AdvertsData, Adverts
from sqlalchemy import or_, and_
from hashlib import sha1

class Business(BasePackage):

    def insert_instrument(self, class_name, instrument, brand, model, registry):
        instrument_id = sha1(f'{class_name}-{instrument}-{brand}-{model}-{registry}'.encode()).hexdigest()
        
        return self.insert_object(table=Instruments, id=instrument_id, instrument_class=class_name, instrument=instrument, brand=brand, model=model, registry=registry)

    def get_instruments_by_attr(self, attr, values=[]):
        return self.get_objects_by_attr(table=Instruments, attr=attr, values=values)


    def insert_advert(self, active, prices, locator, instrument):
        advert_data_id = sha1(f'{prices}-{locator}-{instrument}'.encode()).hexdigest()

        self.insert_object(table=AdvertsData, id=advert_data_id, prices=str(prices), locator=locator, instrument=instrument)

        return self.insert_object(table=Adverts, active=active, data=advert_data_id)

    def get_adverts_by_attr(self, attr, values=[]):
        return self.get_objects_by_attr(table=Adverts, attr=attr, values=values)



    def insert_loan(self, withdrawal, devolution, lessee, ad):
        loan_id = sha1(f'{withdrawal}-{devolution}-{lessee}-{ad}'.encode()).hexdigest()

        return self.insert_object(table=Loans, id=loan_id, withdrawal=withdrawal, devolution=devolution, lessee=lessee, ad=ad)

    def get_loans_by_attr(self, attr, values=[]):
        return self.get_objects_by_attr(table=Loans, attr=attr, values=values)

    def insert_object(self, table, **kwargs):
        try:
            with self.session_scope() as session:
                obj = table(**kwargs)
                session.add(obj)
                session.commit()

            return obj, 0
        except Exception as err:
            print(f'Error: {err}')

            return None, -1

    def get_objects_by_attr(self, table, attr, values=[]):
        if values:
            try:
                with self.session_scope() as session:
                    objects = session.query(table).filter(attr.in_(values)).all()

                return objects, 0
            except Exception as err:
                print(f'Error: {err}')

                return None, -1
        else:
            return [], 0