from rest_framework import serializers


class ModelsSerializer(serializers.ModelSerializer):
    page_size = 10
    page_size_query_param = 'page_size'
