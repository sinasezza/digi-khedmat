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
    list_display = ('id', 'name', 'job_advertising')

# =================================================

@admin.register(models.StudyField)
class StudyFieldAdmin(admin.ModelAdmin):
    list_display = ('id', 'field', 'job_advertising')

# =================================================

@admin.register(models.StudyGrade)
class StudyGradeAdmin(admin.ModelAdmin):
    list_display = ('id', 'grade',)

# =================================================

@admin.register(models.Resume)
class ResumeAdmin(admin.ModelAdmin):
    list_display = ('id', 'full_name', 'title')

# =================================================

@admin.register(models.Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = ('title', 'resume', 'company', 'start_date', 'end_date',)

# =================================================

@admin.register(models.ResumeFile)
class ResumeFileAdmin(admin.ModelAdmin):
    list_display = ('user', 'fname', 'lname', 'advertisement', 'date_sent')

# =================================================

@admin.register(models.Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ('title', 'resume',)

# =================================================

@admin.register(models.Education)
class EducationAdmin(admin.ModelAdmin):
    list_display = ('title', 'resume',)

# =================================================

@admin.register(models.Achievement)
class AchivementAdmin(admin.ModelAdmin):
    list_display = ('title', 'resume')

# =================================================

@admin.register(models.Language)
class LanguageAdmin(admin.ModelAdmin):
    list_display = ('name','resume', 'level',)