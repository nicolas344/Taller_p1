from django.db import models

class Movie(models.Model):
    titel = models.CharField(max_length=100)
    description = models.CharField(max_length=250)
    image = models.ImageField(upload_to='movie/images')
    url = models.URLField(blank=True)
    