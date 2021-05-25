from django.shortcuts import render, get_object_or_404
from .models import Tour, Country, Region, Category
import json 
from django.db.models import Q
from django.conf import settings
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import requests

# Create your views here.
def tour_search(request):
    direction = None
    sort = "id"
    sortkey = sort
    qs = Tour.objects.all()
    region = None
    country = None
    name = None
    if request.GET:
        if "region" in request.GET:
            region = request.GET['region']
            print(region)
            query = Q(region__id__contains=region)
            qs = qs.filter(query).distinct()
            print(qs)
        if "country" in request.GET:
            country = request.GET['country']
        if "name" in request.GET:
            name = request.GET['name']
        
        if 'sort' in request.GET:
            sortkey = request.GET['sort']
            sort = sortkey
            if sortkey == 'name':
                sortkey = 'lower_name'
                games = games.annotate(lower_name=Lower('name'))
            if sortkey == 'genre':
                sortkey = 'genre__name'
            if 'direction' in request.GET:
                direction = request.GET['direction']
                if direction == 'desc':
                    sortkey = f'-{sortkey}'
            tours = qs.order_by(sortkey)

    tours = qs.order_by(sortkey)
    paginator = Paginator(tours, 10)
    page = request.GET.get('page')
    try:
        response = paginator.page(page)
    except PageNotAnInteger:
        response = paginator.page(1)
    except EmptyPage:
        response = paginator.page(paginator.num_pages)
    context={
        'tours': response,
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