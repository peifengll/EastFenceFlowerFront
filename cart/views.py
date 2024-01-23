from django.shortcuts import render
from rest_framework.views import APIView

from libs.utils.base_response import BaseResponse


# Create your views here.


class CartShow(APIView):
    def get(self, request):
        id = request.GET.get("id")
        if id == "" or id is None:
            return BaseResponse(data={"msg": "未获取到用户凭证"}, status=401)

        return render(request, 'cart.html')


class CartDelete(APIView):
    def get(self, request):
        id = request.GET.get("id")
        if id == "" or id is None:
            return BaseResponse(data={"msg": "未获取到用户凭证"}, status=401)

        return render(request, 'cart.html')
