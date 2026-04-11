from django.urls import path, include

urlpatterns = [
    path('', include('candidates.urls')),
    path('employer/', include('employers.urls')),
]
