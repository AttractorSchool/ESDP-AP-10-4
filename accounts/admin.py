from choices import ProfileStatusChoice
from django.contrib import admin
from django.contrib.auth import get_user_model

from .models import GuideProfile, User
from .utils import create_profile, create_user


ALLOWED_TO_EDIT = [
    ProfileStatusChoice.NOT_VERIFIED,
    ProfileStatusChoice.SENT_TO_REWORK,
    ProfileStatusChoice.SENT_TO_VERIFICATION,
    ProfileStatusChoice.REFUSED,
]


# Register your models here.
@admin.register(User)
class CustomAdmin(admin.ModelAdmin):
    exclude = ('is_guide', 'is_tourist', 'password')

    def save_model(self, request, obj, form, change):
        if get_user_model().objects.filter(pk=obj.pk):
            return obj.save()
        user = create_user(form)
        create_profile(user)
        super().save_model(request, obj, form, change)


@admin.register(GuideProfile)
class GuideProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'verification_status')
    list_display_links = ['id']
    list_filter = ('user', 'verification_status', 'current_location')
    search_fields = ('id', 'user', 'verification_status')

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            if obj and obj.verification_status in ALLOWED_TO_EDIT:
                return True
        return super().has_change_permission(request, obj)

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = super().get_readonly_fields(request, obj)

        if request.user.is_superuser:
            if obj and obj.verification_status == ProfileStatusChoice.CONFIRMED:
                readonly_fields += ('verification_status',)

        return readonly_fields

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'
