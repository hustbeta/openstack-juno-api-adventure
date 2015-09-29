#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json

import keystoneclient
import keystoneclient.auth.identity.v3
import keystoneclient.session
import keystoneclient.v3.client
import novaclient.client

import local_settings

auth = keystoneclient.auth.identity.v3.Password(auth_url=local_settings.auth_url_v3,
                                                username=local_settings.username,
                                                password=local_settings.password,
                                                user_domain_name='Default',
                                                project_domain_name='Default',
                                                project_name=local_settings.tenant_name)
session = keystoneclient.session.Session(auth=auth)
nova = novaclient.client.Client('2', session=session)

print json.dumps([fa.to_dict() for fa in nova.flavor_access.list(flavor='e1eeaa07-d1c8-4ccc-955c-29113db0c147')])
'''
print 'remove:', nova.flavor_access.remove_tenant_access('e1eeaa07-d1c8-4ccc-955c-29113db0c147',
                                                         '4f55e99ec6d444bc904acfe358eaac09')
print 'add:', nova.flavor_access.add_tenant_access('e1eeaa07-d1c8-4ccc-955c-29113db0c147',
                                                   '4f55e99ec6d444bc904acfe358eaac09')
'''

