from django.db import models
from django.contrib.auth.models import User
from talentmatch.constants import EDUCATION_LEVELS, WORK_MODES, JOB_TYPES

class EmployerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=100)
    company_info = models.TextField()
    is_member = models.BooleanField(default=False)

    def __str__(self):
        return self.company_name


class JobPosting(models.Model):
    employer = models.ForeignKey(EmployerProfile, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()
    education_required = models.CharField(max_length=20, choices=EDUCATION_LEVELS)
    skills_required = models.TextField()
    years_experience = models.IntegerField(default=0)
    work_mode = models.CharField(max_length=10, choices=WORK_MODES)
    location = models.CharField(max_length=100)
    job_type = models.CharField(max_length=20, choices=JOB_TYPES, default='full_time')
    salary_min = models.IntegerField(default=0)
    salary_max = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class JobApplication(models.Model):
    STATUS = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    ]
    candidate = models.ForeignKey('candidates.CandidateProfile', on_delete=models.CASCADE)
    job = models.ForeignKey(JobPosting, on_delete=models.CASCADE)
    applied_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS, default='pending')

    class Meta:
        unique_together = ('candidate', 'job')
