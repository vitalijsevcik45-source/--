from django.urls import path
from django.contrib.auth import views as auth_views  # 👈 Обов'язково додаємо цей імпорт вгору
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('category/<int:category_id>/', views.category_view, name='category_detail'),
    path('product/<int:product_id>/', views.product_view, name='product_detail'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
    path('profile/', views.profile_view, name='profile'),

    # Маршрути для кошика:
    path('cart/', views.cart_detail_view, name='cart_detail'),
    path('cart/add/<int:product_id>/', views.cart_add_view, name='cart_add'),
    path('cart/remove/<int:product_id>/', views.cart_remove_view, name='cart_remove'),
    path('cart/clear/', views.cart_clear_view, name='cart_clear'),
    path('cart/checkout/', views.checkout, name='checkout'),

    # 🔐 4 вбудовані маршрути для відновлення пароля через пошту:
    path('password_reset/',
         auth_views.PasswordResetView.as_view(template_name='mainapp/password_reset.html'),
         name='password_reset'),

    path('password_reset/done/',
         auth_views.PasswordResetDoneView.as_view(template_name='mainapp/password_reset_done.html'),
         name='password_reset_done'),

    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='mainapp/password_reset_confirm.html'),
         name='password_reset_confirm'),

    path('reset/done/',
         auth_views.PasswordResetCompleteView.as_view(template_name='mainapp/password_reset_complete.html'),
         name='password_reset_complete'),
]