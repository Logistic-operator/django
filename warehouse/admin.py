from django.contrib import admin
from .models import Warehouse
from django.contrib.gis.admin import GISModelAdmin
from django.contrib import messages


class WarehouseAdmin(GISModelAdmin):

    actions = ["create_isochrones_240"]

    @admin.action(description="Create [240m] isochrones")
    def create_isochrones_240(self, request, queryset):
        for warehouse in queryset:
            warehouse.createIsochrones([240])
            self.message_user(
                request,
                'created ' + str(warehouse.id) + ' isochrones [240]',
                messages.SUCCESS,
            )

admin.site.register(Warehouse, WarehouseAdmin)