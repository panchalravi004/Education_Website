from django.shortcuts import redirect, render
from django.http import HttpResponse

def BASE(request):
    return render(request,'base.html')