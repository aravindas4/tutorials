from rest_framework import serializers
from bike_rental.models import Station, Rent

class StationSerializer(serializers.HyperlinkedModelSerializer):
    origin_for_rents = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='rent-detail')
    destination_for_rents = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='rent-detail')


    class Meta:
        model = Station
        fields = (
            'url',
            'pk',
            'name',
            'latitude',
            'longitude',
            'bike_available_quantity',
            'origin_for_rents',
            'destination_for_rents',)

    def validate(self, data):
        name = data.get('name', None)
        if name and Station.objects.filter(name=name).exists():
            raise serializers.ValidationError({"Station":"Name already exists.Please give different one."})
        # latitude = data.get('latitude', None)
        # longitude = data.get('longitude', None)
        # if latitude and longitude and Station.objects.filter(latitude=latitude, longitude=longitude).exists():
        #     raise serializers.ValidationError({"Station":"LL already exists.Please give different LLs."})
        return data

class RentSerializer(serializers.HyperlinkedModelSerializer):
    origin_station = serializers.SlugRelatedField(queryset=Station.objects.all(), slug_field='name')
    destination_station = serializers.SlugRelatedField(queryset=Station.objects.all(), slug_field='name')
    class Meta:
        model = Rent
        fields = (
            'url',
            'origin_station',
            'destination_station',
            'startdate',
            'enddate',
            'is_active',)
        read_only_fields = ('is_active',)

    # def create(self, validated_data):
    #     obj = Rent.objects.create(**validated_data)
    #     obj.save(is_active=True)
    #     return obj

    def validate(self, data):
        enddate = data.get('enddate', None)
        startdate = data.get('startdate', None)
        if enddate:
            data["is_active"] = False
            if startdate and startdate > enddate:
                raise serializers.ValidationError({"Rent":"Startdate is greater than Enddate."})
        return data
