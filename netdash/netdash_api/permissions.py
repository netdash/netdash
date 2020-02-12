from oauth2_provider.contrib.rest_framework.permissions import TokenHasScope


class HasScopeOrPermission(TokenHasScope):
    def has_permission(self, request, view):
        required_scopes = self.get_scopes(request, view)
        return (
            super().has_permission(request, view)
            or (
                request.user and request.user.has_perms(required_scopes)
            )
        )
