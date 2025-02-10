
from rest_framework.views import APIView
from kpop.models import Album, EntertainmentCompany, Fan, Idol, IdolGroup, Song
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Count, Q

class KpopList(APIView):
    def get(self, request, format=None):
        try:
            print("im working")
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
