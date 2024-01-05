import django, os
import sys


from temporalio import activity
from django.apps import apps

from dataclasses import dataclass

@dataclass
class ComposeCreateInput:
    iid: int
    name: str
    point: str
    is_cont: bool

@dataclass
class ComposeCreateNbInput:
    source_iid: int
    target_iid: int
    length: int

@activity.defn
async def create(input: ComposeCreateInput) -> int:
    Railway = apps.get_model(app_label='railway', model_name='Railway')
    the_rw = Railway(
        iid=input.iid, 
        name=input.name,
        point=input.point,
        is_cont=input.is_cont,
        )
    await the_rw.asave()
    return the_rw.id

@activity.defn
async def createNb(input: ComposeCreateNbInput) -> int:
    Railway = apps.get_model(app_label='railway', model_name='Railway')
    Neighborhood = apps.get_model(app_label='railway', model_name='Neighborhood')
    the_nb = Neighborhood(
            source=await Railway.objects.aget(iid=input.source_iid),
            target=await Railway.objects.aget(iid=input.target_iid),
            length=input.length,
        )
    await the_nb.asave()
    return the_nb.id

@activity.defn
async def optimize() -> str:
    Railway = apps.get_model(app_label='railway', model_name='Railway')
    return await Railway.aoptimize()