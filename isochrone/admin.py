from django.contrib import admin
from .models import Isochrone
from django.contrib.gis.admin import GISModelAdmin, TabularInline, action
from django.contrib import messages

class IsochroneAdmin(GISModelAdmin):
    actions = ["test1", 'getRailways']
    exclude = ('railways', 'geom')
    

    @action(description="test1")
    def test1(self, request, queryset):
        queryset[0].test()
        self.message_user(
                request,
                'test ',
                messages.SUCCESS,
            )
        
    @action(description="Get Railways")
    def getRailways(self, request, queryset):
        for obj in queryset:
            obj.getRailways()
            self.message_user(
                    request,
                    'Railways geted',
                    messages.SUCCESS,
                )


admin.site.register(Isochrone, IsochroneAdmin)