from .base import BasePackage
from .models import Instruments, Records, Loans, AdvertsData, Adverts
from sqlalchemy import or_, and_
from hashlib import sha1
from typing import Tuple, List, Dict, Callable, Optional
from datetime import date

class SubPackageInstruments(BasePackage):
    def upsert(self, class_name: str, instrument: str, brand: str, model: str, registry: str, popular: bool = False) -> Tuple[Optional[Instruments], Optional[Exception]]:
        """
        This function upserts an instrument in the instruments table.

        Args:
            class_name: The class of the instrument.
            instrument: The type of the instrument.
            brand: The brand of the instrument.
            model: The model of the instrument.
            registry: The registry code of the instrument.
            popular: The boolean in respect to the popularity of the instrument.

        Returns:
            None, err: If some exception was raised querying in database, where err is an exception.
            obj, None: Otherwise, with 'obj' being the row inserted in the table.
        """
        instrument_id = sha1(f'{class_name}-{instrument}-{brand}-{model}-{registry}'.encode()).hexdigest()

        return self.upsert_object(table=Instruments, id=instrument_id, instrument_class=class_name, instrument=instrument, brand=brand, model=model, registry=registry, popular=popular)

    def get_by_attr(self, attr: object, values: List[object] = list()) -> Tuple[Optional[Instruments], Optional[Exception]]:
        """
        This function gets all the instruments whose attr is in values list.

        Args:
            attr: An attribute of instruments table.
            values: A list with the required values for attr.

        Returns:
            None, err: If some exception was raised querying in database, where err is an exception.
            list, None: Otherwise, with 'list' being [] if values is empty or a list with all the rows that fill any value in values.
        """
        return self.get_objects_by_attr(table=Instruments, attr=attr, values=values)

    def get_all_instruments(self) -> Tuple[Optional[Instruments], Optional[Exception]]:
        """
        This function gets all the instruments in the instruments table.

        Returns:
            None, err: If some exception was raised querying in database, where err is an exception.
            list, None: Otherwise, with 'list' being a list with all the rows in the instruments table.
        """
        return self.get_all_objects(Instruments)

class SubPackageAdverts(BasePackage):
    def upsert(self, active: bool, prices: str, locator: str, instrument: str) -> Tuple[Optional[Adverts], Optional[Exception]]:
        """
        This function upserts an advert in the adverts table.

        Args:
            active: A boolean which tells if the ad is active.
            prices: A str that maps time to price.
            locator: The locator's id.
            instrument: The id of a row in instruments table.

        Returns:
            None, err: If some exception was raised querying in database, where err is an exception.
            obj, None: Otherwise, with 'obj' being the row inserted in the table.
        """
        advert_data_id = sha1(f'{prices}-{locator}-{instrument}'.encode()).hexdigest()

        self.upsert_object(table=AdvertsData, id=advert_data_id, prices=prices, locator=locator, instrument=instrument)

        return self.upsert_object(table=Adverts, id=advert_data_id, active=active, data=advert_data_id)

    def get_by_attr(self, attr: object, values: List[object] = list()) -> Tuple[Optional[List[Adverts]], Optional[Exception]]:
        """
        This function gets all the adverts whose attr is in values list.

        Args:
            attr: An attribute of adverts table.
            values: A list with the required values for attr.

        Returns:
            None, err: If some exception was raised querying in database, where err is an exception.
            list, None: Otherwise, with 'list' being [] if values is empty or a list with all the rows that fill any value in values.
        """
        return self.get_objects_by_attr(table=Adverts, attr=attr, values=values)

    def get_all_adverts(self) -> Tuple[Optional[Adverts], Optional[Exception]]:
        """
        This function gets all the adverts in the adverts table.

        Returns:
            None, err: If some exception was raised querying in database, where err is an exception.
            list, None: Otherwise, with 'list' being a list with all the rows in the adverts table.
        """
        return self.get_all_objects(Adverts)

class SubPackageAdvertsData(BasePackage):
    def get_by_attr(self, attr: object, values: List[object] = list()) -> Tuple[Optional[AdvertsData], Optional[Exception]]:
        """
        This function gets all the adverts datas whose attr is in values list.

        Args:
            attr: An attribute of adverts data table.
            values: A list with the required values for attr.

        Returns:
            None, err: If some exception was raised querying in database, where err is an exception.
            list, None: Otherwise, with 'list' being [] if values is empty or a list with all the rows that fill any value in values.
        """
        return self.get_objects_by_attr(table=AdvertsData, attr=attr, values=values)

    def get_all_adverts_data(self) -> Tuple[Optional[List[AdvertsData]], Optional[Exception]]:
        """
        This function gets all the adverts data in the adverts data table.

        Returns:
            None, err: If some exception was raised querying in database, where err is an exception.
            list, None: Otherwise, with 'list' being a list with all the rows in the adverts data table.
        """
        return self.get_all_objects(AdvertsData)

class SubPackageLoans(BasePackage):
    def upsert(self, withdrawal: date, devolution: date, lessee: str, ad: str) -> Tuple[Optional[Loans], Optional[Exception]]:
        """
        This function upserts a loan in the loans table.

        Args:
            withdrawal: Withdrawal date.
            devolution: Devolution date.
            lessee: The lessee's id.
            ad: The id of a row in adverts data table.

        Returns:
            None, err: If some exception was raised querying in database, where err is an exception.
            obj, None: Otherwise, with 'obj' being the row inserted in the table.
        """
        loan_id = sha1(f'{withdrawal}-{devolution}-{lessee}-{ad}'.encode()).hexdigest()

        return self.upsert_object(table=Loans, id=loan_id, withdrawal=withdrawal, devolution=devolution, lessee=lessee, ad=ad)

    def get_by_attr(self, attr: object, values: List[object] = list()):
        """
        This function gets all the loans whose attr is in values list.

        Args:
            attr: An attribute of loans table.
            values: A list with the required values for attr.

        Returns:
            None, err: If some exception was raised querying in database, where err is an exception.
            list, None: Otherwise, with 'list' being [] if values is empty or a list with all the rows that fill any value in values.
        """
        return self.get_objects_by_attr(table=Loans, attr=attr, values=values)

    def get_all_loans(self) -> Tuple[Optional[List[Loans]], Optional[Exception]]:
        """
        This function gets all the loans in the loans table.

        Returns:
            None, err: If some exception was raised querying in database, where err is an exception.
            list, None: Otherwise, with 'list' being a list with all the rows in the loans table.
        """
        return self.get_all_objects(Loans)

class Business:
    def __init__(self, session_scope: Callable):
        self.instruments: SubPackageInstruments = SubPackageInstruments(session_scope)
        self.adverts: SubPackageAdverts = SubPackageAdverts(session_scope)
        self.adverts_data: SubPackageAdvertsData = SubPackageAdvertsData(session_scope)
        self.loans: SubPackageLoans = SubPackageLoans(session_scope)








