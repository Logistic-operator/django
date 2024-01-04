import django, os
import sys


from temporalio import activity
from django.apps import apps

from dataclasses import dataclass

@dataclass
class ComposeCreateInput:
    phone: str
    point: str

@activity.defn
async def drawAllIsos(wh_id) -> str:
    Warehouse = apps.get_model(app_label='warehouse', model_name='Warehouse')
    the_wh = await Warehouse.objects.filter(id=wh_id).afirst()
    isochrones = await the_wh.acreateIsochrones([240, 480, 720, 960, 1200, 1440])
    return 'done'

@activity.defn
async def findNearestStation(wh_id) -> str:
    Warehouse = apps.get_model(app_label='warehouse', model_name='Warehouse')
    the_wh = await Warehouse.objects.filter(id=wh_id).afirst()
    isochrones = await the_wh.afindNearest()
    return 'done'

@activity.defn
async def create(input: ComposeCreateInput) -> int:
    Warehouse = apps.get_model(app_label='warehouse', model_name='Warehouse')
    old = await Warehouse.objects.filter(point=input.point).afirst()
    if old:
        raise AttributeError('Already Exists!')
    the_wh = Warehouse(phone=input.phone, point=input.point)
    await the_wh.asave()
    return the_wh.id