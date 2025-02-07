from rest_framework import serializers
from vulnerabilities.models import Vulnerability, VULNERABILITY_STATUS, BASE_SEVERITY_METRIC

class VulnerabilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Vulnerability
        fields = ['cveId', 'published', 'vulnStatus', 'description', 'hasBeenFixed', 'baseSeverityMetric']
        extra_kwargs = {
            'vulnStatus': {'choices': VULNERABILITY_STATUS},
            'cveId': {'required': True},
            'published': {'required': True},
            'description': {'required': True},
        }
        
class FixVulnerabilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Vulnerability
        fields = ['hasBeenFixed']
        extra_kwargs = {
            'hasBeenFixed': {'required': True},
        }
        
class UnfixedVulnerabilitySerializer(serializers.Serializer):
    cveId = serializers.CharField()
    published = serializers.DateTimeField()
    vulnStatus = serializers.CharField()
    description = serializers.CharField()
    hasBeenFixed = serializers.BooleanField()
    baseSeverityMetric = serializers.CharField()
    newField = serializers.CharField()
        
    def create(self, validated_data):
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        return super().update(instance, validated_data)