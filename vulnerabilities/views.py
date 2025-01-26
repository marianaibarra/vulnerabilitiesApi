from rest_framework.views import APIView
from vulnerabilities.models import Vulnerability
from vulnerabilities.serializers import VulnerabilitySerializer, FixVulnerabilitySerializer
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
from django.db.models import Count
import requests

nist_url = "https://services.nvd.nist.gov/rest/json/cves/2.0"

# Create your views here.
class VulnerabilityList(APIView):
    def get(self, request, format=None):
        
        try:
            resultsPerPage = request.query_params.get('resultsPerPage', None)
            startIndex = request.query_params.get('startIndex', None)
            
            params = {}
            
            params["resultsPerPage"] = resultsPerPage if resultsPerPage is not None else 10
            params["startIndex"] = startIndex if startIndex is not None else 0
            
            vulnerabilities_api = requests.get(nist_url, params=params)
            
            vulnerabilities_data = vulnerabilities_api.json().get('vulnerabilities')
            
            vulnerabilities_mapped = []
            
            # Mapear los datos de la API a los campos del modelo
            for vulnerability in vulnerabilities_data:
                
                v = vulnerability.get('cve')
                
                cveId = v.get('id')
                published = v.get('published')
                vulnStatus = v.get('vulnStatus')
                description = v.get('descriptions', [])[0].get('value', 'N/A')
                hasBeenFixed = False
                baseSeverityMetric = v.get('metrics', {}).get('cvssMetricV2', {})[0].get('baseSeverity', 'N/A')
                
                vulnerabilities_mapped.append({
                    "cveId": cveId,
                    "published": published,
                    "vulnStatus": vulnStatus,
                    "description": description,
                    "hasBeenFixed": hasBeenFixed,
                    "baseSeverityMetric": baseSeverityMetric
                })
            
            vulnerabilities_fixed = Vulnerability.objects.filter(hasBeenFixed=True)
            
            # Eliminar las vulnerabilidades que ya han sido fixeadas de vulnerabilities_mapped, no importa hacer este paso antes o después de registrar las vulnerabilidades en la base de datos ya que solo las fixeadas (hasBeenFixed=True) serán eliminadas, y estás deben estar en la base de datos
            for vulnerability in vulnerabilities_fixed:
                for i in range(len(vulnerabilities_mapped)):
                    if vulnerability.cveId == vulnerabilities_mapped[i].get('cveId'):
                        vulnerabilities_mapped.pop(i)
                        break
                    
            # Excluir las vulnerabilidades que ya han sido registradas en la base de datos
            filtered_vulnerabilities = []
            for vulnerability in vulnerabilities_mapped:
                if not Vulnerability.objects.filter(cveId=vulnerability.get('cveId')).exists():
                    filtered_vulnerabilities.append(vulnerability)
            
            serializer = VulnerabilitySerializer(data=filtered_vulnerabilities, many=True)
            
            if serializer.is_valid():
                serializer.save()
                return Response({ **params, "vulnerabilities": vulnerabilities_mapped})
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
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
        
class VulnerabilitiesSummary(APIView):
    def get(self, request, format=None):
        
        summary = (
            Vulnerability.objects.values('baseSeverityMetric')
            .annotate(total=Count('baseSeverityMetric'))
            .order_by('-total')
        )
        
        # Crear diccionario para una respuesta más clara
        result = {item['baseSeverityMetric']: item['total'] for item in summary}
        
        return Response(result)
        