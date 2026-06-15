from rest_framework import viewsets, filters, generics, status, permissions
from .models import (UserProfile, Country, City, Service, Hotel,
                     ImageHotel, Room, ImageRoom, Review, BookingHotel)
from .serializers import (UserProfileSerializers, CountrySerializers, CityListSerializers,
                          CityDetailSerializers, ServiceSerializers, HotelListSerializers, HotelDetailSerializers,
                          ImageHotelSerializers, RoomSerializers, ImageRoomSerializers,
                          ReviewSerializers, BookingHotelSerializers, RegisterSerializer, LoginSerializer)
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from .permission import CheckRole, CheckOwner
from .filters import HotelFilter, RoomFilter
from .pagination import HotelPagination, RoomPagination

from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken

class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CustomLoginView(TokenObtainPairView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except Exception:
            return Response({"detail": "Неверные учетные данные"}, status=status.HTTP_401_UNAUTHORIZED)

        user = serializer.validated_data
        return Response(serializer.data, status=status.HTTP_200_OK)


class LogoutView(generics.GenericAPIView):
    def post(self, request, *args, **kwargs):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializers
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class CountryViewSet(viewsets.ModelViewSet):
    queryset = Country.objects.all()
    serializer_class = CountrySerializers
    filter_backends = [filters.SearchFilter]
    search_fields = ['country_name']
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class CityListViewSet(generics.ListAPIView):
    queryset = City.objects.all()
    serializer_class = CityListSerializers
    filter_backends = [filters.SearchFilter]
    search_fields = ['city_name']
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class CityDetailViewSet(generics.RetrieveAPIView):
    queryset = City.objects.all()
    serializer_class = CityDetailSerializers
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class ServiceViewSet(viewsets.ModelViewSet):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializers
    filter_backends = [filters.SearchFilter]
    search_fields = ['service_name']
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class HotelListViewSet(generics.ListCreateAPIView):
    queryset = Hotel.objects.all()
    serializer_class = HotelListSerializers
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ['hotel_name', 'city']
    filterset_class = HotelFilter
    pagination_class = HotelPagination
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, CheckRole]


class HotelDetailViewSet(generics.RetrieveUpdateDestroyAPIView):
    queryset = Hotel.objects.all()
    serializer_class = HotelDetailSerializers
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, CheckOwner]



class ImageHotelViewSet(viewsets.ModelViewSet):
    queryset = ImageHotel.objects.all()
    serializer_class = ImageHotelSerializers
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializers
    filter_backends = [OrderingFilter, DjangoFilterBackend]
    ordering_fields = ['created_at']
    filterset_class = RoomFilter
    pagination_class = RoomPagination
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class ImageRoomViewSet(viewsets.ModelViewSet):
    queryset = ImageRoom.objects.all()
    serializer_class = ImageRoomSerializers
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializers
    filter_backends = [OrderingFilter]
    ordering_fields = ['created_at']
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class BookingHotelViewSet(viewsets.ModelViewSet):
    queryset = BookingHotel.objects.all()
    serializer_class = BookingHotelSerializers
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


