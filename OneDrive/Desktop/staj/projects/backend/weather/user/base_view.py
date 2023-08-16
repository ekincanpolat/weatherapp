import operator
from functools import reduce

from django.conf import settings
from django.core.paginator import InvalidPage
from django.db.models import Q, Value
from django.db.models.functions import Concat
from django.shortcuts import get_object_or_404
from django.urls import path
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import pagination, filters
from rest_framework.compat import distinct
from rest_framework.exceptions import APIException, NotFound
from rest_framework.filters import OrderingFilter, BaseFilterBackend
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet


class CustomPagination(pagination.PageNumberPagination):
    page_size_query_param = 'rows'

    def get_paginated_response(self, data):
        return Response({
            'total': self.page.paginator.count,
            'result': data
        })

    def paginate_queryset(self, queryset, request, view=None):
        page_size = request.data.get(self.page_size_query_param, self.page_size)
        if not page_size:
            return None

        page_size = settings.MAX_ROWS_PER_PAGE if page_size == '-1' else page_size

        paginator = self.django_paginator_class(queryset, page_size)
        page_number = request.data.get(self.page_query_param, 1)
        if page_number in self.last_page_strings:
            page_number = paginator.num_pages

        try:
            self.page = paginator.page(page_number)
        except InvalidPage as exc:
            msg = self.invalid_page_message.format(
                page_number=page_number, message=str(exc)
            )
            raise NotFound(msg)

        if paginator.num_pages > 1 and self.template is not None:
            # The browsable API should display pagination controls.
            self.display_page_controls = True

        self.request = request
        return list(self.page)


class CustomOrderingFilter(OrderingFilter):
    def get_ordering(self, request, queryset, view):
        params = request.data.get(self.ordering_param)
        if params:
            fields = [param.strip() for param in params.split(',')]
            ordering = self.remove_invalid_fields(queryset, fields, view, request)
            if ordering:
                return ordering

        return self.get_default_ordering(view)


class CustomSearchFilter(filters.SearchFilter):
    def get_search_terms(self, request):
        params = request.data.get(self.search_param, '')
        if params is None:
            params = ''
        params = params.replace('\x00', '')  # strip null characters
        params = params.replace(',', ' ')
        # params = params.replace('İ', 'i')
        params = params.replace('i̇', 'i')
        params = params.replace('ı', 'ı')
        params = params.replace('I', 'ı')
        return params.split()

    def filter_queryset(self, request, queryset, view):
        search_fields = self.get_search_fields(view, request)
        search_terms = self.get_search_terms(request)

        if not search_fields or not search_terms:
            return queryset
        for search_field in search_fields:
            if '_' in search_field:
                annotates = dict()
                annotates[search_field] = Concat(search_field.split('_')[0], Value(' '), search_field.split('_')[1])
                queryset = queryset.annotate(**annotates)

        orm_lookups = [
            self.construct_search(str(search_field))
            for search_field in search_fields
        ]

        base = queryset
        conditions = []
        for search_term in search_terms:
            queries = [
                Q(**{orm_lookup: search_term})
                for orm_lookup in orm_lookups
            ]
            conditions.append(reduce(operator.or_, queries))
        queryset = queryset.filter(reduce(operator.and_, conditions))

        if self.must_call_distinct(queryset, search_fields):
            # Filtering against a many-to-many field requires us to
            # call queryset.distinct() in order to avoid duplicate items
            # in the resulting queryset.
            # We try to avoid this if possible, for performance reasons.
            queryset = distinct(queryset, base)
        return queryset


class CustomDjangoFilterBackend(DjangoFilterBackend):
    def get_filterset_kwargs(self, request, queryset, view):
        return {
            'data': request.data,
            'queryset': queryset,
            'request': request,
        }


class DisabledUsersFilter(BaseFilterBackend):

    def filter_queryset(self, request, queryset, view):
        return queryset.filter(user__is_active=True)


class BaseViewSet(ModelViewSet):
    pagination_class = CustomPagination
    default_filters = [CustomSearchFilter, CustomDjangoFilterBackend,  CustomOrderingFilter]


    @classmethod
    def use_for(cls, method):
        return cls.as_view({'post': method})

    def get_serializer_class(self):
        read_serializer_class = getattr(self, 'read_serializer_class', None)
        if read_serializer_class and self.action in ['list', 'retrieve']:
            return read_serializer_class
        else:
            return self.serializer_class

    def get_object(self):
        queryset = self.get_queryset()
        data = self.request.data
        _id = data.get("id")
        if _id is None:
            raise APIException("You should pass id value for retrieve object.")

        obj = get_object_or_404(queryset, pk=_id)
        self.check_object_permissions(self.request, obj)
        if getattr(obj, 'customer', None) and getattr(self.request.user, 'customer', None):
            if obj.customer.id != self.request.user.customer.id:
                return get_object_or_404(queryset, pk=None)
        return obj

    def filter_queryset(self, queryset):
        for backend in list(self.filter_backends + self.default_filters):
            queryset = backend().filter_queryset(self.request, queryset, self)
        return queryset

    def bulk_update(self, request, *args, **kwargs):
        data = request.data
        ids = []
        queryset = self.get_queryset()
        for datum in data:
            _id = datum.get('id')
            if _id is not None:
                ids.append(_id)
                obj = get_object_or_404(queryset, pk=_id)
                serializer = self.get_serializer(obj, data=datum)
                serializer.is_valid(raise_exception=True)
                self.perform_update(serializer)
        instances = queryset.filter(id__in=ids)
        serializer = self.get_serializer(instances, many=True)
        return Response(serializer.data)


def create_view_paths(path_name, view, allowed_methods=None):
    paths = [
        {"path_string": "get{0}s/", "method_name": "list"},
        {"path_string": "get{0}byid/", "method_name": "retrieve"},
        {"path_string": "create{0}/", "method_name": "create"},
        {"path_string": "update{0}/", "method_name": "update"},
        {"path_string": "delete{0}/", "method_name": "destroy"},
        {"path_string": "bulkupdate{0}/", "method_name": "bulk_update"},
    ]
    if allowed_methods is not None and isinstance(allowed_methods, list):
        paths = [_path for _path in paths if _path['method_name'] in allowed_methods]
    return [path(_path['path_string'].format(path_name), view.use_for(_path['method_name'])) for _path in paths]