# Troubleshooting Modules

If a NetDash Module doesn't properly follow conventions, certain integrations might not work. NetDash includes a `diagnose` command to output information about your NetDash Modules that may assist in refactoring them for inclusion in NetDash.

```
python netdash/manage.py diagnose -v2
```

Will output diagnostics for all NetDash Modules, including any exception traces (`-v2` flag).

If an unrecoverable error is encountered while parsing NetDash Modules, all diagnostics up until the error will be displayed.
