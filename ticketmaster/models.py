from django.db import models


class Events(models.Model):

    name = models.CharField(max_length=150)
    venue = models.CharField(max_length=150)
    address = models.CharField(max_length=200)
    link = models.CharField(max_length=300)
    date = models.CharField(max_length=150)
    time = models.CharField(max_length=150)
    image = models.CharField(max_length=300)


class Comments(models.Model):

    comment = models.TextField()
    event_id = models.CharField(max_length=50)