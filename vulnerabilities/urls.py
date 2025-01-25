from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from vulnerabilities import views

urlpatterns = [
    path('vulnerabilities/', views.VulnerabilityList.as_view()),
    path('unfixedVulnerabilities/', views.UnfixedVulnerabilitiesList.as_view()),
    path('fixVulnerability/<str:pk>', views.FixVulnerability.as_view()),
    path("vulnerabilitiesSummary/", views.VulnerabilitiesSummary.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)