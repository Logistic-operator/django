import csv, io
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Railway, Neighborhood
from warehouse.models import batchCreateWF
from django.contrib.gis.geos import GEOSGeometry
from django.apps import apps

from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import (
    api_view, 
    permission_classes,
    renderer_classes,
    parser_classes,
    )
from rest_framework.exceptions import NotFound
from rest_framework.parsers import MultiPartParser, FormParser



def railway_upload(request, name):    
    template = "profile_upload.html"
    
    prompt = {
        'order': 'Order of the CSV should be ...', 
        }
    
    if request.method == "GET":
        return render(request, template, prompt)    
    
    csv_file = request.FILES['file']
    if not csv_file.name.endswith('.csv'):
        messages.error(request, 'THIS IS NOT A CSV FILE')
    names = ['rail','neib', 'wh']
    if name not in names:
        messages.error(request, 'URL not in [' + ','.join(names) + ']')
    if name == 'wh':
        batchCreateWF(csv_file)
        messages.success(request, 'Added batch create to temporal')
        return redirect('/admin/warehouse/warehouse/')
    data_set = csv_file.read().decode('UTF-8')
    io_string = io.StringIO(data_set)
    next(io_string)
    i = 1
    
    for column in csv.reader(io_string, delimiter='\t', quotechar="|"):
        print(name,' ', str(i))
        if name == 'rail':
            Railway.objects.update_or_create(
                iid=column[0],
                name=column[1],
                point=GEOSGeometry(column[2]),
                is_cont=column[4]
            )
        elif name == 'neib':
            Neighborhood.objects.update_or_create(
                source=Railway.objects.get(iid=int(column[0])),
                target=Railway.objects.get(iid=int(column[1])),
                length=column[2],
            )
        i += 1
        
    context = {}
    return render(request, template, context)