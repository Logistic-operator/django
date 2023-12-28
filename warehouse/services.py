import warehouse_pb2
import warehouse_pb2_grpc

def grpc_hook(server):
    warehouse_pb2_grpc.add_MYServicer_to_server(MYServicer(), server)

class MYServicer(warehouse_pb2_grpc.MYServicer):

    def GetPage(self, request, context):
        response = warehouse_pb2.PageResponse(title="Demo object")
        return response