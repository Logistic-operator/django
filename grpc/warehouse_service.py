import sys
sys.path.append('..')

from warehouse.models import Warehouse
from warehouse.serializers import WarehouseModelSerializer
import warehouse_pb2
import warehouse_pb2_grpc
import json


class WarehouseServicer(warehouse_pb2_grpc.WarehouseControllerServicer):
    def List(self, request, context):
        for wh in WarehouseModelSerializer(Warehouse.objects.all(), many=True).data:
            yield toGrpcWarehouse(wh)
    
    def Retrieve(self, request, context):
        wh = WarehouseModelSerializer(Warehouse.objects.filter(id=request.id).first()).data
        return toGrpcWarehouse(wh)
    
    def Create(self, request, context):
        wh = {
            'phone': request.phone,
            'point': json.loads(request.point),
        }
        serializer = WarehouseModelSerializer(data=wh)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return toGrpcWarehouse(serializer.data)
    
    def Change(self, request, context):
        the_wh = Warehouse.objects.get(id=request.id)
        wh = {}
        if request.phone:
            wh['phone'] = request.phone
        if request.point:
            wh['point'] = json.loads(request.point)
        
        serializer = WarehouseModelSerializer(the_wh, data=wh, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return toGrpcWarehouse(serializer.data)
    
    def Delete(self, request, context):
        the_wh = Warehouse.objects.filter(id=request.id).first()
        wh = WarehouseModelSerializer(the_wh).data
        the_wh.delete()
        return toGrpcWarehouse(wh)
    
    def Iso(self, request, context):
        the_wh = Warehouse.objects.filter(id=request.id).first()
        isochrones = the_wh.createIsochrones(request.timespans.split('_'))
        for iso in isochrones:
            yield toGrpcIso(iso)

def toGrpcWarehouse(wh):
    return warehouse_pb2.Warehouse(id=wh['id'], phone=wh['phone'], point=wh['point'])

def toGrpcIso(iso):
    return warehouse_pb2.Isochrone(id=iso.id, warehouse_id=iso.warehouse.id, timespan=iso.timespan, all_geom=iso.all_geom.__str__())