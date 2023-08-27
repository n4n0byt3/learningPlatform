"""
URL configuration for learningplatform project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path
from django.views.generic import TemplateView
from accounts.views import user_views
from accounts.views import subject_views

urlpatterns = [
    path('admin/', admin.site.urls),
    re_path(r'^.*', TemplateView.as_view(template_name='index.html')),

    path('register/', user_views.register_new_account, name='register_new_account'),
    path('verify-email/<str:verification_token>/', user_views.verify_user_email, name='verify_user_email'),
    path('login/', user_views.login_user, name='login_user'),
    path('logout/', user_views.logout_user, name='logout_user'),
    path('forgotten-password/', user_views.forgotten_password, name='forgotten_password'),
    path('profile/<str:username>/', user_views.view_user_profile, name='view_user_profile'),
    path('edit-profile/', user_views.edit_user_profile, name='edit_user_profile'),
    path('change-password/', user_views.change_password, name='change_password'),

    path('all-subjects/', subject_views.get_all_subjects, name='get_all_subjects'),
    path('select-subjects/', subject_views.select_subjects, name='select_subjects'),
    path('update-selected-subjects/', subject_views.update_selected_subjects, name='update_selected_subjects'),

    # Other URL patterns
    # Add more URL patterns as needed
]