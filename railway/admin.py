from django.contrib import admin
from .models import Railway
from django.contrib.gis.admin import GISModelAdmin, TabularInline
from django.contrib import messages
from django_object_actions import DjangoObjectActions, action

class NeighborhoodInline(TabularInline):
    model = Railway.neighbors.through
    fk_name = "source"
    extra = 1

class NeighborhoodOpInline(TabularInline):
    model = Railway.neighbors_op.through
    fk_name = "source"
    extra = 0

class RailwayAdmin(DjangoObjectActions, GISModelAdmin):
    inlines = [
        NeighborhoodInline,
        NeighborhoodOpInline,
    ]
    changelist_actions = ('optimize_routes', 'test',)

    @action(label="Optimize", description="Optimize routes")
    def optimize_routes(self, request, obj):
        obj[0].optimize()
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
    
admin.site.register(Railway, RailwayAdmin)