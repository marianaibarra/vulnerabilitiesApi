from django.db import models

VULNERABILITY_STATUS = [
    ('Received', 'Received'),
    ('Awaiting Analysis', 'Awaiting Analysis'),
    ('Undergoing Analysis', 'Undergoing Analysis'),
    ('Analyzed', 'Analyzed'),
    ('Modified', 'Modified'),
    ('Deferred', 'Deferred'),
    ('Rejected', 'Rejected'),
]

BASE_SEVERITY_METRIC = [
    ('N/A', 'N/A'),
    ('LOW', 'LOW'),
    ('LOWMEDIUM', 'LOWMEDIUM'),
    ('MEDIUM', 'MEDIUM'),
    ('MEDIUMHIGH', 'MEDUIMHIGH'),
    ('HIGH', 'HIGH'),
    ('NOTDEFINED', 'NOTDEFINED'),
]

# Create your models here.
class Vulnerability(models.Model):
    cveId = models.CharField(max_length=100, unique=True)
    published = models.DateTimeField()
    vulnStatus = models.CharField( max_length=50, choices=VULNERABILITY_STATUS, default='Received')
    description = models.CharField(max_length=1000, default='N/A')
    hasBeenFixed = models.BooleanField(default=False)
    baseSeverityMetric = models.CharField(max_length=100, default='N/A', choices=BASE_SEVERITY_METRIC)
    
    class Meta:
        ordering = ['published']
       