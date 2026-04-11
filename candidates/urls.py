from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing, name='landing'),
    path('candidate/signup/', views.candidate_signup, name='candidate_signup'),
    path('candidate/login/', views.candidate_login, name='candidate_login'),
    path('candidate/logout/', views.candidate_logout, name='candidate_logout'),
    path('candidate/profile/', views.candidate_profile, name='candidate_profile'),
    path('candidate/dashboard/', views.candidate_dashboard, name='candidate_dashboard'),
    path('candidate/recommendations/', views.candidate_recommendations, name='candidate_recommendations'),
]
