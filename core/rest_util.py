import json
import datetime

from rest_framework import status
from rest_framework.exceptions import APIException
from django.utils.translation import gettext_lazy as _


class JsonMsg:
    def __init__(self, data=None, msgType: bool = True, msg: str = "", code: int = 0):
        self.msgType = msgType
        self.msg = msg
        self.data = data
        self.code = code

    def to_dict(self):
        """将消息对象转换为字典格式"""
        return {
            'msgType': self.msgType,
            'msg': self.msg,
            'data': self.data
        }

    @staticmethod
    def instance(data, msg: str = "", msg_type: bool = True):
        return JsonMsg(data, msg_type, msg)

    @staticmethod
    def error_data(data, msg: str):
        return JsonMsg(data, False, msg)

    @staticmethod
    def error(msg: str):
        return JsonMsg(msgType=False, msg=msg)

    @staticmethod
    def error_code(msg: str, code: int):
        return JsonMsg(msgType=False, msg=msg, code=code)

    @staticmethod
    def success(data, msg: str):
        return JsonMsg(msgType=True, msg=msg, data=data)

    @staticmethod
    def parse(json_str: str):
        try:
            data = json.loads(json_str)
            return JsonMsg(data.get('data'), data.get('msgType', True), data.get('msg', ""))
        except json.JSONDecodeError:
            return None


class UserSessionRestEntity:
    def __init__(self, sessionId: str = '', userName: str = '', loginTime: datetime = datetime.datetime.now(), ):
        self.sessionId = sessionId
        self.userName = userName
        self.loginTime = loginTime

    def to_dict(self):
        """将消息对象转换为字典格式"""
        return {
            'sessionId': self.sessionId,
            'userName': self.userName,
            'loginTime': self.loginTime
        }


class SessionIdNotFound(APIException):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = _('Authentication credentials were not provided.')
    default_code = 'session_id_missing'

    def __init__(self, msg=None, code=None, extra_data=None):
        """
        自定义认证异常，支持传递额外数据

        Args:
            msg: 自定义错误消息
            code: 自定义错误码
            extra_data: 额外数据字典，将包含在响应中
        """
        if msg is not None:
            self.detail = msg
        else:
            self.detail = self.default_detail

        if code is not None:
            self.code = code
        else:
            self.code = self.default_code

        # 存储额外数据
        self.extra_data = extra_data or {}
