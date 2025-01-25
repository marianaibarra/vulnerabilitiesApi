from rest_framework.views import APIView
from vulnerabilities.models import Vulnerability
from vulnerabilities.serializers import VulnerabilitySerializer
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404

# Create your views here.
class VulnerabilityList(APIView):
    def get(self, request, format=None):
        vulnerabilities = Vulnerability.objects.all()
        serializer = VulnerabilitySerializer(vulnerabilities, many=True)
        return Response(serializer.data)
        

    def post(self, request, format=None):
        serializer = VulnerabilitySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
        
class VulnerabilityDetails(APIView):
    def get_object(self, pk):
        try:
            return Vulnerability.objects.get(pk=pk)
        except Vulnerability.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        vulnerability = self.get_object(pk)
        serializer = VulnerabilitySerializer(vulnerability)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        vulnerability = self.get_object(pk)
        serializer = VulnerabilitySerializer(vulnerability, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        vulnerability = self.get_object(pk)
        vulnerability.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)