from django.urls import path
from .views import (
    CategoriesView, ProductsView, CategoryProductsView, ProductDetailView, AllProducts,
    AddReply
)


app_name = 'store'
urlpatterns = [
    path('', CategoriesView.as_view(), name='home'),
    path('products/', ProductsView.as_view(), name='all'),
    path('category/<slug:slug>/', CategoryProductsView.as_view(), name='category-products'),
    path('detail/<int:product_id>/', ProductDetailView.as_view(), name='detail'),
    path('all-list/', AllProducts.as_view(), name='list'),
    path('reply/<int:product_id>/<int:comment_id>', AddReply.as_view(), name='add_reply'),
]
