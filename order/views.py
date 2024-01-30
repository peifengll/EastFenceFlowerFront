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


class OrderUpdateView(APIView):
    def put(self, request):
        # 知道这是属于什么类型,取消订单？申请退款？确认收获等
        orderid = request.data.get("order_id")
        if orderid is None or orderid == "":
            return BaseResponse(msg="订单信息缺失", status=311)
        typeis = request.data.get("type")
        try:
            obj = Order.objects.filter(order_id=orderid)
            if typeis == "cancer":
                obj.update(stage="0026")
            elif typeis == "pay":
                obj.update(stage="0022")
            elif typeis == "apply":
                obj.update(stage="0025")
            elif typeis == "sure":
                obj.update(stage="0024")
            elif typeis == "feedback":
                content = request.data.get("feedback")
                if content is None or content == "":
                    return BaseResponse(msg="评论怎么为空？", status=313)
                obj.update(remark=content)
            else:
                return BaseResponse(msg="type不符合约束", status=312)
        except Exception as e:
            return BaseResponse(msg="服务器内部错误" + e.__str__(), status=500)
        return BaseResponse(msg="操作成功", status=200)


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
                o.remark,
                o.beihuo_id,
                o.beihuo,
                o.peisong_id,
                o.peisong,
                o.cart_id AS cart_infos 
            FROM
                `order` o 
            WHERE
                o.user_id = %s 
            ORDER BY
                o.order_id DESC
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
            print(cart_infos[0][0]['goods_id'])
            print("*" * 5)
            names = queryNames(goods_id=cart_infos[0][0]['goods_id'])
            print(names)
            i['ename'] = names[0]['ename']
            i['gname'] = names[0]['gname']
            i['flower_id'] = names[0]['flower_id']
    return result


def queryCart(cart_id=None):
    with connection.cursor() as cursor:
        cursor.execute("""   
            SELECT
                c.uname,
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


def queryNames(goods_id=None):
    print(goods_id, "sasas")
    with connection.cursor() as cursor:
        cursor.execute("""   
            select goods.ename, goods.gname,goods.flower_id
            from goods
            where goods_id = %s               
           """, [goods_id])
        columns = [col[0] for col in cursor.description]
        result = [dict(zip(columns, row)) for row in cursor.fetchall()]
    return result
