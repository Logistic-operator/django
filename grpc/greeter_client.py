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
"""The Python implementation of the GRPC helloworld.Greeter client."""

from __future__ import print_function

import logging

import grpc
import warehouse_pb2
import warehouse_pb2_grpc
import isochrone_pb2
import isochrone_pb2_grpc


def run():
    # NOTE(gRPC Python Team): .close() is possible on a channel and should be
    # used in circumstances in which the with statement does not fit the needs
    # of the code.
    print("Will try to greet world ...")
    with grpc.insecure_channel("localhost:50051") as channel:
        stub = isochrone_pb2_grpc.IsochroneControllerStub(channel)
        response = stub.Delete(isochrone_pb2.IsochroneRetrieveRequest(warehouse_id=27, timespan=120))
        # for r in response:
        #     print(r)
        print(response.id)


if __name__ == "__main__":
    logging.basicConfig()
    run()
