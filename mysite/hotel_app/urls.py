from django.urls import path, include
from rest_framework import routers
from .views import (UserProfileViewSet, CountryViewSet, ServiceViewSet,
                    HotelListViewSet, HotelDetailViewSet, ImageHotelViewSet, RoomViewSet, ImageRoomViewSet,
                    ReviewViewSet, BookingHotelViewSet, CityListViewSet, CityDetailViewSet,
                    RegisterView, CustomLoginView, LogoutView)

router = routers.DefaultRouter()

router.register(r'user_profile', UserProfileViewSet, basename='user_profile')
router.register(r'country', CountryViewSet, basename='country')
router.register(r'service', ServiceViewSet, basename='service')
router.register(r'image_hotel', ImageHotelViewSet, basename='image_hotel')
router.register(r'room', RoomViewSet, basename='room')
router.register(r'image_room', ImageRoomViewSet, basename='image_room')
router.register(r'review', ReviewViewSet, basename='review')
router.register(r'booking_hotel', BookingHotelViewSet, basename='booking_hotel')

urlpatterns = [
    path('', include(router.urls)),

    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout', LogoutView.as_view(), name='logout'),

    path('city/', CityListViewSet.as_view(), name='city'),
    path('city/<int:pk>/', CityDetailViewSet.as_view(), name='city_detail'),

    path('hotel/', HotelListViewSet.as_view(), name='hotel'),
    path('hotel/<int:pk>/', HotelDetailViewSet.as_view(), name='hotel_detail')
]
