from django.urls import  path,include
from django.contrib import  admin
from accounts import urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(urls))
]
