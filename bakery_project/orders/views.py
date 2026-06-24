from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Product, Order, UserProfile
from .serializers import ProductSerializer, OrderSerializer
from .forms import UserLoginForm, UserRegisterForm


# Helper function to check user role
def get_user_role(user):
    try:
        return user.profile.role
    except:
        return 'staff'


# Authentication Views

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
        else:
            # Print errors for debugging
            print("Form errors:", form.errors)
    else:
        form = UserRegisterForm()

    return render(request, 'orders/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(
                request,
                username=username,
                password=password
            )

            if user is not None:
                login(request, user)
                return redirect('dashboard')
            else:
                form.add_error(None, 'Invalid username or password')
    else:
        form = UserLoginForm()

    return render(request, 'orders/login.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('home')


# Landing Page

def home(request):
    """Landing page - shown to everyone"""
    return render(request, 'orders/home.html')


# Template Views

@login_required(login_url='login')
@require_http_methods(["GET"])
def dashboard(request):
    user_role = get_user_role(request.user)
    return render(request, 'orders/dashboard.html', {'user_role': user_role})


@login_required(login_url='login')
@require_http_methods(["GET"])
def add_order(request):
    user_role = get_user_role(request.user)

    # Only staff can add orders
    if user_role != 'staff':
        return render(request, 'orders/access_denied.html')

    return render(request, 'orders/add_order.html', {'user_role': user_role})


@login_required(login_url='login')
@require_http_methods(["GET"])
def order_detail(request, pk):
    user_role = get_user_role(request.user)
    return render(request, 'orders/order_detail.html', {'order_id': pk, 'user_role': user_role})


# API ViewSets

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all().order_by('-created_at')
    serializer_class = OrderSerializer

    @action(detail=True, methods=['post'])
    def update_status(self, request, pk=None):
        # Check user role
        try:
            user_role = request.user.profile.role
        except:
            user_role = 'staff'

        # Only staff can update status
        if user_role != 'staff':
            return Response(
                {'error': 'Only staff members can update order status'},
                status=status.HTTP_403_FORBIDDEN
            )

        order = self.get_object()
        new_status = request.data.get('status')

        if new_status in ['pending', 'ready', 'completed', 'cancelled']:
            order.status = new_status
            order.save()

            serializer = self.get_serializer(order)
            return Response({
                'status': 'Order status updated',
                'order': serializer.data
            })

        return Response(
            {'error': 'Invalid status'},
            status=status.HTTP_400_BAD_REQUEST
        )

    @action(detail=False, methods=['get'])
    def today_orders(self, request):
        from django.utils import timezone

        today = timezone.now().date()
        orders = Order.objects.filter(created_at__date=today)

        serializer = self.get_serializer(orders, many=True)
        return Response(serializer.data)