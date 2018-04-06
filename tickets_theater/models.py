from django.db import models
# import django
#
#
# import os
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'theater.settings')
# django.setup()

class Visitor(models.Model):
    idvisitor = models.IntegerField(primary_key=True)
    name = models.CharField( max_length=20)
    surname = models.CharField(max_length=20)
    category_vis = models.IntegerField(default=0)


class Place(models.Model):
    idplace = models.IntegerField(primary_key=True)
    country = models.CharField(max_length=20)
    city = models.CharField(max_length=20)
    address = models.CharField(max_length=20)
    category_pl = models.IntegerField()


class Performance(models.Model):
    idperformance = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=20)
    style = models.CharField(max_length=20)
    author = models.CharField(max_length=20)
    actors = models.CharField(max_length=50)


class Ticket_sales(models.Model):
    idticket_sales = models.IntegerField(primary_key=True)
    date = models.DateTimeField()
    binocular = models.BooleanField()
    row = models.IntegerField()
    sit = models.IntegerField()
    idvisitor = models.ForeignKey(Visitor)
    idperformance = models.ForeignKey(Performance)
    idplace = models.ForeignKey(Place)
