from rest_framework import serializers
from .models import Pet


class PetBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pet
        fields = '__all__'
        read_only_fields = ("created_at", "updated_at")
