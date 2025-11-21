from django.urls import path
from ShopifyApp.views import (
    HomePageView,
    CreateProductView,
    CreateCategoryView,
    ViewProduct,
    EditProduct,
    DeleteProduct,
    SearchProduct,
    CategoryProductView,
    GetProductByCreatedUser,
    AddProductToCart,
    ViewCart,
    UpdateCartAdd,
    UpdateCartSub,
    RemoveCartItem,
    ViewWishlist,
    AddToWishlist,
    RemoveWishlist,
    CheckoutView,
    OrderListView,
    OrderDetailView,
    OrderSuccessView,
    RazorpayCreateOrderView,
    RazorpayVerifyView
    
)

urlpatterns = [
    path('',HomePageView.as_view(),name='home'),
    path('createproduct/',CreateProductView.as_view(),name='create-product'),
    path('createcategory/',CreateCategoryView.as_view(),name='create-category'),
    path('viewproduct/<int:id>/', ViewProduct.as_view(), name='view-product'),
    path('editproduct/<int:id>/', EditProduct.as_view(), name='edit-product'),
    path('deleteproduct/<int:id>/', DeleteProduct.as_view(), name='delete-product'),
    path('searchproduct/', SearchProduct.as_view(), name='search-product'),
    path('category/<int:id>/', CategoryProductView.as_view(), name='category-search'),
    path('user-product/<int:id>/', GetProductByCreatedUser.as_view(), name='user-product'),
    path('add-to-cart/<int:id>/', AddProductToCart.as_view(), name='add-to-cart'),
    path('view-cart/', ViewCart.as_view(), name='view-cart'),

    path('cart/add/<int:item_id>/', UpdateCartAdd.as_view(), name='cart_add'),
    path('cart/sub/<int:item_id>/', UpdateCartSub.as_view(), name='cart_sub'),
    path('cart/remove/<int:item_id>/', RemoveCartItem.as_view(), name='cart_remove'),



path('wishlist/', ViewWishlist.as_view(), name='view-wishlist'),
path('add-wishlist/<int:id>/', AddToWishlist.as_view(), name='add-wishlist'),
path('remove-wishlist/<int:id>/', RemoveWishlist.as_view(), name='remove-wishlist'),

path('checkout/', CheckoutView.as_view(), name='checkout'),


path('orders/', OrderListView.as_view(), name='order-list'),
path('order/<int:pk>/', OrderDetailView.as_view(), name='order-detail'),
# success page
path('order/success/<int:order_id>/', OrderSuccessView.as_view(), name='order-success'),



path('razorpay/pay/<int:order_id>/', RazorpayCreateOrderView.as_view(), name='razorpay-pay'),
path('razorpay/verify/', RazorpayVerifyView.as_view(), name='razorpay-verify'),



    
    
]