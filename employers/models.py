from django.db import models
from django.contrib.auth.models import User

EDUCATION_LEVELS = [
    ('high_school', 'High School'),
    ('associate', 'Associate Degree'),
    ('bachelor', 'Bachelor Degree'),
    ('master', 'Master Degree'),
    ('phd', 'PhD'),
]

WORK_MODES = [
    ('remote', 'Remote'),
    ('onsite', 'On-site'),
    ('hybrid', 'Hybrid'),
]

class EmployerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=100)
    company_info = models.TextField()

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
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
