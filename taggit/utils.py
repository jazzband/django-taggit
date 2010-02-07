from functools import wraps

def parse_tags(tags):
    if tags is None:
        tags = ""
    return [o.strip() for o in tags.split(',') if o.strip()]

def require_instance_manager(func):
    @wraps(func)
    def inner(self, *args, **kwargs):
        if self.object_id is None:
            raise TypeError("Can't call %s with a non-instance manager" % func.__name__)
        return func(self, *args, **kwargs)
    return inner
