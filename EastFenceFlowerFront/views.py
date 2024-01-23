#!/user/bin/env python3
# -*- coding: utf-8 -*-
from rest_framework.views import APIView

from libs.utils.base_response import BaseResponse


class HomeView(APIView):
    def get(self, request):
        return BaseResponse(data={'message': '这是东篱花店的后端技术支持！'}, status=200)
