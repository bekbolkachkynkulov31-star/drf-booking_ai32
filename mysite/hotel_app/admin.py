from django.contrib import admin
from .models import (UserProfile, Country, City, Service, Hotel,
                     ImageHotel, Room, ImageRoom, Review, BookingHotel)

class ImageHotelInline(admin.TabularInline):
    model = ImageHotel
    extra = 1

class ImageRoomInline(admin.TabularInline):
    model = ImageRoom
    extra = 1

class HotelAdmin(admin.ModelAdmin):
    inlines = [ImageHotelInline]

class RoomAdmin(admin.ModelAdmin):
    inlines = [ImageRoomInline]


admin.site.register(UserProfile)
admin.site.register(Country)
admin.site.register(City)
admin.site.register(Service)
admin.site.register(Hotel, HotelAdmin)
admin.site.register(Room, RoomAdmin)
admin.site.register(Review)
admin.site.register(BookingHotel)



