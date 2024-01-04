from rest_framework import serializers
from django.contrib.gis.geos import GEOSGeometry
import json

from .models import Warehouse

class WarehouseModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Warehouse
        exclude = ()
    
    def create(self, validated_data):
        validated_data['point'] = GEOSGeometry(json.dumps(validated_data['point']))
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        point = validated_data.pop('point', None)
        if point:
            setattr(instance, 'point', GEOSGeometry(json.dumps(point)))
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        return instance