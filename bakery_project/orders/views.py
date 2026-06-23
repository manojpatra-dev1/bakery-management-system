from django.shortcuts import render

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Product, Order, OrderItem
from .serializers import ProductSerializer, OrderSerializer, OrderItemSerializer

from django.views.decorators.http import require_http_methods

@require_http_methods(["GET"])
def index(request):
    return render(request, 'orders/index.html')

@require_http_methods(["GET"])
def add_order(request):
    return render(request, 'orders/add_order.html')

@require_http_methods(["GET"])
def order_detail(request, pk):
    return render(request, 'orders/order_detail.html', {'order_id': pk})

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all().order_by('-created_at')
    serializer_class = OrderSerializer

    @action(detail=True, methods=['post'])
    def update_status(self, request, pk=None):
        order = self.get_object()
        new_status = request.data.get('status')

        if new_status in ['pending', 'ready', 'completed', 'cancelled']:
            order.status = new_status
            order.save()
            return Response({'status': 'Order status updated'})
        return Response({'error': 'Invalid status'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'])
    def today_orders(self, request):
        from django.utils import timezone
        today = timezone.now().date()
        orders = Order.objects.filter(created_at__date=today)
        serializer = self.get_serializer(orders, many=True)
        return Response(serializer.data)



