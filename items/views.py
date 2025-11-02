from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from .models import Item
from .serializers import ItemSerializer
import requests
from django.db.models import Sum
from django.shortcuts import render

class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all().order_by('-created_at')
    serializer_class = ItemSerializer

@api_view(['GET'])
def fetch_external_posts(request):
    """
    Example: fetch posts from JSONPlaceholder and return top 5 titles.
    You could optionally save them to DB.
    """
    resp = requests.get('https://jsonplaceholder.typicode.com/posts')
    if resp.status_code != 200:
        return Response({'error':'external API failed'}, status=status.HTTP_502_BAD_GATEWAY)
    data = resp.json()[:5]
    return Response({'posts': [{'id': p['id'], 'title': p['title']} for p in data]})

@api_view(['GET'])
def items_report(request):
    """
    Returns aggregated values for visualization:
    - total_items: count
    - total_quantity: sum of qty
    - total_value: sum(qty * price)
    Also items grouped by name (or top N).
    """
    total_items = Item.objects.count()
    total_qty = Item.objects.aggregate(total_qty=Sum('qty'))['total_qty'] or 0
    total_value = 0
    for it in Item.objects.all():
        total_value += float(it.qty) * float(it.price)
    by_name = Item.objects.order_by('-qty')[:10].values('name','qty')
    return Response({
        'total_items': total_items,
        'total_qty': total_qty,
        'total_value': total_value,
        'top_items': list(by_name),
    })

    def report_page(request):
    return render(request, 'items/report.html')
