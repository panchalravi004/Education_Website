from locale import currency
from django.shortcuts import redirect, render
from django.http import HttpResponse, JsonResponse
from app.models import Categories, Course, Levels, Payment, UserCourse, Video
from django.template.loader import render_to_string
from django.db.models import Sum
from django.contrib import messages
import razorpay
from .settings import *
from time import time
from django.views.decorators.csrf import csrf_exempt

client = razorpay.Client(auth=(KEY_ID,KEY_SECRET))

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

    courseid = Course.objects.get(slug=slug)
    try:
        check_enroll = UserCourse.objects.get(user= request.user, course=courseid)
    except UserCourse.DoesNotExist:
        check_enroll = None
    

    if course.exists():
        data = {
            'course':course.first,
            'category':category,
            'time_duration':time_duration,
            'check_enroll':check_enroll,
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

def CHECKOUT(request,slug):

    print(slug)
    course = Course.objects.get(slug=slug)
    action = request.GET.get('action')    
    order = None

    if course.price == 0:
        course = UserCourse(
            user = request.user,
            course = course,
        )
        course.save()
        messages.success(request,"Course Are Enrolled Successfully !")
        return redirect('mycourse')
    elif action == "create_payment":
        if request.method == "POST":
            first_name = request.POST.get('billing_first_name')
            last_name = request.POST.get('billing_last_name')
            country = request.POST.get('billing_country')
            add_1 = request.POST.get('billing_address_1')
            add_2 = request.POST.get('billing_address_2')
            city = request.POST.get('billing_city')
            state = request.POST.get('billing_state')
            postcode = request.POST.get('billing_postcode')
            phone = request.POST.get('billing_phone')
            email = request.POST.get('billing_email')
            order_comments = request.POST.get('order_comments')

            amount_cal = course.price - (course.price * course.discount / 100)
            amount = int(amount_cal) * 100


            currency = "INR"
            notes = {
                "name":f'{first_name} {last_name}',
                "country":country,
                "address":f'{add_1} {add_2}',
                "city":city,
                "state":state,
                "postcode":postcode,
                "phone":phone,
                "email":email,
                "order_comments":order_comments,
            }

            receipt = f"Skola-{int(time())}"

            order = client.order.create({
                'receipt':receipt,
                'notes':notes,
                'amount':amount,
                'currency':currency,
            })

            payment = Payment(
                course=course,
                user=request.user,
                order_id=order.get('id')
            )
            payment.save()

    data = {
        'course':course,
        'order':order,
    }
    return render(request,'checkout/checkout.html',data)

@csrf_exempt
def VERIFY_PAYMENT(request):
    if request.method == "POST":
        data = request.POST
        # print(data)
        try:
            client.utility.verify_payment_signature(data)
            razorpay_order_id = data['razorpay_order_id']
            razorpay_payment_id = data['razorpay_payment_id']

            payment = Payment.objects.get(order_id = razorpay_order_id)
            payment.payment_id = razorpay_payment_id
            payment.status = True

            usercourse = UserCourse(
                user = payment.user,
                course = payment.course,
            )

            usercourse.save()
            payment.user_course = usercourse
            payment.save()
            context = {
                'data':data,
                'payment':payment,
            }
            return render(request,'verify_payments/success.html',context)

        except:
            return render(request,'verify_payments/fail.html')
            

def MYCOURSE(request):
    course = UserCourse.objects.filter(user=request.user)
    category = Categories.objects.all().order_by('id')[0:5]
    
    data = {
        'course':course,
        'category':category,
    }

    return render(request,'course/mycourse.html',data)