#!/user/bin/env python3
# -*- coding: utf-8 -*-


from django.urls import path

from flowerInfo.views import FlowerInfos, FlowerSort, FlowerAsGoods

urlpatterns = [
    path('allinfo/', FlowerInfos.as_view()),
    path('sort/', FlowerSort.as_view()),
    path('detail/', FlowerAsGoods.as_view()),
]
