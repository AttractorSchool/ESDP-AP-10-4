from django.contrib import admin

# Register your models here.
from .models import Booking, Passenger


class BookingAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'tour', 'booking_status')
    list_display_links = ['id']
    list_filter = ('tour', 'user')
    search_fields = ('tour', 'user')

    class Meta:
        verbose_name = 'Бронь'
        verbose_name_plural = 'Брони'


class PassengerAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'birthdate', 'booking')
    list_display_links = ['id']

    class Meta:
        verbose_name = 'Пассажир'
        verbose_name_plural = 'Пассажиры'


admin.site.register(Booking, BookingAdmin)
admin.site.register(Passenger, PassengerAdmin)
