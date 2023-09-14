import django_filters
from django_filters import DateFilter, CharFilter
from .models import *


class OrderFilter(django_filters.FilterSet):
    start_date = DateFilter(field_name="created_at", lookup_expr="gte", label="From mm/dd/yy")
    end_date = DateFilter(field_name="created_at", lookup_expr="lte", label="To mm/dd/yy")

    class Meta:
        model = Order
        fields = '__all__'
        exclude = ['customer', 'product', 'created_at', 'qty', 'last_modified']


class ProductFilter(django_filters.FilterSet):
    description = CharFilter(field_name="description", lookup_expr="icontains", label="Desc")
    brand = CharFilter(field_name="brand", lookup_expr="icontains", label="Brand")

    class Meta:
        model = Product
        fields = '__all__'
        exclude = ['kind', 'size_in', 'size_mm', 'created_at', 'last_modified']