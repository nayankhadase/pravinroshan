from django.db import models
from django.db.models.base import Model

# Create your models here.
class Rawmaterialdata(models.Model):
    name_id=models.IntegerField()
    rawqty=models.BigIntegerField(default=0)
    totalqty=models.BigIntegerField(default=0)
    totalInvest=models.BigIntegerField(default=0)

class TodaysProdData(models.Model):
    name_id=models.IntegerField()
    produce=models.IntegerField(default=0)
    reject=models.IntegerField(default=0)
    date=models.DateField()

class Instockqty(models.Model):
    name_id=models.IntegerField()
    produceqty=models.IntegerField(default=0)
    rejectqty=models.IntegerField(default=0)

class Totalselling(models.Model):
    name_id=models.IntegerField(null=False)
    sellqty=models.IntegerField(null=False)
    sellingprice=models.IntegerField(null=False)
    totalprice=models.IntegerField(null=False,default=0)
    totalprofit=models.IntegerField(null=False)
    selldate=models.DateField(null=False)

class Manufacturingprice(models.Model):
    name=models.CharField(max_length=20,null=False)
    manucost=models.IntegerField(null=False)
    disc=models.CharField(max_length=200,default='null')