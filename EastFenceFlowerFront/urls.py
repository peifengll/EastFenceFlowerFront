"""
URL configuration for EastFenceFlowerFront project.

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
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from EastFenceFlowerFront.views import HomeView

urlpatterns = [
                  path('', HomeView.as_view(), name='home'),
                  path('admin/', admin.site.urls),
                  path('flower/', include('flowerInfo.urls'), name='flower info'),
                  path('goods/', include('goods.urls'), name='goods info'),
                  path('user/', include('user.urls'), name='user info'),
                  path('cart/', include('cart.urls'), name='cart info'),
                  path('address/', include('address.urls'), name='address info'),
                  path('likes/', include('likes.urls'), name='likes info'),
                  path('order/', include('order.urls'), name='order info'),
                  path('chat/', include('chat.urls'), name='chat record'),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
