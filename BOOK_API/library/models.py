from django.db import models


class Books(models.Model):
    title = models.CharField(max_length=50)
    author = models.TextField(max_length=50)
    published_date = models.TextField(max_length=10)
    ISBN_number = models.IntegerField()
    pages_numbers = models.IntegerField()
    image_link = models.URLField()
    language = models.TextField(max_length=50)

    def __str__(self):
        return self.title

