from rest_framework import serializers
from .models import PollingUnit, AnnouncedPuResults,Lga

class LgaSerializer(serializers.ModelSerializer):
    class Meta:
        model=Lga
        fields='__all__'

class PollingUnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = PollingUnit
        fields = '__all__'

class AnnouncedPuResultsSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnnouncedPuResults
        fields = '__all__'