from rest_framework import serializers
from .models import (UserProfile, Country, City, Service, Hotel,
                     ImageHotel, Room, ImageRoom, Review, BookingHotel)
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['username', 'email', 'password', 'first_name', 'last_name', 'age',
                  'phone_number', 'role']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = UserProfile.objects.create_user(**validated_data)
        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Неверные учетные данные")

    def to_representation(self, instance):
        refresh = RefreshToken.for_user(instance)
        return {
            'user': {
                'username': instance.username,
                'email': instance.email,
            },
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }


class UserProfileSerializers(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['id', 'username']


class CountrySerializers(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = '__all__'


class CityListSerializers(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ['id', 'city_name']


class ServiceSerializers(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = '__all__'


class ImageHotelSerializers(serializers.ModelSerializer):
    class Meta:
        model = ImageHotel
        fields = ['id', 'image']


class ImageRoomSerializers(serializers.ModelSerializer):
    class Meta:
        model = ImageRoom
        fields = ['id', 'image']


class RoomSerializers(serializers.ModelSerializer):
    room_images = ImageRoomSerializers(read_only=True, many=True)
    class Meta:
        model = Room
        fields = ['id', 'room_image',  'room_images', 'room_number', 'room_type', 'price', 'created_at']


class ReviewSerializers(serializers.ModelSerializer):
    user = UserProfileSerializers()
    class Meta:
        model = Review
        fields = ['id', 'user', 'comment', 'stars', 'created_at']


class BookingHotelSerializers(serializers.ModelSerializer):
    class Meta:
        model = BookingHotel
        fields = '__all__'


class HotelListSerializers(serializers.ModelSerializer):
    country = CountrySerializers()
    city = CityListSerializers()
    get_avg_rating = serializers.SerializerMethodField
    get_count_rating = serializers.SerializerMethodField

    class Meta:
        model = Hotel
        fields = ['id', 'hotel_image', 'hotel_name', 'city', 'country', 'get_avg_rating', 'get_count_rating']

        def get_avg_rating(self, obj):
            return obj.get_avg_rating()

        def get_count_rating(self, obj):
            return obj.get_count_rating()


class HotelSimpleSerializers(serializers.ModelSerializer):
    country = CountrySerializers(read_only=True)

    class Meta:
        model = Hotel
        fields = ['id', 'hotel_image', 'hotel_name', 'country']


class CityDetailSerializers(serializers.ModelSerializer):
    city_hotels = HotelSimpleSerializers(read_only=True, many=True)

    class Meta:
        model = City
        fields = ['id', 'city_name', 'city_hotels']


class HotelDetailSerializers(serializers.ModelSerializer):
    country = CountrySerializers()
    city = CityListSerializers()
    images_hotel = ImageHotelSerializers(read_only=True, many=True)
    service = ServiceSerializers(many=True)
    rooms = RoomSerializers(read_only=True, many=True)
    reviews = ReviewSerializers(read_only=True, many=True)
    owner = UserProfileSerializers()
    get_avg_rating = serializers.SerializerMethodField
    get_count_rating = serializers.SerializerMethodField

    class Meta:
        model = Hotel
        fields = ['id', 'hotel_image', 'images_hotel', 'hotel_name', 'city', 'country',
                  'get_avg_rating', 'get_count_rating', 'description',
                    'owner', 'service', 'rooms', 'reviews']

        def get_avg_rating(self, obj):
            return obj.get_avg_rating()

        def get_count_rating(self, obj):
            return obj.get_count_rating()