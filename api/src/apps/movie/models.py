from django.db import models

class Movie(models.Model):
    title = models.CharField(max_length=100, null=True)
    author = models.CharField(max_length=50,null=True)
    year_published = models.CharField(max_length=10, null=True)
    review = models.PositiveIntegerField(null=True)
    
    def __str__(self):
        return self.title 