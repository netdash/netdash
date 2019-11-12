# Host Lookup NetDisco

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
