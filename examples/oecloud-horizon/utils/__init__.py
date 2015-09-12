# coding=utf-8
from django.forms.models import model_to_dict as django_model_to_dict
from django.conf import settings
DEBUG = settings.DEBUG

def JsonResponseFailure(**kwargs):
    if not DEBUG and 'debug' in kwargs:
        del kwargs['debug']
    ret = {'status': 'failure'}
    ret.update(kwargs)
    return ret

def JsonResponseSuccess(**kwargs):
    if not DEBUG and 'debug' in kwargs:
        del kwargs['debug']
    ret = {'status': 'success', 'success': 'true'}
    ret.update(kwargs)
    return ret

def model_to_dict(instance, max_depth=5, depth=0):
    if isinstance(instance, dict):
        return instance
    if not hasattr(instance, '_meta'):
        return None

    opts = instance._meta
    depth += 1
    data = django_model_to_dict(instance)

    for field_name in opts.get_all_field_names():
        _cached_key = '_%s_cache' % field_name
        field = opts.get_field_by_name(field_name)[0]
        if field.__class__.__name__ in ('DateTimeField', 'DateField',
                                        'TimeField'):
            value = getattr(instance, field_name)
            data[field_name] = None
            if value:
                if field.__class__.__name__ == 'DateTimeField':
                    data[field_name] = value.strftime('%Y-%m-%d %H:%M:%S')
                else:
                    data[field_name] = value.isoformat()
        elif field.__class__.__name__ == 'ForeignKey':
            if _cached_key in instance.__dict__:
                if depth >= max_depth:
                    continue
                data[field_name] = {}
                try:
                    value = getattr(instance, field_name)
                except (ObjectDoesNotExist, AttributeError):
                    continue
                data[field_name] = model_to_dict(value, depth=depth)
        elif field.__class__.__name__ in ('RelatedObject', 'ManyToManyField'):
            if field_name in data:
                del data[field_name]
        else:
            data[field_name] = field.value_from_object(instance)

    return data

def model_list_to_dict(instances, max_depth=2, depth=0):
    _list = []

    for instance in instances:
        _list.append(model_to_dict(instance, max_depth=max_depth, depth=depth))

    return _list