# shelf_shape_app/serializers.py
from rest_framework import serializers
from .models import ShelfLayout

class ShelfLayoutSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShelfLayout
        fields = '__all__'
