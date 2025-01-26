from rest_framework.views import APIView
from vulnerabilities.models import Vulnerability
from vulnerabilities.serializers import VulnerabilitySerializer, FixVulnerabilitySerializer
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
from django.db.models import Count
import requests
from rest_framework import permissions

nist_url = "https://services.nvd.nist.gov/rest/json/cves/2.0"

# Create your views here.
class VulnerabilityList(APIView):
    def get(self, request, format=None):
        """
        List all vulnerabilities that have not been fixed yet
        """
        try:
            resultsPerPage = request.query_params.get('resultsPerPage', None)
            startIndex = request.query_params.get('startIndex', None)
            
            params = {}
            
            params["resultsPerPage"] = resultsPerPage if resultsPerPage is not None else 10
            params["startIndex"] = startIndex if startIndex is not None else 0
            
            vulnerabilities_api = requests.get(nist_url, params=params)
            
            vulnerabilities_data = vulnerabilities_api.json().get('vulnerabilities')
            
            vulnerabilities_mapped = []
            
            vulnerabilities_saved = Vulnerability.objects.filter(hasBeenFixed=True)
            
            # Mapear los datos de la API a los campos del modelo
            for vulnerability in vulnerabilities_data:
                
                v = vulnerability.get('cve')
                
                cveId = v.get('id')
                published = v.get('published')
                vulnStatus = v.get('vulnStatus')
                description = (
                    v.get('descriptions', [{}])[0].get('value', 'N/A')
                    if v.get('descriptions') else 'N/A'
                )
                hasBeenFixed = vulnerabilities_saved.filter(cveId=cveId).exists() # Verificar si la vulnerabilidad ya ha sido registrada y está fixed, en cuyo caso colocar en True
                baseSeverityMetric = (
                    v.get('metrics', {}).get('cvssMetricV2', {})[0].get('baseSeverity', 'N/A')
                    if v.get('metrics', {}).get('cvssMetricV2') else 'N/A'
                )
                vulnerabilities_mapped.append({
                    "cveId": cveId,
                    "published": published,
                    "vulnStatus": vulnStatus,
                    "description": description,
                    "hasBeenFixed": hasBeenFixed,
                    "baseSeverityMetric": baseSeverityMetric
                })
                    
            # Excluir las vulnerabilidades que ya han sido registradas en la base de datos
            filtered_vulnerabilities = []
            for vulnerability in vulnerabilities_mapped:
                if not Vulnerability.objects.filter(cveId=vulnerability.get('cveId')).exists():
                    filtered_vulnerabilities.append(vulnerability)
            
            serializer = VulnerabilitySerializer(data=filtered_vulnerabilities, many=True)
            
            if serializer.is_valid():
                serializer.save()
                return Response({ **params, "results": len(vulnerabilities_mapped), "vulnerabilities": vulnerabilities_mapped})
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
class UnfixedVulnerabilitiesList(APIView):
    """
    TODO: Se puede implementar un paginador para mostrar las vulnerabilidades de 10 en 10
    """
    
    """
    List all vulnerabilities that have not been fixed yet
    """
    
    def get(self, request, format=None):
        vulnerabilities = Vulnerability.objects.filter(hasBeenFixed=False)
        serializer = VulnerabilitySerializer(vulnerabilities, many=True)
        return Response({ "results": len(serializer.data), "vulnerabilities": serializer.data} )

class FixVulnerability(APIView):
    
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self, pk):
        try:
            return Vulnerability.objects.get(cveId=pk)
        except Vulnerability.DoesNotExist:
            raise Http404
    
    """
    Fix a vulnerability with the given cveId
    """
    
    def post(self, request, pk, format=None):
        vulnerability = self.get_object(pk=pk)
        serializer = FixVulnerabilitySerializer(vulnerability, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class VulnerabilitiesSummary(APIView):
    
    """
    List the number of vulnerabilities by baseSeverityMetric
    """
    
    def get(self, request, format=None):
        
        summary = (
            Vulnerability.objects.values('baseSeverityMetric')
            .annotate(total=Count('baseSeverityMetric'))
            .order_by('-total')
        )
        
        # Crear diccionario para una respuesta más clara
        result = {item['baseSeverityMetric']: item['total'] for item in summary}
        
        return Response(result)
        