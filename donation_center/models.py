from django.db import models
from datetime import date


class Profile(models.Model):
    username = models.CharField(max_length=150, primary_key=True)
    donation_center = models.CharField(max_length=50)
    email = models.EmailField(max_length=254)
    contact = models.CharField(max_length=15)
    county = models.CharField(max_length=20)
    location = models.CharField(max_length=254)


class BloodDonated(models.Model):
    donation_id = models.CharField(max_length=15, primary_key=True)
    units_donated = models.IntegerField()
    blood_group = models.CharField(max_length=5)
    dc_id = models.CharField(max_length=15)
    date = models.DateField(default=date.today)


class BloodUsed(models.Model):
    used_id = models.CharField(max_length=15, primary_key=True)
    units_used = models.IntegerField()
    blood_group = models.CharField(max_length=5)
    dc_id = models.CharField(max_length=15)
    date = models.DateField(default=date.today)


class BloodRequest(models.Model):
    request_id = models.CharField(max_length=15, primary_key=True)
    units_required = models.IntegerField()
    blood_group = models.CharField(max_length=5)
    dc_id = models.CharField(max_length=15)
    date = models.DateField(default=date.today)
    display = models.CharField(max_length=3)


class Events(models.Model):
    event_name = models.CharField(max_length=100, primary_key=True)
    location = models.CharField(max_length=100)
    date = models.DateField()
    time = models.TimeField()
    dc_id = models.CharField(max_length=15)
    poster = models.ImageField(upload_to='images/')
