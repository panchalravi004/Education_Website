from django.contrib import admin
from app.models import Author, Categories, Course, Levels

# Register your models here.
class CategoriesAdmin(admin.ModelAdmin):
    list_display = ('icon','name')
admin.site.register(Categories,CategoriesAdmin)
admin.site.register(Course)
admin.site.register(Author)
admin.site.register(Levels)