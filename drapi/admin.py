from django.contrib import admin
from .models import AiQuest

# Register your models here.
@admin.register(AiQuest)
class AiQuestAdmin(admin.ModelAdmin):
    list_display=['id','teacher_name','course_name','course_duration','seat']