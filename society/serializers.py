from rest_framework import serializers
from .models import Society_creategroupmodel, Society_memberaddmodel

class SocietySerializer(serializers.ModelSerializer):
    class Meta:
        model = Society_creategroupmodel
        fields = '__all__'

class GroupmemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Society_memberaddmodel
        fields = '__all__'