from django.contrib import admin

from .models import Choice, Genre, Poll, Vote


@admin.register(Poll)
class PollAdmin(admin.ModelAdmin):
    list_display = ["text", "owner", "pub_date", "active"]
    search_fields = ["text", "owner__username"]
    list_filter = ["active"]
    date_hierarchy = "pub_date"


@admin.register(Choice)
class ChoiceAdmin(admin.ModelAdmin):
    list_display = ["choice_text", "poll"]
    search_fields = ["choice_text", "poll__text"]
    autocomplete_fields = ["poll"]


@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = ["choice", "poll", "user"]
    search_fields = ["choice__choice_text", "poll__text", "user__username"]
    autocomplete_fields = ["choice", "poll", "user"]


from mptt.admin import MPTTModelAdmin
from polls.models import Genre, SampleData, SampleDataMptt

admin.site.register(SampleData)
admin.site.register(Genre, MPTTModelAdmin)
admin.site.register(SampleDataMptt, MPTTModelAdmin)
