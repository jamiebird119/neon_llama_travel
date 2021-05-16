from django.contrib import admin
from .models import Tour, Region, Category, Country


class TourAdmin(admin.ModelAdmin):
    fields = (
        "id",
        "href",
        "name",
        "departures_start_date",
        "departures_end_date",
        "category",
        "tour",
        'details',
        'description',
        'images',
        'site_links',
        "departures_href",
        "departures_list",
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
        "name"
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

