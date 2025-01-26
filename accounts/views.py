from django.contrib.auth.models import User
from rest_framework import generics
from accounts.serializers import UserSerializer, CreateUserSerializer

# Create your views here.
class UsersList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = CreateUserSerializer
    
class UsersDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
