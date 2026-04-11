from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import CandidateProfile
from employers.models import JobPosting


def landing(request):
    return render(request, 'landing.html')


def candidate_signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']
        if User.objects.filter(username=username).exists():
            return render(request, 'candidates/signup.html', {'error': 'Username already taken'})
        user = User.objects.create_user(username=username, password=password, email=email)
        login(request, user)
        return redirect('candidate_profile')
    return render(request, 'candidates/signup.html')


def candidate_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user and hasattr(user, 'candidateprofile'):
            login(request, user)
            return redirect('candidate_dashboard')
        return render(request, 'candidates/login.html', {'error': 'Invalid credentials'})
    return render(request, 'candidates/login.html')


def candidate_logout(request):
    logout(request)
    return redirect('landing')


def candidate_profile(request):
    if not request.user.is_authenticated:
        return redirect('candidate_login')
    if request.method == 'POST':
        profile, created = CandidateProfile.objects.get_or_create(user=request.user)
        profile.full_name = request.POST['full_name']
        profile.phone = request.POST['phone']
        profile.education = request.POST['education']
        profile.major = request.POST['major']
        profile.years_experience = request.POST['years_experience']
        profile.skills = request.POST['skills']
        profile.location = request.POST['location']
        profile.save()
        return redirect('candidate_dashboard')
    profile = CandidateProfile.objects.filter(user=request.user).first()
    return render(request, 'candidates/profile.html', {'profile': profile})


def candidate_dashboard(request):
    if not request.user.is_authenticated:
        return redirect('candidate_login')
    query = request.GET.get('q', '')
    if query:
        jobs = JobPosting.objects.filter(description__icontains=query)
    else:
        jobs = JobPosting.objects.all()
    return render(request, 'candidates/dashboard.html', {'jobs': jobs, 'query': query})


def candidate_recommendations(request):
    if not request.user.is_authenticated:
        return redirect('candidate_login')
    try:
        profile = request.user.candidateprofile
    except CandidateProfile.DoesNotExist:
        return redirect('candidate_profile')

    jobs = JobPosting.objects.all()
    scored = []
    candidate_skills = [s.strip().lower() for s in profile.skills.split(',')]

    education_rank = {'high_school': 1, 'associate': 2, 'bachelor': 3, 'master': 4, 'phd': 5}
    candidate_edu_rank = education_rank.get(profile.education, 0)

    for job in jobs:
        score = 0
        job_skills = [s.strip().lower() for s in job.skills_required.split(',')]
        matched_skills = len(set(candidate_skills) & set(job_skills))
        score += matched_skills * 30

        job_edu_rank = education_rank.get(job.education_required, 0)
        if candidate_edu_rank >= job_edu_rank:
            score += 25

        exp_diff = abs(profile.years_experience - job.years_experience)
        if exp_diff == 0:
            score += 25
        elif exp_diff <= 2:
            score += 15
        elif exp_diff <= 4:
            score += 5

        if profile.location.lower() == job.location.lower():
            score += 20

        scored.append((score, job))

    scored.sort(key=lambda x: x[0], reverse=True)
    top_jobs = [{'job': job, 'score': score} for score, job in scored[:10]]
    return render(request, 'candidates/recommendations.html', {'recommendations': top_jobs})
