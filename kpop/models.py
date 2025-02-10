from django.db import models

# Create your models here.
class EntertainmentCompany(models.Model):
    name = models.CharField(max_length=100, unique=True)
    founded_year = models.PositiveIntegerField()
    country = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class IdolGroup(models.Model):
    name = models.CharField(max_length=100, unique=True)
    debut_year = models.PositiveIntegerField()
    company = models.ForeignKey(EntertainmentCompany, on_delete=models.CASCADE, related_name="groups")

    def __str__(self):
        return self.name

class Idol(models.Model):
    name = models.CharField(max_length=100)
    stage_name = models.CharField(max_length=100, unique=False)
    birth_date = models.DateField()
    group = models.ForeignKey(IdolGroup, on_delete=models.SET_NULL, null=True, blank=True, related_name="members")
    company = models.ForeignKey(EntertainmentCompany, on_delete=models.CASCADE, related_name="idols")
    position = models.CharField(max_length=50)  # e.g., Main Vocalist, Rapper
    height_cm = models.PositiveIntegerField()
    weight_kg = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.stage_name} ({self.group.name if self.group else 'Solo'})"

class Album(models.Model):
    title = models.CharField(max_length=100)
    group = models.ForeignKey(IdolGroup, on_delete=models.CASCADE, related_name="albums")
    release_date = models.DateField()

    def __str__(self):
        return f"{self.title} - {self.group.name}"

class Song(models.Model):
    title = models.CharField(max_length=100)
    album = models.ForeignKey(Album, on_delete=models.CASCADE, related_name="songs")
    duration_seconds = models.PositiveIntegerField()
    is_title_track = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.title} ({self.album.group.name})"

class Fan(models.Model):
    username = models.CharField(max_length=50, unique=True)
    favorite_idols = models.ManyToManyField(Idol, related_name="fans")
    favorite_groups = models.ManyToManyField(IdolGroup, related_name="fans")
    favorite_songs = models.ManyToManyField(Song, related_name="fans")

    def __str__(self):
        return self.username