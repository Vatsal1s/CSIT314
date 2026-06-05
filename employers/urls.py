from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.employer_signup, name='employer_signup'),
    path('login/', views.employer_login, name='employer_login'),
    path('logout/', views.employer_logout, name='employer_logout'),
    path('dashboard/', views.employer_dashboard, name='employer_dashboard'),
    path('post-job/', views.post_job, name='post_job'),
    path('candidates/', views.view_candidates, name='view_candidates'),
    path('recommendations/', views.recommendations_list, name='recommendations_list'),
    path('recommendations/<int:job_id>/', views.employer_recommendations, name='employer_recommendations'),
    path('membership/', views.employer_membership_page, name='employer_membership'),
    path('upgrade/', views.employer_upgrade_membership, name='employer_upgrade_membership'),
    path('edit-profile/', views.edit_employer_profile, name='edit_employer_profile'),
    path('delete-job/<int:job_id>/', views.delete_job, name='delete_job'),
    path('applications/<int:job_id>/', views.view_applications, name='view_applications'),
    path('application/<int:app_id>/update/', views.update_application, name='update_application'),
]
