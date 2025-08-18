from rest_framework import viewsets, permissions
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, OpenApiParameter

from .models import Ad, Category
from .serializers import AdSerializer, CategorySerializer
from .permissions import IsOwnerOrReadOnly


@extend_schema(tags=['Категории'])
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all().order_by('name')
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAdminUser | permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [SearchFilter]
    search_fields = ['name']


@extend_schema(tags=['Объявления'])
class AdViewSet(viewsets.ModelViewSet):
    queryset = Ad.objects.select_related('owner', 'category').order_by('-created_at')
    serializer_class = AdSerializer
    permission_classes = [IsOwnerOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['category', 'is_active']
    search_fields = ['title', 'description']
    ordering_fields = ['created_at', 'price']

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
