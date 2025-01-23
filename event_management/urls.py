from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from events.views import index,details,dashboard


urlpatterns = [
    path('',index),
    path('details/<int:id>',details,name='details'),
    path('dashboard',dashboard,name="dashboard"),
    path('admin/', admin.site.urls),
    path('events/', include('events.urls')),
]
