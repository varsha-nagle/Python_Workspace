# shelf_shape_app/models.py
from django.db import models

class ShelfLayout(models.Model):
    layout = models.JSONField()
