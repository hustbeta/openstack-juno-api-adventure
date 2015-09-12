# coding=utf-8
import json
import decimal
import datetime
from django.http.response import HttpResponse


class RevisedDjangoJSONEncoder(json.JSONEncoder):
    """
    JSONEncoder subclass that knows how to encode date/time and decimal types.
    """
    def default(self, o):
        # See "Date Time String Format" in the ECMA-262 specification.
        if isinstance(o, datetime.datetime):
            r = o.strftime('%Y-%m-%d %H:%M:%S')
            if o.microsecond:
                r = r[:23] + r[26:]
            if r.endswith('+00:00'):
                r = r[:-6] + 'Z'
            return r
        elif isinstance(o, datetime.date):
            return o.isoformat()
        elif isinstance(o, datetime.time):
            #if is_aware(o):
            #    raise ValueError("JSON can't represent timezone-aware times.")
            r = o.isoformat()
            if o.microsecond:
                r = r[:12]
            return r
        else:
            return str(o)
            return super(RevisedDjangoJSONEncoder, self).default(o)


class JsonResponseMiddleware(object):
    def process_response(self, request, response):
        if isinstance(response, dict):
            data = json.dumps(response, cls=RevisedDjangoJSONEncoder)
            if 'callback' in request.GET or 'callback' in request.POST:
                data = '%s(%s);' % (request.GET.get('callback', request.POST.get('callback')), data)
                return HttpResponse(data, "text/javascript")
            return HttpResponse(data)
        else:
            return response
