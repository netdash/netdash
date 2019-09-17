class DbRouter:
    '''
    Route netdisco models to an external database.
    Because the database is external, it may not migrate or have external relationships.
    '''

    def db_for_read(self, model, **hints):
        if model._meta.app_label == 'netdisco':
            return 'netdisco'
        return None

    def db_for_write(self, model, **hints):
        if model._meta_app_label == 'netdisco':
            return 'netdisco'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        if obj1._meta.app_label == 'netdisco' and obj2._meta.app_label == 'netdisco':
            return True
        elif obj1._meta.app_label == 'netdisco' or obj2._meta.app_label == 'netdisco':
            return False
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if db == 'netdisco':
            return False
        return None
