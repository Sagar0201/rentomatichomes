# created by sagar kakade


from django.urls import path, re_path
from django.views.static import serve
from .import views
from django.contrib.auth import views as auth_views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # account Urls
    path('Contact/', views.Contact, name="Contact"),
    path('AllRentals/', views.AllRentals, name="AllRentals"),
    path('Rentals/', views.Rentals, name="Rentals"),
    path('Search/', views.Search, name="Search"),

    re_path(r'^media/(?P<path>.*)$', serve, {'document_root':settings.MEDIA_ROOT}),
    re_path(r'^static/(?P<path>.*)$', serve, {'document_root':settings.STATICFILES_DIRS[0]}),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
