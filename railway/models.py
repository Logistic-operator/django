from django.contrib.gis.db import models as models
from isochrone.models import Isochrone
import networkx as nx
from geo.utils import printProgressBar
from django.contrib.gis.geos import GEOSGeometry
import matplotlib.pyplot as plt
from geo.settings import BASE_DIR

from geo.utils import postpone, getRowsFromCSV
from temporalio.client import Client
from .workflows import RailwayCreate, RailwayCreateNb
import asyncio
from asgiref.sync import sync_to_async

from .activities import ComposeCreateInput, ComposeCreateNbInput
import csv, io

class Railway(models.Model):
    iid = models.IntegerField()
    name = models.CharField(max_length=64)
    is_cont = models.BooleanField()
    point = models.PointField()
    neighbors = models.ManyToManyField('self', through='Neighborhood', symmetrical = False, related_name = 'Neighborhood')
    neighbors_op = models.ManyToManyField('self', through='NeighborhoodOp', symmetrical = False, related_name = 'NeighborhoodOp')

    def __str__(self) -> str:
        return self.name
    
    def createIsochrones(self, timespan: [int]):
        isochrones = []
        for time in timespan:
            isochrone = Isochrone.objects.get_or_create(seller=self, timespan=time)[0]
            isochrone.redraw()
            isochrones.append(isochrone)
        return isochrones
    
    @classmethod
    def optimize(cls):
        G, not_conts = getGraph(cls)
        not_conts_count = len(not_conts)
        removeNotConts(G, not_conts, not_conts_count)
        createNeighborhoodOP(G)
        return str(Neighborhood.objects.count()) + '/' + str(NeighborhoodOp.objects.count())
    
    @classmethod
    def test(cls):
        G = nx.Graph()
        nodes = [(node.id, node.point.x, node.point.y) for node in Railway.objects.filter(is_cont=True)]
        for node in nodes:
            G.add_node(node[0], pos=(node[1], node[2]))
        edges = [(edge.source.id, edge.target.id, edge.length) for edge in NeighborhoodOp.objects.all()]
        G.add_weighted_edges_from(edges)
        pos=nx.get_node_attributes(G,'pos')
        nx.draw(G,pos)
        labels = nx.get_edge_attributes(G,'weight')
        nx.draw_networkx_edge_labels(G,pos,edge_labels=labels)
        fig = plt.gcf()
        fig.set_size_inches(80, 60)
        fig.savefig(BASE_DIR / 'static/plot.png', dpi=100)
        # plt.savefig(BASE_DIR / 'static/plot.png', dpi=300, bbox_inches='tight')

def getGraph(cls):
    G = nx.Graph()
    print('Loading graph...')
    not_conts = [railway.id for railway in cls.objects.filter(is_cont=False)]
    edges = [(edge.source.id, edge.target.id, edge.length) for edge in Neighborhood.objects.all()]
    G.add_weighted_edges_from(edges)
    return (G, not_conts)

def createNeighborhoodOP(G):
    print('Creating Optimized Edges...')
    NeighborhoodOp.objects.all().delete()
    new_Neighborhoods = []
    for edge in G.edges(data=True):
        source = Railway.objects.get(id=edge[0])
        target = Railway.objects.get(id=edge[1])
        new_Neighborhoods.append(NeighborhoodOp(source=source, target=target, length=edge[2]['weight']))
    NeighborhoodOp.objects.bulk_create(new_Neighborhoods)
    print('Done')

def removeNotConts(g: nx.Graph, not_conts, total):
    for i, node in enumerate(not_conts):
        printProgressBar(i, total, prefix = 'Railway Optimize Progress:', suffix = 'Complete', length = 40)
        if node in g.nodes:
            edges = g.edges(node, data=True)
            edges = list(edges.__iter__())
            if len(edges) == 0:
                g.remove_node(node)
                continue
            if len(edges) == 1:
                g.remove_edge(edges[0][0], edges[0][1])
                g.remove_node(node)
                continue
            root = edges[0]
            u = root[0] if root[0] != node else root[1]
            for edge in edges[1:]:
                v = edge[0] if edge[0] != node else edge[1]
                if g.has_edge(u, v):
                    g.edges[(u, v)]['weight'] = min(g.edges[(u, v)]['weight'], root[2]['weight'] + edge[2]['weight'])
                else:
                    g.add_weighted_edges_from([(u, v, root[2]['weight'] + edge[2]['weight'])])
                g.remove_edge(edge[0], edge[1])
            g.remove_edge(root[0], root[1])
            g.remove_node(node)

@postpone   
def batchCreateRwWF(file):
    
    data_read = getRowsFromCSV(file)
    
    async def run(rows):
        await NeighborhoodOp.objects.all().adelete()
        await Neighborhood.objects.all().adelete()
        await Railway.objects.all().adelete()
        client = await Client.connect("localhost:7233")
        for row in rows:
            try:
                iid = int(row[0])
                name = row[1]
                point = row[2]
                is_cont = bool(row[4])
                the_id = await client.execute_workflow(
                    RailwayCreate.run, ComposeCreateInput(
                        iid=iid,
                        name=name,
                        point=point,
                        is_cont=is_cont,
                    ), id=f"rw_create_{str(iid)}", task_queue="rw-task-queue"
                )
            except:
                pass
    asyncio.run(run(data_read))

@postpone   
def batchCreateNbWF(file):
    
    data_read = getRowsFromCSV(file)
    
    async def run(rows):
        await NeighborhoodOp.objects.all().adelete()
        await Neighborhood.objects.all().adelete()
        client = await Client.connect("localhost:7233")
        for row in rows:
            try:
                source_iid = int(row[0])
                target_iid = int(row[1])
                length = int(row[2])
                the_id = await client.execute_workflow(
                    RailwayCreateNb.run, ComposeCreateNbInput(
                        source_iid=source_iid,
                        target_iid=target_iid,
                        length=length,
                    ), id=f"rw_nb_create_{str(source_iid)}_{str(target_iid)}", task_queue="rw-task-queue"
                )
            except:
                pass
    asyncio.run(run(data_read))

class Neighborhood(models.Model):
    source = models.ForeignKey(Railway, on_delete=models.CASCADE, related_name = 'source')
    target = models.ForeignKey(Railway, on_delete=models.DO_NOTHING, related_name = 'target', null=True)
    length = models.FloatField()

    def __str__(self) -> str:
        return f'{str(self.source.id)}_{str(self.target.id)}'

class NeighborhoodOp(models.Model):
    source = models.ForeignKey(Railway, on_delete=models.CASCADE, related_name = 'sourceop')
    target = models.ForeignKey(Railway, on_delete=models.DO_NOTHING, related_name = 'targetop', null=True)
    length = models.FloatField()

    def __str__(self) -> str:
        return f'{str(self.source.id)}_{str(self.target.id)}'

