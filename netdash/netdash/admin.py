from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.safestring import mark_safe

from tellme.admin import Feedback, FeedbackAdmin

from .models import User

admin.site.register(User, UserAdmin)


class Django2FeedbackAdmin(FeedbackAdmin):
    def screenshot_thumb(self, feedback):
        print("screenshot_thumb")
        return mark_safe(super().screenshot_thumb(feedback))

    def browser_html(self, feedback):
        print("browser_html")
        return mark_safe(super().browser_html(feedback))


admin.site.unregister(Feedback)
admin.site.register(Feedback, Django2FeedbackAdmin)
print(admin.site)
print("Bazinga")
