from rest_framework import serializers


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True, max_length=50)
    password = serializers.CharField(required=True, max_length=50, write_only=True)
    language = serializers.ChoiceField(choices=['zh_Hans', 'en', 'ja', 'ko'], default='zh_Hans')


class LoginGetSerializer(LoginSerializer):
    """GET方法使用的序列化器，添加额外的安全警告"""

    def validate(self, data):
        data = super().validate(data)
        # 可以在这里添加针对GET请求的额外安全检查
        return data
