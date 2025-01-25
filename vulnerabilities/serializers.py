from rest_framework import serializers
from vulnerabilities.models import Vulnerability, VULNERABILITY_STATUS

class VulnerabilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Vulnerability
        fields = ['id', 'sourceIdentifier', 'published', 'vulnStatus', 'description', 'hasBeenFixed', 'baseSeverityMetric']