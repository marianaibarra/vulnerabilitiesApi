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
# Create your models here.
class Vulnerability(models.Model):
    sourceIdentifier = models.CharField(max_length=100)
    published = models.DateTimeField()
    vulnStatus = models.CharField( max_length=50, choices=VULNERABILITY_STATUS, default='Received',)
    description = models.CharField(max_length=200)
    hasBeenFixed = models.BooleanField(default=False)
    baseSeverityMetric = models.CharField(max_length=100)
    
    class Meta:
        ordering = ['published']