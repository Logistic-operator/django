from django.contrib.gis.db import models as models
import requests
import json
from django.contrib.gis.geos import GEOSGeometry, GeometryCollection
from django.apps import apps
from rest_framework.exceptions import ValidationError
from railway.models import Railway

from geo.utils import printProgressBar

class Isochrone(models.Model):
    warehouse = models.ForeignKey('warehouse.Warehouse', on_delete=models.CASCADE)
    timespan = models.IntegerField() # minutes
    geom = models.PolygonField(null=True)
    # railways = models.ManyToManyField('railway.Railway', through='NeighborhoodRailway', related_name = 'Railways')
    # all_geom = models.GeometryCollectionField(null=True)

    readonly_fields=('geom', 'all_geom')
    unique_together=('warehouse', 'timespan')

    def __str__(self) -> str:
        return str(self.id) + ' ' + self.warehouse.phone + ' ' + str(self.timespan)

    def redraw(self):
        x, y = (str(self.warehouse.point.x), str(self.warehouse.point.y))
        time = str(self.timespan)
        url = 'http://localhost:8002/isochrone?json={"costing":"truck","costing_options":'\
            '{"truck":{"exclude_polygons":[],"maneuver_penalty":5,"country_crossing_penalty":0,'\
            '"country_crossing_cost":600,"length":21.5,"width":2.6,"height":4.11,"weight":21.77,'\
            '"axle_load":9,"hazmat":false,"use_highways":1,"use_tolls":1,"use_ferry":1,"ferry_cost":300,'\
            '"use_living_streets":0.5,"use_tracks":0,"private_access_penalty":450,"ignore_closures":false,'\
            '"closure_factor":9,"service_penalty":15,"service_factor":1,"exclude_unpaved":1,"shortest":false,'\
            '"exclude_cash_only_tolls":false,"top_speed":60,"axle_count":5,"fixed_speed":0,"toll_booth_penalty":0,'\
            '"toll_booth_cost":15,"gate_penalty":300,"gate_cost":30,"include_hov2":false,"include_hov3":false,'\
            '"include_hot":false,"disable_hierarchy_pruning":false}},"contours":[{"time":'+ time +'}],'\
            '"locations":[{"lon":'+ x + ',"lat":'+ y + ',"type":"break"}],"directions_options":{"units":"kilometers"},'\
            '"id":"valhalla_isochrones_lonlat_'+ x + ','+ y + '_range_'+ time +'_interval_'+ time +'"}'
        try:
            data = requests.get(url).json()['features'][0]['geometry']['coordinates']
            json_res = json.dumps({
                'type': 'Polygon',
                'coordinates':[data]
            })
        except Exception as ex:
            raise ValidationError('Smth went wrong')
        self.geom = GEOSGeometry(json_res)
        self.save()
        

    # def getRailways(self):
    #     # query = 'select st.* from (select id as iso_id, geom from isochrone_isochrone where id=%s) as iso cross join railway_railway as st where st.is_cont and ST_Contains(iso.geom, st.point)'
    #     Railway = apps.get_model(app_label='railway', model_name='Railway')
    #     self.railways.clear()
    #     # RWs = Railway.objects.raw(query, [self.id])
    #     RWs = Railway.objects.filter(is_cont=True)
    #     isos = Isochrone.objects.filter(warehouse=self.warehouse)
    #     print(Railway.isochrone_set.all().query)
    #     for iso in isos:
    #         RWs = RWs.difference(iso.railways.through.objects.all().select_related('railway'))
    #     total = len(RWs)
        
    #     for i, r in enumerate(RWs):
    #         if not self.geom.contains(r.point):
    #             continue
    #         trip = self.warehouse.getWhToStationRoute(r)
    #         if not trip['rw']:
    #             continue
    #         rw = NeighborhoodRailway(isochrone=self, railway=r, geom=trip['geom'], length=trip['len'])
    #         rw.save()
    #         printProgressBar(i + 1, total, prefix = 'Railway To Isochrone Progress:', suffix = 'Complete', length = 40)

    #     # self.all_geom = GeometryCollection(self.geom, *[r.point for r in self.railways.all()])
    #     self.save()

# class NeighborhoodRailway(models.Model):
#     isochrone = models.ForeignKey(Isochrone, on_delete=models.CASCADE)
#     railway = models.ForeignKey(Railway, on_delete=models.CASCADE)
#     geom = models.CharField()
#     length = models.FloatField()