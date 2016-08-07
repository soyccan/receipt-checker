from django.conf.urls import patterns, include, url
from django.contrib import admin

from main import views

urlpatterns = [
    # Examples:
    # url(r'^$', 'receipt.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^receipt-checker/$', views.load),
    url(r'^receipt-checker/admin/', include(admin.site.urls)),
    url(r'^receipt-checker/win-num/', views.win_num),
    url(r'^receipt-checker/full-check/', views.full_check),
]
