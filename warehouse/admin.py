from django.contrib import admin
from .models import Warehouse
from django.contrib.gis.admin import GISModelAdmin
from django.contrib import messages


class WarehouseAdmin(GISModelAdmin):

    actions = ["create_isochrones_all", 'find_nearest_station']

    @admin.action(description="Create all isochrones")
    def create_isochrones_all(self, request, queryset):
        for warehouse in queryset:
            warehouse.createIsochrones([240, 480, 720, 960, 1200, 1440])
            self.message_user(
                request,
                'created ' + str(warehouse.id) + ' all isochrones',
                messages.SUCCESS,
            )
    
    @admin.action(description="Find nearest station")
    def find_nearest_station(self, request, queryset):
        for warehouse in queryset:
            warehouse.findNearest()
            self.message_user(
                request,
                'found nearest station for ' + str(warehouse.id),
                messages.SUCCESS,
            )

admin.site.register(Warehouse, WarehouseAdmin)