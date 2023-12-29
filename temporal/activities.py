
from __future__ import print_function

import logging
from temporalio import activity
import grpc

import sys
sys.path.append('..')
sys.path.append('../temp')

import grpc.warehouse_pb2 as warehouse_pb2
import grpc.warehouse_pb2_grpc as warehouse_pb2_grpc
import grpc.isochrone_pb2 as isochrone_pb2
import grpc.isochrone_pb2_grpc as isochrone_pb2_grpc


@activity.defn
async def say_hello() -> list:
    res = []
    with grpc.insecure_channel("localhost:50051") as channel:
        stub = isochrone_pb2_grpc.IsochroneControllerStub(channel)
        response = stub.List(isochrone_pb2.IsochroneListRequest(warehouse_id=27))
        for r in response:
            res.append(isochroneSerializer(r))
    return res

def warehouseSerializer(wh: warehouse_pb2.Warehouse):
    return {
        'id': wh.id,
        'phone': wh.phone,
        'point': wh.point,
        }

def isochroneSerializer(iso: isochrone_pb2.Isochrone):
    return {
        'id': iso.id,
        'warehouse_id': iso.warehouse_id, 
        'timespan': iso.timespan,
        'all_geom': iso.all_geom,
        }