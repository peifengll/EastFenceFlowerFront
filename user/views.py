from datetime import time

from django.shortcuts import render
from django.utils import timezone
from rest_framework import serializers
from rest_framework.views import APIView

import models.models
from libs.utils.base_response import BaseResponse
from user.serializers import UserInfoSerializer


# Create your views here.


class LoginView(APIView):

    def post(self, request):
        user = request.POST.get('user')
        pwd = request.POST.get('pwd')
        print(user, pwd)
        try:
            user = models.models.User.objects.get(phone=user, keyword=pwd)
        except:
            raise serializers.ValidationError("No user found with this username and password.")
        if user == None:
            return BaseResponse(data={'msg': '用户名或密码错误'}, status=203)
        u=UserInfoSerializer(user)
        print(user)
        return BaseResponse(data={'msg': '登录成功','user':u.data}, status=200)


class RegisterView(APIView):
    def post(self, request):
        user = request.POST.get('username')
        pwd = request.POST.get('password')
        if user == "" or user==None or pwd==None or pwd == "":
            return BaseResponse(data={'msg': '手机号或者密码缺失'}, status=202)

        t = None
        try:
            t = models.models.User.objects.get(phone=user)
        except:
            raise "发生巨大报错"
        if t is not None:
            return BaseResponse(data={'msg': '该手机号已经被注册'}, status=201)
        # try:
        today = timezone.now().date()
        a = models.models.User.objects.create(phone=user, keyword=pwd, uname="未命名", time=today, sex='男')
        # except:
        #     raise "注册发生错误"
        print(a)

        return BaseResponse(data={'msg': '注册成功'}, status=200)
