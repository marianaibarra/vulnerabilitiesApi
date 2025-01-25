from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from vulnerabilities import views

urlpatterns = [
    path('vulnerabilities/', views.VulnerabilityList.as_view()),
    path('vulnerabilities/<int:pk>/', views.VulnerabilityDetails.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)