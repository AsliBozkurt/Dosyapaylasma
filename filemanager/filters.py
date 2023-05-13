import django_filters
from django_filters import rest_framework as djfilters
from filemanager.models import FileManager


class FileManagerFilter(django_filters.FilterSet):

    created_date = django_filters.CharFilter(method="create_date_filter")
    name = django_filters.CharFilter(field_name="name", lookup_expr="icontains")

    class Meta:
        model = FileManager
        fields = ["created_date", "name"]

    def create_date_filter(self, queryset, name, value):

        # import time
        # print(time.time())

        value = value.split(",")

        if (len(value) == 1) or (len(value) == 0):
            end = datetime.now()
            start = datetime.now() - timedelta(30)
        else:
            end = value[1]
            end = f"{end} 23:59:59"
            start = value[0]

        return queryset.filter(created_date__gte=start, created_date__lt=end)
        # return queryset.filter((Q(created_date__gte=start) & Q(created_date__lte=end)))
