from django.contrib import admin

from .models import CustomUser, Profile
from .utils import create_profile


# Register your models here.
@admin.register(CustomUser)
class CustomAdmin(admin.ModelAdmin):

    def save_model(self, request, obj, form, change):
        create_profile(form)
        super().save_model(request, obj, form, change)


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'is_guide', 'verification_status', 'current_location')
    list_display_links = ['id']
    list_filter = ('user', 'is_guide', 'verification_status', 'current_location')
    search_fields = ('id', 'user', 'is_guide', 'verification_status')
    list_editable = ('is_guide', 'verification_status', 'current_location')

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'


admin.site.register(Profile, ProfileAdmin)
