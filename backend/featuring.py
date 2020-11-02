from ..data.business import SubPackageInstruments
from typing import List

def saveNew10PopularIntruments(new10PopularInstruments: List[str]) -> None:
    if len(new10PopularInstruments) != 10:
        raise Exception('Invalid number of new popular instruments.')

    databaseSubsystem = SubPackageInstruments()

    allIntruments = databaseSubsystem.get_all_instruments()[0]

    if any([instrument not in map(lambda instrument: instrument.intrument, allIntruments) for instrument in new10PopularInstruments]):
        raise Exception('Invalid new popular intrument.')

    [databaseSubsystem.upsert(instrument.class_name, instrument.instrument, instrument.brand, instrument.model, instrument.registry, instrument.instrument in new10PopularInstruments) for instrument in allIntruments]