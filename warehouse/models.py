from django.contrib.gis.db import models as models
from isochrone.models import Isochrone

class Warehouse(models.Model):
    phone = models.CharField(max_length=15)
    point = models.PointField()

    def __str__(self) -> str:
        return str(self.id) + ' ' + self.phone
    
    def createIsochrones(self, timespan: [int]):
        isochrones = []
        for time in timespan:
            isochrone = Isochrone.objects.get_or_create(warehouse=self, timespan=time)[0]
            isochrone.redraw()
            isochrones.append(isochrone)
        return isochrones