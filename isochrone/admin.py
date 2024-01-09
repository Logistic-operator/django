from django.contrib import admin
from .models import Isochrone
from django.contrib.gis.admin import GISModelAdmin, TabularInline, action
from django.contrib import messages

class IsochroneAdmin(GISModelAdmin):
    actions = ["cascade_delete", 'getRailways']
    exclude = ()
    

    @admin.action(description="Cascade delete")
    def cascade_delete(self, request, queryset):
        for iso in queryset:
            iso.delete()
        self.message_user(
            request,
            'deleted',
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