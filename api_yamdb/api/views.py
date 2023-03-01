from rest_framework import filters, mixins, permissions, viewsets

from reviews.models import Category, Genre, GenreTitle, Title

from .serializers import CategorySerializer, GenreSerializer, TitleSerializer


class GenreViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (permissions.AllowAny,)


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (permissions.AllowAny,)


class TitleViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    permission_classes = (permissions.AllowAny,)
