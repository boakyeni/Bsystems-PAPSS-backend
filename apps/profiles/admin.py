from django.contrib import admin

from .models import Company, Rep, ContactPerson, Country


# class ProfileAdmin(admin.ModelAdmin):
#     list_display = ["id", "pkid", "user", "phone_number", "country", "city"]
#     list_filter = ["gender", "country", "city"]
#     list_display_links = ["id", "pkid", "user"]


# admin.site.register(Profile, ProfileAdmin)
admin.site.register(Company)
admin.site.register(Rep)
admin.site.register(ContactPerson)
admin.site.register(Country)
