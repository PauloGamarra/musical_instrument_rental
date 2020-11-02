from ..data.business import SubPackageInstruments, SubPackageAdverts
from ..data.models import Adverts
from typing import List, Tuple

def loadInstrumentsAndItsPopularitySortedByPopularityAndByAlphabetics() -> List[Tuple[str, bool]]:
    databaseSubsystem = SubPackageInstruments()

    return list(sorted(map(lambda instrument: (instrument.instrument, instrument.popular), databaseSubsystem.get_all_instruments()[0]), key=lambda instrument: (0 if instrument[1] else 1, instrument[0])))

def loadActiveAdvertsIdsByInstrument(instrumentType: str) -> List[str]:
    databaseSubsystem = SubPackageAdverts()

    return [advert.id for advert in databaseSubsystem.get_all_adverts()[0] if advert.active]

def loadAdvertInstrumentBrandById(advertId: str) -> str:
    databaseSubsystem = SubPackageAdverts()

    return databaseSubsystem.get_by_attr(Adverts.id, [advertId])[0].data.instrument.brand

def loadAdvertInstrumentModelById(advertId: str) -> str:
    databaseSubsystem = SubPackageAdverts()

    return databaseSubsystem.get_by_attr(Adverts.id, [advertId])[0].data.instrument.model

def loadAdvertLocatorNameById(advertId: str) -> str:
    databaseSubsystem = SubPackageAdverts()

    return databaseSubsystem.get_by_attr(Adverts.id, [advertId])[0].data.locator

def loadListOfPricesInBRLByDurationInDaysBrandById(advertId: str) -> List[Tuple[float, int]]:
    databaseSubsystem = SubPackageAdverts()

    return list(map(lambda priceByDuration: (float(priceByDuration.split(':')[0]), int(priceByDuration.split(':')[1])),databaseSubsystem.get_by_attr(Adverts.id, [advertId]).data.prices.split(',')[0]))

def deactivateAdvert(advertId: str) -> None:
    databaseSubsystem = SubPackageAdverts()

    advert = databaseSubsystem.get_by_attr(Adverts.id, [advertId])[0]

    databaseSubsystem.upsert(False, advert.prices, advert.locator, advert.instrument)


def saveNewAdvert(listOfPricesInBRLByDurationInDays: List[Tuple[float, int]], locatorName: str, instrumentClass: str, instrumentType: str, instrumentBrand: str = '', instrumentModel: str = '', instrumentSerialCode: str = '') -> None:
    if instrumentClass.lower() not in ['cordas', 'sopro', 'percussão']:
        raise Exception('Invalid instrument class.')

    if instrumentType == '':
        raise Exception('No instrument type informed.')

    if locatorName.split(' ') < 2 or any([not word.isalpha() for word in locatorName.split(' ')]):
        raise Exception('No valid locator name informed.')

    if len(listOfPricesInBRLByDurationInDays) == 0:
        raise Exception('No price informed.')

    databaseSubsystem = SubPackageInstruments()

    databaseSubsystem.upsert(instrumentClass.lower(), instrumentType.lower(), instrumentBrand.lower(), instrumentModel.lower(), instrumentSerialCode.lower())

    insertedInstrumentId = list(filter(lambda instrument: instrument.instrumentClass == instrumentClass.lower() and instrument.instrument == instrumentType.lower() and instrument.brand == instrumentBrand.lower() and instrument.model == instrumentModel.lower() and instrument.registry == instrumentSerialCode.lower(), databaseSubsystem.get_all_instruments()[0]))[0].id

    databaseSubsystem = SubPackageAdverts()

    databaseSubsystem.upsert(True, ','.join(map(lambda priceByDuration: f"{priceByDuration[0]:.02f}:{priceByDuration[1]}", listOfPricesInBRLByDurationInDays)), locatorName, insertedInstrumentId)



