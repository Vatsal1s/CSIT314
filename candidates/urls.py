from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing, name='landing'),
    path('candidate/signup/', views.candidate_signup, name='candidate_signup'),
    path('candidate/login/', views.candidate_login, name='candidate_login'),
    path('candidate/logout/', views.candidate_logout, name='candidate_logout'),
    path('candidate/dashboard/', views.candidate_dashboard, name='candidate_dashboard'),
    path('candidate/jobs/', views.candidate_jobs, name='candidate_jobs'),
    path('candidate/recommendations/', views.candidate_recommendations, name='candidate_recommendations'),
    path('candidate/membership/', views.membership_page, name='candidate_membership'),
    path('candidate/upgrade/', views.upgrade_membership, name='candidate_upgrade_membership'),
    path('candidate/apply/<int:job_id>/', views.apply_to_job, name='apply_to_job'),
]
