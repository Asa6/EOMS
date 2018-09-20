"""EOMS URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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

# from django.contrib import admin
from django.urls import path

from cmdb.views import Login
from cmdb.views import Admin
from cmdb.views import Register
from cmdb.views import Hosts
from cmdb.views import Page_not_found
from cmdb.views import UserManager
from cmdb.views import Test

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('login', Login.as_view()),
    path('admin', Admin.as_view()),
    path('register', Register.as_view()),
    path('hosts', Hosts.as_view()),
    path('user_manager', UserManager.as_view()),
    path('test', Test.as_view()),

]

handler404 = Page_not_found.as_view()
