from django.contrib import admin

from .models import Tour, TourRating


class TourAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'moderation_status', 'start_date', 'end_date')
    list_display_links = ['id']
    list_filter = ('moderation_status', 'author', 'start_date', 'end_date')
    search_fields = ('author', 'title', 'moderation_status')
    list_editable = ('title', 'moderation_status')

    class Meta:
        verbose_name = 'Тур'
        verbose_name_plural = 'Туры'


class TourRatingAdmin(admin.ModelAdmin):
    list_display = ('id', 'tourist', 'tour', 'correspondence', 'professionalism')
    list_display_links = ['id']
    list_filter = ('tour', 'tourist')
    search_fields = ('tour', 'tourist')

    class Meta:
        verbose_name = 'Рейтинг'
        verbose_name_plural = 'Рейтинги'


admin.site.register(Tour, TourAdmin)
admin.site.register(TourRating, TourRatingAdmin)
