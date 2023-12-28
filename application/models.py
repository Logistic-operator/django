from django.db import models

class Application(models.Model):
    applicant = models.ForeignKey('warehouse.Warehouse', on_delete=models.SET_NULL, null=True)
    app_type = models.CharField() # sell, buy
    product = models.CharField()
    volume = models.FloatField()
    