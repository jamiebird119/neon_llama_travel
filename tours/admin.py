from django.contrib import admin
from .models import Tour, Region, Category, Country


class TourAdmin(admin.ModelAdmin):
    fields = (
        "id",
        "href",
        "name",
        "category",
        'details',
        'description',
        'images',
        'itinerary',
        'site_links',
        "from_price",
        "region",
        "start_country",
        "finish_country",
        "visited_countries"
    )
    list_display = (
        "id",
        "name",
        "start_country",
        "finish_country",
        "region",
        "departures_list",
        "from_price"
    )

    ordering = ("name",)


class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "href",
        "name",
        "description",
        "category_type"
    )


class CountryAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "href",
        "name",
        "continent"
    )


class RegionAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "href",
        "name"
    )


admin.site.register(Tour, TourAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Country, CountryAdmin)
admin.site.register(Region, RegionAdmin)

