from rest_framework.views import APIView
from vulnerabilities.models import Vulnerability
from vulnerabilities.serializers import VulnerabilitySerializer, FixVulnerabilitySerializer
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404

# Create your views here.
class VulnerabilityList(APIView):
    def get(self, request, format=None):
        vulnerabilities = Vulnerability.objects.all()
        serializer = VulnerabilitySerializer(vulnerabilities, many=True)
        return Response(serializer.data)
    
class UnfixedVulnerabilitiesList(APIView):
    def get(self, request, format=None):
        vulnerabilities = Vulnerability.objects.filter(hasBeenFixed=False)
        serializer = VulnerabilitySerializer(vulnerabilities, many=True)
        return Response(serializer.data)

class FixVulnerability(APIView):
    def post(self, request, format=None):
        serializer = FixVulnerabilitySerializer(data=request.data)
        if serializer.is_valid():
            vulnerability = Vulnerability.objects.get(id=serializer.data['id'])
            vulnerability.hasBeenFixed = serializer.data['hasBeenFixed']
            vulnerability.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)