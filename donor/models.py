from django.db import models


class Donor(models.Model):
    boolean_choices = ((True, 'Yes'), (False, 'No'))
    username = models.CharField(max_length=100, primary_key=True)
    email = models.EmailField()
    dob = models.DateField()
    blood_group = models.CharField(max_length=3)
    contact = models.CharField(max_length=15)
    county = models.CharField(max_length=20)
    subscribe = models.CharField(max_length=5)


class LastDonDate(models.Model):
    username = models.CharField(max_length=150)
    date = models.DateField()
    venue = models.CharField(max_length=254)
    don_date_id = models.AutoField(primary_key=True)
