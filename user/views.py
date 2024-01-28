import time as time_
from datetime import time

import numpy as np
from django.http import HttpResponse
from django.shortcuts import render
from django.utils import timezone
from rest_framework import serializers
from rest_framework.views import APIView

import models.models
from EastFenceFlowerFront import settings
from address.serializers import AddressInfoSerializer
from libs.utils.base_response import BaseResponse
from user.serializers import UserInfoSerializer


# Create your views here.


class LoginView(APIView):

    def post(self, request):
        user = request.POST.get('username')
        pwd = request.POST.get('password')
        print(user, pwd)
        try:
            user = models.models.User.objects.get(phone=user, keyword=pwd)
        except:
            raise serializers.ValidationError("No user found with this username and password.")
        if user is None:
            return BaseResponse(data={'msg': '用户名或密码错误'}, status=203)
        u = UserInfoSerializer(user)
        print(user)
        adds = models.models.Address.objects.filter(u_id=user.user_id)
        ser = AddressInfoSerializer(adds, many=True)
        return BaseResponse(msg='登录成功', data={'address': ser.data, 'user': u.data}, status=200)


class RegisterView(APIView):
    def post(self, request):
        user = request.POST.get('username')
        pwd = request.POST.get('password')
        if user == "" or user == None or pwd == None or pwd == "":
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


class UploadView(APIView):
    def post(self, request):
        print("403????")
        # 获取一个文件管理器对象
        userid = request.data.get('user_id')
        if userid is None or userid == "":
            return BaseResponse(msg="用户凭证未获取到", status=401)
        file = None
        if 'pic' in request.FILES:
            file = request.FILES['pic']
        # if file is None:
        #     return BaseResponse(msg="图片未获取到", status=308)
        phone = request.data.get('phone')
        nickname = request.data.get('nickname')
        age = request.data.get('age')
        location = request.data.get('location')
        email = request.data.get('email')
        gender = request.data.get('gender')
        bio = request.data.get('bio')
        print(phone, nickname, age, location, email, gender, bio)
        try:
            obj = models.models.User.objects.filter(user_id=userid)
            if phone:
                obj.update(phone=phone)
            if nickname:
                obj.update(uname=nickname)
            if age:
                obj.update(age=age)
            if location:
                obj.update(address=location)
            if email:
                obj.update(e_mail=email)
            if gender:
                obj.update(sex=gender)
            if bio:
                obj.update(intor=bio)
            # 保存文件
            if file is not None:
                new_name = getNewName('avatar')  # 具体实现在自己写的uploads.py下
                # 将要保存的地址和文件名称
                where = '%s/users/%s' % (settings.MEDIA_ROOT, new_name)
                # 分块保存image
                content = file.chunks()
                with open(where, 'wb') as f:
                    for i in content:
                        f.write(i)

                # 上传文件名称到数据库
                obj.filter(user_id=1).update(photo=new_name)
            # 返回的httpresponse
        except Exception as e:
            return BaseResponse(msg="服务器内部错误", status=500)
        return BaseResponse(msg="返回成功", status=200, data={})


# def upload_handle(request):
#     print("403????")
#     # 获取一个文件管理器对象
#     file = request.FILES['pic']
#
#     # 保存文件
#     new_name = getNewName('avatar')  # 具体实现在自己写的uploads.py下
#     # 将要保存的地址和文件名称
#     where = '%s/users/%s' % (settings.MEDIA_ROOT, new_name)
#     # 分块保存image
#     content = file.chunks()
#     with open(where, 'wb') as f:
#         for i in content:
#             f.write(i)
#
#     # 上传文件名称到数据库
#     models.models.User.objects.filter(user_id=1).update(photo=new_name)
#     # 返回的httpresponse
#     return HttpResponse('ok')


def getNewName(file_type):
    # 前面是file_type+年月日时分秒
    new_name = time_.strftime(file_type + '-%Y%m%d%H%M%S', time_.localtime())
    # 最后是5个随机数字
    # Python中的numpy库中的random.randint(a, b, n)表示随机生成n个大于等于a，小于b的整数
    ranlist = np.random.randint(0, 10, 5)
    for i in ranlist:
        new_name += str(i)
    # 加后缀名
    new_name += '.jpg'
    # 返回字符串
    return new_name
