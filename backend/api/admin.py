from django.contrib import admin
from .models import Submission
# Register your models here.

@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ('fileName', 'task', 'uploaded_at', 'user', 'display_score')
    search_fields = ('fileName', 'task', 'user__username')  # Fields to search
    list_filter = ('task', 'uploaded_at', 'user')  # Filters to use in the admin panel

    def display_score(self, obj):
        return obj.score  # Display the score JSON
    display_score.short_description = "Score"