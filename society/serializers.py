from rest_framework import serializers
from .models import SocietyModel

class SocietySerializer(serializers.ModelSerializer):
    class Meta:
        model = SocietyModel
        fields = '__all__'