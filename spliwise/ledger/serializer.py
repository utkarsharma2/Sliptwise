
from rest_framework import  serializers
from . import models

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = '__all__'

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Event
        fields = '__all__'


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Group
        fields = '__all__'
        depth = 1

class ContributionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Contributions
        fields = '__all__'
        depth = 1

class LedgerSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Ledger
        fields = '__all__'
        depth = 1