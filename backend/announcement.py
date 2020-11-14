from data.business import SubPackageInstruments, SubPackageAdverts, SubPackageAdvertsData
from data.models import Instruments, Adverts, AdvertsData, Users
from data.auth import Auth
from typing import List, Tuple

class SubPackageAnnouncements():
    def __init__(self, session_scope):
        self.session_scope = session_scope

    def loadInstrumentsAndItsPopularitySortedByPopularityAndByAlphabetics(self) -> List[Tuple[str, bool]]:
        databaseSubsystem = SubPackageInstruments(self.session_scope)

        return list(sorted(set(map(lambda instrument: (instrument.instrument, instrument.popular), databaseSubsystem.get_all_instruments()[0])), key=lambda instrument: (0 if instrument[1] else 1, instrument[0])))

    def loadActiveAdvertsIdsByInstrument(self, instrumentType: str) -> List[str]:
        databaseSubsystem = SubPackageAdverts(self.session_scope)

        allAdverts = databaseSubsystem.get_all_adverts()[0]

        return [advert.id for advert in allAdverts if advert.active and SubPackageInstruments(self.session_scope).get_by_attr(Instruments.id, [SubPackageAdvertsData(self.session_scope).get_by_attr(AdvertsData.id, [advert.data])[0][0].instrument])[0][0].instrument == instrumentType]

    def loadAdvertInstrumentBrandById(self, advertId: str) -> str:
        databaseSubsystem = SubPackageAdverts(self.session_scope)

        advertDataId = databaseSubsystem.get_by_attr(Adverts.id, [advertId])[0][0].data

        databaseSubsystem = SubPackageAdvertsData(self.session_scope)

        instrumentId = databaseSubsystem.get_by_attr(AdvertsData.id, [advertDataId])[0][0].instrument

        databaseSubsystem = SubPackageInstruments(self.session_scope)

        return databaseSubsystem.get_by_attr(Instruments.id, [instrumentId])[0][0].brand

    def loadAdvertInstrumentModelById(self, advertId: str) -> str:
        databaseSubsystem = SubPackageAdverts(self.session_scope)

        advertDataId = databaseSubsystem.get_by_attr(Adverts.id, [advertId])[0][0].data

        databaseSubsystem = SubPackageAdvertsData(self.session_scope)

        instrumentId = databaseSubsystem.get_by_attr(AdvertsData.id, [advertDataId])[0][0].instrument

        databaseSubsystem = SubPackageInstruments(self.session_scope)

        return databaseSubsystem.get_by_attr(Instruments.id, [instrumentId])[0][0].model

    def loadAdvertLocatorUsernameById(self, advertId: str) -> str:
        databaseSubsystem = SubPackageAdverts(self.session_scope)

        advertDataId = databaseSubsystem.get_by_attr(Adverts.id, [advertId])[0][0].data

        databaseSubsystem = SubPackageAdvertsData(self.session_scope)

        locatorId = databaseSubsystem.get_by_attr(AdvertsData.id, [advertDataId])[0][0].locator

        databaseSubsystem = Auth(self.session_scope)

        return databaseSubsystem.get_user(user_id=locatorId)[0].name

    def loadListOfPricesInBRLByDurationInDaysBrandById(self, advertId: str) -> List[Tuple[float, int]]:
        databaseSubsystem = SubPackageAdverts(self.session_scope)

        advertDataId = databaseSubsystem.get_by_attr(Adverts.id, [advertId])[0][0].data

        databaseSubsystem = SubPackageAdvertsData(self.session_scope)

        return list(map(lambda priceByDuration: (float(priceByDuration.split(':')[0]), int(priceByDuration.split(':')[1])),databaseSubsystem.get_by_attr(AdvertsData.id, [advertDataId])[0][0].prices.split(',')))

    def deactivateAdvert(self, advertId: str) -> None:
        databaseSubsystem = SubPackageAdverts(self.session_scope)
        advertsDataSubsystem = SubPackageAdvertsData(self.session_scope)

        advert = databaseSubsystem.get_by_attr(Adverts.id, [advertId])[0][0]
        advertData = advertsDataSubsystem.get_by_attr(AdvertsData.id, [advert.data])[0][0]

        databaseSubsystem.upsert(False, advertData.prices, advertData.locator, advertData.instrument)

    def saveNewAdvert(self, listOfPricesInBRLByDurationInDays: List[Tuple[float, int]], locatorEmail: str, instrumentClass: str, instrumentType: str, instrumentBrand: str = '', instrumentModel: str = '', instrumentSerialCode: str = '') -> None:
        if instrumentClass.lower() not in ['cordas', 'sopro', 'percussão']:
            raise Exception('Invalid instrument class.')

        if instrumentType == '':
            raise Exception('No instrument type informed.')

        if len(listOfPricesInBRLByDurationInDays) == 0:
            raise Exception('No price informed.')

        if any([priceByDuration[0] <= 0 or priceByDuration[1] <= 0 for priceByDuration in listOfPricesInBRLByDurationInDays]):
            raise Exception('Price or duration <= 0.')

        databaseSubsystem = SubPackageInstruments(self.session_scope)

        databaseSubsystem.upsert(instrumentClass.lower(), instrumentType.lower(), instrumentBrand.lower(), instrumentModel.lower(), instrumentSerialCode.lower(), any(list(map(lambda instrument: instrument.popular, databaseSubsystem.get_by_attr(Instruments.instrument, [instrumentType])[0]))))

        insertedInstrumentId = list(filter(lambda instrument: instrument.instrument_class == instrumentClass.lower() and instrument.instrument == instrumentType.lower() and instrument.brand == instrumentBrand.lower() and instrument.model == instrumentModel.lower() and instrument.registry == instrumentSerialCode.lower(), databaseSubsystem.get_all_instruments()[0]))[0].id

        databaseSubsystem = Auth(self.session_scope)

        locatorId = databaseSubsystem.get_user(email=locatorEmail)[0].id

        databaseSubsystem = SubPackageAdverts(self.session_scope)

        databaseSubsystem.upsert(True, ','.join(map(lambda priceByDuration: f"{priceByDuration[0]:.02f}:{priceByDuration[1]}", listOfPricesInBRLByDurationInDays)), locatorId, insertedInstrumentId)



