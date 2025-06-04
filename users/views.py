from django.http import JsonResponse
from django.contrib.auth import authenticate, login
from django.utils.translation import gettext as _, activate
from rest_framework.views import APIView
from rest_framework import status

from core.language_util import language_map
from core.rest_util import JsonMsg
from .serializers import LoginSerializer, LoginGetSerializer
import logging
from django.utils.translation import get_language

logger = logging.getLogger(__name__)


class LoginView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        """使用POST方法进行登录（推荐方式）"""
        serializer = LoginSerializer(data=request.data)
        if not serializer.is_valid():
            return JsonResponse(
                JsonMsg(
                    msgType=False,
                    msg=_('Invalid request parameters'),
                    code=40001
                ).to_dict(),
                status=status.HTTP_400_BAD_REQUEST)

        return self._process_login(request, serializer)

    def get(self, request):
        """使用GET方法进行登录（兼容性支持，安全性较低）"""
        serializer = LoginGetSerializer(data=request.query_params)
        if not serializer.is_valid():
            return JsonResponse(
                JsonMsg(
                    msgType=False,
                    msg=_('Invalid request parameters'),
                    code=40001
                ).to_dict(),
                status=status.HTTP_400_BAD_REQUEST)

        return self._process_login(request, serializer)

    def _process_login(self, request, serializer):
        """处理登录的通用逻辑"""
        username = serializer.validated_data['username']
        password = serializer.validated_data['password']

        # 支持更多语言代码映射

        # 获取并映射语言代码
        lang_code = serializer.validated_data.get('language', 'zh_Hans')
        activate(lang_code)
        request.LANGUAGE_CODE = language_map.get(lang_code, 'zh-hans')

        user = authenticate(request, username=username, password=password)
        if user is None:
            return JsonResponse(
                JsonMsg(
                    msgType=False,
                    msg=_('Invalid credentials'),
                    code=40101
                ).to_dict(),
                status=status.HTTP_401_UNAUTHORIZED
            )

        if not user.is_active:
            return JsonResponse(
                JsonMsg(
                    msgType=False,
                    msg=_('User account is disabled'),
                    code=40301
                ).to_dict(),
                status=status.HTTP_403_FORBIDDEN
            )

        # 登录用户并刷新session
        login(request, user)
        # 如果每次登陆修改令牌，则反注释如下代码
        # request.session.cycle_key()

        return JsonResponse(
            JsonMsg(
                data={
                    'session_id': request.session.session_key,
                    'username': user.username
                },
                msgType=True,
                msg=_('Login successful'),
                code=20000
            ).to_dict(),
            status=status.HTTP_200_OK
        )
