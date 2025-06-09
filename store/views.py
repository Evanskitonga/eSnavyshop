from django.shortcuts import render

from rest_framework import generics, permissions,filters
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Product, Order, OrderItem
from .serializers import (
    ProductSerializer, OrderSerializer, RegisterSerializer, UserSerializer
)
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes

# 🔐 Register
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer


class LoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(username=username, password=password)
        if user is not None:
            refresh = RefreshToken.for_user(user)
            return Response({
                'user': {
                    'username': user.username,
                },
                'tokens': {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }
            })
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)



# 👤 Get current user info
class UserView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)


# 🛍️ Products
class ProductListView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'description']


class ProductDetailView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


# 🧾 Orders
class CreateOrderView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        items = request.data.get('items', [])
        if not items:
            return Response({'error': 'No items provided'}, status=400)

        order = Order.objects.create(user=request.user)

        for item in items:
            product_id = item['product']
            quantity = item['quantity']
            OrderItem.objects.create(
                order=order,
                product=Product.objects.get(id=product_id),
                quantity=quantity
            )

        serializer = OrderSerializer(order)
        return Response(serializer.data)


class UserOrdersView(generics.ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)


# views.py
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def place_order(request):
    user = request.user
    data = request.data
    items = data['items']
    mobile_number = data.get('mobile_number', '')

    order = Order.objects.create(user=user,  mobile_number=mobile_number,payment_status="Paid")

    for item in items:
        product = Product.objects.get(id=item['product'])
        OrderItem.objects.create(order=order, product=product, quantity=item['quantity'])

    return Response({'message': 'Order placed successfully!'})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_orders(request):
    user = request.user
    orders = Order.objects.filter(user=user).order_by('-created_at')
    serializer = OrderSerializer(orders, many=True)
    return Response(serializer.data)