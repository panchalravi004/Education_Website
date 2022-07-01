from django.contrib import admin
from app.models import Author, Categories, Course, Levels, Payment, Requirements, UserCourse, What_you_learn, Lesson, Video, Language

# Register your models here.
class CategoriesAdmin(admin.ModelAdmin):
    list_display = ('icon','name')

class What_you_learn_Tubelar(admin.TabularInline):
    model = What_you_learn

class Requirements_Tubelar(admin.TabularInline):
    model = Requirements

class Video_Tubelar(admin.TabularInline):
    model = Video

class Lesson_Tubelar(admin.TabularInline):
    model = Lesson

class CourseAdmin(admin.ModelAdmin):
    inlines = (What_you_learn_Tubelar,Requirements_Tubelar,Video_Tubelar,Lesson_Tubelar)



admin.site.register(Categories,CategoriesAdmin)
admin.site.register(Course,CourseAdmin)
admin.site.register(Author)
admin.site.register(Levels)
admin.site.register(Requirements)
admin.site.register(Lesson)
admin.site.register(What_you_learn)
admin.site.register(Language)
admin.site.register(UserCourse)
admin.site.register(Payment)