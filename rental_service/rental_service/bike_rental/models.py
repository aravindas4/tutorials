from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save, post_delete
from datetime import datetime
# Create your models here.

class Base(models.Model):
	"created and modified dates"

	created  = models.DateTimeField(auto_now_add=True)
	modified = models.DateTimeField(auto_now=True)

class Station(Base):
	name                    = models.CharField(max_length=20)
	latitude                = models.IntegerField(default=0)
	longitude               = models.IntegerField(default=0)
	bike_available_quantity = models.IntegerField(default=0)

	class Meta:
		db_table            = "station"
		unique_together     = ('latitude','longitude',)

	def __str__(self):
		return self.name

class Rent(Base):
	origin_station          = models.ForeignKey(Station,on_delete=models.CASCADE, related_name="origin_for_rents")
	destination_station     = models.ForeignKey(Station,on_delete=models.CASCADE, related_name="destination_for_rents")
	startdate               = models.DateTimeField(default=datetime.now)
	enddate                 = models.DateTimeField(null=True)
	is_active               = models.BooleanField(default=False)

	class Meta:
		db_table            = "rent"

	def __init__(self, *args, **kwargs):
		self.is_active = True
		super(Rent, self).__init__(*args, **kwargs)

	def save(self, *args, **kwargs):
		if not self.id:
			self.is_active = True
			self.enddate = None
			self.origin_station.bike_available_quantity -=1
			self.origin_station.save()
		else:
			if self.enddate and self.is_active:
				self.is_active = False
				self.destination_station.bike_available_quantity +=1
				self.destination_station.save()
		super(Rent, self).save(*args, **kwargs)

@receiver(post_delete, sender=Rent)
def rent_post_delete(sender, instance, **kwargs):
	if instance.is_active:
		instance.origin_station.bike_available_quantity +=1
		instance.origin_station.save()
