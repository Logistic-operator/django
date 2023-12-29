# Copyright 2015 gRPC authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""The Python implementation of the GRPC helloworld.Greeter server."""

from concurrent import futures
import logging

import grpc
import warehouse_pb2_grpc
import isochrone_pb2_grpc
import django, os
import sys
sys.path.append('..')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "geo.settings")
 
django.setup()

from warehouse_service import WarehouseServicer
from isochrone_service import IsochroneServicer

def serve():
    port = "50051"
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    warehouse_pb2_grpc.add_WarehouseControllerServicer_to_server(WarehouseServicer(), server)
    isochrone_pb2_grpc.add_IsochroneControllerServicer_to_server(IsochroneServicer(), server)
    server.add_insecure_port("[::]:" + port)
    server.start()
    print("Server started, listening on " + port)
    server.wait_for_termination()


if __name__ == "__main__":
    logging.basicConfig()
    serve()