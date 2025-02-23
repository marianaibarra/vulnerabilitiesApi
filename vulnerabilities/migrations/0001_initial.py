# Generated by Django 5.1.5 on 2025-01-25 18:24

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Vulnerability',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sourceIdentifier', models.CharField(max_length=100)),
                ('published', models.DateTimeField()),
                ('vulnStatus', models.CharField(choices=[('Received', 'Received'), ('Awaiting Analysis', 'Awaiting Analysis'), ('Undergoing Analysis', 'Undergoing Analysis'), ('Analyzed', 'Analyzed'), ('Modified', 'Modified'), ('Deferred', 'Deferred'), ('Rejected', 'Rejected')], default='Received', max_length=50)),
                ('description', models.CharField(max_length=200)),
                ('hasBeenFixed', models.BooleanField(default=False)),
                ('baseSeverityMetric', models.CharField(max_length=100)),
            ],
            options={
                'ordering': ['published'],
            },
        ),
    ]
