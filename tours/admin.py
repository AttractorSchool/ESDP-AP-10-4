from django.contrib import admin

from .models import Tour


class TourAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'moderation_status', 'start_date', 'end_date')
    list_display_links = ['id']
    list_filter = ('moderation_status', 'author', 'start_date', 'end_date')
    search_fields = ('author', 'title', 'moderation_status')
    list_editable = ('title', 'moderation_status')

    class Meta:
        verbose_name = 'Тур'
        verbose_name_plural = 'Туры'


admin.site.register(Tour, TourAdmin)
