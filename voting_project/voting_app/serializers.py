from rest_framework import serializers
from .models import PollingUnit, AnnouncedPuResults,Lga

class MyPollingUnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = PollingUnit
        fields = ['id','polling_unit_id', 'ward_id', 'lga_id', 'uniquewardid', 'polling_unit_number', 'polling_unit_name', 'polling_unit_description', 'lat', 'long', 'entered_by_user', 'user_ip_address']


class AnnouncedPuResultsSerializerFormCreation(serializers.Serializer):
    polling_unit_uniqueid = serializers.CharField(max_length=50)
    results = serializers.ListField(
        child=serializers.DictField(
            child=serializers.IntegerField()
        )
    )
    entered_by_user = serializers.CharField(max_length=50)
    user_ip_address = serializers.CharField(max_length=50)

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