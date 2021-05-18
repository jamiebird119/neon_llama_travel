from django.core.management.base import BaseCommand, CommandError
from tours.models import Category, Country, Region, Tour
from django.conf import settings
import requests
import json
import traceback
import subprocess
import math
from django.core.management import call_command


class Command(BaseCommand):
    help = 'Find tour itineraries'

    def handle(self, *args, **options):
        tours = Tour.objects.all()
        for item in tours:
            tour_id = item.id
            tour_obj = Tour.objects.get(pk=tour_id)
            headers = {
                "X-Application-Key":
                f"{settings.G_KEY}",
            }
            response = requests.get(tour_obj.structured_itinerary, headers=headers)
            resource = response.json()
            itinerary = {}
            for item in resource["days"]:
                itinerary[item["day"]]= {"summary": item["summary"],
                "label": item["label"]}
            
            tour_obj.itinerary = [itinerary]
            print(tour_obj.itinerary)
            tour_obj.save()
            print(f"Itinerary for {tour_obj.name} saved.")
