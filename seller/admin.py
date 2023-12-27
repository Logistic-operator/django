from django.contrib import admin
from .models import Seller
from django.contrib.gis.admin import GISModelAdmin
from django.contrib import messages


class SellerAdmin(GISModelAdmin):

    actions = ["create_isochrones_240"]

    @admin.action(description="Create [240m] isochrones")
    def create_isochrones_240(self, request, queryset):
        for seller in queryset:
            seller.createIsochrones([240])
            self.message_user(
                request,
                'created ' + str(seller.id) + ' isochrones [240]',
                messages.SUCCESS,
            )

admin.site.register(Seller, SellerAdmin)