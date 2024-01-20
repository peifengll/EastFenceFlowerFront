#!/user/bin/env python3
# -*- coding: utf-8 -*-


from django.urls import path

from flowerInfo.views import FlowerInfos

urlpatterns = [
    path('allinfo/', FlowerInfos.as_view()),
]
