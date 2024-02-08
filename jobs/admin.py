from django.contrib import admin
from . import models


@admin.register(models.JobAdvertising)
class JobAdvertisingAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')

# =================================================

@admin.register(models.CooperationType)
class CooperationTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'type',)

# =================================================

@admin.register(models.JobGroup)
class JobGroupAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)

# =================================================

@admin.register(models.StudyField)
class StudyFieldAdmin(admin.ModelAdmin):
    list_display = ('id', 'field',)

# =================================================

@admin.register(models.StudyGrade)
class StudyGradeAdmin(admin.ModelAdmin):
    list_display = ('id', 'grade',)