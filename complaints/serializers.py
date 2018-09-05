from rest_framework import serializers
from .models import TicketDescription, TicketList, TicketsName


class TicketListSerializer(serializers.ModelSerializer):
    class Meta:
        model = TicketList
        fields = '__all__'


class TicketDescriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TicketDescription
        fields = '__all__'


class TicketsNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = TicketsName
        fields = '__all__'