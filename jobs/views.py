import uuid
from django.db.models import Q
from django.db.models.query import QuerySet
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect, HttpResponseBadRequest, FileResponse
from django.forms import modelformset_factory

from generics import models as generics_models
from . import models, forms, decorators


# ************************************** JOB ADVERTISING VIEWS **************************************

@decorators.log_before_after
def job_list_view(request):
    jobs = models.JobAdvertising.objects.filter(status='published')
        
    # response to search job
    search_input = request.GET.get('search-area') or ''
    if search_input:
        jobs = jobs.filter(
            Q(title__icontains=search_input) | 
            Q(summary__icontains=search_input) | 
            Q(description__icontains=search_input) |
            Q(cooperation_types__type__icontains=search_input) | 
            Q(study_grade__grade__icontains=search_input) |  
            Q(gender__icontains=search_input) |  
            Q(categories__title__icontains=search_input) |  
            Q(tags__name__icontains=search_input) |  
            Q(region__state__icontains=search_input) |  
            Q(region__city__icontains=search_input)   
        ).distinct()
    
    # Pagination
    paginated = Paginator(jobs, 6) 
    page_number = request.GET.get("page")  
    paginated_jobs = paginated.get_page(page_number)
        
    context = {
        'jobs': paginated_jobs,
        'search_input': search_input,
    }
    return render(request, 'jobs/job-list.html', context)

# ---------------------------------------------------------

@decorators.log_before_after
def job_detail_view(request: HttpRequest, job_slug: str):
    job = get_object_or_404(models.JobAdvertising, slug=job_slug, status='published')    
    job.increment_views()
    
    # check if user added this advertising to his favorites
    try:
        favorite = request.user.favorites.get(object_id=job.id) 
    except:
        favorite = None
    
    resume_form = forms.ResumeForm()
    resume_file_form = forms.ResumeFileForm()
        
    context = {
        'job': job,
        'favorite': favorite,
        'resume_form': resume_form,
        'resume_file_form': resume_file_form,
    }
    return render (request, 'jobs/job-detail.html', context)

    
# ---------------------------------------------------------

@login_required(login_url='accounts:login')
def job_create_view(request: HttpRequest) -> HttpResponse:
    """View to create a new ad."""
    # If the request is not from POST method then display blank form
    if request.method == 'POST':
        form = forms.JobAdvertisingForm(request.POST)
        
        if form.is_valid():
            new_job = form.save(commit=False)
            new_job.owner = request.user
            new_job.save()
            
            # update cooperation types
            types = request.POST.getlist('cooperation_types')
            new_job.update_cooperation_types(types)
            
            # update tags
            tags = request.POST.getlist('tags')
            new_job.update_tags(tags)

            # update categories
            cats = request.POST.getlist('categories')
            new_job.update_categories(cats)
            
            messages.success(request, "آگهی شما با موفقیت ایجاد شد.")
            return redirect('accounts:user-panel')
        else:
            print(f"error : {form.errors.as_data()}")
            messages.warning(request, "لطفا فرم را به طور صحیح پر کنید.")
            form = forms.JobAdvertisingForm(request.POST)
    else:
        form = forms.JobAdvertisingForm()
        
    
    categories = generics_models.JobCategory.objects.all()
    tags = generics_models.Tag.objects.all()
    regions = generics_models.Region.objects.all()
    study_grades = models.StudyGrade.objects.all()
    cooperation_types = models.CooperationType.objects.all()
    
        
    context = {
        'form': form,
        'categories': categories,
        'tags': tags,
        'regions': regions,
        'study_grades': study_grades,
        'cooperation_types': cooperation_types,
    }        
    
    return render(request, 'jobs/job-create.html', context)

# ---------------------------------------------------------

@login_required(login_url='accounts:login')
@decorators.owner_required
def job_update_view(request: HttpRequest, job_slug: str):
    job = get_object_or_404(models.JobAdvertising, slug=job_slug)
    
    if request.method == "POST":
        form = forms.JobAdvertisingForm(request.POST, request.FILES, instance=job)
        if form.is_valid():
            updated_job = form.save()
            
            # update cooperation types
            types = request.POST.getlist('cooperation_types')
            updated_job.update_cooperation_types(types)
            
            # update tags and categories
            tags = request.POST.getlist('tags')
            updated_job.update_tags(tags)

            # update categories
            cats = request.POST.getlist('categories')
            updated_job.update_categories(cats)
            
            messages.info(request, "آگهی شما بروز رسانی شد.")
            return redirect('accounts:user-panel')
        else:
            # print(f"error : {form.errors.as_data()}")
            messages.warning(request, "لطفا فرم را به طور صحیح پر کنید.")
            form = forms.JobAdvertisingForm(request.POST, instance=job)
    else:
        form = forms.JobAdvertisingForm(instance=job) 
    
    categories = generics_models.JobCategory.objects.all()
    tags = generics_models.Tag.objects.all()
    regions = generics_models.Region.objects.all()
    study_grades = models.StudyGrade.objects.all()
    cooperation_types = models.CooperationType.objects.all()
    
        
    context = {
        'job': job,
        'form': form,
        'categories': categories,
        'tags': tags,
        'regions': regions,
        'study_grades': study_grades,
        'cooperation_types': cooperation_types,
    }        
    
    return render(request, 'jobs/job-update.html', context)

# ---------------------------------------------------------

@login_required(login_url='accounts:login')
@decorators.owner_required
def job_delete_view(request: HttpRequest, job_id: str, job_slug: str):
    job = get_object_or_404(models.JobAdvertising, slug=job_slug)
    
    if request.method == "POST":
        job.delete()
        messages.success(request, f"{job} has been deleted.")
        return reverse_lazy("jobs:job-list")
    
# ---------------------------------------------------------


# ************************************** RESUME VIEWS **************************************


@login_required(login_url="accounts:login")
def resume_list_view(request: HttpRequest) -> HttpResponse:
    resumes = request.user.rcv_resumes.all()
    resume_files = request.user.rcv_resume_files.all()
    
    print(f"resume files is {resume_files}")
    
    context = {
        'resumes': resumes,
        'resume_files': resume_files,
    }
    return render(request, 'jobs/resumes/resume-list.html', context)

# ---------------------------------------------------------

@login_required
@decorators.resume_connection_required
def resume_file_detail_view(request: HttpRequest, id: str) -> HttpResponse:
    resume = get_object_or_404(models.ResumeFile, id=id)
        
    context = {
        'resume': resume,
    }
        
    return  render(request, 'jobs/resumes/resume-file-detail.html', context)

# ---------------------------------------------------------

@login_required
@decorators.resume_connection_required
def pdf_preview_view(request, id):
    resume = get_object_or_404(models.ResumeFile, id=id)
    return FileResponse(open(f'{resume.pdf_file.path}', 'rb'), content_type='application/pdf')

# ---------------------------------------------------------

@login_required
@decorators.resume_connection_required
def resume_detail_view(request : HttpRequest, id: str):
    resume = get_object_or_404(models.Resume, id=id)
    
    context = {
        'resume': resume,
    }
    
    return  render(request, 'jobs/resumes/resume-detail.html', context)

# ---------------------------------------------------------

@login_required(login_url="accounts:login")
@require_POST
def  resume_file_create_view(request: HttpRequest, job_slug: str) -> HttpResponseRedirect:
    job_advertising = get_object_or_404(models.JobAdvertising, slug=job_slug)
    
    form = forms.ResumeFileForm(data=request.POST or None, files=request.FILES or None)
    
    if form.is_valid():
        resume = form.save(commit=False)
        resume.user = request.user
        resume.advertisement = job_advertising
        resume.employer = job_advertising.owner
        resume.save()
        
        messages.success(request, f"رزومه شما برای {resume.employer.username} ارسال شد.")
        return redirect('jobs:job-detail', job_slug=job_slug)
        
    else:
        print(f"error : {form.errors.as_data()}")
        messages.error(request, "خطایی پیش آمده لطفا دوباره تلاش کنید")
        return redirect('jobs:job-detail', job_slug=job_slug)

# ---------------------------------------------------------

@login_required(login_url="accounts:login")
@require_POST
def resume_create_view(request: HttpRequest, job_slug: str) -> HttpResponseRedirect:
    job_advertising = get_object_or_404(models.JobAdvertising, slug=job_slug)
    form = forms.ResumeForm(data=request.POST or None, files=request.FILES or None)
    
    print(f"request files is {request.FILES}/n")

    if form.is_valid():
        resume = form.save(commit=False)
        resume.user = request.user
        resume.advertisement = job_advertising
        resume.employer = job_advertising.owner
        resume.save()
        
        return redirect(resume.get_complete_url())
    
    else:
        print(f"error : {form.errors.as_data()}")
        messages.error(request, "خطایی پیش آمده لطفا دوباره تلاش کنید")
        return redirect('jobs:job-detail', job_slug=job_slug)

# ---------------------------------------------------------

@login_required(login_url="accounts:login")
@decorators.resume_owner_required
def resume_complete_view(request, resume_id):
    resume = get_object_or_404(models.Resume, id=resume_id)
    
    # Create formsets for related models
    ExperienceFormSet = modelformset_factory(models.Experience, form=forms.ExperienceForm, extra=1)
    SkillFormSet = modelformset_factory(models.Skill, form=forms.SkillForm, extra=1)
    EducationFormSet = modelformset_factory(models.Education, form=forms.EducationForm, extra=1)
    AchievementFormSet = modelformset_factory(models.Achievement, form=forms.AchievementForm, extra=1)
    LanguageFormSet = modelformset_factory(models.Language, form=forms.LanguageForm, extra=1)

    if request.method == 'POST':
        resume_form = forms.ResumeForm(data=request.POST, files=request.FILES, instance=resume)
        # Save formsets if they are valid
        experience_formset = ExperienceFormSet(request.POST, prefix='experience', queryset=models.Experience.objects.none())
        skill_formset = SkillFormSet(request.POST, prefix='skill', queryset=models.Skill.objects.none())
        education_formset = EducationFormSet(request.POST, prefix='education', queryset=models.Education.objects.none())
        achievement_formset = AchievementFormSet(request.POST, prefix='achievement', queryset=models.Achievement.objects.none())
        language_formset = LanguageFormSet(request.POST, prefix='language', queryset=models.Language.objects.none())

        if (resume_form.is_valid() and
            experience_formset.is_valid() and
            skill_formset.is_valid() and
            education_formset.is_valid() and
            achievement_formset.is_valid() and
            language_formset.is_valid()):
            
            updated_resume = resume_form.save()
            
            # Save formsets with the main form instance
            for form in experience_formset:
                new_exp = form.save(commit=False)
                new_exp.resume = updated_resume
                new_exp.save()

            for form in skill_formset:
                new_skill = form.save(commit=False)
                new_skill.resume = updated_resume
                new_skill.save()

            for form in education_formset:
                new_edu = form.save(commit=False)
                new_edu.resume = updated_resume
                new_edu.save()

            for form in achievement_formset:
                new_ach = form.save(commit=False)
                new_ach.resume = updated_resume
                new_ach.save()

            for form in language_formset:
                new_lang = form.save(commit=False)
                new_lang.resume = updated_resume
                new_lang.save()

            updated_resume.send()
            messages.success(request, f"رزومه شما برای {resume.employer.username} ارسال شد.")
            return redirect(resume.advertisement.get_absolute_url())
        else:
            messages.error(request, "An error occurred while processing formsets.")
    else:
        resume_form = forms.ResumeForm(instance=resume)
        # Initialize formsets with queryset filtered by the current resume instance
        experience_formset = ExperienceFormSet(prefix='experience', queryset=resume.experiences.all())
        skill_formset = SkillFormSet(prefix='skill', queryset=resume.skills.all())
        education_formset = EducationFormSet(prefix='education', queryset=resume.educations.all())
        achievement_formset = AchievementFormSet(prefix='achievement', queryset=resume.achievements.all())
        language_formset = LanguageFormSet(prefix='language', queryset=resume.languages.all())

    context = {
        'resume': resume,
        'resume_form': resume_form,
        'experience_formset': experience_formset,
        'skill_formset': skill_formset,
        'education_formset': education_formset,
        'achievement_formset': achievement_formset,
        'language_formset': language_formset,
    }
    return render(request, 'jobs/resumes/resume-create-complete.html', context)

# ---------------------------------------------------------
