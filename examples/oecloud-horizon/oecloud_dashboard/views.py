# coding=utf-8
import django
from django.contrib import auth
from django.contrib.auth import views as django_auth_views
from django.utils import http
from django.utils import functional
from django.conf import settings

from django.contrib.auth import  login as django_auth_login
from django.http import HttpResponse, HttpResponseRedirect
from django.template.response import TemplateResponse

from oecloud_dashboard import forms
from openstack_auth import user as auth_user
from openstack_auth import utils
from utils import JsonResponseFailure, JsonResponseSuccess

try:
    is_safe_url = http.is_safe_url
except AttributeError:
    is_safe_url = utils.is_safe_url


def login(request, extra_context=None, **kwargs):
    redirect = request.GET.get('redirect',
        request.POST.get('redirect', kwargs.get('redirect', '')))
    template_name = kwargs.get('template', 'auth/login.html')


    if (request.user.is_authenticated() and
            auth.REDIRECT_FIELD_NAME not in request.GET and
            auth.REDIRECT_FIELD_NAME not in request.POST):
        return shortcuts.redirect(settings.LOGIN_REDIRECT_URL)

    initial = {}
    current_region = request.session.get('region_endpoint', None)
    requested_region = request.GET.get('region', None)
    regions = dict(getattr(settings, "AVAILABLE_REGIONS", []))
    if requested_region in regions and requested_region != current_region:
        initial.update({'region': requested_region})

    if request.method == "POST":
        if django.VERSION >= (1, 6):
            authentication_form = functional.curry(forms.Login)
        else:
            authentication_form = functional.curry(forms.Login, request)
    else:
        authentication_form = functional.curry(forms.Login, initial=initial)

    if request.method == "POST":
        form = authentication_form(request, data=request.POST)
        if form.is_valid():
            django_auth_login(request, form.get_user())

    else:
        form = authentication_form(request)


    if request.user.is_authenticated():
        print 'user.is_authenticated'
        auth_user.set_session_from_user(
            request,
            request.user
        )
        regions = dict(forms.Login.get_region_choices())
        region = request.user.endpoint
        region_name = regions.get(region)
        request.session['region_endpoint'] = region
        request.session['region_name'] = region_name
        print u'验证'
        u = request.user
        d = u.__dict__
        return JsonResponseSuccess(msg='success', user=d)

    context = {
        'form': form,
        'redirect': redirect,
    }
    return TemplateResponse(request, template_name, context)















    # Get our initial region for the form.
    initial = {}
    current_region = request.session.get('region_endpoint', None)
    requested_region = request.GET.get('region', 'http://controller:5000/v3')
    regions = dict(getattr(settings, "AVAILABLE_REGIONS", []))
    if requested_region in regions and requested_region != current_region:
        initial.update({'region': requested_region})

    if request.method == "POST":
        # NOTE(saschpe): Since https://code.djangoproject.com/ticket/15198,
        # the 'request' object is passed directly to AuthenticationForm in
        # django.contrib.auth.views#login:
        if django.VERSION >= (1, 6):
            authentication_form = functional.curry(forms.Login)
        else:
            authentication_form = functional.curry(forms.Login, request)
    else:
        authentication_form = functional.curry(forms.Login, initial=initial)

    if request.method == "POST":
        form = authentication_form(request, data=request.POST)
        if form.is_valid():
            django_auth_login(request, form.get_user())

        else:
            print 3333333, form.errors

    # Set the session data here because django's session key rotation
    # will erase it if we set it earlier.
    if request.user.is_authenticated():
        print 'user.is_authenticated'
        auth_user.set_session_from_user(
            request,
            request.user
        )
        regions = dict(forms.Login.get_region_choices())
        region = request.user.endpoint
        region_name = regions.get(region)
        request.session['region_endpoint'] = region
        request.session['region_name'] = region_name
        print u'验证'
        u = request.user
        lst = [
            'authorized_tenants',
            'available_services_regions',
            'backend',
            'check_password',
            'default_services_region',
            'delete',
            'domain_id',
            'domain_name',
            'enabled',
            'endpoint',
            'get_all_permissions',
            'get_group_permissions',
            'groups',
            'has_a_matching_perm',
            'has_module_perms',
            'has_perm',
            'has_perms',
            'id',
            'is_active',
            'is_anonymous',
            'is_authenticated',
            'is_staff',
            'is_superuser',
            'is_token_expired',
            'last_login',
            'pk',
            'project_id',
            'project_name',
            'roles',
            'save',
            'service_catalog',
            'services_region',
            'set_password',
            'tenant_id',
            'tenant_name',
            'token',
            'user_domain_id',
            'user_domain_name',
            'user_permissions',
            'username'
            ]
        for k in lst:
            print k, ':', getattr(u, k), '\n', '-' * 20
        return HttpResponse('success')
    else:
        return HttpResponseRedirect('/demo/login')
