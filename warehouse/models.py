from django.contrib.gis.db import models as models
from isochrone.models import Isochrone
from django.db.models import Count
import requests

class Warehouse(models.Model):
    phone = models.CharField(max_length=15)
    point = models.PointField()
    nearest_railway = models.ForeignKey('railway.Railway', on_delete=models.SET_NULL, null=True, blank=True, )
    nearest_railway_length = models.FloatField(blank=True, null=True)

    def __str__(self) -> str:
        return str(self.id) + ' ' + self.phone
    
    def createIsochrones(self, timespan: []):
        isochrones = []
        for time in timespan:
            isochrone = Isochrone.objects.get_or_create(warehouse=self, timespan=int(time))[0]
            isochrone.redraw()
            isochrones.append(isochrone)
        return isochrones
    
    def findNearest(self):
        nearest_st = {'rw':None, 'len': 10000000}
        rws = Isochrone.objects.filter(warehouse=self)\
            .annotate(num_railways=Count('railways'))\
            .filter(num_railways__gt=0)\
            .order_by('timespan')[0]\
            .railways.all()
        for rw in rws:
            new_route = self.getWhToStationRoute(rw)
            nearest_st = new_route if new_route['len'] < nearest_st['len'] else nearest_st
        self.nearest_railway = nearest_st['rw']
        self.nearest_railway_length = nearest_st['len']
        self.save()
        return self

    def getWhToStationRoute(self, rw):
        url = 'http://localhost:8002/route?json={"costing":"truck","costing_options":{"truck":{"exclude_polygons":[],"maneuver_penalty":5,"country_crossing_penalty":0,"country_crossing_cost":600,"length":21.5,"width":2.6,"height":4.11,"weight":21.77,"axle_load":9,"hazmat":false,"use_highways":1,"use_tolls":1,"use_ferry":1,"ferry_cost":300,"use_living_streets":0.5,"use_tracks":0,"private_access_penalty":450,"ignore_closures":false,"closure_factor":9,"service_penalty":15,"service_factor":1,"exclude_unpaved":1,"shortest":false,"exclude_cash_only_tolls":false,"top_speed":60,"axle_count":5,"fixed_speed":0,"toll_booth_penalty":0,"toll_booth_cost":15,"gate_penalty":300,"gate_cost":30,"include_hov2":false,"include_hov3":false,"include_hot":false,"disable_hierarchy_pruning":false}},"exclude_polygons":[],"locations":[{"lon":'+ str(self.point.x) + ',"lat":'+ str(self.point.y) + ',"type":"break"},{"lon":'+ str(rw.point.x) + ',"lat":'+ str(rw.point.y) + ',"type":"break"}],"directions_options":{"units":"kilometers"},"id":"valhalla_directions"}'
        try:
            len = requests.get(url).json()['trip']['summary']['length']
        except Exception as ex:
            return {'rw':None, 'len': 10000001}
        return {
            'rw': rw,
            'len': len
        }