# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import isochrone_pb2 as isochrone__pb2


class IsochroneControllerStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.List = channel.unary_stream(
                '/isochrone.IsochroneController/List',
                request_serializer=isochrone__pb2.IsochroneListRequest.SerializeToString,
                response_deserializer=isochrone__pb2.Isochrone.FromString,
                )
        self.Retrieve = channel.unary_unary(
                '/isochrone.IsochroneController/Retrieve',
                request_serializer=isochrone__pb2.IsochroneRetrieveRequest.SerializeToString,
                response_deserializer=isochrone__pb2.Isochrone.FromString,
                )
        self.Delete = channel.unary_unary(
                '/isochrone.IsochroneController/Delete',
                request_serializer=isochrone__pb2.IsochroneRetrieveRequest.SerializeToString,
                response_deserializer=isochrone__pb2.Isochrone.FromString,
                )
        self.ListRailways = channel.unary_stream(
                '/isochrone.IsochroneController/ListRailways',
                request_serializer=isochrone__pb2.IsochroneRetrieveRequest.SerializeToString,
                response_deserializer=isochrone__pb2.Railway.FromString,
                )


class IsochroneControllerServicer(object):
    """Missing associated documentation comment in .proto file."""

    def List(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def Retrieve(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def Delete(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def ListRailways(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_IsochroneControllerServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'List': grpc.unary_stream_rpc_method_handler(
                    servicer.List,
                    request_deserializer=isochrone__pb2.IsochroneListRequest.FromString,
                    response_serializer=isochrone__pb2.Isochrone.SerializeToString,
            ),
            'Retrieve': grpc.unary_unary_rpc_method_handler(
                    servicer.Retrieve,
                    request_deserializer=isochrone__pb2.IsochroneRetrieveRequest.FromString,
                    response_serializer=isochrone__pb2.Isochrone.SerializeToString,
            ),
            'Delete': grpc.unary_unary_rpc_method_handler(
                    servicer.Delete,
                    request_deserializer=isochrone__pb2.IsochroneRetrieveRequest.FromString,
                    response_serializer=isochrone__pb2.Isochrone.SerializeToString,
            ),
            'ListRailways': grpc.unary_stream_rpc_method_handler(
                    servicer.ListRailways,
                    request_deserializer=isochrone__pb2.IsochroneRetrieveRequest.FromString,
                    response_serializer=isochrone__pb2.Railway.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'isochrone.IsochroneController', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class IsochroneController(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def List(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_stream(request, target, '/isochrone.IsochroneController/List',
            isochrone__pb2.IsochroneListRequest.SerializeToString,
            isochrone__pb2.Isochrone.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def Retrieve(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/isochrone.IsochroneController/Retrieve',
            isochrone__pb2.IsochroneRetrieveRequest.SerializeToString,
            isochrone__pb2.Isochrone.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def Delete(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/isochrone.IsochroneController/Delete',
            isochrone__pb2.IsochroneRetrieveRequest.SerializeToString,
            isochrone__pb2.Isochrone.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def ListRailways(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_stream(request, target, '/isochrone.IsochroneController/ListRailways',
            isochrone__pb2.IsochroneRetrieveRequest.SerializeToString,
            isochrone__pb2.Railway.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)