from rest_framework.pagination import PageNumberPagination


class CustomPagination(PageNumberPagination):
    """
    pagination avoids loading all the DB table rows into Application server RAM leading to OOM
    and DB server load
    """
    page_size = 10
    max_page_size = 100

    def get_page_number(self, request, paginator):
        return request.data.get("page_no", 1)

    def get_page_size(self, request):
        page_size = request.data.get("page_size")
        if page_size:
            return min(int(page_size), self.max_page_size)
        return self.page_size