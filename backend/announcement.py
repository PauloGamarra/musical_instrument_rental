from data.business import SubPackageInstruments, SubPackageAdverts
from data.models import Adverts, Instruments
from typing import List, Tuple

class SubPackageAnnouncements():
    def __init__(self, session_scope):
        self.session_scope = session_scope

    def loadInstrumentsAndItsPopularitySortedByPopularityAndByAlphabetics(self) -> List[Tuple[str, bool]]:
        databaseSubsystem = SubPackageInstruments(self.session_scope)

        return list(sorted(map(lambda instrument: (instrument.instrument, instrument.popular), databaseSubsystem.get_all_instruments()[0]), key=lambda instrument: (0 if instrument[1] else 1, instrument[0])))

    def loadActiveAdvertsIdsByInstrument(self, instrumentType: str) -> List[str]:
        databaseSubsystem = SubPackageAdverts(self.session_scope)

        return [advert.id for advert in databaseSubsystem.get_all_adverts()[0] if advert.active]

    def loadAdvertInstrumentBrandById(self, advertId: str) -> str:
        databaseSubsystem = SubPackageAdverts(self.session_scope)

        instrumentId = databaseSubsystem.get_by_attr(Adverts.id, [advertId])[0][0].data.instrument

        databaseSubsystem = SubPackageInstruments(self.session_scope)

        return databaseSubsystem.get_by_attr(Instruments.id, [instrumentId])[0][0].brand

    def loadAdvertInstrumentModelById(self, advertId: str) -> str:
        databaseSubsystem = SubPackageAdverts(self.session_scope)

        instrumentId = databaseSubsystem.get_by_attr(Adverts.id, [advertId])[0][0].data.instrument

        databaseSubsystem = SubPackageInstruments(self.session_scope)

        return databaseSubsystem.get_by_attr(Instruments.id, [instrumentId])[0][0].model

    def loadAdvertLocatorUsernameById(self, advertId: str) -> str:
        databaseSubsystem = SubPackageAdverts(self.session_scope)

        return databaseSubsystem.get_by_attr(Adverts.id, [advertId])[0][0].data.locator

    def loadListOfPricesInBRLByDurationInDaysBrandById(self, advertId: str) -> List[Tuple[float, int]]:
        databaseSubsystem = SubPackageAdverts(self.session_scope)

        return list(map(lambda priceByDuration: (float(priceByDuration.split(':')[0]), int(priceByDuration.split(':')[1])),databaseSubsystem.get_by_attr(Adverts.id, [advertId])[0][0].data.prices.split(',')[0]))

    def deactivateAdvert(self, advertId: str) -> None:
        databaseSubsystem = SubPackageAdverts(self.session_scope)

        advert = databaseSubsystem.get_by_attr(Adverts.id, [advertId])[0][0]

        databaseSubsystem.upsert(False, advert.prices, advert.locator, advert.instrument)

    def saveNewAdvert(self, listOfPricesInBRLByDurationInDays: List[Tuple[float, int]], locatorUsername: str, instrumentClass: str, instrumentType: str, instrumentBrand: str = '', instrumentModel: str = '', instrumentSerialCode: str = '') -> None:
        if instrumentClass.lower() not in ['cordas', 'sopro', 'percussão']:
            raise Exception('Invalid instrument class.')

        if instrumentType == '':
            raise Exception('No instrument type informed.')

        if len(listOfPricesInBRLByDurationInDays) == 0:
            raise Exception('No price informed.')

        databaseSubsystem = SubPackageInstruments(self.session_scope)

        databaseSubsystem.upsert(instrumentClass.lower(), instrumentType.lower(), instrumentBrand.lower(), instrumentModel.lower(), instrumentSerialCode.lower(), any(list(map(lambda instrument: instrument.popular, databaseSubsystem.get_by_attr(Instruments.instrument, [instrumentType])[0]))))

        insertedInstrumentId = list(filter(lambda instrument: instrument.instrument_class == instrumentClass.lower() and instrument.instrument == instrumentType.lower() and instrument.brand == instrumentBrand.lower() and instrument.model == instrumentModel.lower() and instrument.registry == instrumentSerialCode.lower(), databaseSubsystem.get_all_instruments()[0]))[0].id

        databaseSubsystem = SubPackageAdverts(self.session_scope)

        databaseSubsystem.upsert(True, ','.join(map(lambda priceByDuration: f"{priceByDuration[0]:.02f}:{priceByDuration[1]}", listOfPricesInBRLByDurationInDays)), locatorUsername, insertedInstrumentId)



