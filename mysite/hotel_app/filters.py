from django_filters.rest_framework import FilterSet
from .models import Hotel, Room

class HotelFilter(FilterSet):
    class Meta:
        model = Hotel
        fields = {
            'country': ['exact'],
            'city': ['exact'],
            'service': ['exact']
        }


class RoomFilter(FilterSet):
    class Meta:
        model = Room
        fields = {
            'room_type': ['exact'],
            'price': ['gt', 'lt']
        }
