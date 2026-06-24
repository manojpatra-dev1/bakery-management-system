from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ProductViewSet, OrderViewSet, home, dashboard, add_order, order_detail,
    register, user_login, user_logout
)

router = DefaultRouter()
router.register(r'products', ProductViewSet)
router.register(r'orders', OrderViewSet)

urlpatterns = [
    # Home & Auth
    path('', home, name='home'),  # Landing page
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),

    # Protected Routes
    path('dashboard/', dashboard, name='dashboard'),
    path('add-order/', add_order, name='add_order'),
    path('order/<int:pk>/', order_detail, name='order_detail'),

    # API
    path('api/', include(router.urls)),
]