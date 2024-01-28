import json

from django.db import connection
from django.shortcuts import render
from django.utils import timezone
from rest_framework.views import APIView

from libs.utils.base_response import BaseResponse
from models.models import Order, Address
from order.serializers import OrderInfoSerializer


# Create your views here.

class OrderAddView(APIView):
    def post(self, request):
        userid = request.data.get("user_id")
        if userid is None or userid == "":
            return BaseResponse(msg="用户凭证缺失", status=401)
        money = request.data.get("money")
        cart_ids = request.data.get("cart_id")
        # print(cart_ids)
        # print(cart_ids[0])
        if type(cart_ids) == str:
            cart_ids = json.loads(cart_ids)
        address_id = request.data.get("address_id")

        try:
            obj = Address.objects.get(add_id=address_id)
            today = timezone.now()
            Order.objects.create(time=today, stage='0021', address_id=address_id, money=money, user_id=userid,
                                 cart_id=cart_ids, phone=obj.phone, aname=obj.uname, address=obj.address)
        except Exception as e:
            return BaseResponse(msg="服务器内部错误" + e.__str__(), status=500)
        return BaseResponse(msg="操作成功", status=200)


class OrderListView(APIView):
    def get(self, request):
        userid = request.GET.get("user_id")
        if userid is None or userid == "":
            return BaseResponse(msg="用户凭证缺失", status=401)
        try:

            res = custom_query2(userid=userid)

            # print(res)
        except Exception as e:
            return BaseResponse(msg="服务器内部错误" + e.__str__(), status=500)
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
                
                o.aname,
                o.phone,
                o.address
            FROM
                `order` o
            INNER JOIN cart c ON o.cart_id = c.cart_id
            WHERE
                o.user_id = %s;
        """, [userid])
        columns = [col[0] for col in cursor.description]
        result = [dict(zip(columns, row)) for row in cursor.fetchall()]

    return result


def custom_query2(userid=None):
    with connection.cursor() as cursor:
        cursor.execute("""   
            SELECT
                o.order_id,
                o.stage,
                o.time,
                o.money,
                o.aname,
                o.phone,
                o.address,
                o.cart_id as cart_infos
            FROM
                `order` o
            WHERE
                o.user_id = %s;
        """, [userid])

        columns = [col[0] for col in cursor.description]
        result = [dict(zip(columns, row)) for row in cursor.fetchall()]
        for i in result:
            cart_ids = eval(i['cart_infos'])
            # 拿到cart_ids
            cart_infos = []
            for j in cart_ids:
                cart_infos.append(queryCart(j))
            i['cart_infos'] = cart_infos
    return result


def queryCart(cart_id=None):
    with connection.cursor() as cursor:
        cursor.execute("""   
            SELECT
                c.uname,
                c.gname,
                c.num,
                c.size,
                c.price,
                c.goods_id
            FROM
                cart c 
            WHERE
                c.cart_id = %s;
        """, [cart_id])
        columns = [col[0] for col in cursor.description]
        result = [dict(zip(columns, row)) for row in cursor.fetchall()]

    return result
