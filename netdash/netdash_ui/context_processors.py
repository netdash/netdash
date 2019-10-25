from django.conf import settings


def feedback(request):
    return {'FEEDBACK_EMAIL': getattr(settings, 'FEEDBACK_EMAIL', None)}
