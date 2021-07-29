from django.urls import path
from . import views
from django.conf.urls import static
from django.conf import settings
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', views.index, name='learnerahome'),
    #path('signup/', views.signup, name='learnerasignup'),
    path('allcourses/', views.allcourses, name='allcourses'),
    path('CourseDetail/<int:id>', views.coursedetail, name='coursedetail'),
    path('dashboard/<str:id>',views.dashboard,name='dashboard'),
    path('contact/',views.contact,name='contact'),
    path('about/',views.about,name='about'),
    path('checkout/',views.checkout,name='checkout'),
    path('handlerequest/<str:id>',views.handlerequest,name='handlerequest'),
    path('logout', LogoutView.as_view(), name="logout"),
    path('search/',views.search,name='search'),
]
