from django.urls import path

from .views import getWH, getWHs, createWH, updateWH, removeWH, createIsochrones

app_name = 'warehouse'

urlpatterns = [
    path('', getWH, name='get'),
    path('all', getWHs, name='get all'),
    path('new', createWH, name='create'),
    path('update', updateWH, name='update'),
    path('del', removeWH, name='delete'),
    path('iso', createIsochrones, name='isochrones'),
]