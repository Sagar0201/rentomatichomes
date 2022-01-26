# created by sagar kakade


from django.urls import path,re_path
from django.views.static import serve
from .import views
from django.contrib.auth import views as auth_views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # account Urls
    path('SignUp/', views.SignUp, name="SignUp"),
    path('Login/', views.Login, name="Login"),
    path('SignOut/', views.SignOut, name="SignOut"),
    path('AddHome/', views.AddHome, name="AddHome"),
    path('Profile/', views.Profile, name="Profile"),
    path('Message/', views.Message, name="Message"),
    path('Message_Chat/', views.Message_Chat, name="Message_Chat"),


    # for forget password
    path('reset_password/', auth_views.PasswordResetView.as_view(
        template_name="oners/Accounts/reset_password.html"), name='reset_password'),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(
        template_name="oners/Accounts/password_reset_sent.html"), name='password_reset_done'),
    path('reset/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(
        template_name="oners/Accounts/password_reset_form.html"), name='password_reset_confirm'),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(
        template_name="oners/Accounts/password_reset_done.html"), name='password_reset_complete'),
    path('change_password/', auth_views.PasswordChangeView.as_view(
        template_name="oners/Accounts/change_password.html"), name='change_password'),
    path('password_change_done/', auth_views.PasswordChangeDoneView.as_view(
        template_name="oners/Accounts/password_change_done.html"), name='password_change_done'),

    path('change_password/', auth_views.PasswordChangeView.as_view(
        template_name="oners/Accounts/change_password.html"), name='change_password'),
    path('password_change_done/', auth_views.PasswordChangeDoneView.as_view(
        template_name="oners/Accounts/password_change_done.html"), name='password_change_done'),

    re_path(r'^media/(?P<path>.*)$', serve, {'document_root':settings.MEDIA_ROOT}),
    re_path(r'^static/(?P<path>.*)$', serve, {'document_root':settings.STATICFILES_DIRS[0]}),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
