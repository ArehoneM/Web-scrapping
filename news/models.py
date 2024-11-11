from django.db import models

# Create your models here.
class Article(models.Model):
    title = models.CharField(max_length=255)
    excerpt = models.TextField()
    date = models.DateTimeField()
    link = models.URLField()
    author = models.CharField(max_length=255)
    content = models.TextField()
    image = models.URLField()

    def __str__(self):
        return self.title
