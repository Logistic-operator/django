from django.contrib import admin
from .models import Railway, Neighborhood, NeighborhoodOp
from django.contrib.gis.admin import GISModelAdmin, TabularInline
from django.contrib import messages
from django_object_actions import DjangoObjectActions, action
from django.shortcuts import redirect

class NeighborhoodAdmin(DjangoObjectActions, GISModelAdmin):
    changelist_actions = ('import_CSV',)

    @action(label="Import CSV", description="Import CSV")
    def import_CSV(self, request, obj):
        return redirect('/upload-csv/neib')

class RailwayAdmin(DjangoObjectActions, GISModelAdmin):
    changelist_actions = ('optimize_routes', 'import_CSV',)

    @action(label="Optimize", description="Optimize routes")
    def optimize_routes(self, request, obj):
        obj[0].optimizeWF()
        self.message_user(
            request,
            'optimized',
            messages.SUCCESS,
        )
    @action(label="Draw graph", description="Draw graph")
    def test(self, request, obj):
        obj[0].test()
        self.message_user(
            request,
            'Link http://localhost:8001/static/plot.png plot file',
            messages.SUCCESS,
        )

    @action(label="Import CSV", description="Import CSV")
    def import_CSV(self, request, obj):
        return redirect('/upload-csv/rail')
    
admin.site.register(Railway, RailwayAdmin)
admin.site.register(Neighborhood, NeighborhoodAdmin)
admin.site.register(NeighborhoodOp, admin.ModelAdmin)