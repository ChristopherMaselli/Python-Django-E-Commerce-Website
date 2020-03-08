from django.db import models

# Create your models here.


class profile(models.Model):
    name = models.CharField(max_length=120)
    # description = models.TextField(null=True) Makes the field allow for empty description fields
    description = models.TextField(default='description default text')
    # location = models.CharField(
    #    max_length=120, default='my location default', blank=True, null=True)
    #job = models.CharField(max_length=120, null=True)

    # This will give the reference to the model, what you see when selecting between profiles
    def __unicode__(self):
        return self.name
