from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import EmployerProfile, JobPosting, JobApplication
from talentmatch.utils import fuzzy_check
from candidates.models import CandidateProfile


def employer_signup(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        company_name = request.POST['company_name']
        company_info = request.POST['company_info']
        if User.objects.filter(email=email).exists():
            return render(request, 'employers/signup.html', {'error': 'Email already registered'})
        user = User.objects.create_user(username=email, email=email, password=password)
        EmployerProfile.objects.create(user=user, company_name=company_name, company_info=company_info)
        login(request, user)
        return redirect('employer_dashboard')
    return render(request, 'employers/signup.html')


def employer_login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        try:
            user_obj = User.objects.get(email=email)
            user = authenticate(request, username=user_obj.username, password=password)
        except User.DoesNotExist:
            user = None
        if user and hasattr(user, 'employerprofile'):
            login(request, user)
            return redirect('employer_dashboard')
        return render(request, 'employers/login.html', {'error': 'Invalid credentials'})
    return render(request, 'employers/login.html')


def employer_logout(request):
    logout(request)
    return redirect('landing')


def employer_dashboard(request):
    if not request.user.is_authenticated:
        return redirect('employer_login')
    jobs = JobPosting.objects.filter(employer__user=request.user)
    employer = request.user.employerprofile
    return render(request, 'employers/dashboard.html', {'jobs': jobs, 'employer': employer})


def post_job(request):
    if not request.user.is_authenticated:
        return redirect('employer_login')
    if request.method == 'POST':
        employer = request.user.employerprofile
        JobPosting.objects.create(
            employer=employer,
            title=request.POST['title'],
            description=request.POST['description'],
            education_required=request.POST['education_required'],
            skills_required=request.POST['skills_required'],
            years_experience=request.POST['years_experience'],
            work_mode=request.POST['work_mode'],
            location=request.POST['location'],
            job_type=request.POST['job_type'],
            salary_min=request.POST['salary_min'],
            salary_max=request.POST['salary_max'],
        )
        return redirect('employer_dashboard')
    return render(request, 'employers/post_job.html')


def recommendations_list(request):
    if not request.user.is_authenticated:
        return redirect('employer_login')
    jobs = JobPosting.objects.filter(employer__user=request.user)
    return render(request, 'employers/recommendations_list.html', {'jobs': jobs})


def view_candidates(request):
    if not request.user.is_authenticated:
        return redirect('employer_login')

    candidates = CandidateProfile.objects.all()
    query = request.GET.get('q', '')
    education_filter = request.GET.get('education', '')
    experience_filter = request.GET.get('experience', '')
    work_mode_filter = request.GET.get('work_mode', '')
    location_filter = request.GET.get('location', '')

    if education_filter:
        candidates = candidates.filter(education=education_filter)
    if experience_filter:
        candidates = candidates.filter(years_experience__gte=experience_filter)
    if work_mode_filter:
        candidates = candidates.filter(preferred_work_mode=work_mode_filter)
    if location_filter:
        candidates = candidates.filter(location__icontains=location_filter)

    if query:
        matched_ids = []
        for c in candidates:
            text = f"{c.skills} {c.major} {c.work_experience} {c.full_name} {c.location} {c.preferred_location} {c.get_education_display()}"
            if fuzzy_check(query, text):
                matched_ids.append(c.id)
        candidates = candidates.filter(id__in=matched_ids)

    return render(request, 'employers/candidates.html', {
        'candidates': candidates,
        'query': query,
        'education_filter': education_filter,
        'experience_filter': experience_filter,
        'work_mode_filter': work_mode_filter,
        'location_filter': location_filter,
    })


def employer_recommendations(request, job_id):
    if not request.user.is_authenticated:
        return redirect('employer_login')
    try:
        job = JobPosting.objects.get(id=job_id, employer__user=request.user)
    except JobPosting.DoesNotExist:
        return redirect('employer_dashboard')
    candidates = CandidateProfile.objects.all()
    results = []

    job_skills = [s.strip().lower() for s in job.skills_required.split(',')]
    edu_rank = {'high_school': 1, 'associate': 2, 'bachelor': 3, 'master': 4, 'phd': 5}
    job_level = edu_rank.get(job.education_required, 0)

    for c in candidates:
        score = 0
        cand_skills = [s.strip().lower() for s in c.skills.split(',')]
        skill_matches = len(set(cand_skills) & set(job_skills))
        if job_skills:
            score += round((skill_matches / len(job_skills)) * 25)

        cand_level = edu_rank.get(c.education, 0)
        if cand_level >= job_level:
            score += 20

        exp_gap = abs(c.years_experience - job.years_experience)
        if exp_gap == 0:
            score += 20
        elif exp_gap <= 2:
            score += 12
        elif exp_gap <= 4:
            score += 5

        if c.location.lower() == job.location.lower():
            score += 15

        if c.preferred_work_mode and c.preferred_work_mode == job.work_mode:
            score += 10

        if c.preferred_location and c.preferred_location.lower() == job.location.lower():
            score += 10

        results.append((score, c))

    results.sort(key=lambda x: x[0], reverse=True)

    employer = request.user.employerprofile
    if employer.is_member:
        top_candidates = [{'candidate': c, 'score': s} for s, c in results]
    else:
        top_candidates = [{'candidate': c, 'score': s} for s, c in results[:10]]

    return render(request, 'employers/recommendations.html', {
        'recommendations': top_candidates,
        'job': job,
        'is_member': employer.is_member,
    })


def edit_employer_profile(request):
    if not request.user.is_authenticated:
        return redirect('employer_login')
    employer = request.user.employerprofile
    if request.method == 'POST':
        employer.company_name = request.POST['company_name']
        employer.company_info = request.POST['company_info']
        employer.save()
        return redirect('employer_dashboard')
    return render(request, 'employers/edit_profile.html', {'employer': employer})


def employer_membership_page(request):
    if not request.user.is_authenticated:
        return redirect('employer_login')
    employer = request.user.employerprofile
    return render(request, 'employers/membership.html', {'employer': employer})


def delete_job(request, job_id):
    if not request.user.is_authenticated:
        return redirect('employer_login')
    if request.method == 'POST':
        try:
            job = JobPosting.objects.get(id=job_id, employer__user=request.user)
            job.delete()
        except JobPosting.DoesNotExist:
            pass
    return redirect('employer_dashboard')


def employer_upgrade_membership(request):
    if not request.user.is_authenticated:
        return redirect('employer_login')
    if request.method == 'POST':
        employer = request.user.employerprofile
        employer.is_member = True
        employer.save()
    return redirect('employer_dashboard')


def view_applications(request, job_id):
    if not request.user.is_authenticated:
        return redirect('employer_login')
    try:
        job = JobPosting.objects.get(id=job_id, employer__user=request.user)
    except JobPosting.DoesNotExist:
        return redirect('employer_dashboard')
    applications = JobApplication.objects.filter(job=job).select_related('candidate').order_by('-applied_at')
    return render(request, 'employers/applications.html', {'job': job, 'applications': applications})


def update_application(request, app_id):
    if not request.user.is_authenticated:
        return redirect('employer_login')
    if request.method == 'POST':
        try:
            app = JobApplication.objects.get(id=app_id, job__employer__user=request.user)
            new_status = request.POST.get('status')
            if new_status in ('accepted', 'rejected'):
                app.status = new_status
                app.save()
            return redirect('view_applications', job_id=app.job_id)
        except JobApplication.DoesNotExist:
            pass
    return redirect('employer_dashboard')
