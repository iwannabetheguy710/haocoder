from django.contrib import admin

from .models import *

class ProfileAdmin(admin.ModelAdmin):
	search_fields = ['user__username']
	autocomplete_fields = ["user"]

# Register your models here.
admin.site.register(Profile, ProfileAdmin)