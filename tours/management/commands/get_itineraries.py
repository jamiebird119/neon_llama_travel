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
        all_tours = Tour.objects.all()
        for item in all_tours:
            try:
                # CHECK IF TOUR IS IN DATABASE
                tour = Tour.objects.get(
                    pk=item.id)
                tour_url = f"https://rest.gadventures.com/tour_dossiers/{item.id}"
                regions = {
                    1: "CA",
                    2: "EU",
                    3: "AS",
                    4: "EU",
                    5: "SA",
                    6: "AF", 
                    7: "NA",
                    9: "EU",
                    10: "AF",
                    14: "OC"
                }
                headers = {
                    "X-Application-Key":
                    f"{settings.G_KEY}",
                }
                response = requests.get(
                    tour_url, headers=headers)
                resource = response.json()
                if tour.region.id != regions[int(resource["geography"]["region"]["id"])]:
                    tour.region=Region.objects.get(
                                pk=regions[int(resource["geography"]["region"]["id"])])
                    tour.save()
                    self.stdout.write(self.style.SUCCESS(
                        f'Tour  {tour.name} already in database, region updated. {tour.id}'))
                else:
                    self.stdout.write(self.style.ERROR(
                        f'Tour  {tour.name} already in database. {tour.id}'))

                    continue
            except Exception as e:
                try:
                    # DOWNLOAD TOUR DATA FOR EACH TOUR AND SAVE
                    tour_url = f"https://rest.gadventures.com/tour_dossiers/{item['id']}"
                    print(tour_url)
                    regions = {
                        1: "AF",
                        2: "AN",
                        3: "AS",
                        4: "EU",
                        5: "SA",
                        6: "OC",
                        7: "NA",
                        9: "EU",
                        10: "AF",
                        14: "OC"
                    }
                    headers = {
                        "X-Application-Key":
                        f"{settings.G_KEY}",
                    }
                    response = requests.get(
                        tour_url, headers=headers)
                    resource = response.json()
                    tour_details = {}
                    tour = Tour(
                        id=resource["id"],
                        href=resource["href"],
                        name=resource["name"],
                        slug=resource["slug"],
                        product_line=resource["product_line"],
                        description=resource["description"],
                        structured_itinerary=resource["structured_itineraries"][0]["href"],
                        details=resource["details"],
                        images=resource["images"],
                        site_links=resource["site_links"],
                        departures_href=resource["departures"]["href"],
                        region=Region.objects.get(
                            pk=regions[int(resource["geography"]["region"]["id"])]),
                        start_country=Country.objects.get(
                            pk=resource["geography"]["start_country"]["id"]),
                        finish_country=Country.objects.get(
                            pk=resource["geography"]["finish_country"]["id"])
                    )
                    itin_response = requests.get(
                        resource["structured_itineraries"][0]["href"], headers=headers)
                    itin_resource = itin_response.json()
                    itinerary = {}
                    for item in itin_resource["days"]:
                        itinerary[item["day"]] = {"summary": item["summary"],
                                                  "label": item["label"]}
                    tour.itinerary = [itinerary]
                    tour.save()
                    for i in resource["categories"]:
                        tour.category.add(
                            Category.objects.get(pk=i["id"]))
                    tour.save()
                    self.stdout.write(self.style.SUCCESS(
                        'Tour  "%s" saved' % tour.name))
                except Exception as e:
                    print("Tour request failed")
                    print(traceback.format_exc())
