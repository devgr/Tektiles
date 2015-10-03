from django.contrib import admin

from companion.models import Catagories, Topics, Fabrics

class CompanionAdmin(admin.ModelAdmin):
	pass

# Register your models here.
admin.site.register(Fabrics, CompanionAdmin)
admin.site.register(Catagories, CompanionAdmin)
admin.site.register(Topics, CompanionAdmin)
