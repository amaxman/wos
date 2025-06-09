import os

from django.db import models

from model.models import BasicModel, post_image_path
from django.core.files.storage import default_storage
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class DictType(BasicModel):
    dict_name = models.CharField(verbose_name=_('Dict Type Name'), max_length=100)
    dict_type = models.CharField(verbose_name=_('Dict Type Cate'), max_length=50)
    is_sys = models.CharField(verbose_name=_('Is System'), max_length=1, default='0')
    status = models.CharField(verbose_name=_('Status'), max_length=1, default='0')

    def __str__(self):
        return self.dict_name

    class Meta:
        verbose_name = _('Dict Type')
        verbose_name_plural = _('Dict Type Admin')
        db_table = 'sys_dict_type'
        ordering = ['dict_type']


class DictData(BasicModel):
    dict_label = models.CharField(verbose_name=_('Dict Data Label'), max_length=100)
    dict_value = models.CharField(verbose_name=_('Dict Data Value'), max_length=100)
    dict_order_num = models.IntegerField(verbose_name=_('Dict Data Order Num'), null=True, blank=True, default=0)
    dict_type = models.ForeignKey(
        to=DictType,
        on_delete=models.CASCADE,
        related_name='items',
        parent_link=True,
        verbose_name=_('Dict Data Name')
    )
    is_sys = models.CharField(verbose_name=_('Is System'), max_length=1, default='0')
    status = models.CharField(verbose_name=_('Status'), max_length=1, default='0')

    def __str__(self):
        return self.dict_label

    class Meta:
        verbose_name = _('Dict Data')
        verbose_name_plural = _('Dict Data')
        db_table = 'sys_dict_data'
        ordering = ['dict_type', 'dict_order_num', 'dict_value']


class MobileAccess(BasicModel):
    access_title = models.CharField(verbose_name=_('Mobile Access Title'), max_length=10)
    access_code = models.CharField(verbose_name=_('Mobile Access Code'), max_length=20)
    access_order_num = models.IntegerField(verbose_name=_('Mobile Access Order Num'), null=True, blank=True, default=0)
    access_icon = models.ImageField(verbose_name=_('Mobile Access Image'), upload_to=post_image_path)

    def __str__(self):
        return self.access_title

    def delete(self, *args, **kwargs):
        # 删除文件前先检查是否存在
        if self.access_icon:
            if os.path.isfile(self.access_icon.path):
                os.remove(self.access_icon.path)
        # 调用父类的 delete 方法删除数据库记录
        super().delete(*args, **kwargs)

    # 批量删除实例并清理文件
    def bulk_delete_with_file_cleanup(queryset):
        for instance in queryset:
            if instance.access_icon:
                # 删除文件
                if default_storage.exists(instance.access_icon.name):
                    default_storage.delete(instance.access_icon.name)

        # 执行批量删除
        queryset.delete()

    class Meta:
        verbose_name = _('Mobile Access')
        verbose_name_plural = _('Mobile Access')
        db_table = 'sys_mobile_access'
        ordering = ['access_order_num', 'access_code']


class MobileAccessUser(BasicModel):
    mobile_access = models.ForeignKey(
        to=MobileAccess,
        on_delete=models.CASCADE,
        related_name='items',
        parent_link=True,
        verbose_name=_('Mobile Access')
    )
    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name='items',
        parent_link=True,
        verbose_name=_('Mobile Access User')
    )
    create_by = models.ForeignKey(to=User, verbose_name=_('Create By'), on_delete=models.SET_NULL,
                                  null=True,
                                  related_name='mobile_access_user_user', blank=True)
    create_time = models.DateTimeField(_('Create Time'), default=timezone.now)

    def save(
            self,
            *args,
            force_insert=False,
            force_update=False,
            using=None,
            update_fields=None,
    ):
        """
        重写save方法，添加错误处理和友好提示
        """
        userId = self.user_id
        mobileAccessId = self.mobile_access_id
        if userId is None or userId == '':
            raise ValidationError(_('Mobile Access User User_Id required'))
        if mobileAccessId is None or mobileAccessId == '':
            raise ValidationError(_('Mobile Access User Access_Id required'))
        id = self.id
        mobileAccessUserEntity = MobileAccessUser.objects.filter(user_id=userId,
                                                                 mobile_access_id=mobileAccessId).exclude(id=id).first()
        if mobileAccessUserEntity is not None:
            raise ValidationError(_('Mobile Access User Save Repeated'))
        try:
            # 在保存前设置一些默认值
            if not self.user_id:
                self.user = self._get_current_user()

            # 调用原始的save方法
            super().save(
                *args,
                force_insert=force_insert,
                force_update=force_update,
                using=using,
                update_fields=update_fields,
            )


        except Exception as e:
            # 记录详细错误日志

            # 抛出带友好信息的验证错误
            raise ValidationError("保存失败，请检查输入信息或联系管理员") from e

    def __str__(self):
        return self.mobile_access.access_title + ' ' + self.user.first_name + ' ' + self.user.last_name

    class Meta:
        verbose_name = _('Mobile Access User')
        verbose_name_plural = _('Mobile Access User')
        db_table = 'sys_mobile_access_user'
        ordering = ['create_time']
