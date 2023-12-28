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

from .models import Isochrone
from warehouse.models import Warehouse
from .renderers import IsochroneJSONRenderer
from .serializers import IsochroneModelSerializer

@api_view(['GET'])
@permission_classes([AllowAny])
def getISOs(req):
    iso = req.data.get('isochrone', None)
    if not iso:
        raise NotAcceptable(detail='Payload is wrong')
    warehouse_id = iso.get('warehouse_id', None)
    warehouse = getWH(warehouse_id)
    theISOs = Isochrone.objects.filter(warehouse=warehouse)    
    serializer = IsochroneModelSerializer(theISOs, many=True)
    return Response({'isochrones': serializer.data}, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([AllowAny])
@renderer_classes([IsochroneJSONRenderer])
def getISO(req):
    iso = req.data.get('isochrone', None)
    if not iso:
        raise NotAcceptable(detail='Payload is wrong')
    warehouse_id = iso.get('warehouse_id', None)
    timespan = iso.get('timespan', None)
    warehouse = getWH(warehouse_id)
    theISO = Isochrone.objects.filter(warehouse=warehouse, timespan=timespan).first()
    if not theISO:
        raise NotFound(detail='No such isochrone')
    serializer = IsochroneModelSerializer(theISO)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['DELETE'])
@permission_classes([AllowAny])
@renderer_classes([IsochroneJSONRenderer])
def removeISO(req):
    iso = req.data.get('isochrone', None)
    if not iso:
        raise NotAcceptable(detail='Payload is wrong')
    warehouse_id = iso.get('warehouse_id', None)
    timespan = iso.get('timespan', None)
    warehouse = getWH(warehouse_id)
    theISO = Isochrone.objects.filter(warehouse=warehouse, timespan=timespan).first()
    if not theISO:
        raise NotFound(detail='No such isochrone')
    serializer = IsochroneModelSerializer(theISO)
    theISO.delete()
    return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)

@api_view(['DELETE'])
@permission_classes([AllowAny])
def removeISOs(req):
    iso = req.data.get('isochrone', None)
    if not iso:
        raise NotAcceptable(detail='Payload is wrong')
    warehouse_id = iso.get('warehouse_id', None)
    timespan = iso.get('timespan', None)
    warehouse = getWH(warehouse_id)
    theISOs = Isochrone.objects.filter(warehouse=warehouse)
    serializer = IsochroneModelSerializer(theISOs, many=True)
    for theISO in theISOs:
        theISO.delete()
    return Response({'isochrones': serializer.data}, status=status.HTTP_204_NO_CONTENT)

def getWH(warehouse_id):
    if warehouse_id:
        warehouse = Warehouse.objects.filter(id=warehouse_id).first()
        if not warehouse:
            raise NotFound(detail='No such warehouse')
        return warehouse