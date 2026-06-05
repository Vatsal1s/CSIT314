from django.db import models
from django.contrib.auth.models import User
from talentmatch.constants import EDUCATION_LEVELS, WORK_MODES

class CandidateProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    education = models.CharField(max_length=20, choices=EDUCATION_LEVELS)
    major = models.CharField(max_length=100)
    years_experience = models.IntegerField(default=0)
    work_experience = models.TextField(blank=True)
    skills = models.TextField()
    location = models.CharField(max_length=100)
    preferred_work_mode = models.CharField(max_length=10, choices=WORK_MODES, blank=True)
    preferred_location = models.CharField(max_length=100, blank=True)
    is_member = models.BooleanField(default=False)

    def __str__(self):
        return self.full_name
