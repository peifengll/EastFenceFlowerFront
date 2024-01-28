import json

from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.views import APIView

from cart.serializers import CartShowSerializers
from libs.utils.base_response import BaseResponse
from models.models import Cart


# Create your views here.


class CartAddView(APIView):

    def post(self, request):
        # print("json", request.body)
        request_data = request.body.decode("utf-8")
        # print("data : ", request_data)
        try:
            request_data = json.loads(request_data)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON format"})
        # print("request_data: ", request_data)
        # 提取参数
        gname = request_data.get('gname')
        # print("gname: ", gname)
        # 解析 goods_ids 字符串为列表
        goods_ids = request_data.get('goods_id', '[]')
        # print("goods_ids_str: ",goods_ids_str[0])
        # goods_ids = json.loads(goods_ids_str)
        # print("goods_ids loads: ", goods_ids)
        num = request_data.get('num')
        uname = request_data.get('uname')
        userid = request_data.get('user_id')

        # 解析 price 字符串为字典
        price = request_data.get('price', '{}')
        # print("price_str", price)
        # print(price[goods_ids[0]])
        # price = json.loads(price_str)
        if userid is None or userid == "":
            return BaseResponse(data={}, status=401, msg="用户凭证丢失")

        if goods_ids == "" or goods_ids is None:
            return BaseResponse(data={}, status=301, msg="商品消息丢失")
        id_list = []
        for i in goods_ids:
            # 如果是同样的数据，
            c = None
            try:
                c = Cart.objects.get(user_id=userid, goods_id=i)
            except Exception as e:
                pass
            try:
                if c is not None:
                    Cart.objects.filter(user_id=userid, goods_id=i).update(num=int(c.num) + int(num))
                    id_list.append(c.cart_id)
                else:
                    k = Cart.objects.create(user_id=userid,
                                            uname=uname,
                                            gname=gname,
                                            goods_id=i,
                                            num=num,
                                            price=price[i][1],
                                            size=price[i][0]
                                            )
                    id_list.append(k.cart_id)
            except Exception as e:
                return BaseResponse(data={'error': e.__str__()}, status=500, msg="添加失败")
        return BaseResponse(data={"ids": id_list}, status=200, msg="添加成功")


class CartShow(APIView):
    def get(self, request):
        id = request.GET.get("user_id")
        if id == "" or id is None:
            return BaseResponse(data={}, status=401, msg="未获取到用户凭证")
        lists = Cart.objects.filter(user_id=id)
        ser = CartShowSerializers(lists, many=True)
        return BaseResponse(data=ser.data, status=200, msg="未获取到用户凭证")


class CartDelete(APIView):
    def delete(self, request):
        id = request.GET.get("id")
        if id == "" or id is None:
            return BaseResponse(data={"msg": "未获取到用户凭证"}, status=401)

        return render(request, 'cart.html')
