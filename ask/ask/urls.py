"""ask URL Configuration

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
from qa.views import test, main, popular, question, ask, login_view, signup_view,\
                    logout_view, delete, user_view

urlpatterns = [
    path('', main, name='main'),
    path('admin/', admin.site.urls),
    path('login/', login_view, name='login'),
    path('signup/', signup_view, name='signup'),
    path('logout/', logout_view, name='logout'),
    path('question/<int:id>/', question, name='question'),
    path('ask/', ask, name='ask'),
    path('popular/', popular, name='popular'),
    path('new/', test, name='test'),
    path('delete/', delete, name='delete'),
    path('user/<str:nickname>', user_view, name='user'),
]
