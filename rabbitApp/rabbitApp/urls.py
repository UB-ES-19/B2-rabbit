"""rabbitApp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from rabbit import views
from rabbitApp import settings

urlpatterns = [ 
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', views.login_user, name='login'),
    path('submit', views.create_post, name='submit'),
    path('logout',views.logout_user, name='logout'),
    path('imgsubmit/', views.post_img, name='img_submit'),
    path('linksubmit/', views.post_link, name='link_submit'),
    path('warrensubmit', views.create_warren, name='warren_submit'),
    path('search', views.search, name='search'),
    path('w/<str:name>/', views.warren, name='warren'),
    path('w/<str:name>', views.warren, name='warren'),
    path('r/<str:name>/', views.profile, name='profile'),
    path('r/<str:name>', views.profile, name='profile'),
    path('delete/<str:id>',views.delete, name='delete'),
    path('follow/', views.follow, name='follow'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
