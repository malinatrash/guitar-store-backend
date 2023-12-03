from django.db import models
from django.utils import timezone


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
        ('ожидает', 'Ожидает'),
        ('в обработке', 'В обработке'),
        ('отправлен', 'Отправлен'),
        ('доставлен', 'Доставлен'),
        ('отменен', 'Отменен'),
    ]

    order_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    order_date = models.DateField(default=timezone.now)
    order_status = models.CharField(
        max_length=50, choices=ORDER_STATUS_CHOICES, default='ожидает')
    total_price = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True)
    products = models.ManyToManyField(
        Product, related_name='orders', through='OrderProduct')

    def __str__(self):
        return f"Заказ {self.order_id} от {self.user_id}"


class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(
        default=1)  # Количество товаров в заказе

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
