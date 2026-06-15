from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.core.validators import MaxValueValidator, MinValueValidator

USER_ROLE = (
('owner', 'owner'),
('client', 'client')
)

class UserProfile(AbstractUser):
    age = models.PositiveSmallIntegerField(default=0, validators=[MinValueValidator(16), MaxValueValidator(75)])
    phone_number = PhoneNumberField(region='KG', default='+996')
    profile_image = models.ImageField(upload_to='profile_image/', null=True, blank=True)
    role = models.CharField(max_length=6, choices=USER_ROLE, default='client')


class Country(models.Model):
    country_name = models.CharField(max_length=32, unique=True)

    def __str__(self):
        return self.country_name


class City(models.Model):
    city_name = models.CharField(max_length=32)

    def __str__(self):
        return self.city_name


class Service(models.Model):
    service_icon = models.ImageField(upload_to='service_icon/')
    service_name = models.CharField(max_length=32, unique=True)

    def __str__(self):
        return self.service_name


class Hotel(models.Model):
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='city_hotels')
    hotel_name = models.CharField(max_length=32)
    hotel_image = models.ImageField(upload_to='hotel_images/')
    description = models.TextField()
    service = models.ManyToManyField(Service)
    owner = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

    def __str__(self):
        return self.hotel_name

    def get_avg_rating(self):
        reviews = self.reviews.all()
        if reviews.exists():
            return sum([i.stars for i in reviews]) / reviews.count()
        return 0

    def get_count_rating(self):
        reviews = self.reviews.all()
        if reviews.exists():
            return reviews.count()
        return 0




class ImageHotel(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='images_hotel')
    image = models.ImageField(upload_to='images_hotel/')


class Room(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='rooms')
    room_number = models.PositiveSmallIntegerField(default=0)
    room_image = models.ImageField(upload_to='room_images/')
    ROOM_TYPE = (
    ('Одноместный', 'Одноместный'),
    ('Двухместный', 'Двухместный'),
    ('Семейный', 'Семейный'),
    ('Люкс', 'Люкс')
    )
    room_type = models.CharField(max_length=15, choices=ROOM_TYPE)
    ROOM_STATUS = (
    ('Свободень', 'Свободень'),
    ('Забронировать', 'Забронировать')
    )
    room_status = models.CharField(max_length=15, choices=ROOM_STATUS, default='Свободень')
    price = models.PositiveSmallIntegerField(default=0)
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'Hotel: {self.hotel}: Room: {self.room_number}'

class ImageRoom(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='room_images')
    image = models.ImageField(upload_to='images_room/')


class Review(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='reviews')
    comment = models.TextField(null=True, blank=True)
    stars = models.PositiveSmallIntegerField(choices=[(i, str(i))for i in range(1, 11)], null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user}: {self.hotel}'


class BookingHotel(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    check_in = models.DateField()
    check_out = models.DateField()
    grow_up = models.PositiveSmallIntegerField(default=0)
    children = models.PositiveSmallIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user}: hotel: {self.hotel}'







