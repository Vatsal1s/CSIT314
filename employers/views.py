from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import EmployerProfile, JobPosting
from candidates.models import CandidateProfile


def employer_signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']
        company_name = request.POST['company_name']
        company_info = request.POST['company_info']
        if User.objects.filter(username=username).exists():
            return render(request, 'employers/signup.html', {'error': 'Username already taken'})
        user = User.objects.create_user(username=username, password=password, email=email)
        EmployerProfile.objects.create(user=user, company_name=company_name, company_info=company_info)
        login(request, user)
        return redirect('employer_dashboard')
    return render(request, 'employers/signup.html')


def employer_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
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
    return render(request, 'employers/dashboard.html', {'jobs': jobs})


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
        )
        return redirect('employer_dashboard')
    return render(request, 'employers/post_job.html')


def view_candidates(request):
    if not request.user.is_authenticated:
        return redirect('employer_login')
    candidates = CandidateProfile.objects.all()
    skill_filter = request.GET.get('skill', '')
    education_filter = request.GET.get('education', '')
    experience_filter = request.GET.get('experience', '')
    search_query = request.GET.get('q', '')

    if skill_filter:
        candidates = candidates.filter(skills__icontains=skill_filter)
    if education_filter:
        candidates = candidates.filter(education=education_filter)
    if experience_filter:
        candidates = candidates.filter(years_experience__gte=experience_filter)
    if search_query:
        candidates = candidates.filter(skills__icontains=search_query) | candidates.filter(major__icontains=search_query)

    return render(request, 'employers/candidates.html', {
        'candidates': candidates,
        'skill_filter': skill_filter,
        'education_filter': education_filter,
        'experience_filter': experience_filter,
        'search_query': search_query,
    })


def employer_recommendations(request, job_id):
    if not request.user.is_authenticated:
        return redirect('employer_login')
    job = JobPosting.objects.get(id=job_id)
    candidates = CandidateProfile.objects.all()
    scored = []

    job_skills = [s.strip().lower() for s in job.skills_required.split(',')]
    education_rank = {'high_school': 1, 'associate': 2, 'bachelor': 3, 'master': 4, 'phd': 5}
    job_edu_rank = education_rank.get(job.education_required, 0)

    for candidate in candidates:
        score = 0
        candidate_skills = [s.strip().lower() for s in candidate.skills.split(',')]
        matched_skills = len(set(candidate_skills) & set(job_skills))
        score += matched_skills * 30

        candidate_edu_rank = education_rank.get(candidate.education, 0)
        if candidate_edu_rank >= job_edu_rank:
            score += 25

        exp_diff = abs(candidate.years_experience - job.years_experience)
        if exp_diff == 0:
            score += 25
        elif exp_diff <= 2:
            score += 15
        elif exp_diff <= 4:
            score += 5

        if candidate.location.lower() == job.location.lower():
            score += 20

        scored.append((score, candidate))

    scored.sort(key=lambda x: x[0], reverse=True)
    top_candidates = [{'candidate': c, 'score': s} for s, c in scored[:10]]
    return render(request, 'employers/recommendations.html', {'recommendations': top_candidates, 'job': job})
