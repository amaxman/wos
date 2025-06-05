from rest_framework.exceptions import APIException

from core.rest_util import JsonMsg
from django.utils.translation import gettext_lazy as _


# 自定义异常类
class CustomAPIException(APIException):
    status_code = 400  # 默认状态码
    default_detail = '发生了自定义错误'
    default_code = 'custom_error'

    def __init__(self, jsonMsg: JsonMsg):
        if jsonMsg is None:
            self.detail = self.default_detail
            self.code = self.default_code
            return
        self.detail = jsonMsg.msg
        self.code = jsonMsg.code
        self.msgType = jsonMsg.msgType
        self.data = jsonMsg.data


# 自定义异常处理器
def custom_exception_handler(exc, context):
    # 延迟导入，避免循环依赖
    from rest_framework.views import exception_handler
    from rest_framework.response import Response

    # 调用原始异常处理器
    response = exception_handler(exc, context)

    # 自定义处理逻辑
    if response is not None:
        if isinstance(exc, CustomAPIException):
            customAPIException: CustomAPIException = exc
            jsonMsg = JsonMsg(msgType=False, msg=customAPIException.detail, code=response.status_code)
            response.data = jsonMsg.to_dict()
        else:
            jsonMsg = JsonMsg(msgType=False, msg=_('Exception Unknown'), code=response.status_code)
            response.data = jsonMsg.to_dict()
        return response

    # 处理其他异常
    jsonMsg = JsonMsg(msgType=False, msg=_('Exception Internal'), code=500)
    return Response(jsonMsg.to_dict(), status=500)
