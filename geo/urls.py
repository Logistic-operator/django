"""
URL configuration for geo project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from railway.views import railway_upload, getAll

urlpatterns = [
    path('admin/', admin.site.urls),
    path('upload-csv/<str:name>', railway_upload),
    path('get-all', getAll, name='get all'),
    path('wh/', include('warehouse.urls', namespace='warehouse')),
    path('iso/', include('isochrone.urls', namespace='isochrone')),
    path('app/', include('application.urls', namespace='application')),
    path('rw/', include('railway.urls', namespace='railway')),
]
