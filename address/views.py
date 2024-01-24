from django.shortcuts import render
from rest_framework.views import APIView

from address.serializers import AddressInfoSerializer
from libs.utils.base_response import BaseResponse
from models.models import Address


# Create your views here.


class AddressShowView(APIView):
    def get(self, request):
        userid = request.GET.get('user_id')
        if userid is None or userid == "":
            return BaseResponse(msg="未获取到用户凭证", status=401)
        adds = Address.objects.filter(u_id=userid)
        ser = AddressInfoSerializer(adds, many=True)
        return BaseResponse(msg="获取成功", data=ser.data, status=200)


class AddressAddView(APIView):
    def post(self, request):
        userid = request.data.get('user_id')
        if userid is None or userid == "":
            return BaseResponse(msg="未获取到用户凭证", status=401)
        name = request.data.get('uname')
        phone = request.data.get('phone')
        address = request.data.get('address')
        try:
            Address.objects.create(uname=name, phone=phone, address=address, u_id=userid)
        except Exception as e:
            return BaseResponse(msg="添加错误", status=500)
        return BaseResponse(msg="添加成功", status=200)


class AddressDelView(APIView):
    def delete(self, request):
        add_id = request.data.get('id')
        if add_id is None or add_id == "":
            return BaseResponse(msg="传参错误", status=304)
        try:
            Address.objects.filter(add_id=add_id).delete()
        except Exception as e:
            return BaseResponse(msg="删除错误", status=500)
        return BaseResponse(msg="删除成功", status=200)


class AddressUpdateView(APIView):
    def put(self, request):
        add_id = request.data.get('id')
        name = request.data.get('uname')
        phone = request.data.get('phone')
        address = request.data.get('address')
        if add_id is None or add_id == "":
            return BaseResponse(msg="传参错误", status=304)
        try:
            obj = Address.objects.filter(add_id=add_id)
            if name != "" and name is not None:
                obj.update(uname=name)
            if phone != "" and phone is not None:
                obj.update(phone=phone)
            if address != "" and address is not None:
                obj.update(address=address)
        except Exception as e:
            return BaseResponse(msg="修改错误", status=500)
        return BaseResponse(msg="修改成功", status=200)
