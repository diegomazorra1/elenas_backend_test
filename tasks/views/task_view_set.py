from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination
from rest_framework import viewsets, filters, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from tasks.models import Task
from tasks.serializers import TaskSerializer


class ExtendedPagination(PageNumberPagination):
    page_size = 8

    def get_paginated_response(self, data):
        return Response({
            'count': self.page.paginator.count,
            'num_pages': self.page.paginator.num_pages,
            'page_number': self.page.number,
            'page_size': self.page_size,
            'next_link': self.get_next_link(),
            'previous_link': self.get_previous_link(),
            'results': data
        })


class TaskViewSet(viewsets.ModelViewSet):
    """
        User task manager
    """
    serializers_class = TaskSerializer
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    filter_backends = [DjangoFilterBackend,
                       filters.SearchFilter, filters.OrderingFilter]

    search_fields = ['title', 'description']
    ordering_fields = ['title']

    filterset_fields = {
        'creation_date': ['exact'],
    }
    # Sistema de paginación
    pagination_class = PageNumberPagination
    pagination_class.page_size = 8

    def create(self, request):
        """
        Create Method
        """
        serializer = self.serializers_class(data=request.data)

        if serializer.is_valid():
            serializer.validated_data['user'] = request.user
            serializer.save()

            return Response(
                {'status': 'Saved'}, status=status.HTTP_201_CREATED)

        return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        permission_classes = [IsAuthenticated]

        return [permission() for permission in permission_classes]

    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False):
            return Task.objects.none()
        queryset = self.queryset
        query_set = queryset.filter(user=self.request.user)
        return query_set
