import networkx as nx
import matplotlib.pyplot as plt
from django.contrib.gis.geos import GEOSGeometry
import json

G = nx.Graph()

G.add_node(1, pos = (35.548645, 46.456584))
G.add_node(2, pos = (49.548645, 48.456584))
G.add_weighted_edges_from([(1,2,35)])
pos=nx.get_node_attributes(G,'pos')
nx.draw(G,pos)
labels = nx.get_edge_attributes(G,'weight')
nx.draw_networkx_edge_labels(G,pos,edge_labels=labels)
plt.savefig('../static/plot.png', dpi=300, bbox_inches='tight')
