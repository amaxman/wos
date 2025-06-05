from django.contrib.sessions.models import Session
from django.contrib.auth.models import User
from django.utils import timezone
from rest_framework import authentication
from django.utils.translation import gettext_lazy as _, activate, get_language

from core.exception import CustomAPIException
from core.language_util import language_map
from core.rest_util import JsonMsg
from django.http import JsonResponse
from rest_framework import exceptions
from datetime import datetime, timedelta


class SessionIdAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        # 从 URL 参数或请求体中获取 sessionId
        session_id = request.query_params.get('sessionId') or request.data.get('sessionId')
        lang_code = request.query_params.get('language') or request.data.get('language')
        if not lang_code:
            lang_code = 'zh_Hans'
        activate(lang_code)
        request.LANGUAGE_CODE = language_map.get(lang_code, 'zh-hans')

        if not session_id:
            # 未提供 sessionId，返回 None 表示此认证器无法处理
            return self._handle_no_session_id(request)

        try:
            # 获取 Session 对象
            session = Session.objects.get(session_key=session_id)

            # 检查会话是否过期

            if session.expire_date < timezone.now():
                # 如果令牌有效则自动增加7小时，请使用如下2行代码
                session.set_expiry(datetime.now() + timedelta(hours=7))
                session.save()
                # 如果令牌过期，则直接使用如下代码，抛出异常
                # raise CustomAPIException(JsonMsg(msgType=False, msg=_('Session has expired'), code=404))

            # 从会话中获取用户 ID
            session_data = session.get_decoded()
            user_id = session_data.get('_auth_user_id')

            if not user_id:
                raise CustomAPIException(JsonMsg(msgType=False, msg=_('Invalid session data'), code=404))

            # 获取关联的用户对象
            try:
                user = User.objects.get(pk=user_id)
            except User.DoesNotExist:
                raise CustomAPIException(JsonMsg(msgType=False, msg=_('User not found'), code=404))

            # 验证用户是否活跃
            if not user.is_active:
                raise CustomAPIException(JsonMsg(msgType=False, msg=_('User is inactive'), code=404))

            # 认证成功，返回用户和认证信息
            return (user, None)

        except Session.DoesNotExist:
            # 会话不存在，拒绝访问
            raise CustomAPIException(JsonMsg(msgType=False, msg=_('Invalid session ID'), code=404))

    def _handle_no_session_id(self, request):
        """处理未找到 session_id 的情况"""
        # 检查请求是否期望 JSON 响应
        if request.accepted_media_type == 'application/json':
            # 返回 JSON 格式的错误响应

            response_data = JsonMsg(code=40102, msg=_('Authentication credentials were not provided.'),
                                    msgType=False).to_dict()
            return JsonResponse(response_data, status=401)
        else:
            # 非 JSON 请求，抛出标准的 DRF 异常
            # raise exceptions.AuthenticationFailed(
            #     _('Invalid Media Type')
            # )
            raise CustomAPIException(JsonMsg(msgType=False, msg=_('Invalid Media Type'), code=404))
