from django.urls import path
from . import views
from django.conf.urls import static
from django.conf import settings

urlpatterns = [
    path('', views.index, name='learnerahome'),
    path('allcourses/', views.allcourses, name='allcourses'),
    path('CourseDetail/<int:id>', views.coursedetail, name='coursedetail'),
    path('dashboard/<str:id>',views.dashboard,name='dashboard'),
    path('contact/',views.contact,name='contact'),
    path('about/',views.about,name='about'),
    path('checkout/',views.checkout,name='checkout'),
]
