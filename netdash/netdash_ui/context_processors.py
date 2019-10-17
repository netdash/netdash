from django.conf import settings


def feedback(request):
    return {'FEEDBACK_EMAIL': settings.FEEDBACK_EMAIL}
