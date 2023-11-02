"""
URL configuration for guitar_store project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from backend_api.migrations.Views import WishlistAPIView
from backend_api.migrations.Views.CommentAPIView import CommentsAPIView
from backend_api.migrations.Views.CountryAPIView import CountryAPIView
from backend_api.migrations.Views.ShoppingCartAPIView import ShoppingCartAPIView
from backend_api.migrations.Views.UserAPIView import UserAPIView
from backend_api.migrations.Views.VendorAPIView import VendorAPIView
from backend_api.views import OrderAPIView, ProductAPIView, ProductCategoryAPIView, ProductCommentAPIView


urlpatterns = [
    path("admin/", admin.site.urls),
    path('api/user', UserAPIView.as_view()),
    path('api/orders', OrderAPIView.as_view()),
    path('api/products', ProductAPIView.as_view()),
    path('api/comments', CommentsAPIView.as_view()),
    path('api/product_categories', ProductCategoryAPIView.as_view()),
    path('api/product_comments', ProductCommentAPIView.as_view()),
    path('api/carts', ShoppingCartAPIView.as_view()),
    path('api/vendors', VendorAPIView.as_view()),
    path('api/countries', CountryAPIView.as_view()),
    path('api/wishlist', WishlistAPIView.WhishlistAPIView.as_view()),
]
