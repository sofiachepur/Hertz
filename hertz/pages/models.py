from django.db import models
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.core.mail import send_mail


class Subscriber(models.Model):
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
class ProductType(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Product(models.Model):
    title = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    characteristics = models.TextField()
    care = models.TextField()
    image1 = models.ImageField(upload_to='products/')
    image2 = models.ImageField(upload_to='products/', blank=True, null=True)
    image3 = models.ImageField(upload_to='products/', blank=True, null=True)
    image4 = models.ImageField(upload_to='products/', blank=True, null=True)
    image5 = models.ImageField(upload_to='products/', blank=True, null=True)
    quantity = models.PositiveIntegerField(default=0)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    product_type = models.ForeignKey(
        ProductType,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    def __str__(self):
        return self.title


class Order(models.Model):

    PAYMENT_STATUS_CHOICES = [
        ('pending', 'Очікує оплати'),
        ('paid',    'Оплачено'),
        ('failed',  'Помилка оплати'),
    ]

    ORDER_STATUS_CHOICES = [
        ('new',      'Оформлено'),
        ('shipped',  'Відправлено'),
        ('received', 'Отримано'),
    ]

    name           = models.CharField(max_length=100)
    phone          = models.CharField(max_length=30)
    address        = models.TextField()
    receiver_name  = models.CharField(max_length=100, blank=True, null=True)
    receiver_phone = models.CharField(max_length=30,  blank=True, null=True)
    email          = models.EmailField(blank=True, null=True)
    comment        = models.TextField(blank=True, null=True)
    delivery_method = models.CharField(max_length=100, blank=True, null=True)
    delivery_city   = models.CharField(max_length=100, blank=True, null=True)
    delivery_branch = models.CharField(max_length=200, blank=True, null=True)
    payment_method  = models.CharField(max_length=100, blank=True, null=True)
    payment_status  = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='pending')
    order_status    = models.CharField(max_length=20, choices=ORDER_STATUS_CHOICES, default='new')
    total_price     = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at      = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Замовлення #{self.id} — {self.name}'


class OrderItem(models.Model):
    order    = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product  = models.ForeignKey('Product', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price    = models.DecimalField(max_digits=10, decimal_places=2)

    def total(self):
        return self.quantity * self.price


@receiver(post_save, sender=Order)
def send_new_order_email(sender, instance, created, **kwargs):
    if created and instance.email:
        try:
            send_mail(
                subject=f'Замовлення #{instance.id} — оформлено',
                message=f'Вітаємо, {instance.name}!\n\nВаше замовлення #{instance.id} успішно оформлено.\nСума: {instance.total_price} грн\n\nГарного дня, команда Герць',
                from_email=None,
                recipient_list=[instance.email],
                fail_silently=True,
            )
        except Exception:
            pass


@receiver(pre_save, sender=Order)
def send_status_change_email(sender, instance, **kwargs):
    if not instance.pk:
        return
    try:
        old = Order.objects.get(pk=instance.pk)
    except Order.DoesNotExist:
        return

    if not instance.email:
        return

    payment_messages = {
        'pending': 'Очікується оплата вашого замовлення',
        'paid':    'Оплату підтверджено',
        'failed':  'На жаль, оплата не пройшла. Спробуйте ще раз',
    }

    order_messages = {
        'new':      'Ваше замовлення оформлено і передано в обробку',
        'shipped':  'Ваше замовлення відправлено. Очікуйте на доставку',
        'received': 'Ваше замовлення отримано. Дякуємо за покупку!',
    }

    if old.payment_status != instance.payment_status:
        msg = payment_messages.get(instance.payment_status)
        if msg:
            try:
                send_mail(
                    subject=f'Замовлення #{instance.id} — статус оплати',
                    message=f'Вітаємо, {instance.name}!\n\n{msg}\n\nГарного дня, команда Герць',
                    from_email=None,
                    recipient_list=[instance.email],
                    fail_silently=True,
                )
            except Exception:
                pass

    if old.order_status != instance.order_status:
        msg = order_messages.get(instance.order_status)
        if msg:
            try:
                send_mail(
                    subject=f'Замовлення #{instance.id} — статус замовлення',
                    message=f'Вітаємо, {instance.name}!\n\n{msg}\n\nГарного дня, команда Герць',
                    from_email=None,
                    recipient_list=[instance.email],
                    fail_silently=True,
                )
            except Exception:
                pass