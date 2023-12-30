import sys
sys.path.append('..')

from warehouse.models import Warehouse
from railway.models import Railway
import warehouse_pb2
import warehouse_pb2_grpc
from django.contrib.gis.geos import GEOSGeometry


class WarehouseServicer(warehouse_pb2_grpc.WarehouseControllerServicer):
    def List(self, request, context):
        for wh in Warehouse.objects.all():
            yield toGrpcWarehouse(wh)
    
    def Retrieve(self, request, context):
        wh = Warehouse.objects.filter(id=request.id).first()
        return toGrpcWarehouse(wh)
    
    def Create(self, request, context):
        wh = Warehouse(
            phone=request.phone,
            point=GEOSGeometry(request.point),
            )
        wh.save()
        return toGrpcWarehouse(wh)
    
    def Change(self, request, context):
        the_wh = Warehouse.objects.get(id=request.id)
        if request.phone:
            the_wh.phone = request.phone
        if request.point:
            the_wh.point = GEOSGeometry(request.point)
        if request.nearest_railway_id:
            the_wh.nearest_railway = Railway.objects.get(id=request.nearest_railway_id)
        if request.nearest_railway_length:
            the_wh.nearest_railway_length = request.nearest_railway_length
        the_wh.save()
        return toGrpcWarehouse(the_wh)
    
    def Delete(self, request, context):
        the_wh = Warehouse.objects.filter(id=request.id).first()
        wh = toGrpcWarehouse(the_wh)
        the_wh.delete()
        return toGrpcWarehouse(wh)
    
    def Iso(self, request, context):
        the_wh = Warehouse.objects.filter(id=request.id).first()
        if request.timespans == 'all':
            isochrones = the_wh.createIsochrones([240, 480, 720, 960, 1200, 1440])
        else:
            isochrones = the_wh.createIsochrones(request.timespans.split('_'))
        for iso in isochrones:
            yield toGrpcIso(iso)
    
    def NearestStation(self, request, context):
        the_wh = Warehouse.objects.filter(id=request.id).first()
        the_wh.findNearest()
        return toGrpcWarehouse(the_wh)

def toGrpcWarehouse(wh: Warehouse):
    return warehouse_pb2.Warehouse(
        id=wh.id, 
        phone=wh.phone, 
        point=wh.point.__str__(),
        nearest_railway_id=wh.nearest_railway.id,
        nearest_railway_length=wh.nearest_railway_length
        )

def toGrpcIso(iso):
    return warehouse_pb2.Isochrone(id=iso.id, warehouse_id=iso.warehouse.id, timespan=iso.timespan, all_geom=iso.all_geom.__str__())