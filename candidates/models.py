from django.db import models
from django.contrib.auth.models import User

EDUCATION_LEVELS = [
    ('high_school', 'High School'),
    ('associate', 'Associate Degree'),
    ('bachelor', 'Bachelor Degree'),
    ('master', 'Master Degree'),
    ('phd', 'PhD'),
]

class CandidateProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    education = models.CharField(max_length=20, choices=EDUCATION_LEVELS)
    major = models.CharField(max_length=100)
    years_experience = models.IntegerField(default=0)
    skills = models.TextField()
    location = models.CharField(max_length=100)

    def __str__(self):
        return self.full_name
