from django.contrib import admin
from app.models import Categories

# Register your models here.
class CategoriesAdmin(admin.ModelAdmin):
    list_display = ('icon','name')
admin.site.register(Categories,CategoriesAdmin)