from django.urls import path

from .views import getProductsSell, getProductsBuy, getApplications, getRoute

app_name = 'application'

urlpatterns = [
    path('products/sell/', getProductsSell, name='get products sell'),
    path('products/buy/', getProductsBuy, name='get products buy'),
    path('wh/', getApplications, name='get applications'),
    path('route/', getRoute, name='get route'),
]