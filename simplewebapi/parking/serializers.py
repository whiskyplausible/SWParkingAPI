from rest_framework import serializers
from parking.models import CarParks

class CarParkSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CarParks
        fields = ('carpark_id', 'name', 'location', 'address', 'postcode', 'location', 'spaces', 'min_cost_pence', 'features', 'operator')


