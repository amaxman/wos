import json
import datetime


class JsonMsg:
    def __init__(self, data=None, msgType: bool = True, msg: str = ""):
        self.msgType = msgType
        self.msg = msg
        self.data = data

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
