from data.business import SubPackageLoans, SubPackageAdverts, SubPackageAdvertsData
from data.models import Loans, Adverts, AdvertsData, Users
from datetime import date
from backend.records import RecordsBackend
from backend.announcement import SubPackageAnnouncements
from data.auth import Auth



class LoansBackend():
    def __init__(self, session_scope):
        self.session_scope = session_scope

    def loadLocatorData(self, ad_id:str):
        AdvertsSubsystem = SubPackageAdverts(self.session_scope)
        AdvertsDataSubsystem = SubPackageAdvertsData(self.session_scope)
        UsersSubsystem = Auth(self.session_scope)

        ad_data_id = AdvertsSubsystem.get_by_attr(Adverts.id, [ad_id])[0][0].data
        locator_id = AdvertsDataSubsystem.get_by_attr(AdvertsData.id, [ad_data_id])[0][0].locator
        locator = UsersSubsystem.get_objects_by_attr(Users, Users.id, [locator_id])[0][0]

        return {'name': locator.name,
                'email': locator.email}


    def saveNewLoan(self, withdrawal: date, devolution: date, lessee:str, ad_data_id:str):
        if withdrawal > date.today():
            raise Exception('Invalid withdrawal date')
        if devolution > date.today():
            raise Exception('Invalid devolution date')
        if withdrawal < devolution:
            raise Exception('Invalid loan period')

        loansSubsystem = SubPackageLoans(self.session_scope)

        return loansSubsystem.upsert(withdrawal, devolution, lessee.lower(), ad_data_id.lower())

    def saveNewLoanByAdId(self, withdrawal: date, devolution: date, lessee:str, ad_id:str):
        AdvertsSubsystem = SubPackageAdverts(self.session_scope)

        ad_data_id = AdvertsSubsystem.get_by_attr(Adverts.id, [ad_id])[0][0].data

        return self.saveNewLoan(withdrawal, devolution, lessee, ad_data_id)

    def computeCharge(self, withdrawal: str, devolution: str, ad_id:str):
        if withdrawal > date.today():
            raise Exception('Invalid withdrawal date')
        if devolution > date.today():
            raise Exception('Invalid devolution date')
        if withdrawal < devolution:
            raise Exception('Invalid loan period')

        withdrawal = self.stringToDate(withdrawal)
        devolution = self.stringToDate(devolution)

        announcements = SubPackageAnnouncements(self.session_scope)
        pricesByDuration = announcements.loadListOfPricesInBRLByDurationInDaysBrandById(ad_id)
        pricesByDuration = sorted(pricesByDuration, key=lambda x: x[1], reverse=True)

        loan_duration = devolution - withdrawal
        partial_duration = loan_duration.days
        charge = 0
        for price_by_duration in pricesByDuration:
            num_durations = partial_duration // price_by_duration[1]
            charge += num_durations * price_by_duration[0]

        if charge == 0:
            charge = pricesByDuration[-1][0]

        return charge


    def deactivate_ad(self, ad_id):
        ad_backend = SubPackageAnnouncements(self.session_scope)

        ad_backend.deactivateAdvert(ad_id)

    def saveNewRecordByLoanData(self,withdrawal, devolution, lessee, ad_id, rating):
        loanSubsystem = SubPackageLoans(self.session_scope)
        records = RecordsBackend(self.session_scope)

        loan_id = [loan for loan in loanSubsystem.get_all_loans()[0] if loan.withdrawal==withdrawal and
                                                                        loan.devolution==devolution and
                                                                        loan.lessee == lessee and loan.ad == ad_id
                  ][0].id

        records.saveNewRecord(loan_id, rating=8)

    def stringToDate(self, date_string):

        date_elements = [int(element) for element in date_string.split('-')]

        return date(date_elements[0], date_elements[1], date_elements[2])

    def processLoan(self, withdrawal, devolution, lessee, ad_id, rating=3):

        withdrawal = self.stringToDate(withdrawal)
        devolution = self.stringToDate(devolution)

        #save loan
        self.saveNewLoanByAdId(withdrawal, devolution, lessee, ad_id)

        #deactivate ad
        self.deactivate_ad(ad_id)

        #save record
        self.saveNewRecordByLoanData(withdrawal, devolution, lessee, ad_id, rating)
