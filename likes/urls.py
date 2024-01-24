#!/user/bin/env python3
# -*- coding: utf-8 -*-
from django.urls import path

from likes.views import LikesAddView, LikesDelView, LikesShowView

urlpatterns = [
    path('add', LikesAddView.as_view()),
    path('delete', LikesDelView.as_view()),
    path('allinfo', LikesShowView.as_view()),
]
