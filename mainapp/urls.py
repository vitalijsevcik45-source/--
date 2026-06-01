from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('category/<int:category_id>/', views.category_view, name='category_detail'),
    path('product/<int:product_id>/', views.product_view, name='product_detail'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
    path('profile/', views.profile_view, name='profile'),

    # Нові маршрути для кошика:
    path('cart/', views.cart_detail_view, name='cart_detail'),
    path('cart/add/<int:product_id>/', views.cart_add_view, name='cart_add'),
    path('cart/remove/<int:product_id>/', views.cart_remove_view, name='cart_remove'),
    path('cart/clear/', views.cart_clear_view, name='cart_clear'),
]