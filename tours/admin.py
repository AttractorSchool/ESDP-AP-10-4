# from django.contrib import admin
#
# from .models import Tour
#
#
# class TourAdmin(admin.ModelAdmin):
#     list_display = ('id', 'author', 'title', 'moderation_status', 'price', 'start_date', 'end_date')
#     list_display_links = ['id']
#     list_filter = ('moderation_status', 'author', 'start_date', 'end_date')
#     search_fields = ('author', 'title', 'moderation_status')
#     list_editable = ('title', 'moderation_status', 'price', 'start_date', 'end_date')
#
#     class Meta:
#         verbose_name = 'Тур'
#         verbose_name_plural = 'Туры'
#
#
# admin.site.register(Tour, TourAdmin)
