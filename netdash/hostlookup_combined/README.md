# Host Lookup Combined

Combines BlueCat and NetDisco hostlookup results into a single view.

## Prerequisities

`hostlookup_bluecat` must be in `EXTRA_APPS`:
```
EXTRA_APPS = [
    'hostlookup_bluecat',
]
```

A database named `netdisco` must be set in `DATABASES`:
```
DATABASES = {
    "default": "postgres://netdash@database/netdash",
    "netdisco": "postgres://username:password@netdisco.spam.org:5432/netdisco",
}
```

NetDisco models must be routed to the correct database.
You can use the built-in NetDisco DbRouter for this:
```
DATABASE_ROUTERS = 'hostlookup_netdisco.db_router.DbRouter'
```

BlueCat settings are required:
```
BAM_USERNAME = 'alice'
BAM_PASSWORD = 'swordfish'
BAM_SERVER = 'bluecat.spam.org'
```
