from django.conf.urls import include, url
from django.contrib import admin

from main import views

urlpatterns = [
    # Examples:
    # url(r'^$', 'receipt.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^receipt-checker/$', views.load),
    url(r'^receipt-checker/admin/', admin.site.urls),
    url(r'^receipt-checker/win-num/', views.win_num),
    url(r'^receipt-checker/full-check/', views.full_check),
]


# static files with ./manage.py runserver
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from receipt import settings
if settings.DEBUG == True:
    urlpatterns += staticfiles_urlpatterns()
