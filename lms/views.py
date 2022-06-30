from django.shortcuts import redirect, render
from django.http import HttpResponse
from app.models import Categories, Course

def BASE(request):
    return render(request,'base.html')

def HOME(request):

    category = Categories.objects.all().order_by('id')[0:5]
    course = Course.objects.filter(status="PUBLISH").order_by('-id')
    
    data = {
        'category':category,
        'course':course,
    }
    return render(request,'Main/home.html',data)

def SINGLE_COURSE(request):
    return render(request,'Main/single_course.html')

def CONTACT(request):
    return render(request,'Main/contact_us.html')
    
def ABOUT(request):
    return render(request,'Main/about_us.html')
