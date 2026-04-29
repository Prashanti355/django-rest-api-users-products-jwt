from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.products import selectors, services
from apps.products.models import Product
from apps.products.permissions import IsAdminOnly, IsAdminOrStaff
from apps.products.serializers import (
    ProductCreateSerializer,
    ProductDetailSerializer,
    ProductListSerializer,
    ProductUpdateSerializer,
)


@extend_schema_view(
    list=extend_schema(tags=["Products"]),
    retrieve=extend_schema(tags=["Products"]),
    create=extend_schema(tags=["Products"]),
    update=extend_schema(tags=["Products"]),
    partial_update=extend_schema(tags=["Products"]),
    destroy=extend_schema(tags=["Products"]),
    restore=extend_schema(tags=["Products"]),
    search=extend_schema(tags=["Products"]),
    by_price=extend_schema(tags=["Products"]),
)
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()

    def get_queryset(self):
        return selectors.get_visible_products_for_user(self.request.user)

    def get_serializer_class(self):
        if self.action == "create":
            return ProductCreateSerializer

        if self.action == "list":
            return ProductListSerializer

        if self.action in ["update", "partial_update"]:
            return ProductUpdateSerializer

        return ProductDetailSerializer

    def get_permissions(self):
        if self.action in ["create", "update", "partial_update"]:
            return [IsAuthenticated(), IsAdminOrStaff()]

        if self.action in ["destroy", "restore"]:
            return [IsAuthenticated(), IsAdminOnly()]

        return [IsAuthenticated()]

    def perform_create(self, serializer):
        services.create_product(
            {
                **serializer.validated_data,
                "owner": self.request.user,
            },
            actor=self.request.user,
            request=self.request,
        )

    def perform_update(self, serializer):
        services.update_product(
            self.get_object(),
            serializer.validated_data,
            actor=self.request.user,
            request=self.request,
        )

    def perform_destroy(self, instance):
        services.soft_delete_product(
            instance, actor=self.request.user, request=self.request
        )

    @action(detail=True, methods=["patch"])
    def restore(self, request, pk=None):
        product = Product.objects.get(id=pk)
        product = services.restore_product(
            product,
            actor=request.user,
            request=request,
        )
        serializer = ProductDetailSerializer(product)
        return Response(serializer.data)

    @action(detail=False, methods=["get"])
    def search(self, request):
        query = request.query_params.get("q", "")
        products = selectors.search_products(query)
        serializer = ProductListSerializer(products, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["get"])
    def by_price(self, request):
        min_price = request.query_params.get("min_price")
        max_price = request.query_params.get("max_price")

        products = selectors.filter_products_by_price(min_price, max_price)
        serializer = ProductListSerializer(products, many=True)
        return Response(serializer.data)
