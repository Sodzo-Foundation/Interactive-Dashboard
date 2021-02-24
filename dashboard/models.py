from django.db import models

from django.contrib.auth.models import User


class Pollutants(models.Model):
    created_on = models.DateTimeField(auto_now_add=True, editable=False, verbose_name='Date')
    category = models.CharField(max_length=255,blank=True, editable=True, verbose_name='Category')
    village = models.CharField(max_length=255,blank=True, editable=True, verbose_name='Village')
    city_district = models.CharField(max_length=255,blank=True, editable=True, verbose_name='Town')
    suburb = models.CharField(max_length=255,blank=True, editable=True, verbose_name='Suburb')
    location = models.CharField(max_length=255,blank=True, editable=True, verbose_name='Location')
    district = models.CharField(max_length=255,blank=True, editable=True, verbose_name='District')
    state = models.CharField(max_length=255,blank=True, editable=True, verbose_name='State')
    lat = models.CharField(max_length=255, blank=True,  editable=True, verbose_name='Latitude')
    long = models.CharField(max_length=255,blank=True, editable=True, verbose_name='Longitude')
    address = models.CharField(max_length=255,blank=True, editable=True, verbose_name='Address')
    count = models.CharField(max_length=255,blank=True, editable=True, verbose_name='Count')
    country = models.CharField(max_length=255,blank=True, editable=True, verbose_name='Country')
    
    class Meta:
        ordering = ['created_on']
        verbose_name = "Pollutant"
        #unique_together = ["created_on","address", "lat","long"]
        unique_together = ["created_on","lat","long"]

        def __unicode__(self):
            return self.category
    
    #class Meta:
    #    db_table = 'Pollutants'

class ConfirmedPollutants(models.Model):
    created_on = models.DateTimeField(auto_now_add=True, editable=False, verbose_name='Date')
    pollutant = models.ForeignKey(Pollutants, blank=True, editable=True,on_delete = models.CASCADE)
    total = models.CharField(max_length=255, blank=True, editable=True, verbose_name='Total')
    shores = models.CharField(max_length=255, blank=True, editable=True, verbose_name='Shores')
    
    
    class Meta:
        ordering = ['created_on']
        verbose_name = "Confirmed Pollutant"
        unique_together = ["pollutant"]

        def __unicode__(self):
            return self.pollutant
