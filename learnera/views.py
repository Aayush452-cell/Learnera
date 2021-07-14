from django.shortcuts import render
from django.http import HttpResponse
from .models import allcourse,profile
from math import ceil
from django.dispatch import receiver
from allauth.account.signals import user_logged_in,user_signed_up


# Create your views here.

def index(request):
    return render(request, 'learnera/index.html')

def contact(request):
    return render(request, 'learnera/contact.html')

def about(request):
    return render(request, 'learnera/about.html')

def checkout(request):
    return render(request, 'learnera/checkout.html')

def allcourses(request):
    courses = []
    course = allcourse.objects.values('category', 'id')
    cours = {item['category'] for item in course}
    for cs in cours:
        cst = allcourse.objects.filter(category=cs)
        n = len(cst)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))
        courses.append([cst, range(1, nSlides), nSlides])
    params = {'courses': courses}
    return render(request, 'learnera/allcourses.html', params)

@receiver(user_logged_in)
def populate_profile(request,sociallogin , user, **kwargs):
    if sociallogin.account.provider == 'google':
        user_data = user.socialaccount_set.filter(provider='google')[0].extra_data
        print(user_data)
        picture_url = user_data['picture']
        email = user_data['email']
        name = user_data['name']
        u_id = user_data['id']
        Profile = profile(name=name,email=email,picture_url=picture_url,u_id=u_id)
        Profile.save()

@receiver(user_signed_up)
def populate_profile(request,sociallogin , user, **kwargs):
    if sociallogin.account.provider == 'google':
        user_data = user.socialaccount_set.filter(provider='google')[0].extra_data
        print(user_data)
        picture_url = user_data['picture']
        email = user_data['email']
        name = user_data['name']
        u_id = user_data['id']
        Profile = profile(name=name,email=email,picture_url=picture_url,u_id=u_id)
        Profile.save()


def coursedetail(request, id):
    course = allcourse.objects.filter(id=id)
    return render(request, 'learnera/CourseDetail.html', {'course': course[0]})


def dashboard(request,id):
    Profile = profile.objects.filter(u_id=id)
    return render(request,'learnera/dashboard.html',{'Profile':Profile})