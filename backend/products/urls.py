from django.urls import path
from .views import (
    CategoryListView, ProductListView, ProductDetailView,
    ProductReviewListCreateView, WishlistView, WishlistRemoveView
)

urlpatterns = [
    path('categories/', CategoryListView.as_view(), name='category-list'),
    path('', ProductListView.as_view(), name='product-list'),
    path('<slug:slug>/', ProductDetailView.as_view(), name='product-detail'),
    path('<int:product_id>/reviews/', ProductReviewListCreateView.as_view(), name='product-reviews'),
    path('wishlist/', WishlistView.as_view(), name='wishlist'),
    path('wishlist/<int:product_id>/', WishlistRemoveView.as_view(), name='wishlist-remove'),
]
