from django.db import models

# Create your models here.
# biography and awards


class Awards(models.Model):
    title = models.CharField(max_length=20)
    name = models.CharField(max_length=30)
    award_title = models.CharField(max_length=100)
    award_image_1 = models.ImageField(upload_to='awards_1/')
    award_image_2 = models.ImageField(upload_to='awards_2/')
    brief_profile = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.title} {self.name}'
