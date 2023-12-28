from rest_framework import serializers
from django.contrib.gis.geos import GEOSGeometry
import json

from .models import Isochrone

class IsochroneModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Isochrone
        exclude = ()