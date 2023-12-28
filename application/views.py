from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import (
    api_view, 
    permission_classes,
    renderer_classes,
    parser_classes,
    )
from rest_framework.exceptions import NotFound, NotAcceptable
from rest_framework.parsers import MultiPartParser, FormParser

from warehouse.models import Warehouse
from .renderers import WarehouseJSONRenderer
from .serializers import WarehouseModelSerializer

@api_view(['GET'])
@permission_classes([AllowAny])
@renderer_classes([WarehouseJSONRenderer])
def getWH(req):
    wh = req.data.get('warehouse', None)
    if not wh:
        raise NotAcceptable(detail='Payload is wrong')
    id = wh.get('id', None)
    phone = wh.get('phone', None)
    theWH = None
    if id:
        theWH = Warehouse.objects.filter(id=id).first()
    elif phone:
        theWH = Warehouse.objects.filter(phone=phone).first()
    if not theWH:
        raise NotFound(detail='No such warehouse')
    serializer = WarehouseModelSerializer(theWH)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([AllowAny])
@renderer_classes([WarehouseJSONRenderer])
def createWH(req):
    wh = req.data.get('warehouse', None)
    serializer = WarehouseModelSerializer(data=wh)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['DELETE'])
@permission_classes([AllowAny])
@renderer_classes([WarehouseJSONRenderer])
def removeWH(req):
    wh = req.data.get('warehouse', None)
    if not wh:
        raise NotAcceptable(detail='Payload is wrong')
    id = wh.get('id', None)
    theWH = None
    if id:
        theWH = Warehouse.objects.filter(id=id).first()
    if not theWH:
        raise NotFound(detail='No such warehouse')
    serializer = WarehouseModelSerializer(theWH)
    theWH.delete()
    return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)

@api_view(['PATCH'])
@permission_classes([AllowAny])
@renderer_classes([WarehouseJSONRenderer])
def updateWH(req):
    updWH = req.data.get('warehouse', None)
    if not updWH:
        raise NotAcceptable(detail='Payload is wrong')
    id = updWH.get('id', None)
    theWH = None
    if id:
        theWH = Warehouse.objects.filter(id=id).first()
    if not theWH:
        raise NotFound(detail='No such warehouse')
    serializer = WarehouseModelSerializer(
        theWH, data=updWH, partial=True
    )
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, status=status.HTTP_200_OK)
        
