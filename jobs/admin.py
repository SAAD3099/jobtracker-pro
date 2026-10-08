from django.contrib import admin
from .models import JobApplication
@admin.register(JobApplication)
class ApplicationAdmin(admin.ModelAdmin):
    list_display=['company','role','user','status','applied_date']
    list_filter=['status']
    search_fields=['company','role']
