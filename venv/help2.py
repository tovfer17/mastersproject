from sqlalchemy.types import Text, Float
from sqlalchemy.schema import Column
from tropofy.database.tropofy_orm import DataSetMixin
from tropofy.app import AppWithDataSets, Step, StepGroup
from tropofy.widgets import SimpleGrid, KMLMap
from simplekml import Kml


class Store(DataSetMixin):
    name = Column(Text)
    latitude = Column(Float)
    longitude = Column(Float)


class MyKMLMap(KMLMap):
    def get_kml(self, app_session):
        kml = Kml()
        for store in app_session.data_set.query(Store).all():
            kml.newpoint(name=store.name, coords=[(store.longitude, store.latitude)])
        return kml.kml()


class MyFirstApp(AppWithDataSets):
    def get_name(self):
        return "My First App"

    def get_gui(self):
        return [
            StepGroup(name='Stores', steps=[Step(name='Stores', widgets=[SimpleGrid(Store)])]),
            StepGroup(name='Map', steps=[Step(name='Map', widgets=[MyKMLMap()])])
        ]