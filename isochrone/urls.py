from django.urls import path

from .views import getISO, getISOs, removeISO, removeISOs

app_name = 'isochrone'

urlpatterns = [
    path('', getISO, name='get'),
    path('all', getISOs, name='get all'),
    path('del', removeISO, name='delete'),
    path('del/all', removeISOs, name='delete all'),
]