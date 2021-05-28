from .models import Category, Region, Country
from django.shortcuts import get_object_or_404


def geography(request):
    continents = Region.objects.all()
    countries = Country.objects.all()
    geog = {}
    region_geog = {}
    for cont in continents:
        local = countries.filter(continent=cont).order_by("name")
        cont_countries = []
        for item in local:
            cont_countries.append(item)
        region_geog[cont] = cont_countries
    geog["countries"] = countries
    geog["continents"] = continents
    geog["region_geog"] = region_geog
    return geog


def category(request):
    categories = {}
    category = Category.objects.all()
    control = get_object_or_404(Category, name="Control")
    types = category.filter(category_type=control)   
    for item in types:
        item_vars = []
        filtered = category.filter(category_type=item)
        for cat in filtered:
            item_vars.append(cat)
        categories[item.name.lower().replace(" ","_")] = item_vars
    return categories