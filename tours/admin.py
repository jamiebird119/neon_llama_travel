from django.contrib import admin
from .models import Tour, Region, Category, Country, Geography

# Register your models here.


class TourAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "href",
        "name",
        "slug",
        "product_line",
        "departures_start_date",
        "departures_end_date",
        "description",
        "booking_company",
        "structured_itineraries",
        "category",
        "details",
        "images",
        "site_links",
        "tour",
        "departures_href",
        "departures_list",
        "from_price"
    )

    ordering = ()


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

class GeographyAdmin(admin.ModelAdmin):
    list_display = (
         "geograpy",
         "region",
         "primary_country",
         "start_country",
         "finish_country"
    )

admin.site.register(Tour, TourAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Country, CountryAdmin)
admin.site.register(Region, RegionAdmin)
admin.site.register(Geography, GeographyAdmin)
