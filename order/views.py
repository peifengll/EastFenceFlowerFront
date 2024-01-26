import json

from django.db import connection
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
        cart_ids = request.data.get("cart_id")
        cart_ids = json.loads(cart_ids)
        address_id = request.data.get("address_id")

        try:
            today = timezone.now()
            for i in cart_ids:
                Order.objects.create(time=today, stage='0021', address_id=address_id, money=money, user_id=userid,
                                     cart_id=i)
        except Exception as e:
            return BaseResponse(msg="服务器内部错误", status=500)
        return BaseResponse(msg="操作成功", status=200)


class OrderListView(APIView):
    def get(self, request):
        userid = request.GET.get("user_id")
        if userid is None or userid == "":
            return BaseResponse(msg="用户凭证缺失", status=401)
        try:
            res = custom_query(userid=userid)
            # print(res)
        except Exception as e:
            return BaseResponse(msg="服务器内部错误", status=500)
        return BaseResponse(data=res, msg="没啥问题", status=200)


def custom_query(userid=None):
    with connection.cursor() as cursor:
        cursor.execute("""   
            SELECT
                o.order_id,
                o.stage,
                o.time,
                o.money,
                c.uname,
                c.gname,
                c.num,
                a.uname AS aname,
                a.phone,
                a.address
            FROM
                `order` o
            INNER JOIN cart c ON o.cart_id = c.cart_id
            INNER JOIN address a ON o.address_id = a.add_id
            WHERE
                o.user_id = %s;
        """, [userid])
        columns = [col[0] for col in cursor.description]
        result = [dict(zip(columns, row)) for row in cursor.fetchall()]
    return result
