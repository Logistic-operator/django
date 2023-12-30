
from __future__ import print_function

import logging
from temporalio import activity
import grpc

import sys
sys.path.append('..')
sys.path.append('../grpc')

import warehouse_pb2
import warehouse_pb2_grpc
import isochrone_pb2
import isochrone_pb2_grpc

grpc_url = 'localhost:50051'

@activity.defn
async def drawAllIsos(wh_id) -> list:
    res = []
    with grpc.insecure_channel(grpc_url) as channel:
        stub = warehouse_pb2_grpc.WarehouseControllerStub(channel)
        response = stub.Iso(warehouse_pb2.WarehouseIsoRequest(id=wh_id, timespans='all'))
        for r in response:
            res.append(isochroneSerializer(r))
    return res

@activity.defn
async def createWH(wh) -> dict:
    with grpc.insecure_channel(grpc_url) as channel:
        stub = warehouse_pb2_grpc.WarehouseControllerStub(channel)
        response = stub.Create(warehouse_pb2.Warehouse(phone=wh.phone, point=wh.point))
        return warehouseSerializer(response)

@activity.defn
async def findNearestRailway(wh_id) -> dict:
    with grpc.insecure_channel(grpc_url) as channel:
        stub = warehouse_pb2_grpc.WarehouseControllerStub(channel)
        response = stub.NearestStation(warehouse_pb2.WarehouseRetrieveRequest(id=wh_id))
        return warehouseSerializer(response)

def warehouseSerializer(wh: warehouse_pb2.Warehouse):
    return {
        'id': wh.id,
        'phone': wh.phone,
        'point': wh.point,
        'nearest_railway_id': wh.nearest_railway_id,
        'nearest_railway_length': wh.nearest_railway_length,
        }

def isochroneSerializer(iso: isochrone_pb2.Isochrone):
    return {
        'id': iso.id,
        'warehouse_id': iso.warehouse_id, 
        'timespan': iso.timespan,
        'all_geom': iso.all_geom,
        }