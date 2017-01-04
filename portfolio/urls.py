from django.conf.urls import url
from portfolio import views

urlpatterns = [
        url(r'^$', views.index, name='index'),
        url(r'^about/$', views.about, name='about'),
        url(r'add_category/$', views.add_category, name='add_category'),
        url(r'^category/(?P<category_name_slug>[\w\-]+)/$', views.show_category, name = 'show_category'),
        url(r'^category/(?P<category_name_slug>[\w\-]+)/add_product/$', views.add_product, name = 'add_product'),
        url(r'^restricted/$', views.restricted, name = 'restricted'),
        url(r'^goto/$', views.track_url, name='goto'),
        url(r'^like/$', views.like_category, name='like_category'),
        url(r'^suggest/$', views.suggest_category, name='suggest_category'),

            ]
