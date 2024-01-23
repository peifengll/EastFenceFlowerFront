import json

from django.shortcuts import render
from rest_framework.views import APIView

from cart.serializers import CartShowSerializers
from libs.utils.base_response import BaseResponse
from models.models import Cart


# Create your views here.

class CartAddView(APIView):
    def post(self, request):
        userid = request.POST.get('user_id')
        print(userid)
        if userid is None or userid == "":
            return BaseResponse(data={}, status=401, msg="用户凭证丢失")
        uname = request.POST.get('uname')
        gname = request.POST.get('gname')
        goodsid = request.POST.get('goods_id')
        try:
            goodsid = json.loads(goodsid)
        except Exception as e:
            return BaseResponse(msg="数据解析错误", status=500)

        price = request.POST.get('price')
        try:
            price = json.loads(price)
        except Exception as e:
            return BaseResponse(msg="数据解析错误", status=500)

        num = request.POST.get('num')
        if goodsid == "" or goodsid is None:
            return BaseResponse(data={}, status=301, msg="商品消息丢失")
        try:
            k = Cart.objects.create(user_id=userid,
                                    uname=uname,
                                    gname=gname,
                                    goods_id=goodsid[0],
                                    num=num,
                                    price=price[goodsid[0]]
                                    )

            print(k)
            k = Cart.objects.create(user_id=userid,
                                    uname=uname,
                                    gname=gname,
                                    goods_id=goodsid[1],
                                    num=num,
                                    price=price[goodsid[1]]
                                    )

            print(k)
            k = Cart.objects.create(user_id=userid,
                                    uname=uname,
                                    gname=gname,
                                    goods_id=goodsid[2],
                                    num=num,
                                    price=price[goodsid[2]]
                                    )

            print(k)
        except Exception as e:
            print(e)
            return BaseResponse(data={'error': e.__str__()}, status=500, msg="添加失败")
        return BaseResponse(data={}, status=200, msg="添加成功")


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
