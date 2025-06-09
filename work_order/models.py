from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

from model.models import BasicModel
from datetime import timedelta
from django.utils.translation import gettext_lazy as _

from system.models import DictData, DictType
from django.db.models import Q


def get_dict_cate():
    dict_type_ids = DictType.objects.filter(dict_type='work_order_cate').values_list('id', flat=True)
    return Q(dict_type_id__in=dict_type_ids)


def get_dict_level():
    dict_type_ids = DictType.objects.filter(dict_type='work_order_level').values_list('id', flat=True)
    return Q(dict_type_id__in=dict_type_ids)


class WorkOrder(BasicModel):
    title = models.CharField(verbose_name=_('Work Order Title'), max_length=100)
    content = models.TextField(verbose_name=_('Work Order Content'))
    start_date = models.DateField(verbose_name=_('Start Date'), default=timezone.now)
    end_date = models.DateField(verbose_name=_('End Date'), null=True, blank=True)

    cate = models.ForeignKey(
        to=DictData,
        verbose_name=_('Work Order Cate'),
        on_delete=models.SET_NULL, null=True,
        related_name='cate',
        blank=True,
        limit_choices_to=get_dict_cate
    )
    level = models.ForeignKey(to=DictData, verbose_name=_('Work Order Level'), on_delete=models.SET_NULL, null=True,
                              related_name='level', blank=True,
                              limit_choices_to=get_dict_level)

    create_by = models.ForeignKey(to=User, verbose_name=_('Create By'), on_delete=models.SET_NULL, null=True,
                                  related_name='created_work_order', )
    create_time = models.DateTimeField(_('Create Time'), default=timezone.now)
    update_by = models.ForeignKey(to=User, verbose_name=_('Update By'), on_delete=models.SET_NULL, null=True,
                                  related_name='updated_work_order', )
    update_time = models.DateTimeField(verbose_name=_('Update Time'), default=timezone.now)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('Work Order')
        verbose_name_plural = _('Work Order')
        db_table = 'tb_work_order'
        ordering = ['-start_date']


class WorkOrderStaff(BasicModel):
    work_order = models.ForeignKey(
        to=WorkOrder,
        on_delete=models.CASCADE,
        verbose_name=_('Work Order'),
        related_name='items',
        parent_link=True,
        limit_choices_to={'start_date__gte': timezone.now() - timedelta(days=3)}
    )
    staff = models.ForeignKey(to=User, verbose_name=_('Work Order Executor'), on_delete=models.SET_NULL, null=True,
                                 related_name='work_order_staff_staff_id', blank=True)
    work_order_percent = models.DecimalField(verbose_name=_('Work Order Staff Percent'), max_digits=5, decimal_places=2, default='0')
    create_by = models.ForeignKey(to=User, verbose_name=_('Create By'), on_delete=models.SET_NULL,
                                  null=True,
                                  related_name='created_work_order_staff', blank=True)
    create_time = models.DateTimeField(_('Create Time'), default=timezone.now)
    update_by = models.ForeignKey(to=User, verbose_name=_('Update By'), on_delete=models.SET_NULL, null=True,
                                  related_name='updated_work_order_staff', blank=True)
    update_time = models.DateTimeField(verbose_name=_('Update Time'), default=timezone.now)

    def __str__(self):
        return self.work_order.title

    class Meta:
        verbose_name = _('Work Order Staff')
        verbose_name_plural = _('Work Order Staff')
        db_table = 'tb_work_order_staff'
