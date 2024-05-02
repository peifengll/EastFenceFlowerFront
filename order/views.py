import json

from django.db import connection, transaction
from django.shortcuts import render
from django.utils import timezone
from rest_framework.views import APIView

import models.models
from libs.utils.base_response import BaseResponse
from models.models import Order, Address, Flower, Cart, Goods
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
        infos = Cart.objects.filter(cart_id__in=cart_ids)
        #  total flower num,就是花要减去的, 然后 单独的只需要看每个满不满足即可，
        noway = True
        msg = ""
        for i in infos:
            good = Goods.objects.get(goods_id=i.goods_id)
            if int(good.total_num) < int(i.num):
                msg += " 你购买的 %s数量超过库存,该产品库存只有%s \n" % (good.gname, good.total_num)
                noway = False
        if not noway:
            return BaseResponse(msg=msg, status=317)
        try:
            obj = Address.objects.get(add_id=address_id)
            today = timezone.now()
            with transaction.atomic():
                for i in infos:
                    good = Goods.objects.get(goods_id=i.goods_id)
                    fl = Flower.objects.get(flower_id=good.flower_id)
                    good.total_num = Minus(good.total_num, i.num)
                    good.salenum = Add(good.salenum, i.num)
                    fl.num = Minus(fl.num, i.num)
                    fl.save()
                    good.save()
                Order.objects.create(time=today, stage='0021', address_id=address_id, money=money, user_id=userid,
                                     cart_id=cart_ids, phone=obj.phone, aname=obj.uname, address=obj.address)
        except Exception as e:
            return BaseResponse(msg="服务器内部错误" + e.__str__(), status=500)
        return BaseResponse(msg="操作成功", status=200)


#  没得cart的那个
class OrderAddViewWithNoCart(APIView):
    """
    设计上就只要
     num
     goodsid []
     money
     addressid
    """

    def post(self, request):
        userid = request.data.get("user_id")
        if userid is None or userid == "":
            return BaseResponse(msg="用户凭证缺失", status=401)
        num = request.data.get("num")
        goodid = request.data.get("goodsid")
        addressid = request.data.get("address_id")
        print(goodid)
        int_list = [int(x) for x in goodid]
        goodid = int_list
        print(goodid)
        if not addressid or not goodid or not num:
            return BaseResponse(msg="参数缺失", status=400)

        noway = True
        msg = ""
        for i in goodid:
            good = Goods.objects.get(goods_id=i)
            if int(good.total_num) < int(num):
                msg += " 你购买的 %s数量超过库存,该产品库存只有%s \n" % (good.gname, good.total_num)
                noway = False
            if not noway:
                return BaseResponse(msg=msg, status=317)
        try:
            totalmoney = 0
            obj = Address.objects.get(add_id=addressid)
            today = timezone.now()
            for i in goodid:
                good = Goods.objects.get(goods_id=i)
                money = int(num) * int(good.charge)
                totalmoney += money
                with transaction.atomic():
                    good = Goods.objects.get(goods_id=i)
                    fl = Flower.objects.get(flower_id=good.flower_id)
                    good.total_num = Minus(good.total_num, num)
                    good.salenum = Add(good.salenum, num)
                    fl.num = Minus(fl.num, num)
                    fl.save()
                    good.save()
            Order.objects.create(time=today, stage='0021', address_id=addressid, money=totalmoney, user_id=userid,
                                 phone=obj.phone, aname=obj.uname, address=obj.address, goods_id=str(goodid), num=num)
        except Exception as e:
            print(e.__str__())
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


# 按照id查
class OrderShowView(APIView):
    def get(self, request):
        # 知道这是属于什么类型,取消订单？申请退款？确认收获等
        orderid = request.GET.get("order_id")
        if orderid is None or orderid == "":
            return BaseResponse(msg="缺失订单信息", status=313)
        res = None
        try:
            res = queryOneOrder(orderid)
            # info = models.models.Order.objects.get(order_id=orderid)
            # res = OrderInfoSerializer(info)
        except  models.models.Order.DoesNotExist:
            return BaseResponse(msg="没得这个数据哦！", status=200)
        except Exception as e:
            return BaseResponse(msg="服务器内部错误" + e.__str__(), status=500)

        return BaseResponse(msg="操作成功", data=res, status=200)


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


def queryOneOrder(orderid=None):
    with connection.cursor() as cursor:
        cursor.execute("""   
            SELECT
                o.*
            FROM
                `order` o 
            WHERE
                o.order_id = %s 
        """, [orderid])
        columns = [col[0] for col in cursor.description]
        result = [dict(zip(columns, row)) for row in cursor.fetchall()]
        print(result)

        for i in result:
            list = json.loads(i['goods_id'])
            print(i['goods_id'])
            print("list : ", list)
            cartinfo = [None for i in list]
            print(cartinfo)
            print(cartinfo[0])
            po = models.models.User.objects.get(user_id=i['user_id'])
            uname = po.uname
            for item in range(0, len(list)):
                map = queryNames(list[item])
                map[0]['num'] = i['num']
                map[0]['uname'] = uname
                map[0]['goods_id'] = list[item]
                del map[0]['ename']
                del map[0]['gname']
                del map[0]['flower_id']
                cartinfo[item] = map
                print("k,v:", item, list[item])
                print(map)
            i['cart_infos'] = cartinfo
            # size
            names = queryNames(goods_id=list[0])
            i['ename'] = names[0]['ename']
            i['gname'] = names[0]['gname']
            i['flower_id'] = int(names[0]['flower_id'])
    result=result[0]
    return result

def custom_query2(userid=None):
    with connection.cursor() as cursor:
        cursor.execute("""   
            SELECT
                o.*
            FROM
                `order` o 
            WHERE
                o.user_id = %s 
            ORDER BY
                o.order_id DESC
        """, [userid])
        columns = [col[0] for col in cursor.description]
        result = [dict(zip(columns, row)) for row in cursor.fetchall()]
        print(result)

        for i in result:
            list = json.loads(i['goods_id'])
            print(i['goods_id'])
            print("list : ", list)
            cartinfo = [None for i in list]
            print(cartinfo)
            print(cartinfo[0])
            po = models.models.User.objects.get(user_id=i['user_id'])
            uname = po.uname
            for item in range(0, len(list)):
                map = queryNames(list[item])
                map[0]['num'] = i['num']
                map[0]['uname'] = uname
                map[0]['goods_id'] = list[item]
                del map[0]['ename']
                del map[0]['gname']
                del map[0]['flower_id']
                cartinfo[item] = map
                print("k,v:", item, list[item])
                print(map)
            i['cart_infos'] = cartinfo
            # size
            names = queryNames(goods_id=list[0])
            i['ename'] = names[0]['ename']
            i['gname'] = names[0]['gname']
            i['flower_id'] = int(names[0]['flower_id'])
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
    # print(goods_id, "sasas")
    with connection.cursor() as cursor:
        cursor.execute("""   
            select goods.ename, goods.gname,goods.flower_id,goods.size,goods.size,goods.charge as price
            from goods
            where goods_id = %s               
           """, [goods_id])
        columns = [col[0] for col in cursor.description]
        result = [dict(zip(columns, row)) for row in cursor.fetchall()]
    return result


def Minus(a, b):
    a = int(a)
    b = int(b)
    return str(a - b)


def Add(a, b):
    a = int(a)
    b = int(b)
    return str(a + b)
