from django.contrib import admin
from .models import Pollutants, ConfirmedPollutants



class PollutantsAdmin(admin.ModelAdmin):
    #readonly_fields = ["created_on", "category", "lat", "long","location", "district"]
    search_fields = ["village","suburb","location", "city_district","state","district","address"]
    list_display = ["created_on", "category", "lat", "long","village","suburb","location","city_district","state", "district","count","address","country"]
    pass


class ConfirmedPollutantsAdmin(admin.ModelAdmin):
    #readonly_fields = ["created_on", "pollutant_category", "pollutant_location", "pollutant_district", "shores","total"]
    #list_display = ["created_on", "pollutant__category", "pollutant_location", "pollutant_district", "shores","total"]
    #list_display = ["created_on","pollutant_id","pollutant_category","pollutant_location","pollutant_district", "shores","total"]
    list_display = ["created_on","pollutant_category","pollutant_location","pollutant_district", "shores","total"]

    def pollutant_category(self, obj):
        return obj.pollutant.category
    def pollutant_location(self, obj):
        return obj.pollutant.location
    def pollutant_district(self, obj):
        return obj.pollutant.district
    pass

#admin.site.unregister(Pollutants)
admin.site.site_header = 'Lawuna Project Administration'
admin.site.register(Pollutants, PollutantsAdmin)
admin.site.register(ConfirmedPollutants, ConfirmedPollutantsAdmin)
