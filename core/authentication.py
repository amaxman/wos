from django.contrib.sessions.models import Session
from django.contrib.auth.models import User
from django.utils import timezone
from rest_framework import authentication, exceptions


class SessionIdAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        # 从 URL 参数或请求体中获取 sessionId
        session_id = request.query_params.get('sessionId') or request.data.get('sessionId')

        if not session_id:
            # 未提供 sessionId，返回 None 表示此认证器无法处理
            return None

        try:
            # 获取 Session 对象
            session = Session.objects.get(session_key=session_id)

            # 检查会话是否过期
            if session.expire_date < timezone.now():
                raise exceptions.AuthenticationFailed('Session has expired')

            # 从会话中获取用户 ID
            session_data = session.get_decoded()
            user_id = session_data.get('_auth_user_id')

            if not user_id:
                raise exceptions.AuthenticationFailed('Invalid session data')

            # 获取关联的用户对象
            try:
                user = User.objects.get(pk=user_id)
            except User.DoesNotExist:
                raise exceptions.AuthenticationFailed('User not found')

            # 验证用户是否活跃
            if not user.is_active:
                raise exceptions.AuthenticationFailed('User is inactive')

            # 认证成功，返回用户和认证信息
            return (user, None)

        except Session.DoesNotExist:
            # 会话不存在，拒绝访问
            raise exceptions.AuthenticationFailed('Invalid session ID')
