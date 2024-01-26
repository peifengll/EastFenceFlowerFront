from django.shortcuts import render
from django.utils import timezone
from rest_framework.views import APIView

from libs.utils.base_response import BaseResponse
from models.models import Order


# Create your views here.

class OrderAddView(APIView):
    def post(self, request):
        userid = request.data.get("user_id")
        if userid is None or userid == "":
            return BaseResponse(msg="用户凭证缺失", status=401)
        money = request.data.get("money")
        cart_id = request.data.get("cart_id")
        address_id = request.data.get("address_id")

        try:
            today = timezone.now()
            Order.objects.create(time=today, stage='0021', address_id=address_id, money=money, user_id=userid,
                                 cart_id=cart_id)
        except Exception as e:
            return BaseResponse(msg="服务器内部错误", status=500)
        return BaseResponse(msg="操作成功", status=200)
