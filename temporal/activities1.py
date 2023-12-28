import json
import sys, os
import django

sys.path.append('..')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "geo.settings")
django.setup()


# from asgiref.sync import sync_to_async

from temporalio import activity
# from isochrone.models import Isochrone
from warehouse.models import Warehouse
from django.contrib.gis.geos import GEOSGeometry


@activity.defn
async def say_hello(id: int) -> str:
    obj = await Warehouse.objects.afirst()#.aget(id=id)
    res = f"Hello, {obj.phone}!"
    return res

@activity.defn
async def createWH(newWH) -> str:
    await Warehouse(
            phone=newWH['phone'],
            point=GEOSGeometry(json.dumps(newWH['point'])),
        ).asave()
    obj = None
    async for obj in Warehouse.objects.filter(phone=newWH['phone']).first():
        obj = await Warehouse.objects.afilter(phone=newWH['phone'])
    res = f"Hello, {obj.point}!"
    return res