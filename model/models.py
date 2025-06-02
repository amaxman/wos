import datetime
import os
import uuid

import pytz
from django.db import models
import json
import re
from django.db.models import Model
from django.utils import timezone


class BasicModel(models.Model):
    sys_id = models.CharField(verbose_name="系统标识", max_length=64, default='', null=True, blank=True)
    remarks = models.TextField(verbose_name="备注", default='', null=True, blank=True)

    class Meta:
        abstract = True,


def to_camel_case(snake_str: str):
    """将蛇形命名转换为驼峰命名"""
    components = snake_str.split('_')
    return components[0] + ''.join(x.title() for x in components[1:])


def model_to_camel_case_json(instance):
    """将模型实例转换为驼峰命名的JSON字符串"""
    return json.dumps(instance, cls=CamelCaseJSONEncoder, ensure_ascii=False)


def model_to_entity(instance):
    if instance is None:
        return None
    json_str = model_to_camel_case_json(instance)
    if json_str is None or json_str == '':
        return None
    return json.loads(json_str)


class CamelCaseJSONEncoder(json.JSONEncoder):
    """自定义JSON编码器，处理datetime和模型字段映射"""

    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            obj = timezone.localtime(obj)
            datetime_str = obj.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
            return datetime_str
        if isinstance(obj, Model):
            # 将模型对象转换为字典并处理字段映射
            fields = {}
            for field in obj._meta.get_fields():
                try:
                    value = getattr(obj, field.name)
                    # 处理关联对象
                    if isinstance(value, Model):
                        fields[field.name] = value.pk
                    else:
                        fields[field.name] = value
                except Exception:
                    pass
            fields = {k: v for k, v in fields.items() if k not in {'id', 'frame_filename'}}
            # 字段映射：sys_id -> id
            if 'sys_id' in fields:
                fields['id'] = fields.pop('sys_id')
            # 将字典键转换为驼峰格式
            return {to_camel_case(key): value for key, value in fields.items()}
        return super().default(obj)


def post_image_path(instance, filename):
    # 获取文件扩展名
    ext = filename.split('.')[-1]
    # 使用当前日期和随机字符串作为文件名
    filename = f'{timezone.now().strftime("%Y%m%d")}_{uuid.uuid4().hex[:8]}.{ext}'
    # 文件会被上传到 MEDIA_ROOT/static/face/<year>/<month>/<filename> 目录
    return os.path.join('static', 'face',
                        str(timezone.now().year),
                        str(timezone.now().month),
                        filename)
