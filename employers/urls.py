from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.employer_signup, name='employer_signup'),
    path('login/', views.employer_login, name='employer_login'),
    path('logout/', views.employer_logout, name='employer_logout'),
    path('dashboard/', views.employer_dashboard, name='employer_dashboard'),
    path('post-job/', views.post_job, name='post_job'),
    path('candidates/', views.view_candidates, name='view_candidates'),
    path('recommendations/<int:job_id>/', views.employer_recommendations, name='employer_recommendations'),
]
