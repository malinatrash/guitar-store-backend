from django.contrib import admin

from backend_api.models import User, Order, Product, ProductCategory, ProductComment, ShoppingCart, Wishlist, Vendor, \
    CountryOfOrigin, OrderProduct

from django.contrib import admin

admin.site.register(User)
admin.site.register(Order)
admin.site.register(Product)
admin.site.register(ProductCategory)
admin.site.register(ProductComment)
admin.site.register(ShoppingCart)
admin.site.register(Wishlist)
admin.site.register(Vendor)
admin.site.register(CountryOfOrigin)
admin.site.register(OrderProduct)
