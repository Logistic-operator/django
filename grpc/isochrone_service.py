import sys
sys.path.append('..')

from isochrone.models import Isochrone
from warehouse.models import Warehouse
import isochrone_pb2
import isochrone_pb2_grpc
import json


class IsochroneServicer(isochrone_pb2_grpc.IsochroneControllerServicer):
    def List(self, request, context):
        for iso in Isochrone.objects.filter(warehouse__id=request.warehouse_id):
            yield toGrpcIso(iso)
    
    def Retrieve(self, request, context):
        iso = Isochrone.objects.get(warehouse__id=request.warehouse_id, timespan=request.timespan)
        return toGrpcIso(iso)
    
    def Delete(self, request, context):
        the_iso = Isochrone.objects.get(warehouse__id=request.warehouse_id, timespan=request.timespan)
        res = toGrpcIso(the_iso)
        the_iso.delete()
        return res

def toGrpcIso(iso):
    return isochrone_pb2.Isochrone(id=iso.id, warehouse_id=iso.warehouse.id, timespan=iso.timespan, all_geom=iso.all_geom.__str__())