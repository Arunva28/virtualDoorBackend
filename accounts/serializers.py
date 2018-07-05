from rest_framework import serializers
from .models import AccountsModel


class AccountsSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccountsModel
        fields = '__all__'
