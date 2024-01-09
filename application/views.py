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

from .models import Application
from warehouse.models import Warehouse
import json

from django.contrib.gis.geos import MultiLineString, LineString
from warehouse.models import Warehouse, NeighborhoodRailway
from railway.models import Railway


@api_view(['GET'])
@permission_classes([AllowAny])
def getProductsSell(req):
    return Response({'products': Application.getProductsSell()}, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([AllowAny])
def getProductsBuy(req):
    return Response({'products': Application.getProductsBuy()}, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([AllowAny])
def getApplications(req):
    formInfo = req.data
    new_app = Application(
        app_type=formInfo['appType'],
        product=formInfo['product'],
        volume=formInfo['volume'],
        warehouse=Warehouse.objects.get(id=formInfo['wh_id']),
        )
    new_app.save()
    # new_app = Application.objects.first()
    corApps = Application.getCorespondingApps(new_app)
    return Response({
        'appFrom': appToGeoJSON(new_app),
        'appTos': [appToGeoJSON(app) for app in corApps]
        }, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([AllowAny])
def getRoute(req):
    app = Application.objects.get(id=req.data['appFromId'])
    res = []
    try:
        route = app.getRoutesToApp(req.data['appToId'])
        wh_to_rw_1 = NeighborhoodRailway.objects.get(warehouse__id=route[1]-100000, railway__id=route[2]).geom
        wh_to_rw_2 = NeighborhoodRailway.objects.get(warehouse__id=route[-2]-100000, railway__id=route[-3]).geom
        wh_to_wh = Warehouse.objects.get(id=route[1]-100000).getWhToStationRoute(Warehouse.objects.get(id=route[-2]-100000))['geom']
        rw_ml = rwIdsToMultiLine(route[2:-2])
        res.append({'shape': wh_to_rw_1})
        res.append({'shape': wh_to_rw_2})
        res.append({'forward': wh_to_wh})
        res.append({'points': rw_ml})
    except:
        app2 = Application.objects.get(id=req.data['appToId'])
        wh_to_wh = app.warehouse.getWhToStationRoute(app2.warehouse)['geom']
        res.append({'forward': wh_to_wh})
    
    return Response({
        'edges': res
        }, status=status.HTTP_200_OK)

def appToGeoJSON(app):
    return {
        "type": "Feature",
        "geometry": json.loads(app.warehouse.point.json),
        "properties": {
            "id": app.id,
            "app_type": app.app_type,
            "product": app.product,
            "volume": app.volume
        }
    }

def rwIdsToMultiLine(rw_ids):
    points = []
    for id in rw_ids:
        point = Railway.objects.get(id=id).point
        points.append((
            point.y, point.x
        ))
    return points