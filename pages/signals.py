import requests

from django.dispatch import receiver
from django.db.models.signals import pre_save

from core.models import SiteConfiguration
from .models import Spot


@receiver(pre_save, sender=Spot)
def pre_save_spot(instance, **kwargs):
    def update_coordinates():
        url = 'https://maps.googleapis.com/maps/api/geocode/json'
        params = {'sensor': 'false', 'address': instance.address,
                  'key': SiteConfiguration.get_solo().google_maps_api_key}
        try:
            r = requests.get(url, params=params)
            results = r.json().get('results')
            location = results[0]['geometry']['location']
            return location['lat'], location['lng']
        except Exception as e:
            print(e)
            return 0.0, 0.0

    try:
        old_object = Spot.objects.get(pk=instance.pk)
    except Spot.DoesNotExist:
        instance.lat, instance.lng = update_coordinates()
    else:
        if instance.address and (old_object.address != instance.address):  # Address Changed
            instance.lat, instance.lng = update_coordinates()
