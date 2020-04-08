from django.db import models

class Group(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField() 
    def __str__(self): 
        return self.title


