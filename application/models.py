from django.db import models
from globalvar.models import Globalvar
import networkx as nx

class Application(models.Model):
    warehouse = models.ForeignKey('warehouse.Warehouse', on_delete=models.CASCADE, null=True)
    app_type = models.CharField() # sell, buy
    product = models.CharField()
    volume = models.FloatField()

    @property
    def warehouse_point(self):
        return self.warehouse.point

    def clean(self):
        if self.app_type not in ('sell', 'buy'):
            raise ValidationError('app_type should have value equals "buy" or "sell"')

    def getRoutesToApp(self, app_id):
        G = Globalvar.objects.get(name='graph').args
        # for i in range(10000):
        #     nx.dijkstra_path(G, 100015, 103449)
        return nx.dijkstra_path(G, self.id + 200000, app_id + 200000)

    def addAppToGraph(self):
        var = Globalvar.objects.get(name='graph')
        G = var.args
        G.add_weighted_edges_from([(self.id+200000, self.warehouse.id+100000, 0)])
        var.args = G
        var.save()

    @classmethod
    def getProductsSell(self):
        return self.objects.filter(app_type='sell').values('product').distinct()

    @classmethod
    def getProductsBuy(self):
        return self.objects.filter(app_type='buy').values('product').distinct()
    
    @classmethod
    def getAppsBuy(self, product, volume):
        return self.objects.filter(app_type='buy', product=product, volume__lte=volume)

    @classmethod
    def getAppsSell(self, product, volume):
        return self.objects.filter(app_type='sell', product=product, volume__gte=volume)
    
    @classmethod
    def getCorespondingApps(self, app):
        if app.app_type == 'sell':
            return self.getAppsBuy(product=app.product, volume=app.volume)
        if app.app_type == 'buy':
            return self.getAppsSell(product=app.product, volume=app.volume)

from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=Application, dispatch_uid="add_app_to_graph")
def add_app_to_graph(sender, instance, **kwargs):
    instance.addAppToGraph()