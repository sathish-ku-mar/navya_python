"""navya URL Configuration

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
from django.contrib import admin
from django.urls import path
from .views import UserViewSet
urlpatterns = [
    path('admin/', admin.site.urls),
    path(r'user/<slug:id>/', UserViewSet.as_view({'get': 'get_user_permissions'})),
    path(r'checkpermission/', UserViewSet.as_view({'get': 'get_checkpermission'})),
    path(r'roles/<slug:roleid>/', UserViewSet.as_view({'post': 'modify_permissions_of_role'})),
    path(r'permissions/<slug:permission_id>/', UserViewSet.as_view({'delete': 'delete_permission'})),
]
