from .base import BasePackage
from .models import Instruments, Records, Loans, AdvertsData, Adverts
from sqlalchemy import or_, and_
from hashlib import sha1

class SubPackageInstruments(BasePackage):
    def insert(self, class_name, instrument, brand, model, registry):
        """
        This function inserts an instrument in the instruments table.

        Args:
            class_name: The class of the instrument.
            instrument: The type of the instrument.
            brand: The brand of the instrument.
            model: The model of the instrument.
            registry: The registry code of the instrument.

        Returns:
            None, -1: If some exception was raised querying in database.
            obj, 0: Otherwise, with 'obj' being the row inserted in the table.
        """
        instrument_id = sha1(f'{class_name}-{instrument}-{brand}-{model}-{registry}'.encode()).hexdigest()
        
        return self.insert_object(table=Instruments, id=instrument_id, instrument_class=class_name, instrument=instrument, brand=brand, model=model, registry=registry)

    def get_by_attr(self, attr, values=[]):
        """
        This function gets all the instruments whom attr is in values list.

        Args:
            attr: An attribute of instruments table.
            values: A list with the required values for attr.

        Returns:
            None, -1: If some exception was raised querying in database.
            list, 0: Otherwise, with 'list' being [] if values is empty or a list with all the rows that fill any value in values.
        """
        return self.get_objects_by_attr(table=Instruments, attr=attr, values=values)

class SubPackageAdverts(BasePackage):
    def insert(self, active, prices, locator, instrument):
        """
        This function inserts an advert in the adverts table.

        Args:
            active: A boolean which tells if the ad is active.
            prices: An dict that maps time to price.
            locator: The locator's e-mail of the instrument.
            instrument: The id of a row in instruments table.

        Returns:
            None, -1: If some exception was raised querying in database.
            obj, 0: Otherwise, with 'obj' being the row inserted in the table.
        """
        advert_data_id = sha1(f'{prices}-{locator}-{instrument}'.encode()).hexdigest()

        self.insert_object(table=AdvertsData, id=advert_data_id, prices=str(prices), locator=locator, instrument=instrument)

        return self.insert_object(table=Adverts, active=active, data=advert_data_id)

    def get_by_attr(self, attr, values=[]):
        """
        This function gets all the adverts whom attr is in values list.

        Args:
            attr: An attribute of adverts table.
            values: A list with the required values for attr.

        Returns:
            None, -1: If some exception was raised querying in database.
            list, 0: Otherwise, with 'list' being [] if values is empty or a list with all the rows that fill any value in values.
        """
        return self.get_objects_by_attr(table=Adverts, attr=attr, values=values)

class SubPackageLoans(BasePackage):
    def insert(self, withdrawal, devolution, lessee, ad):
        """
        This function inserts a loan in the loans table.

        Args:
            withdrawal: Withdrawal date.
            devolution: Devolution date.
            lessee: The lessee's e-mail of this loan.
            ad: The id of a row in adverts data table.

        Returns:
            None, -1: If some exception was raised querying in database.
            obj, 0: Otherwise, with 'obj' being the row inserted in the table.
        """
        loan_id = sha1(f'{withdrawal}-{devolution}-{lessee}-{ad}'.encode()).hexdigest()

        return self.insert_object(table=Loans, id=loan_id, withdrawal=withdrawal, devolution=devolution, lessee=lessee, ad=ad)

    def get_by_attr(self, attr, values=[]):
        """
        This function gets all the loans whom attr is in values list.

        Args:
            attr: An attribute of loans table.
            values: A list with the required values for attr.

        Returns:
            None, -1: If some exception was raised querying in database.
            list, 0: Otherwise, with 'list' being [] if values is empty or a list with all the rows that fill any value in values.
        """
        return self.get_objects_by_attr(table=Loans, attr=attr, values=values)

class Business:
    def __init__(self, session_scope):
        self.instruments = SubPackageInstruments(session_scope)
        self.adverts = SubPackageAdverts(session_scope)
        self.loans = SubPackageLoans(session_scope)
    


    


    

    