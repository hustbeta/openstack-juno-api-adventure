#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json

import keystoneclient.auth.identity.v3
import keystoneclient.session
import cinderclient.client

import local_settings

auth = keystoneclient.auth.identity.v3.Password(auth_url=local_settings.auth_url_v3,
                                                username=local_settings.username,
                                                password=local_settings.password,
                                                user_domain_name='Default',
                                                project_domain_name='Default',
                                                project_name=local_settings.tenant_name)
session = keystoneclient.session.Session(auth=auth)
cinder = cinderclient.client.Client('2', session=session)

'''
q = cinder.quotas.get('422b53b9339f427abca6a1eab3c1cdd1', usage=False)
for attr in dir(q):
    try:
        print attr, getattr(q, attr)
    except:
        print 'no attr:', attr
'''
q = cinder.quotas.get('ff281ae03464482fb9b584c69fdb10e7', usage=True)
for attr in dir(q):
    try:
        print attr, getattr(q, attr)
    except:
        print 'no attr:', attr
'''
ret = {}
for attr in dir(q):
    if attr == 'id' or attr.startswith('_'):
        continue
    if attr.startswith('backup') or attr.startswith('gigabytes') or attr.startswith('snapshots') \
            or attr.startswith('volumes'):
        obj = getattr(q, attr)
        ret[attr] = obj
print json.dumps(ret)
'''

