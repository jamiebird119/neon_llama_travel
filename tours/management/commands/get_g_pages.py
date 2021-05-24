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
    help = 'Find and tour pages'

    def handle(self, *args, **options):

        try:
            url = "https://rest.gadventures.com/tours?page=1"
            headers = {
                "X-Application-Key":
                f"{settings.G_KEY}",
            }
            response = requests.get(url, headers=headers)
            resource = response.json()
            # CALCULATE NUMBER OF PAGE RESULTS AVAILABLE
            no_pages = math.ceil(
                resource["count"]/resource["max_per_page"])
            page = 1
            while page < no_pages:
                # FOR EACH PAGE RETURN LIST OF TOURS
                page_url = f"https://rest.gadventures.com/tours?page={page}"
                try:
                    page_response = requests.get(
                        page_url, headers=headers)
                    page_resource = page_response.json()
                    # ITERATE THROUGH PAGE RESULTS FOR EACH TOUR ID
                    for item in page_resource["results"]:
                        try:
                            # CHECK IF TOUR IS IN DATABASE
                            tour = Tour.objects.get(
                                pk=item["id"])
                            self.stdout.write(self.style.ERROR(
                                'Tour  "%s" already in database' % tour.name))
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
                                    5: "NA",
                                    6: "OC",
                                    7: "SA",
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

                except Exception as e:
                    print(e)
                    print("Page unavailable")
                page += 1
        except Exception as e:
            print(traceback.format_exc())
            print(e)
