# OAuth2

NetDash supports two-legged OAuth2 for API usage out of the box. Because it uses [`django-auth2-toolkit`](https://django-oauth-toolkit.readthedocs.io/en/latest/), its documentation will serve as the most complete reference.

## Securing API Views

At a high level, NetDash adds a 1:1 mapping between Scopes and Permissions via `netdash.scopes.PermissionsScopes`, which is configured to override `django-oauth2-toolkit`'s default Scopes implementation via the setting `SCOPES_BACKEND_CLASS`. The default Application model is also overridden by `netdash.models.Application` via the setting `OAUTH2_PROVIDER_APPLICATION_MODEL` to provide a many-to-many relationship with Groups. In concert, these two overrides effectively allow you to add Permissions (as Scopes) to your requested AccessTokens, but only if the requesting Application belongs to a Group that has access to those Permissions. Finally, each NetDash Module created from the default template can use `nd_module.api.permissions.HasScopeOrPermission` to permit API access only if the User/AccessToken has the required Permissions/Scopes.

To summarize:
* Permissions and Scopes are roughly equivalent within NetDash.
* Applications can be added to Groups to access the same Scopes as a User would get Permissions.
* The Permission/Scope equivalence works only for NetDash Module API Views that use `HasScopeOrPermission` as demonstrated in the default template.

## Crash Course

What follows is a high-level overview of the workflow of Auth2 usage in NetDash:

1. A developer decides they want to write an application that uses a NetDash Module's API.
2. A NetDash admin creates an Application on behalf of the developer via NetDash's Admin panel. It is created with a `Grant Type` of `Client Credentials`. It is added to the Groups required to access the APIs it needs, following the principle of least privilege.
3. The created Application's `Client ID` and `Client Secret` are securely transferred to the developer.
4. The developer can use the `Client ID` and `Client Secret` to request and manage AccessTokens via `/api/o/token/` and `/api/o/revoke_token/`. For example:
```
curl -X POST -d "grant_type=client_credentials&scope=hostlookup_combined.can_view_module" -u"<client_id>:<client_secret>" netdash.example.com/api/o/token/
```
5. Once the developer obtains an AccessToken, they can use it to access an API resource like so:
```
curl -X GET -H "Authorization: Bearer <token>" netdash.example.com/api/hostlookup/?q=10.100.100.10&bluecat_config=123
```

## Three-Legged OAuth2

Three-legged OAuth2 is not currently supported out of the box, but we would welcome a merge request with a tested implementation.