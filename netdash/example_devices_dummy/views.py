from django.shortcuts import render
from django.contrib.auth.decorators import permission_required


@permission_required("example_devices_dummy.can_view_module", raise_exception=True)
def index(request):
    return render(request, "example_devices_dummy/index.html")
