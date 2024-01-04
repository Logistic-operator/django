import sys
sys.path.append('..')

from railway.models import Railway, Neighborhood, NeighborhoodOp
import railway_pb2
import railway_pb2_grpc
import json


class RailwayServicer(railway_pb2_grpc.RailwayControllerServicer):
    def OptimizeNeighborhood(self, request, context):
        return railway_pb2.Optimized(result= Railway.optimize())

def toGrpcRw(rw):
    return railway_pb2.Railway(
        id=rw.id, 
        iid=rw.iid, 
        point=rw.point.__str__(), 
        is_cont=rw.is_cont, 
        )