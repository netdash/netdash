from django.shortcuts import render
from django.contrib.auth.decorators import permission_required


@permission_required("example_error_no_app_name.can_view_module", raise_exception=True)
def index(request):
    return render(request, "example_error_no_app_name/index.html")
