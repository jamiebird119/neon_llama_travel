from django.shortcuts import render, get_object_or_404
from .models import Tour, Country, Region, Category
import json 
from django.conf import settings
import requests

# Create your views here.
def tour_search(request):
    context={
        
    }
    template ='search.html'
    return render(request, template, context)


def tour_details(request, tour_id):
    tour = get_object_or_404(Tour, pk=tour_id)
    images = {}
    details = {}
    itinerary = {}
    for item in json.loads(tour.images):
        images[item["type"]]= item["image_href"]
    for item in tour.category.all():
        details[item.category_type.name.lower().replace(" ", "_")]=item.name
    for item in json.loads(tour.details):
        if item["detail_type"]["label"].lower().replace(" ", "_").replace("'","") == "packing_list":
            details[item["detail_type"]["label"].lower().replace(" ", "_").replace("'","")] = item["body"].split("\n")
        else:
            details[item["detail_type"]["label"].lower().replace(" ", "_").replace("'","")] = item["body"]

    for item in json.loads(tour.itinerary)[0]:
        itinerary[item] = json.loads(tour.itinerary)[0][item]
        
    context={
       'tour': tour,
       "images": images,
       "details": details,
       "itinerary": itinerary
    }
    template="tour_details.html"
    return render(request,template, context)