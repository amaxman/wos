from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

from model.models import BasicModel, post_image_path
from django import forms
from datetime import timedelta


class WorkOrder(BasicModel):
    title = models.CharField(verbose_name='标题', max_length=100)
    content = models.TextField(verbose_name='内容')
    start_date = models.DateField(verbose_name='开始日期', default=timezone.now)
    end_date = models.DateField(verbose_name='结束日期', null=True, blank=True)
    create_by = models.ForeignKey(to=User, verbose_name='创建人', on_delete=models.SET_NULL, null=True,
                                  related_name='created_work_order', )
    create_time = models.DateTimeField('创建时间', default=timezone.now)
    update_by = models.ForeignKey(to=User, verbose_name='更新人', on_delete=models.SET_NULL, null=True,
                                  related_name='updated_work_order', )
    update_time = models.DateTimeField(verbose_name='更新日期', default=timezone.now)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = '工单'
        verbose_name_plural = '工单'
        db_table = 'tb_work_order'
        ordering = ['-start_date']


class WorkOrderStaff(BasicModel):
    work_order = models.ForeignKey(
        to=WorkOrder,
        on_delete=models.CASCADE,
        verbose_name='工单',
        related_name='items',
        parent_link=True,
        limit_choices_to={'start_date__gte': timezone.now() - timedelta(days=3)}
    )
    staff_id = models.ForeignKey(to=User, verbose_name='执行人', on_delete=models.SET_NULL, null=True,
                                 related_name='work_order_staff_staff_id', blank=True)
    work_order_percent = models.DecimalField(verbose_name='完成百分比', max_digits=5, decimal_places=2, default='0')
    create_by = models.ForeignKey(to=User, verbose_name='创建人', on_delete=models.SET_NULL, null=True,
                                  related_name='created_work_order_staff', blank=True)
    create_time = models.DateTimeField('创建时间', default=timezone.now)
    update_by = models.ForeignKey(to=User, verbose_name='更新人', on_delete=models.SET_NULL, null=True,
                                  related_name='updated_work_order_staff', blank=True)
    update_time = models.DateTimeField(verbose_name='更新日期', default=timezone.now)

    def __str__(self):
        return self.work_order.title

    class Meta:
        verbose_name = '工单人员'
        verbose_name_plural = '工单人员'
        db_table = 'tb_work_order_staff'
