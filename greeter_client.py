from __future__ import print_function

import logging

import grpc
import warehouse_pb2
import warehouse_pb2_grpc


def run():
    # NOTE(gRPC Python Team): .close() is possible on a channel and should be
    # used in circumstances in which the with statement does not fit the needs
    # of the code.
    with grpc.insecure_channel("localhost:50051") as channel:
        stub = warehouse_pb2_grpc.WarehouseControllerStub(channel)
        response = stub.List(warehouse_pb2.WarehouseListRequest())
    print(response)


if __name__ == "__main__":
    logging.basicConfig()
    run()