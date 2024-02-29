from django.contrib import admin
from django.utils.html import mark_safe

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


class ExperienceInline(admin.StackedInline):
    model = models.Experience
    extra = 0

class SkillInline(admin.StackedInline):
    model = models.Skill
    extra = 0

class EducationInline(admin.StackedInline):
    model = models.Education
    extra = 0

class AchievementInline(admin.StackedInline):
    model = models.Achievement
    extra = 0

class LanguageInline(admin.StackedInline):
    model = models.Language
    extra = 0

@admin.register(models.Resume)
class ResumeAdmin(admin.ModelAdmin):
    list_display = ('user', 'employer', 'advertisement', 'fname', 'lname', 'date_sent')
    ordering = ('-user', '-date_sent')
    readonly_fields = ('image_tag',)
    inlines = [ExperienceInline, SkillInline, EducationInline, AchievementInline, LanguageInline]

    fieldsets = (
        (None, {
            'fields': ('user', 'employer', 'advertisement', 'fname', 'lname', 'image', 'image_tag')
        }),
        ('Other Information', {
            'fields': ('description', 'military_service', 'telephone', 'email', 'linkedin', 'github', 'website'),
        }),
    )

    def image_tag(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" style="max-width:200px;max-height:200px" />')
        else:
            return '-'

    image_tag.short_description = 'عکس رزومه'


# =================================================

@admin.register(models.Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = ('title', 'resume', 'company', 'start_date', 'end_date',)

# =================================================

@admin.register(models.ResumeFile)
class ResumeFileAdmin(admin.ModelAdmin):
    list_display = ('user', 'employer', 'advertisement', 'fname', 'lname', 'advertisement', 'date_sent')
    ordering = ('-user', '-date_sent')

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