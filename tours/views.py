from django.shortcuts import render, get_object_or_404
from .models import Tour, Country, Region, Category
import json 
from django.db.models import Q
from django.conf import settings
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import requests

# Create your views here.
def tour_search(request):
    qs = Tour.objects.all()
    region = None
    country = None
    name = None
    header = None
    trip_type = None
    direction = request.GET.get('direcition', None)
    sortkey = request.GET.get('sort', "id")

    if request.method == "POST":
        name = request.POST.get("name", None)
        country = request.POST.get("country", None)
        trip_type = request.POST.get("trip_type",None)
    
    if request.method == "GET":
        region = request.GET.get("region", None)
        country = request.GET.get("country", None)


    if trip_type:
        print(f"trip_type: {trip_type}")
        query = Q(category__name__contains=trip_type)| Q(category__name__contains=trip_type)
        qs = qs.filter(query).distinct()
    if region:
        query = Q(region__contains=region)| Q(region__contains=region)
        qs = qs.filter(query).distinct()
    if country:
        print(f"country: {country}")
        query = Q(start_country__name__contains=country)| Q(finish_country__name__contains=country)
        qs = qs.filter(query).distinct()
        if not region:
                country_obj = get_object_or_404(Country, name=country)
                region = country_obj.continent
    if name:
        query = Q(tour__name__icontains=name)| Q(tour__name__icontains=name)
        qs = qs.filter(query).distinct()

    if sortkey == 'name':
        sortkey = 'lower_name'
        games = games.annotate(lower_name=Lower('name'))
        if direction == 'desc':
            sortkey = f'-{sortkey}'
    tours = qs.order_by(sortkey)

    responses_no = len(tours)
    paginator = Paginator(tours, 10)
    page = request.GET.get('page')
    try:
        response = paginator.page(page)
    except PageNotAnInteger:
        response = paginator.page(1)
    except EmptyPage:
        response = paginator.page(paginator.num_pages)
    context={
        'region':region,
        'country':country,
        'name':name,
        'header': header,
        'tours': response,
        'responses_no': responses_no
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