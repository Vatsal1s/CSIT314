from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import CandidateProfile
from talentmatch.utils import fuzzy_check
from employers.models import JobPosting, JobApplication


def landing(request):
    return render(request, 'landing.html')


def candidate_signup(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        if User.objects.filter(email=email).exists():
            return render(request, 'candidates/signup.html', {'error': 'Email already registered'})
        user = User.objects.create_user(username=email, email=email, password=password)
        login(request, user)
        return redirect('candidate_dashboard')
    return render(request, 'candidates/signup.html')


def candidate_login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        try:
            user_obj = User.objects.get(email=email)
            user = authenticate(request, username=user_obj.username, password=password)
        except User.DoesNotExist:
            user = None
        if user and hasattr(user, 'candidateprofile'):
            login(request, user)
            return redirect('candidate_dashboard')
        return render(request, 'candidates/login.html', {'error': 'Invalid credentials'})
    return render(request, 'candidates/login.html')


def candidate_logout(request):
    logout(request)
    return redirect('landing')


def candidate_dashboard(request):
    if not request.user.is_authenticated:
        return redirect('candidate_login')
    if request.method == 'POST':
        p, created = CandidateProfile.objects.get_or_create(user=request.user)
        p.full_name = request.POST['full_name']
        p.phone = request.POST['phone']
        p.education = request.POST['education']
        p.major = request.POST['major']
        p.years_experience = request.POST['years_experience']
        p.work_experience = request.POST['work_experience']
        p.skills = request.POST['skills']
        p.location = request.POST['location']
        p.preferred_work_mode = request.POST['preferred_work_mode']
        p.preferred_location = request.POST['preferred_location']
        p.save()
        return redirect('candidate_dashboard')
    profile = CandidateProfile.objects.filter(user=request.user).first()
    applications = []
    if profile:
        applications = JobApplication.objects.filter(candidate=profile).select_related('job', 'job__employer').order_by('-applied_at')
    return render(request, 'candidates/dashboard.html', {'profile': profile, 'applications': applications})


def candidate_jobs(request):
    if not request.user.is_authenticated:
        return redirect('candidate_login')
    profile = CandidateProfile.objects.filter(user=request.user).first()
    if not profile:
        return redirect('candidate_dashboard')

    query = request.GET.get('q', '')
    location_filter = request.GET.get('location', '')
    job_type_filter = request.GET.get('job_type', '')
    work_mode_filter = request.GET.getlist('work_mode')
    salary_min = request.GET.get('salary_min', '0')
    exp_level = request.GET.get('exp_level', '')

    jobs = JobPosting.objects.all()

    if location_filter:
        jobs = jobs.filter(location__icontains=location_filter)
    if job_type_filter:
        jobs = jobs.filter(job_type=job_type_filter)
    if work_mode_filter:
        jobs = jobs.filter(work_mode__in=work_mode_filter)
    try:
        salary_min_int = int(salary_min)
    except ValueError:
        salary_min_int = 0
    if salary_min_int > 0:
        jobs = jobs.filter(salary_max__gte=salary_min_int)
    if exp_level == 'entry':
        jobs = jobs.filter(years_experience__lte=2)
    elif exp_level == 'mid':
        jobs = jobs.filter(years_experience__gte=3, years_experience__lte=5)
    elif exp_level == 'senior':
        jobs = jobs.filter(years_experience__gte=6)

    if query:
        matched_ids = []
        for job in jobs:
            text = f"{job.title} {job.description} {job.skills_required} {job.location} {job.get_work_mode_display()} {job.get_job_type_display()} {job.employer.company_name} {job.employer.company_info}"
            if fuzzy_check(query, text):
                matched_ids.append(job.id)
        jobs = jobs.filter(id__in=matched_ids)

    applied_ids = set(JobApplication.objects.filter(candidate=profile).values_list('job_id', flat=True))

    return render(request, 'candidates/jobs.html', {
        'jobs': jobs,
        'query': query,
        'location_filter': location_filter,
        'job_type_filter': job_type_filter,
        'work_mode_filter': work_mode_filter,
        'salary_min': salary_min,
        'exp_level': exp_level,
        'applied_ids': applied_ids,
    })


def candidate_recommendations(request):
    if not request.user.is_authenticated:
        return redirect('candidate_login')
    profile = CandidateProfile.objects.filter(user=request.user).first()
    if not profile:
        return redirect('candidate_dashboard')
    jobs = JobPosting.objects.all()
    results = []
    cand_skills = [s.strip().lower() for s in profile.skills.split(',')]
    edu_rank = {'high_school': 1, 'associate': 2, 'bachelor': 3, 'master': 4, 'phd': 5}
    cand_level = edu_rank.get(profile.education, 0)

    for job in jobs:
        score = 0
        job_skills = [s.strip().lower() for s in job.skills_required.split(',')]
        skill_matches = len(set(cand_skills) & set(job_skills))
        if job_skills:
            score += round((skill_matches / len(job_skills)) * 25)

        job_level = edu_rank.get(job.education_required, 0)
        if cand_level >= job_level:
            score += 20

        exp_gap = abs(profile.years_experience - job.years_experience)
        if exp_gap == 0:
            score += 20
        elif exp_gap <= 2:
            score += 12
        elif exp_gap <= 4:
            score += 5

        if profile.location.lower() == job.location.lower():
            score += 15

        if profile.preferred_work_mode and profile.preferred_work_mode == job.work_mode:
            score += 10

        if profile.preferred_location and profile.preferred_location.lower() == job.location.lower():
            score += 10

        results.append((score, job))

    results.sort(key=lambda x: x[0], reverse=True)

    if profile.is_member:
        top_jobs = [{'job': j, 'score': s} for s, j in results]
    else:
        top_jobs = [{'job': j, 'score': s} for s, j in results[:10]]

    applied_ids = set(JobApplication.objects.filter(candidate=profile).values_list('job_id', flat=True))

    return render(request, 'candidates/recommendations.html', {
        'recommendations': top_jobs,
        'is_member': profile.is_member,
        'applied_ids': applied_ids,
    })


def membership_page(request):
    if not request.user.is_authenticated:
        return redirect('candidate_login')
    profile = CandidateProfile.objects.filter(user=request.user).first()
    return render(request, 'candidates/membership.html', {'profile': profile})


def upgrade_membership(request):
    if not request.user.is_authenticated:
        return redirect('candidate_login')
    if request.method == 'POST':
        p = CandidateProfile.objects.filter(user=request.user).first()
        if p:
            p.is_member = True
            p.save()
    return redirect('candidate_membership')


def apply_to_job(request, job_id):
    if not request.user.is_authenticated:
        return redirect('candidate_login')
    if request.method == 'POST':
        profile = CandidateProfile.objects.filter(user=request.user).first()
        if not profile:
            return redirect('candidate_dashboard')
        try:
            job = JobPosting.objects.get(id=job_id)
            JobApplication.objects.get_or_create(candidate=profile, job=job)
        except JobPosting.DoesNotExist:
            pass
    next_page = request.POST.get('next', 'candidate_jobs')
    return redirect(next_page)
