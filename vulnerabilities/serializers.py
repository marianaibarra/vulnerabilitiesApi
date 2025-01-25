from rest_framework import serializers
from vulnerabilities.models import Vulnerability, VULNERABILITY_STATUS

class VulnerabilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Vulnerability
        fields = ['id', 'cveId', 'published', 'vulnStatus', 'description', 'hasBeenFixed', 'baseSeverityMetric']
        extra_kwargs = {
            'vulnStatus': {'choices': VULNERABILITY_STATUS},
            'cveId': {'required': True},
            'published': {'required': True},
            'description': {'required': True},
        }
        
class FixVulnerabilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Vulnerability
        fields = ['cveId', 'hasBeenFixed']
        extra_kwargs = {
            'hasBeenFixed': {'required': True},
        }