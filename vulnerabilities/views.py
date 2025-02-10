from rest_framework.views import APIView
from vulnerabilities.models import Vulnerability
from vulnerabilities.serializers import VulnerabilitySerializer, FixVulnerabilitySerializer, UnfixedVulnerabilitySerializer
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
from django.db.models import Count, Q
import requests
from rest_framework import permissions
from rest_framework.decorators import api_view
from rest_framework.reverse import reverse

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
            """TODO: Creo que esto lo puedo hacer sobreescribiendo el metodo @save del modelo."""
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
        try:
            
            newFieldValue = request.query_params.get('NewFieldValue', None)
            
            vulnerabilities = Vulnerability.objects.exclude(    
                baseSeverityMetric__contains="H", 
                ).exclude(published__year=1995)
            # .filter(published__year=1995, )
            
            vulnerabilities__mapped = []
            
            for vulnerability in vulnerabilities.values():
                vulnerabilities__mapped.append({
                    **vulnerability,
                    "newField": newFieldValue
                })
            
            
            serializer = UnfixedVulnerabilitySerializer(vulnerabilities__mapped, many=True)
            return Response({ "results": len(serializer.data), "vulnerabilities": serializer.data} )
        except Exception as e: 
            print(e)
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

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
        try:
            summary = (
                Vulnerability.objects
                .values('baseSeverityMetric')
                .annotate(baseseverity=Count('baseSeverityMetric', 
                                             filter=~Q(published__gt="1991-01-01")
                                             ))
                .order_by('-baseseverity')
                # .aggregate(something=Count('baseSeverityMetric'), minji=Count('baseSeverityMetric'))
            )
            
            print(type(summary))
            
            # Crear diccionario para una respuesta más clara
            result = {item['baseSeverityMetric']: item['baseseverity'] for item in summary}
            
            return Response(result)
        except Exception as err:
            print(err)
    

class VulnerabilityDetail(APIView):
    def get(self, request, pk, format=None):
        print(type(pk), pk)
        return Response("Hello", pk)

# Root view

@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'vulnerabilities': reverse('vulnerability-list', request=request, format=format),
        'unfixed-vulnerabilities': reverse('unfixed-vulnerabilities-list', request=request, format=format),
        'fix-vulnerability': reverse('fix-vulnerability', request=request, format=format),
        'vulnerabilities-summary': reverse('vulnerabilities-summary', request=request, format=format),
    })