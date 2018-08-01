from rest_framework import serializers
from .models import AccountsModel, Description


class AccountsSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccountsModel
        fields = '__all__'


class AccountsDescriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Description
        fields = '__all__'


class AccountsExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccountsModel
        fields = ('Amount',)