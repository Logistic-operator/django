
from __future__ import print_function

import logging
from temporalio import activity

import django, os
import sys
sys.path.append('..')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "geo.settings")
 
django.setup()
from warehouse.models import Warehouse
# from railway.models import Railway

@activity.defn
async def drawAllIsos(wh_id) -> str:
    the_wh = Warehouse.objects.filter(id=wh_id).first()
    isochrones = the_wh.createIsochrones([240, 480, 720, 960, 1200, 1440])
    return 'done'