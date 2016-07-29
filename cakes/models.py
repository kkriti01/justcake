from __future__ import unicode_literals

from django.db import models


class Cake(models.Model):
    title = models.CharField(max_length=300)
    price = models.FloatField()
    image = models.ImageField(upload_to='cakes')

    def __unicode__(self):
        return self.title


class Category(models.Model):
    name = models.CharField(max_length=200)
    cakes = models.ManyToManyField(Cake)

    def __unicode__(self):
        return self.name
