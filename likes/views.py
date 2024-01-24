from django.shortcuts import render
from rest_framework.views import APIView

from libs.utils.base_response import BaseResponse
from likes.serializers import LikesInfoSerializer
from models.models import Likes


# Create your views here.

class LikesAddView(APIView):
    def post(self, request):
        userid = request.data.get("user_id")
        flowerid = request.data.get("flower_id")
        price = request.data.get("price")
        image = request.data.get("image")
        if userid is None or flowerid is None or userid == "" or flowerid == "":
            return BaseResponse(msg='flowerid 和 userid 不能为空', status=306)
        try:
            Likes.objects.create(
                user_id=userid,
                flower_id=flowerid,
                price=price,
                image=image,
            )
        except Exception as e:
            return BaseResponse(msg='数据未插入', status=500)
        return BaseResponse(msg='添加喜欢成功', status=200)


class LikesShowView(APIView):
    def get(self, request):
        userid = request.GET.get("user_id")
        if userid is None or userid == "":
            return BaseResponse(msg='未获取到用户凭证', status=401)
        infos = []
        try:
            infos = Likes.objects.filter(
                user_id=userid,
            )
            info = LikesInfoSerializer(infos, many=True)
        except Exception as e:
            return BaseResponse(msg='内部错误' + e.__str__(), status=500)
        return BaseResponse(msg='添加喜欢成功', data=info.data, status=200)


class LikesDelView(APIView):
    def delete(self, request):
        likes_id = request.data.get("id")
        if likes_id is None or likes_id == "":
            return BaseResponse(msg='未获取到likes_id', status=401)
        try:
            Likes.objects.filter(
                like_id=likes_id,
            ).delete()
        except Exception as e:
            return BaseResponse(msg='删除失败' + e.__str__(), status=500)
        return BaseResponse(msg='删除成功', status=200)
