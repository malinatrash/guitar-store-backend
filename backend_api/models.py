from datetime import timedelta
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
import uuid


class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    role = models.CharField(max_length=50, choices=[
                            ('admin', 'Admin'), ('client', 'Client')])

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class ProductCategory(models.Model):
    category_id = models.AutoField(primary_key=True)
    category_name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.category_name


class Vendor(models.Model):
    vendor_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class CountryOfOrigin(models.Model):
    country_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Product(models.Model):
    product_id = models.AutoField(primary_key=True)
    category_id = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=100)
    product_description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    in_stock = models.BooleanField()
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    country_of_origin = models.ForeignKey(
        CountryOfOrigin, on_delete=models.CASCADE)
    year_of_production = models.IntegerField()
    image_url = models.CharField(max_length=255)

    def __str__(self):
        return self.product_name


class Order(models.Model):
    ORDER_STATUS_CHOICES = [
        ('открыт', 'Открыт'),
        ('закрыт', 'Закрыт'),
    ]

    # Другие поля модели

    order_status = models.CharField(
        max_length=50, choices=ORDER_STATUS_CHOICES, default='открыт')
    order_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    order_date = models.DateField(default=timezone.now)
    total_price = models.DecimalField(
        max_digits=10, decimal_places=2)
    products = models.ManyToManyField(
        Product, related_name='orders', through='OrderProduct')

    def __str__(self):
        return f"Заказ {self.order_id} от {self.user_id}"


class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.product.product_name}"


class ProductComment(models.Model):
    comment_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    comment_text = models.TextField()
    likes_count = models.IntegerField(default=0)
    comment_date = models.DateField()

    def __str__(self):
        return f"Comment by {self.user_id} on {self.product_id}"


class ShoppingCart(models.Model):
    cart_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    products_count = models.IntegerField()

    def __str__(self):
        return f"Cart for {self.user_id}: {self.products_count} items"


class Wishlist(models.Model):
    wishlist_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return f"Wishlist for {self.user_id}"


class Session(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    session_id = models.TextField()
    session_data = models.JSONField(null=True, blank=True)
    expiration_time = models.DateTimeField()

    @classmethod
    def create_session(cls, user, session_id):
        expiration_time = timezone.now() + timedelta(minutes=15)
        return cls.objects.create(user=user, session_id=session_id, expiration_time=expiration_time)

    @classmethod
    def get_session(cls, session_id):
        try:
            return cls.objects.get(session_id=session_id)
        except cls.DoesNotExist:
            return None

    def is_expired(self):
        return self.expiration_time < timezone.now()

    def delete_session(self):
        self.delete()
