from django.shortcuts import redirect, render
from django.http import HttpResponse, JsonResponse
from app.models import Categories, Course, Levels, Video
from django.template.loader import render_to_string
from django.db.models import Sum

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

    category = Categories.get_all_category(Categories)
    course = Course.objects.filter(status="PUBLISH").order_by('id')
    level = Levels.objects.all()

    freecourse_count = Course.objects.filter(price=0).count()
    paidcourse_count = Course.objects.filter(price__gte=1).count()

    data = {
        'category':category,
        'level':level,
        'course':course,
        'freecourse_count':freecourse_count,
        'paidcourse_count':paidcourse_count,
    }

    return render(request,'Main/single_course.html',data)

def FILLTER_DATA(request):

    category = request.GET.getlist('category[]')
    level = request.GET.getlist('level[]')
    price = request.GET.getlist('price[]')
    sort = request.GET.getlist('sort[]')

    print(sort)

    if price ==["priceFree"]:
        course = Course.objects.filter(price=0)

    elif price ==["pricePaid"]:
        course = Course.objects.filter(price__gte=1)
        
    elif price ==["priceAll"]:
        course = Course.objects.all()
        
    elif category:
        course = Course.objects.filter(category__id__in=category).order_by('-id')
    elif level:
        course = Course.objects.filter(level__id__in=level).order_by('-id')
    
    else:
        course = Course.objects.all().order_by('-id')

    data  = {
        'course':course
    }
    t = render_to_string('ajax/course.html',data)

    return JsonResponse({'data': t})

def CONTACT(request):
    category = Categories.objects.all().order_by('id')[0:5]
    data = {
        'category':category,
    }

    return render(request,'Main/contact_us.html',data)
    
def ABOUT(request):
    category = Categories.objects.all().order_by('id')[0:5]
    data = {
        'category':category,
    }
    return render(request,'Main/about_us.html',data)

def COURSE_DETAIL(request,slug):

    course = Course.objects.filter(slug=slug)
    category = Categories.objects.all().order_by('id')[0:5]
    time_duration = Video.objects.filter(course__slug=slug).aggregate(sum=Sum('time_duration'))

    if course.exists():
        data = {
            'course':course.first,
            'category':category,
            'time_duration':time_duration,
        }

        return render(request,'course/course_details.html',data)
    else:
        return redirect('404')

def PAGE_NOT_FOUND(request):
    category = Categories.objects.all().order_by('id')[0:5]
    data = {
        'category':category,
    }
    return render(request,'error/error.html',data)

def SEARCH_COURSE(request):
    
    query = request.GET.get('query')

    category = Categories.objects.all().order_by('id')[0:5]
    course = Course.objects.filter(title__icontains = query)
    print(course)
    data = {
        'course':course,
        'category':category,
    }

    return render(request,'search/search.html',data)
