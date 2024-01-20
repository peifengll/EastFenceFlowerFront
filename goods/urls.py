#!/user/bin/env python3
# -*- coding: utf-8 -*-


from django.urls import path

from goods.views import GoodsInfo

urlpatterns = [
    path('allinfo/', GoodsInfo.as_view()),
]
