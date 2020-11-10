from data.historicalRecords import HistoricalRecords
from data.business import SubPackageLoans, SubPackageAdvertsData, SubPackageInstruments
from data.models import Loans, Adverts, Instruments, Users, AdvertsData
from data.auth import Auth

class RecordsBackend():
    def __init__(self, session_scope):
        self.session_scope = session_scope

    def saveNewRecord(self, loan_id, rating):
        if rating < 0 or rating > 10:
            raise Exception('Invalid rating')

        recordsSystem = HistoricalRecords(self.session_scope)

        return recordsSystem.upsert(loan_id, rating)

    def loadUserDataById(self, user_id):
        userSubsystem = Auth(self.session_scope)

        user_data = userSubsystem.get_objects_by_attr(Users, Users.id, [user_id])[0][0]

        return {'id': user_id,
                'name': user_data.name,
                'email': user_data.email}

    def loadLoansDataById(self, loan_id):
        loanSubsystem = SubPackageLoans(self.session_scope)

        loan = loanSubsystem.get_by_attr(Loans.id, [loan_id])[0][0]


        return {'withdrawal' : loan.withdrawal,
                'devolution' : loan.devolution,
                'lessee' : self.loadUserDataById(loan.lessee)}

    def loadInstrumentDataById(self, instrument_id):
        instrumentSubsystem = SubPackageInstruments(self.session_scope)

        instrument = instrumentSubsystem.get_by_attr(Instruments.id, [instrument_id])[0][0]

        return {'instrument_class': instrument.instrument_class,
                'instrument': instrument.instrument,
                'brand': instrument.brand,
                'model': instrument.model,
                'registry': instrument.registry}

    def loadAdvertDataByLoanId(self, loan_id):
        advertsSubsystem = SubPackageAdvertsData(self.session_scope)
        loanSubsystem = SubPackageLoans(self.session_scope)

        advert_id = loanSubsystem.get_by_attr(Loans.id, [loan_id])[0][0].ad
        print('advert_id: {}'.format(advert_id))
        print(advertsSubsystem.get_all_adverts_data())
        advert = advertsSubsystem.get_by_attr(AdvertsData.id, [advert_id])[0][0]

        return {'locator': self.loadUserDataById(advert.locator),
                'instrument': self.loadInstrumentDataById(advert.instrument)}

    def loadRecords(self):
        recordsSubsystem = HistoricalRecords(self.session_scope)

        return [{'advert':self.loadAdvertDataByLoanId(record.loan),
                 'loan': self.loadLoansDataById(record.loan),
                 'rating':record.rating}
                for record in recordsSubsystem.get_all_records()[0]]

    def loadLocatorRecords(self, user_id):
        return [record for record in self.loadRecords() if record['advert']['locator']['id'] == user_id]
    def loadLesseeRecords(self, user_id):
        return [record for record in self.loadRecords() if record['loan']['lessee']['id'] == user_id]