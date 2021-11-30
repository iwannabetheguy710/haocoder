from django.contrib import admin
from .models import *

from martor.widgets import AdminMartorWidget

class ContestAdmin(admin.ModelAdmin):
	formfield_overrides = {
		models.TextField: {'widget': AdminMartorWidget},
	}
class ProblemAdmin(admin.ModelAdmin):
	formfield_overrides = {
		models.TextField: {'widget': AdminMartorWidget},
	}

# Register your models here.
admin.site.register(Contest, ContestAdmin)
admin.site.register(Problem, ProblemAdmin)
admin.site.register(Leaderboard, ProblemAdmin)