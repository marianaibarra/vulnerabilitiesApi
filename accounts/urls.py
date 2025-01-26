from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from accounts import views

urlpatterns = [
    path('accounts/', views.UsersList.as_view()),
    path('accounts/<int:pk>/', views.UsersDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)