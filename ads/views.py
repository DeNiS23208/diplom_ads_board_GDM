from rest_framework import viewsets, permissions, status
from rest_framework.exceptions import NotAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

from .models import Ad, Category
from .serializers import AdSerializer, CategorySerializer
from .permissions import IsOwnerOrReadOnly
from .filters import AdFilter


class CategoryViewSet(viewsets.ModelViewSet):
    """
    Категории:
    - Просмотр: всем
    - Создание/редактирование/удаление: только авторизованным
    """
    queryset = Category.objects.all().order_by('name')
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [SearchFilter]
    search_fields = ['name']


class AdViewSet(viewsets.ModelViewSet):
    """
    Объявления:
    - Просмотр: всем
    - Создание: только авторизованным (owner = текущий пользователь)
    - Редактирование/удаление: только владелец (или staff)
    """
    queryset = Ad.objects.select_related('owner', 'category').order_by('-created_at')
    serializer_class = AdSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    # Поиск/сортировка/фильтрация
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = AdFilter
    search_fields = ['title', 'description']
    ordering_fields = ['created_at', 'price']

    def perform_create(self, serializer):
        # ВАЖНО: не даём анониму дойти до save(owner=AnonymousUser)
        user = self.request.user
        if not user or not user.is_authenticated:
            raise NotAuthenticated("Требуется аутентификация для создания объявления.")
        serializer.save(owner=user)

    # --- Экшены модерации (только для staff/admin) ---
    def get_permissions(self):
        if self.action in ['approve', 'reject', 'archive']:
            return [permissions.IsAdminUser()]
        return super().get_permissions()

    @action(detail=True, methods=['post'])
    def archive(self, request, pk=None):
        ad = self.get_object()
        ad.status = Ad.Status.ARCHIVED
        ad.save(update_fields=['status'])
        return Response({'status': ad.status}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        ad = self.get_object()
        ad.status = Ad.Status.PUBLISHED
        ad.save(update_fields=['status'])
        return Response({'status': ad.status}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def reject(self, request, pk=None):
        ad = self.get_object()
        ad.status = Ad.Status.DRAFT
        ad.save(update_fields=['status'])
        return Response({'status': ad.status}, status=status.HTTP_200_OK)
