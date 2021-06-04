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
    branded = None
    service_level = None
    physical_grading = None
    travel_style = None
    activity = None
    direction = request.GET.get('direction', None)
    sortkey = request.GET.get('sort', "id")
    current = {}

    if request.method == "POST":
        name = request.POST.get("name", None)
        country = request.POST.get("country", None)
        trip_type = request.POST.get("trip_type", None)
        branded = request.POST.get("branded", None)
        service_level = request.POST.get("service_level", None)
        physical_grading = request.POST.get("physical_grading", None)
        travel_style = request.POST.get("travel_style", None)
        activity = request.POST.get("activity", None)
        page = request.POST.get('page', None)

    if request.method == "GET":
        name = request.POST.get("name", None)
        region = request.GET.get("region", None)
        country = request.GET.get("country", None)
        trip_type = request.GET.get("trip_type", None)
        branded = request.GET.get("branded", None)
        service_level = request.GET.get("service_level", None)
        physical_grading = request.GET.get("physical_grading", None)
        travel_style = request.GET.get("travel_style", None)
        activity = request.GET.get("activity", None)
        page = request.GET.get('page', None)

    if trip_type:
        query = Q(category__name__contains=trip_type) | Q(
            category__name__contains=trip_type)
        qs = qs.filter(query).distinct()
        current["trip_type"] = trip_type
    if branded:
        query = Q(category__name__contains=branded) | Q(
            category__name__contains=branded)
        qs = qs.filter(query).distinct()
        current["branded"] = branded
    if activity:
        query = Q(category__name__contains=activity) | Q(
            category__name__contains=activity)
        qs = qs.filter(query).distinct()
        current["activity"] = activity
    if service_level:
        query = Q(category__name__contains=service_level) | Q(
            category__name__contains=service_level)
        qs = qs.filter(query).distinct()
        current["service_level"] = service_level
    if physical_grading:
        query = Q(category__name__contains=physical_grading) | Q(
            category__name__contains=physical_grading)
        qs = qs.filter(query).distinct()
        current["physical_grading"] = physical_grading
    if travel_style:
        query = Q(category__name__contains=travel_style) | Q(
            category__name__contains=travel_style)
        qs = qs.filter(query).distinct()
        current["travel_style"] = travel_style
    if region:
        query = Q(region=region) | Q(region=region)
        qs = qs.filter(query).distinct()
        region = get_object_or_404(Region, id=region)
    if country:
        query = Q(start_country__name__contains=country) | Q(
            finish_country__name__contains=country)
        qs = qs.filter(query).distinct()
        current["country"] = country
        if not region:
            country_obj = get_object_or_404(Country, name=country)
            region = country_obj.continent
    if name:
        query = Q(tour__name__icontains=name) | Q(tour__name__icontains=name)
        qs = qs.filter(query).distinct()
        current["name"] = name

    if sortkey == 'name':
        sortkey = 'lower_name'
        games = games.annotate(lower_name=Lower('name'))
        if direction == 'desc':
            sortkey = f'-{sortkey}'
    tours = qs.order_by(sortkey)
    current_url="?"
    if current:
        for key, value in current.items():
            string = f"{key}={value}&"
            current_url += string
    responses_no = len(tours)
    paginator = Paginator(tours, 20)
    no_info = False
    if len(tours) == 0:
        no_info = True
    no_of_pages = int(responses_no/20)

    try:
        response = paginator.page(page)
    except PageNotAnInteger:
        response = paginator.page(1)
        page = 1
    except EmptyPage:
        response = paginator.page(paginator.num_pages)

    if page == no_of_pages:
        prev_p = int(page) - 1
        next_p = None
    elif page == 1:
        next_p = 2
        prev_p = None
    else:
        next_p = int(page) + 1
        prev_p = int(page) - 1
    context = {
        'activity': activity,
        'region': region,
        'country': country,
        'name': name,
        'header': header,
        'tours': response,
        'responses_no': responses_no,
        'no_of_pages': no_of_pages,
        'next': next_p,
        'prev': prev_p,
        'page': page,
        'no_info': no_info,
        'branded': branded,
        'service_level': service_level,
        'physical_grading': physical_grading,
        'travel_style': travel_style,
        'current_url': current_url
    }
    template = 'search.html'
    return render(request, template, context)


def tour_details(request, tour_id):
    tour = get_object_or_404(Tour, pk=tour_id)
    images = {}
    details = {}
    itinerary = {}
    try:
        for item in json.loads(tour.images):
            images[item["type"]] = item["image_href"]
        for item in tour.category.all():
            details[item.category_type.name.lower().replace(" ", "_")
                    ] = item.name
        for item in json.loads(tour.details):
            if item["detail_type"]["label"].lower().replace(" ", "_").replace("'", "") == "packing_list":
                details[item["detail_type"]["label"].lower().replace(
                    " ", "_").replace("'", "")] = item["body"].split("\n")
            else:
                details[item["detail_type"]["label"].lower().replace(
                    " ", "_").replace("'", "")] = item["body"]

        for item in json.loads(tour.itinerary)[0]:
            itinerary[item] = json.loads(tour.itinerary)[0][item]
        
        print(details)
        context = {
            'tour': tour,
            "images": images,
            "details": details,
            "itinerary": itinerary
        }
        template = "tour_details.html"
        return render(request, template, context)

    except Exception as e:
        for item in json.loads(json.loads(tour.images)):
            images[item["type"]] = item["image_href"]
        for item in tour.category.all():
            details[item.category_type.name.lower().replace(" ", "_")
                    ] = item.name
        for item in json.loads(json.loads(tour.details)):
            if item["detail_type"]["label"].lower().replace(" ", "_").replace("'", "") == "packing_list":
                details[item["detail_type"]["label"].lower().replace(
                    " ", "_").replace("'", "")] = item["body"].split("\n")
            else:
                details[item["detail_type"]["label"].lower().replace(
                    " ", "_").replace("'", "")] = item["body"]

        for item in json.loads(json.loads(tour.itinerary))[0]:
            itinerary[item] = json.loads(json.loads(tour.itinerary))[0][item]
    print(details)
    context = {
        'tour': tour,
        "images": images,
        "details": details,
        "itinerary": itinerary
    }
    template = "tour_details.html"
    return render(request, template, context)
