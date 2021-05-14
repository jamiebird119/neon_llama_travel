from django.core.management.base import BaseCommand, CommandError
from tours.models import Category, Country, Region, Tour
from django.conf import settings
import requests
import json
import traceback


class Command(BaseCommand):
    help = 'Find and save tour data'

    def handle(self, *args, **options):
        regions = {
            1: "AF",
            2: "AN",
            3: "AS",
            4: "EU",
            5: "NA",
            6: "OC",
            7: "SA",
        }
        try:
            url = "https://rest.gadventures.com/tour_dossiers/22997"
            headers = {
                "X-Application-Key":
                f"{settings.G_KEY}",
            }
            response = requests.get(url, headers=headers)
            resource = response.json()
            tour_details = {}
            try:
                tour = Tour.objects.get(pk=resource["id"])
                return resource["id"]

            except Exception as err:
                print(err)
                print(regions[int(resource["geography"]["region"]["id"])])
                tour = Tour(
                    id=resource["id"],
                    href=resource["href"],
                    name=resource["name"],
                    slug=resource["slug"],
                    product_line=resource["product_line"],
                    departures_start_date=resource["departures_start_date"],
                    departures_end_date=resource["departures_end_date"],
                    description=resource["description"],
                    structured_itineraries=resource["structured_itineraries"][0]["href"],
                    details=resource["details"],
                    images=resource["images"],
                    site_links=resource["site_links"],
                    tour=resource["id"],
                    departures_href=resource["departures"]["href"],
                    region=Region.objects.get(
                        pk=regions[int(resource["geography"]["region"]["id"])]),
                    start_country=Country.objects.get(
                        pk=resource["geography"]["start_country"]["id"]),
                    finish_country=Country.objects.get(
                        pk=resource["geography"]["finish_country"]["id"])
                )
                tour.save()
                for i in resource["categories"]:
                    tour.category.add(Category.objects.get(pk=i["id"]))
                tour.save()
                print("all saved")
        except Exception as err:
            print(err)
