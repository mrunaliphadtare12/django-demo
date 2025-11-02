from rest_framework import routers
from .views import ItemViewSet, fetch_external_posts, items_report
from django.urls import path, include
from .views import report_page

router = routers.DefaultRouter()
router.register(r'items', ItemViewSet, basename='item')

urlpatterns = [
    path('', include(router.urls)),
    path('external/posts/', fetch_external_posts, name='external-posts'),
    path('reports/items/', items_report, name='items-report'),
    path('report/', report_page, name='report_page'),
]
