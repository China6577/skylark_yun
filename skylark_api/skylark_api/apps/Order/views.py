from rest_framework.generics import CreateAPIView
from .models import Order
from .serializers import OrderModelSerializer
from rest_framework.permissions import IsAuthenticated
# Create your views here.
class OrderAPIView(CreateAPIView):
    """订单视图"""
    queryset = Order.objects.filter(is_show=True,is_deleted=False)
    serializer_class = OrderModelSerializer
    # permission_classes = [IsAuthenticated]