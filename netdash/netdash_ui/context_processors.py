from django.conf import settings


def feedback(request):
    return {'FEEDBACK_EMAIL': getattr(settings, 'FEEDBACK_EMAIL', None)}


def login_url(request):
    return {'LOGIN_URL': getattr(settings, 'LOGIN_URL', '/admin/login/')}
