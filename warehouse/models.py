from collections.abc import Iterable
from typing import Any, Coroutine
from django.contrib.gis.db import models as models
from isochrone.models import Isochrone
from django.db.models import Count
import requests
import asyncio
from django.apps import apps

from geo.utils import postpone, getRowsFromCSV
from temporalio.client import Client
from .workflows import WarehouseIsos, WarehouseNearest, WarehouseCreate
import asyncio
from asgiref.sync import sync_to_async

from .activities import ComposeCreateInput
# from geo.utils import printProgressBar


class Warehouse(models.Model):
    phone = models.CharField(max_length=15)
    point = models.PointField(unique=True)
    railways = models.ManyToManyField('railway.Railway', through='NeighborhoodRailway', related_name = 'Railways')

    def __str__(self) -> str:
        return str(self.id) + ' ' + self.phone
    
    async def acreateIsochrones(self, timespan: []):
        return await sync_to_async(self.createIsochrones)(timespan)

    def createIsochrones(self, timespan: []):
        isochrones = []
        for time in timespan:
            isochrone = Isochrone.objects.get_or_create(warehouse=self, timespan=int(time))[0]
            isochrone.redraw()
        self.getRailways()
    
    @postpone
    def createIsochronesWF(self):
        # subprocess.run(f'temporal workflow start -t wh-task-queue --type WarehouseIsos -w wh_iso_{self.id} -i {self.id}')
        # subprocess.run(f'temporal workflow start -t wh-task-queue --type WarehouseNearest -w wh_near_{self.id} -i {self.id}')
        async def run():
            client = await Client.connect("localhost:7233")
            await client.execute_workflow(
                WarehouseIsos.run, self.id, id=f"wh_iso_{self.id}", task_queue="wh-task-queue"
            )
        asyncio.run(run())

    def getRailways(self):
        Railway = apps.get_model(app_label='railway', model_name='Railway')
        self.railways.clear()
        RWs = Railway.objects.filter(is_cont=True)
        isos = Isochrone.objects.filter(warehouse=self).order_by('timespan')
        total = len(RWs)
        ex_RWs = []
        for iso in isos:
            for i, r in enumerate(RWs):
                if not iso.geom.contains(r.point) or r in ex_RWs:
                    continue
                ex_RWs.append(r)
                trip = self.getWhToStationRoute(r)
                if not trip['rw']:
                    continue
                rw = NeighborhoodRailway(warehouse=self, isochrone=iso, railway=r, geom=trip['geom'], length=trip['len'])
                rw.save()
            if len(ex_RWs) > 0:
                break
    
    def addNbRwToGraph(self):
        Globalvar = apps.get_model(app_label='globalvar', model_name='Globalvar')
        var = Globalvar.objects.get(name='graph')
        G = var.args
        G.add_weighted_edges_from([(edge.warehouse.id + 100000, edge.railway.id, edge.length) for edge in self.railways.through.objects.filter(warehouse=self)])
        var.args = G
        var.save()
    
    @postpone
    def findNearestWF(self):
        # subprocess.run(f'temporal workflow start -t wh-task-queue --type WarehouseIsos -w wh_iso_{self.id} -i {self.id}')
        # subprocess.run(f'temporal workflow start -t wh-task-queue --type WarehouseNearest -w wh_near_{self.id} -i {self.id}')
        async def run():
            client = await Client.connect("localhost:7233")
            await client.execute_workflow(
                WarehouseNearest.run, self.id, id=f"wh_near_{self.id}", task_queue="wh-task-queue"
            )
        asyncio.run(run())

    async def afindNearest(self):
        return await sync_to_async(self.getRailways)()
    
    def findNearest(self):
        nearest_st = {'rw':None, 'len': 10000000}
        isos = Isochrone.objects.filter(warehouse=self)\
            .order_by('timespan')
        rws = None
        for iso in isos:
            rws = iso.railways.through.objects.all()
            if rws.count() != 0:
                break
        for rw in rws:
            new_route = self.getWhToStationRoute(rw.railway)
            nearest_st = new_route if new_route['len'] < nearest_st['len'] else nearest_st
        self.nearest_railway = nearest_st['rw']
        self.nearest_railway_length = nearest_st['len']
        self.save()
        return self

    def getWhToStationRoute(self, rw):
        url = 'http://localhost:8002/route?json={"costing":"truck","costing_options":{"truck":{"exclude_polygons":[],"maneuver_penalty":5,"country_crossing_penalty":0,"country_crossing_cost":600,"length":21.5,"width":2.6,"height":4.11,"weight":21.77,"axle_load":9,"hazmat":false,"use_highways":1,"use_tolls":1,"use_ferry":1,"ferry_cost":300,"use_living_streets":0.5,"use_tracks":0,"private_access_penalty":450,"ignore_closures":false,"closure_factor":9,"service_penalty":15,"service_factor":1,"exclude_unpaved":1,"shortest":false,"exclude_cash_only_tolls":false,"top_speed":60,"axle_count":5,"fixed_speed":0,"toll_booth_penalty":0,"toll_booth_cost":15,"gate_penalty":300,"gate_cost":30,"include_hov2":false,"include_hov3":false,"include_hot":false,"disable_hierarchy_pruning":false}},"exclude_polygons":[],"locations":[{"lon":'+ str(self.point.x) + ',"lat":'+ str(self.point.y) + ',"type":"break"},{"lon":'+ str(rw.point.x) + ',"lat":'+ str(rw.point.y) + ',"type":"break"}],"directions_options":{"units":"kilometers"},"id":"valhalla_directions"}'
        try:
            len = requests.get(url).json()['trip']['summary']['length']
            geom = requests.get(url).json()['trip']['legs'][0]['shape']
        except Exception as ex:
            return {'rw':None, 'len': 10000001}
        return {
            'rw': rw,
            'geom': geom,
            'len': len
        }

@postpone   
def batchCreateWF(file):
    data_read = getRowsFromCSV(file)
    async def run(rows):
        client = await Client.connect("localhost:7233")
        for row in rows:
            the_wh = None
            the_id = None
            try:
                phone = row[0]
                point = row[1]
                the_id = await client.execute_workflow(
                    WarehouseCreate.run, ComposeCreateInput(phone=phone, point=point), id=f"wh_create_{phone}", task_queue="wh-task-queue"
                )
            except:
                the_wh = await Warehouse.objects.filter(point=point).afirst()

                the_id = the_wh.id
            if the_wh:
                if await sync_to_async(the_wh.railways.count)() == 0:
                    try:
                        await client.execute_workflow(
                            WarehouseIsos.run, the_id, id=f"wh_iso_{str(the_id)}", task_queue="wh-task-queue"
                        )
                        # await client.execute_workflow(
                        #     WarehouseNearest.run, the_id, id=f"wh_near_{str(the_id)}", task_queue="wh-task-queue"
                        # )
                    except:
                        pass
        Globalvar = apps.get_model(app_label='globalvar', model_name='Globalvar')
        Globalvar.load_graph()
    asyncio.run(run(data_read))

@postpone
def batchCreateIsochronesWF(queryset):
    async def run():
        client = await Client.connect("localhost:7233")
        async for warehouse in queryset:
            await client.execute_workflow(
                WarehouseIsos.run, warehouse.id, id=f"wh_iso_{warehouse.id}", task_queue="wh-task-queue"
            )
    asyncio.run(run())

@postpone
def batchFindNearestWF(queryset):
    async def run():
        client = await Client.connect("localhost:7233")
        async for warehouse in queryset:
            await client.execute_workflow(
                WarehouseNearest.run, warehouse.id, id=f"wh_near_{warehouse.id}", task_queue="wh-task-queue"
            )
    asyncio.run(run())

class NeighborhoodRailway(models.Model):
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE)
    isochrone = models.ForeignKey(Isochrone, on_delete=models.CASCADE)
    railway = models.ForeignKey('railway.Railway', on_delete=models.CASCADE)
    geom = models.CharField()
    length = models.FloatField()