from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from kpop import views

urlpatterns = [
    path('kpop/', views.KpopList.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)