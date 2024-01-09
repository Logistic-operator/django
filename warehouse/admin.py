from django.contrib import admin
from .models import Warehouse, batchCreateIsochronesWF, batchFindNearestWF
from django.contrib.gis.admin import GISModelAdmin
from django.contrib import messages
from django_object_actions import DjangoObjectActions, action
from django.shortcuts import redirect
from geo.utils import postpone

import asyncio

class WarehouseAdmin(DjangoObjectActions, GISModelAdmin):

    actions = ["create_isochrones_all", 'find_nearest_station', 'cascade_delete']
    changelist_actions = ('import_CSV',)
    
    @admin.action(description="Create all isochrones")
    def create_isochrones_all(self, request, queryset):
        batchCreateIsochronesWF(queryset)
        self.message_user(
            request,
            'created batch all isochrones',
            messages.SUCCESS,
        )
    
    @admin.action(description="Cascade delete")
    def cascade_delete(self, request, queryset):
        for warehouse in queryset:
            id = warehouse.id
            warehouse.delete()
            self.message_user(
                request,
                'deleted ' + str(id) + '',
                messages.SUCCESS,
            )
    
    @admin.action(description="Find nearest station")
    def find_nearest_station(self, request, queryset):
        batchFindNearestWF(queryset)
        self.message_user(
            request,
            'found nearest station for batch added to temporal workflows',
            messages.SUCCESS,
        )
    @action(label="Import CSV", description="Import CSV")
    def import_CSV(self, request, obj):
        return redirect('/upload-csv/wh')

admin.site.register(Warehouse, WarehouseAdmin)