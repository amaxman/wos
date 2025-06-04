from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from core.rest_util import JsonMsg, UserSessionRestEntity


class LoginView(APIView):
    """
    支持 GET 请求的登录视图
    通过 URL 参数 loginId 和 loginPassword 进行认证
    返回 sessionId 和用户信息
    """
    authentication_classes = []  # 登录接口不需要认证
    permission_classes = []

    def get(self, request):
        login_id = request.query_params.get('loginId')
        login_password = request.query_params.get('loginPassword')

        if not login_id or not login_password:
            return Response(
                JsonMsg.error('无登陆信息').to_dict(),
                status=status.HTTP_400_BAD_REQUEST
            )

        # 使用 Django 内置认证系统
        user = authenticate(username=login_id, password=login_password)

        if user is not None:
            if user.is_active:
                # 登录用户，创建 session
                login(request, user)

                # 返回 sessionId 和用户信息
                userSession = UserSessionRestEntity(request.session.session_key, user.username)
                jsonMsg = JsonMsg.success(userSession.to_dict(), '登录成功')

                return Response(jsonMsg.to_dict(), status=status.HTTP_200_OK)
            else:
                return Response(
                    JsonMsg.error('账户已禁用').to_dict(),
                    status=status.HTTP_403_FORBIDDEN
                )
        else:
            return Response(
                JsonMsg.error('用户名或密码错误').to_dict(),
                status=status.HTTP_401_UNAUTHORIZED
            )
