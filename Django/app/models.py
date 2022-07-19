from django.contrib.auth.models import User
from django.db import models


class Link(models.Model):
    full_link = models.CharField(max_length=255)
    short_link = models.CharField(max_length=25)
    users = models.ManyToManyField(User)

