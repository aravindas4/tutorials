from django.shortcuts import render
from rest_framework import viewsets
# Create your views here.
from bike_rental.models import Station, Rent
from bike_rental.serializers import StationSerializer, RentSerializer

class StationViewSet(viewsets.ModelViewSet):
    queryset = Station.objects.all()
    serializer_class = StationSerializer

class RentViewSet(viewsets.ModelViewSet):
    queryset = Rent.objects.all()
    serializer_class = RentSerializer
