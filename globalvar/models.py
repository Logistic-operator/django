from django.db import models
from picklefield.fields import PickledObjectField
from django.apps import apps
import networkx as nx

class Globalvar(models.Model):
    name = models.CharField()
    args = PickledObjectField(null=True)

    @classmethod
    def load_graph(cls):
        G = nx.Graph()
        print('Loading graph...')
        NeighborhoodOp = apps.get_model(app_label='railway', model_name='NeighborhoodOp')
        NeighborhoodRailway = apps.get_model(app_label='warehouse', model_name='NeighborhoodRailway')
        Application = apps.get_model(app_label='application', model_name='Application')
        edges = [(edge.source.id, edge.target.id, edge.length) for edge in NeighborhoodOp.objects.all()]
        edges.extend([(edge.warehouse.id + 100000, edge.railway.id, edge.length) for edge in NeighborhoodRailway.objects.all()])
        edges.extend([(edge.id+200000, edge.warehouse.id+100000, 0) for edge in Application.objects.all()])
        G.add_weighted_edges_from(edges)
        gr = Globalvar.objects.get_or_create(name='graph')[0]
        gr.args = G
        gr.save()