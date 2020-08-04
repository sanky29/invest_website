from . import views
from django.urls import path

urlpatterns = [
    path('', views.home),
    path('register/',views.UserSignUpView.as_view(), name='register'),
    path('email/', views.verify_email),
    path('login/', views.signinview, name='login'),
    path('submit/', views.Submit),
    path('home/', views.page),
    path('logout/',views.logoutview, name='logout'),
    path('general/',views.generalview, name='general')
]
