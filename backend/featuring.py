from data.business import SubPackageInstruments
from typing import List

class SubPackageFeaturing():
    def __init__(self, session_scope):
        self.session_scope = session_scope

    def saveNew10PopularIntruments(self, new10PopularInstruments: List[str]) -> None:
        if len(new10PopularInstruments) != 10:
            raise Exception('Invalid number of new popular instruments.')

        databaseSubsystem = SubPackageInstruments(self.session_scope)

        allIntruments = databaseSubsystem.get_all_instruments()[0]

        if any([instrument not in list(map(lambda instrument: instrument.instrument, allIntruments)) for instrument in new10PopularInstruments]):
            raise Exception('Invalid new popular intrument.')

        [databaseSubsystem.upsert(instrument.instrument_class, instrument.instrument, instrument.brand, instrument.model, instrument.registry, instrument.instrument in new10PopularInstruments) for instrument in allIntruments]