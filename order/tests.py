from django.test import TestCase
from celery import task
from django.core.mail import send_mail
from .models import Order

# Create your tests here.


@task
def order_created(order_id):
    """
    此任务用来在在订单成功创建时发送一封电子邮件通知
    :param order_id:
    :return:
    """
    order = Order.objects.get(id=order_id)
    subject = 'Order nr. {}'.format(order.id)
    message = 'Dear {}.\n\nYou have successfully placed an order. Your order id is {}.'.\
        format(order.first_name, order.id)
    mail_sent = send_mail(subject, message, 'admin@webshop.com', [order.email])
    return mail_sent