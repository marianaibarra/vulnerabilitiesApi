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
    def get_object(self, pk):
        try:
            return Vulnerability.objects.get(cveId=pk)
        except Vulnerability.DoesNotExist:
            raise Http404
    
    def post(self, request, pk, format=None):
        vulnerability = self.get_object(pk=pk)
        serializer = FixVulnerabilitySerializer(vulnerability, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        