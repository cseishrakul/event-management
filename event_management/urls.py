from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from events.views import details,admin_dashboard,all_events
from core.views import index,no_permission,aboutPage,blogPage,contactPage
from debug_toolbar.toolbar import debug_toolbar_urls
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('',index,name='home'),
    path('events/', all_events, name='all_events'),
    path('about/', aboutPage, name='aboutPage'),
    path('blog/', blogPage, name='blogPage'),
    path('contact/', contactPage, name='contactPage'),
    path('details/<int:id>',details,name='details'),
    path('admin/dashboard/',admin_dashboard,name="ad-dashboard"),
    path('admin/', admin.site.urls),
    path('events/', include('events.urls')),
    path('users/', include('users.urls')),
    path('no-permission/',no_permission,name='no-permission')
]+ debug_toolbar_urls()

urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)